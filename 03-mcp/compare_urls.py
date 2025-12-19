from server import fetch_page_markdown

urls = [
    'https://github.com/alexeygrigorev/minsearch',
    'https://github.com/alexeygrigorev/minsearch/',
    'https://raw.githubusercontent.com/alexeygrigorev/minsearch/master/README.md',
    'https://github.com/alexeygrigorev/minsearch/blob/master/README.md',
]
for u in urls:
    try:
        md = fetch_page_markdown(u)
        print(u, 'len=', len(md))
    except Exception as e:
        print(u, 'ERROR', e)
