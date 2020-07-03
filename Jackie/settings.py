# -*- coding: utf-8 -*-

# Jcrapy settings for Jackie project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Jackie'

SPIDER_MODULES = ['Jackie.spiders']

SPIDER_MIDDLEWARES = {
   'Jackie.middlewares.JackieSpiderMiddleware': 543,
}
SCHEDULER = 'Jcrapy.core.scheduler.Scheduler'
DOWNLOADER = 'Jcrapy.core.downloader.Downloader'

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'Jackie.pipelines.JackiePipeline': 300,
}


