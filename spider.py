# -*- utf-8 -*-
import requests
from lxml import etree

url = "https://movie.douban.com/celebrity/1003494/photos/?type=C&start=%s&sortby=like&size=a&subtype=a"
headers = {
    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
    'referer':'https://movie.douban.com/celebrity/1003494/photos/?type=C&start=30&sortby=like&size=a&subtype=a'
}
for i in range(20):
    print('第%d页' % i)
    html = etree.HTML(requests.get(url % (i * 30), headers=headers).content.decode())
    img_links = html.xpath('//*[@class="cover"]/a/img/@src')
    for img_link in img_links:
        body = requests.get(img_link, headers=headers).content
        with open('./bg/' + img_link.split('/')[-1].split('.')[0] + '.jpg', 'wb') as f:
            f.write(body)
