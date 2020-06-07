from Jcrapy.commands import JcrapyCommand

class Command(JcrapyCommand):
    def run(self, args):
        if len(args) < 1:
            raise UsageError()
        spname = args[0]
        crawl_defer = self.crawler_process.crawl(spname)

        self.crawler_process.start()

