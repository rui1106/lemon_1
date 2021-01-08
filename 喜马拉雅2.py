import json
import os
import re

import jsonpath
import requests

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
    "cookie": "_xmLog=h5&3abef489-b7c1-4015-9594-2fa41e9a072d&2.1.2; x_xmly_traffic=utm_source%253A%2526utm_medium%253A%2526utm_campaign%253A%2526utm_content%253A%2526utm_term%253A%2526utm_from%253A"
}


def xmly_download(pages):
    url = 'https://www.ximalaya.com/gerenchengzhang/12627033/'
    print(url)
    r1 = requests.get(url, headers=headers)
    r1.encoding = 'utf-8'
    # print(r1.text)
    ret = re.search(r'<head><title>(.*?M)', r1.text)
    name = ret.group(1)

    # url = 'https://www.ximalaya.com/yinyue/291718/'
    nums = re.search(r'([\d]+)', url)
    num = nums.group(1)
    print(num)
    xmly_names = []
    xmly_list = []
    for page in range(1, pages + 1):
        url2 = 'https://www.ximalaya.com/revision/album/v1/getTracksList?albumId=%s&pageNum=%s' % (num, page)
        r = requests.get(url2, headers=headers)
        content = json.loads(r.content)

        xmly_url_lists = jsonpath.jsonpath(content, '$..tracks')[0]
        for xmly_url_list in xmly_url_lists:
            xmly_name = xmly_url_list['title']
            u = xmly_url_list['trackId']
            xmly_names.append(xmly_name)
            xmly_list.append(u)

    print(xmly_names)
    print(xmly_list)
    # print(xmly_names[0])
    # ret = re.search(r"(.*?》)", xmly_names[0])
    # name = ret.group(1)
    if not os.path.exists('./%s' % name):
        os.mkdir('./%s' % name)
    # print(name)
    i = 0
    for xmly in xmly_list:
        download_url = 'https://www.ximalaya.com/revision/play/v1/audio?id=%s&ptype=1' % xmly
        r2 = requests.get(download_url, headers=headers)
        r2.encoding = 'utf-8'
        xmly_html = r2.text
        xmly_html = json.loads(xmly_html)
        xmly_urls = jsonpath.jsonpath(xmly_html, '$..data')[0]
        xmly_u = xmly_urls['src']
        print(xmly_u)
        r3 = requests.get(xmly_u, headers=headers)
        # file_name = os.mkdir('./%s'% )
        with open('./%s/%s.mp3' % (name, xmly_names[i]), 'wb') as f:
            f.write(r3.content)
        i += 1


if __name__ == '__main__':
    # url = input(str('请输入你要下载的网址:'))
    pages = int(input('请输入你要下载的页数'))
    xmly_download(pages)
