## MCP Homework — Reproduction and Usage Guide

This repository contains the starter code and helper scripts used to complete the MCP homework (Model Context Protocol). The files include a FastMCP server (`main.py`), a search/index implementation (`search.py`) and several small test helpers. This README documents how to reproduce the homework answers and how to use the included tools.

### Prerequisites (Windows / PowerShell)

- Python 3.12+ (recommended)
- A virtual environment is recommended. From the project root run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If you don't have `requirements.txt`, install the minimal set manually:

```powershell
python -m pip install fastmcp requests uv minsearch scikit-learn numpy
```

### Question 1 — uv lock

- After running `uv init` and `uv add fastmcp`, inspect `uv.lock` for the `fastmcp` package entry.
- Inside its `wheels` array you will find `hash = "sha256:..."`. Copy the first sha256 value exactly.

Example (in this repo the first wheel sha256 found was):

```
sha256:fb3e365cc1d52573ab89caeba9944dd4b056149097be169bce428e011f0a57e5
```

### Question 2 — Run the FastMCP server

- The server code lives in `main.py`. Start it with `uv`:

```powershell
uv --directory C:/full/path/to/03-mcp run python main.py
```

- The server prints a startup banner showing the transport used (one of `stdio`, `http`, `https`, or `sse`). Use that transport to interact. Note: when the transport is `stdio` you must send JSON-RPC messages; for interactive tests use the HTTP transport or call the local Python functions.

### Question 3 — Scrape tool (Jina Reader)

- To fetch any web page as Markdown use the Jina reader prefix: `https://r.jina.ai/{TARGET_URL}`. Example:

```powershell
python -c "import requests; print(len(requests.get('https://r.jina.ai/https://github.com/alexeygrigorev/minsearch').text))"
```

- Note: raw vs blob vs HTML pages return different Markdown content; counts will vary slightly depending on the exact URL and HTTP headers.

### Question 4 — Integrate the Tool and count occurrences

- `main.py` exposes a `count_word_on_page(url, word)` function and registers it as an MCP tool. The fastest way to run the check locally (without using the MCP UI) is:

```powershell
.\.venv\Scripts\Activate.ps1
python -c "from main import count_word_on_page; print(count_word_on_page('https://datatalks.club','data'))"
```

- If you prefer the UI, start the server with `transport='http'` (the `main.py` in this repo already runs with `mcp.run(transport='http')`) and open the provided HTTP endpoint in a browser.

### Question 5 — Implement Search

- `search.py` downloads `https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip` (skips download if already present), extracts `.md` and `.mdx` files, strips the leading archive folder from filenames (so `fastmcp-main/docs/…` becomes `docs/…`), and indexes them using `minsearch.Index`.
- The script provides a `index_and_search(docs, query, topk=5)` helper and a `main()` that runs a sample search for the query `"demo"`.

To run the search locally:

```powershell
.\.venv\Scripts\Activate.ps1
python search.py
```

The top result for the query `demo` in the indexed `fastmcp` archive is:

```
examples/testing_demo/README.md
```

### Question 6 — Search tool integration (extra)

- The repository also integrates the search as an MCP tool. `main.py` registers a `search_docs(query)` tool that returns the top-5 filenames for a query.
- You can call it locally as:

```powershell
python -c "from main import search_docs; print(search_docs('demo'))"
```

### Developer notes & implementation details

- `main.py` exposes helper functions and registers them with FastMCP via `@mcp.tool` or `mcp.tool(...)`.
- `search.py` uses `minsearch.Index(text_fields=['content'], keyword_fields=['filename'])` to index documents following the `minsearch` API.

### Files of interest

- `main.py` — MCP server and tools (`fetch_page_markdown`, `count_word_on_page`, `search_docs`).
- `search.py` — download, extract and index `.md`/`.mdx` files and perform queries.
- `ui_server.py` — a small local UI used during development (optional).

If you want, I can:
- Commit and push these final changes, including `search.py` and `main.py` updates.
- Add a `requirements.txt` listing all runtime dependencies.
- Remove development helpers like `ui_server.py` if you prefer a minimal repo.

