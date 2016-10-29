class UrlPool(object):
    def __init__(self):
        urlstr = "http://a.jd.com/coupons.html?page={}"
        self.urls = [ urlstr.format(x) for x in range(3,5)]

    def get(self):
        for url in self.urls:
            # print(url)
            yield url

    def insert(self, url):
        if len(url)>5 and (url[:5] == 'http:'):
            self.urls.append(url)
        else:
            self.urls.append('http:' + url)
        print(len(self.urls), self.urls[-1])

# import time
# if __name__ == '__main__':
#     url = UrlPool()
#     for x in url.get():
#         url.insert('111')
#         time.sleep(3)
#         print(x)
#         if x == 'http://111':
#             break
#
