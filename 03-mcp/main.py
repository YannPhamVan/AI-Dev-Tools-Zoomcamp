from fastmcp import FastMCP
import requests
from urllib.parse import urlparse
import search as search_module

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers

    FR: Ajouter deux nombres
    EN: Add two numbers
    """
    return a + b

def _fetch_page_markdown_impl(url: str) -> str:
    parsed = urlparse(url)
    if not parsed.scheme:
        target = f"https://{url}"
    else:
        target = url
    jina_url = f"https://r.jina.ai/{target}"
    resp = requests.get(jina_url, timeout=20)
    resp.raise_for_status()
    return resp.text

# Enregistrer la fonction implémentation comme tool (FastMCP)
# FR: Enregistrer la fonction implémentation comme outil FastMCP
# EN: Register the implementation function as a FastMCP tool
mcp.tool(_fetch_page_markdown_impl)

def fetch_page_markdown(url: str) -> str:
    """Callable normal pour tests rapides (appelle l'impl)

    FR: Callable normal pour tests rapides (appelle l'impl)
    EN: Callable for quick local tests (forwards to the implementation)
    """
    return _fetch_page_markdown_impl(url)

def _count_word_impl(url: str, word: str) -> int:
    text = _fetch_page_markdown_impl(url)
    return text.lower().count(word.lower())

# enregistrer la fonction de comptage comme outil MCP
# FR: enregistrer la fonction de comptage comme outil MCP
# EN: register the counting function as an MCP tool
mcp.tool(_count_word_impl)

def count_word_on_page(url: str, word: str) -> int:
    """Callable normal pour tests rapides (appelle l'impl)

    FR: Callable normal pour tests rapides (appelle l'impl)
    EN: Callable for quick local tests (forwards to the implementation)
    """
    return _count_word_impl(url, word)


# --- Search tool integration (Question 6) ---
try:
    # Ensure zip is present and build docs list once at import time
    # FR: Assurer que l'archive zip est présente et construire la liste de documents une fois à l'import
    # EN: Ensure the zip archive is present and build the document list once at import
    search_module.ensure_zip()
    _indexed_docs = search_module.build_docs_from_zip(search_module.DATA_ZIP)
except Exception:
    _indexed_docs = []


def _search_impl(query: str) -> list:
    """Search implementation that returns top 5 filenames for a query.

    FR: Implémentation de recherche qui retourne les 5 premiers noms de fichiers pour une requête.
    EN: Search implementation that returns the top 5 filenames for a query.
    """
    if not _indexed_docs:
        return []
    res = search_module.index_and_search(_indexed_docs, query, topk=5)
    return [r.get('filename') for r in res]

# register as MCP tool
# FR: enregistrer comme outil MCP
# EN: register as an MCP tool
mcp.tool(_search_impl)


def search_docs(query: str) -> list:
    """Public callable for local testing that forwards to the implementation.

    FR: Fonction publique appelable localement pour les tests qui délègue à l'implémentation.
    EN: Public callable for local testing that forwards to the implementation.
    """
    return _search_impl(query)

def main():
    print("Hello from 03-mcp!")


if __name__ == "__main__":
    main()
    mcp.run()
