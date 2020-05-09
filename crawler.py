"""
author:sqa
time:2020/5/8 17:10
爬取单词网页
"""
import requests
from bs4 import BeautifulSoup

url_list = []
content_list = []
for x in range(10):
    base_url = 'https://www.shanbay.com/wordlist/104899/202159/?page={}'.format(x)
    url_list.append(base_url)
# print(table.select('.span10'))
for x in range(10):
    base_url = 'https://www.shanbay.com/wordlist/104899/202159/?page={}'.format(x)
    url_list.append(base_url)
for url in url_list:
    html = requests.get(url).text
    bs = BeautifulSoup(html, "html.parser")
    table = bs.table
    for row in table.select('.row'):
        content = {'word': row.select('.span2')[0].text, 'meaning': row.select('.span10')[0].text}
        content_list.append(content)

final_list = []
for content in content_list:
    final = {'word': content['word']}
    try:
        final['part_speech'] = content['meaning'].split('.')[0]
        final['meaning'] = content['meaning'].split('.')[1]
        final_list.append(final)
    except IndexError:
        continue
# final_list
for final in final_list:
    with open('dictionary.txt', 'a') as f:
        f.write(str(final) + '\n')
