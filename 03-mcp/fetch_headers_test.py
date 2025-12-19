import requests, hashlib
url = 'https://r.jina.ai/https://github.com/alexeygrigorev/minsearch'
headers_variants = {
    'default': None,
    'curl': {'User-Agent': 'curl/7.88.1'},
    'mozilla': {'User-Agent': 'Mozilla/5.0'},
    'accept-md': {'Accept': 'text/markdown'},
    'accept-html': {'Accept': 'text/html'},
}
for name, hdr in headers_variants.items():
    r = requests.get(url, headers=hdr, timeout=20)
    r.raise_for_status()
    txt = r.text
    print(name, 'len=', len(txt), 'sha256=', hashlib.sha256(txt.encode('utf-8')).hexdigest())
print('\npreview (first 200 chars) for default:\n')
print(requests.get(url).text[:200])
