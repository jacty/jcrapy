ACCEPTED_ENCODINGS = [b'gzip', b'deflate']

class HttpCompressionMiddleware:
    """This middleware allows compressed (gzip, deflate) traffic to be sent/received from web sites"""
    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('COMPRESSION_ENABLED'):
            raise NotConfigured
        return cls()

    def process_request(self, request, spider):
        request.headers.setdefault('Accept-Encoding', b", ".join(ACCEPTED_ENCODINGS))

    def process_response(self, request, response, spider):
        print('process_response in httpcompression')