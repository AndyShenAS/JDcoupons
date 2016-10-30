import  scrapy
from coupons.items import  CouponsItem
import  pdb
import  json

class CouponsSpider(scrapy.Spider):

    name = "coupons"
    allowed_domains = ['jd.com']
    start_urls = ["http://a.jd.com/coupons.html?page={}"\
                      .format(x) for x in range(1, 20)]

    def parse(self, response):
        pages = response.xpath("//*[@class=\"quan-item quan-d-item quan-item-acoupon \"]")
        for page in  pages:
            metadata = self._xpathCounponsMetaData(page)
            url = 'http://'+ metadata['dataLinkurl'][0]
            yield scrapy.Request(url=url, meta=metadata, callback= self.classfy)

    def _xpathCounponsMetaData(self,page):
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
        metadata = {'dataKey': dataKey,
                    'dataLinkurl': dataLinkurl,
                    'rmb': rmb,
                    'type': type_,
                    'limit': limit,
                    'range': range_,
                    'usable': usable,
                    'timeLong': timeLong}
        return metadata


    def classfy(self, response):
        gooditem = CouponsItem()
        url = response.url
        print('parse',response.meta)
        head = url.split('.')[0]
        if head == 'http://search':
            ids = self._parseGoods(response)
            gooditem['good'] = (response.meta,ids)
            yield gooditem
        elif head == 'http://what':
            print('what')
        elif head == 'http://mall':
            print('mall')
        elif head == 'http://hotel':
            print('hotel')


    def _parseGoods(self, response):
        ids = []
        goods = response.xpath("//*[@id=\"J_goodsList\"]//ul//li")
        for good in goods:
            goodId = good.xpath('@data-sku').extract()[0]
            ids.append(goodId)
        return ids

    def close(spider, reason):
        goods = {}
        with open('data\\items.json', 'rb') as f:
            for line in f.readlines():
                value, keys = json.loads(line.decode('utf-8'))['good']
                for key in keys:
                    if key in goods.keys():
                        goods[key].append(value)
                    else:
                        goods[key] = [value]

        with open('data\\goods.json', 'wb') as f:
            goodsjs = json.dumps(goods).encode('utf-8')
            f.write(goodsjs)
