import os
import requests
import zipfile
import io
from typing import List, Dict

DATA_ZIP = "fastmcp-main.zip"
DATA_URL = "https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip"


def ensure_zip():
    if os.path.exists(DATA_ZIP):
        print(f"Found {DATA_ZIP}, skipping download")
        return
    print(f"Downloading {DATA_URL} -> {DATA_ZIP} ...")
    r = requests.get(DATA_URL, stream=True, timeout=60)
    r.raise_for_status()
    with open(DATA_ZIP, 'wb') as f:
        for chunk in r.iter_content(1024 * 64):
            if chunk:
                f.write(chunk)


def build_docs_from_zip(zip_path: str) -> List[Dict[str, str]]:
    docs = []
    with zipfile.ZipFile(zip_path, 'r') as z:
        for name in z.namelist():
            lower = name.lower()
            if lower.endswith('.md') or lower.endswith('.mdx'):
                # read file
                with z.open(name) as fh:
                    data = fh.read()
                    try:
                        text = data.decode('utf-8')
                    except Exception:
                        text = data.decode('utf-8', errors='ignore')
                # remove first path component
                parts = name.split('/', 1)
                filename = parts[1] if len(parts) > 1 else parts[0]
                docs.append({'filename': filename, 'content': text})
    return docs


def index_and_search(docs: List[Dict[str, str]], query: str, topk: int = 5) -> List[Dict[str, object]]:
    """Index documents with minsearch.Index and return topk results.

    Uses the `minsearch` API (Index.fit and Index.search) as requested.
    """
    try:
        from minsearch import Index
    except Exception as e:
        raise RuntimeError("minsearch is required. Install with pip install minsearch") from e

    # prepare documents for minsearch: ensure fields 'content' and 'filename'
    idx = Index(text_fields=['content'], keyword_fields=['filename'])
    idx.fit(docs)
    res = idx.search(query, num_results=topk, output_ids=False)
    # results are documents (dict); attach score if present (minsearch returns docs only)
    return res


def main():
    ensure_zip()
    docs = build_docs_from_zip(DATA_ZIP)
    print(f"Indexed {len(docs)} markdown files")
    results = index_and_search(docs, 'demo', topk=5)
    print("Top 5 for query 'demo':")
    for r in results:
        # r is a document dict produced by minsearch.Index.search
        print(r.get('filename'))


if __name__ == '__main__':
    main()
