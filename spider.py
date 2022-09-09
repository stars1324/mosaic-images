# -*- utf-8 -*-
import requests
from lxml import etree
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()

url = "https://movie.douban.com/celebrity/1003494/photos/?type=C&start=%s&sortby=like&size=a&subtype=a"
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'referer':'https://movie.douban.com/celebrity/1003494/photos/?type=C&start=%s&sortby=like&size=a&subtype=a'
}
for i in range(20):
    print('第%d页' % i)
    html = etree.HTML(requests.get(url % (i * 30), headers=headers, verify=False).content.decode())
    img_links = html.xpath('//*[@class="cover"]/a/img/@src')
    for img_link in img_links:
        body = requests.get(img_link, headers=headers).content
        with open('./bg/' + img_link.split('/')[-1].split('.')[0] + '.jpg', 'wb') as f:
            f.write(body)
