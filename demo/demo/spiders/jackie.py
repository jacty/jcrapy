import scrapy


class JackieSpider(scrapy.Spider):
    name = 'jackie'
    allowed_domains = ['web.archive.org']
    start_urls = ['http://web.archive.org/cdx/search/cdx?url=jackiechan.com&output=json']

    def parse(self, response):
        print('~'*20, response)
