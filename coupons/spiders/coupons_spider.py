import scrapy
from scrapy.loader import ItemLoader
from coupons.items import CouponsItem
import pdb
from  .urlpool import UrlPool

class CouponsSpider(scrapy.Spider):
    name = "coupons"

    def start_requests(self):
        # self.goodIds = set()
        # self.goodUrls = set()

        # urlstr = "http://a.jd.com/coupons.html?page={}"
        # urls = [ urlstr.format(x) for x in range(3,5)]
        urls = UrlPool()
        for url in  urls.get():
            yield  scrapy.Request(url = url, callback=self.parse)

        for url in self.items['good']['url']:
            print(url)
            yield  scrapy.Request(url = url, callback=self.parseGoods)

        print(self.items['good']['url'])

    def parse(self, response):
        pages = response.xpath("//*[@class=\"quan-item quan-d-item quan-item-acoupon \"]")
        for page in  pages:
            dataKey = page.xpath('@data-key').extract()
            dataLinkurl = page.xpath('@data-linkurl').extract()
            rmb = page.xpath('div//div[1]//strong/text()').extract()[0]
            type_ = page.xpath('div//div[1]//div//div[1]//text()').extract()[0]
            limit = page.xpath('div//div[1]//div//div[2]//text()').extract()
            limit = ''.join(limit).strip()
            range_ = page.xpath('div//div[2]//div[1]//text()').extract()[0].strip()
            usable = page.xpath('div//div[2]//div[2]//text()').extract()[0].strip()
            timeLong = page.xpath('div//div[2]//div[3]//text()').extract()[0].strip()
            # state = page.xpath('div[3]//div[1]//text()').extract()[0]
            self._classify(dataLinkurl[0])
            # print(dataLinkurl)
        # print(self.goodIds)

    def _classify(self,url):
        head = url.split('.')[0]
        if head == '//search':
            # print(url)
            self.items['good']['url'].add("https:"+url)
            # scrapy.Request(url="https:" + url, callback=self.parse2)
        elif head == '//what':
            print('what')
        elif head == '//mall':
            print('mall')

        # print(self.goodIds)

    def parseGoods(self, response):
        # print('getin second link')
        goods = response.xpath("//*[@id=\"J_goodsList\"]//ul//li")
        for good in goods:
            # print('good',good)
            goodId = good.xpath('@data-sku').extract()[0]
            # print('good',goodId)
            self.items['good']['id'].add(goodId)



class




