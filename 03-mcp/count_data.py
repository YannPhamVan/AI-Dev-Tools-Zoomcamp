import requests
url='https://r.jina.ai/https://datatalks.club'
r=requests.get(url, timeout=20)
r.raise_for_status()
text=r.text
count=text.lower().count('data')
print(count)
