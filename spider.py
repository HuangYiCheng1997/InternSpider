import requests
from lxml import etree
from fontprocesster import FontProcesster as FP
import re

class InternSpider(object):
    def __init__(self):
        super().__init__()
        self.index = 'https://www.shixiseng.com'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
        self.session = requests.Session()
        self.session.headers = headers
        self.links = set() # 用来存实习链接.
        self.fp = FP()

    @staticmethod
    def process_detail(details):
        pattern = re.compile(r'\xa0|\r|\n|\s')
        job_detail = re.sub(pattern, '', details)
        return job_detail

    def find_interns(self, keyword, pages=1): # 找实习
        for p in range(1,pages+1):
            param = '/interns?k={k}&p={p}'.format(k=keyword, p=p)
            url = self.index + param
            r = self.session.get(url)
            html = etree.HTML(r.text)
            hrefs = html.xpath('//div[@class="names cutom_font"]/a/@href')
            for href in hrefs:
                self.links.add(self.index+href)

    def intern_detail(self, url):
        text = self.session.get(url).text
        html = etree.HTML(text)
        job_name = html.xpath('//*[@class="new_job_name"]/text()')[0]
        job_money = html.xpath('//*[@class="job_money cutom_font"]/text()')[0]
        job_position = html.xpath('//*[@class="job_position"]/text()')[0]
        job_week = html.xpath('//*[@class="job_week cutom_font"]/text()')[0]
        job_academic = html.xpath('//*[@class="job_academic"]/text()')[0]
        job_time = html.xpath('//*[@class="job_time cutom_font"]/text()')[0]
        job_detail = html.xpath('//*[@class="job_detail"]')[0].xpath('string(.)')

        job_money = self.fp.process(job_money)
        job_week = self.fp.process(job_week)
        job_time = self.fp.process(job_time)
        job_detail = self.process_detail(job_detail)
        
        intern = {
                    'job_name': job_name,
                    'job_money': job_money,
                    'job_position': job_position,
                    'job_week': job_week,
                    'job_academic': job_academic,
                    'job_time': job_time,
                    'job_detail': job_detail
                }

        print(intern)
        #return intern



if __name__ == '__main__':
    spider = InternSpider()
    spider.find_interns('爬虫',10)
    for link in spider.links:
        spider.intern_detail(link)
