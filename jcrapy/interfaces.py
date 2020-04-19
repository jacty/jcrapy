from zope.interface import Interface

class ISpiderLoader(Interface):

    def from_settings(settings):
        print('ISpiderLoader.from_settings')
    
    def load(spider_name):
        print('ISpiderLoader.load')

    def list():
        print('ISpiderLoader.list')

    def find_by_request(request):
        print('ISpiderLoader.find_by_request')
