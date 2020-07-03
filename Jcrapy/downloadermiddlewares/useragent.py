"""Set User-Agent header per spider or use a default value from settings"""

class UserAgentMiddleware:
    """This middleware allows spiders to override the user_agent"""

    def __init__(self, user_agent='Jcrapy'):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings['USER_AGENT'])
        return o

    def spider_opened(self, spider):
        print('UserAgentMiddleware.spider_opened')

    def process_request(self, request, spider):
        if self.user_agent:
            print('process_request', request.headers)
            request.headers.setdefault(b'User-Agent', self.user_agent)