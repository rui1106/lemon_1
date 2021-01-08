import json

import jsonpath
import requests

url = 'https://www.ximalaya.com/revision/play/v1/audio?id=353467583&ptype=1'

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
    "cookie": "_xmLog=h5&3abef489-b7c1-4015-9594-2fa41e9a072d&2.1.2; x_xmly_traffic=utm_source%253A%2526utm_medium%253A%2526utm_campaign%253A%2526utm_content%253A%2526utm_term%253A%2526utm_from%253A",
    "Referer": 'https://www.ximalaya.com/yinyue/43584386/353469332',
    "xm-sign": '0104e61fd09fee2d6a005f3a07ee293c78136710de78eec0d'
}

r = requests.get(url, headers=headers)

# with open('喜马拉雅.html', 'w', encoding='utf-8') as f:
#     f.write(r.text)

r.encoding = 'utf-8'
xmly_html = r.text
xmly_html = json.loads(xmly_html)
xmly_urls = jsonpath.jsonpath(xmly_html, '$..data')[0]
xmly_url = xmly_urls['src']
print(xmly_url)

r2 = requests.get(xmly_url, headers=headers)
with open('xmly.mp3', 'wb') as f:
    f.write(r2.content)

