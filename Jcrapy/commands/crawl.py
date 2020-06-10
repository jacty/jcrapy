from Jcrapy.commands import JcrapyCommand
from Jcrapy.exceptions import UsageError

class Command(JcrapyCommand):
    def run(self, args):
        if len(args) < 1:
            raise UsageError()
        elif len(args) > 1:
            raise UsageError("Only ONE spider is supported.")
        spname = args[0]
        #running CrawlerProcess.crawl(spname)
        crawl_defer = self.crawler_process.crawl(spname)
        print('crawl.py')
        return
        self.crawler_process.start()

