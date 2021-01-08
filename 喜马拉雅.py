import json

import jsonpath
import requests

url = 'https://www.ximalaya.com/revision/album/v1/getTracksList?albumId=291718&pageNum=1'

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
    "cookie": "_xmLog=h5&3abef489-b7c1-4015-9594-2fa41e9a072d&2.1.2; x_xmly_traffic=utm_source%253A%2526utm_medium%253A%2526utm_campaign%253A%2526utm_content%253A%2526utm_term%253A%2526utm_from%253A",
    "xm-sign": "010f76a54c39de77267b65f51dea87bb2a071949a65e587fb"
}
#
r = requests.get(url, headers=headers)
r.encoding = 'utf-8'
with open('xmly.html', 'w', encoding='utf-8') as f:
    f.write(r.text)

xmly_names = []
xmly_list = []
with open('xmly.html', 'r', encoding='utf-8') as f:
    xmly_content = f.read()
    content = json.loads(xmly_content)

    xmly_url_lists = jsonpath.jsonpath(content, '$..tracks')[0]
    for xmly_url_list in xmly_url_lists:
        xmly_name = xmly_url_list['title']
        u = xmly_url_list['url'].split('/')
        xmly_names.append(xmly_name)
        xmly_list.append(u[3])

print(xmly_list)


def xzyp(xmly_url, i):
    r2 = requests.get(xmly_url, headers=headers)
    r2.encoding = 'utf-8'
    xmly_html = r2.text
    xmly_html = json.loads(xmly_html)
    xmly_urls = jsonpath.jsonpath(xmly_html, '$..data')[0]
    xmly_u = xmly_urls['src']
    print(xmly_u)
    r3 = requests.get(xmly_u, headers=headers)
    with open('./喜马拉雅音频/%s.mp3' % xmly_names[i], 'wb') as f:
        f.write(r3.content)


if __name__ == '__main__':
    i = 0
    for x in xmly_list:
        xmly_url = 'https://www.ximalaya.com/revision/play/v1/audio?id=%s&ptype=1' % x
        xzyp(xmly_url, i)
        i += 1
