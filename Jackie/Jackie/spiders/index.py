# -*- coding: UTF-8 -*-

import scrapy
from Jspider.itemLoader import PostLoader
from Jspider.items import PostItem

class JSpider(scrapy.Spider):
    name='Jackie'
    start_urls = [
                'http://www.jackiechan.com/news/',
                'http://jackiechan.com/blog/',
                 'http://www.jackiechan.com/scrapbook/'
                ]
    allowd_domains=['jackiechan.com']
    def parse(self, response):
        # follow links to article pages
        for post in response.css('.post .title a'):
            yield response.follow(post, self.parse_post)

        next_page = response.css('.alignleft a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_post(self, response):
        
        loader = PostLoader(item=PostItem(), response=response)
        loader.add_css('title','.title a::text')
        loader.add_css('url','.title a::attr(href)')
        loader.add_css('date','.meta a:first-child::text')
        loader.add_value('category',response.url.split('/')[3])
        
        if response.url.split('/')[3]=='scrapbook':
            #scrapbook channel's url has no date segment, so I have to
            # coding it into dateNum field.
            dateStr = response.css('.meta a:first-child::text').get()
            day = dateStr.split('.')[0]
            monthMap ={"January":"01","February":"02","March":"03",
                        "April":"04","May":"05","June":"06",
                        "July":"07","August":"08","September":"09",
                        "October":"10","November":"11","December":"12"}
            month = monthMap[dateStr.split(" ")[1]]
            year = dateStr.split(" ")[2]
            dateVal = year+month+day 
            loader.add_value('dateNum',dateVal)
        else:
            loader.add_value('dateNum',response.url.split('/')[4]+response.url.split('/')[5]+response.url.split('/')[6])

        loader.add_css('content', '.entry')
        return loader.load_item()


        
        
