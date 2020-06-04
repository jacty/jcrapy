from Jcrapy.commands import JcrapyCommand

class Command(JcrapyCommand):
    def run(self, args):
        if len(args) < 1:
            raise UsageError()
        spname = args[0]
        crawl_defer = self.crawler_process.crawl(spname)

        if getattr(crawl_defer, 'result', None) is not None and issubclass(crawl_defer.result.type, Exception):
            print('Command.run',getattr(crawl_defer, 'result'))
            self.exitcode = 1
        else:
            self.crawler_process.start()

            # if self.crawler_process.bootstrap_failed or \
            #     (hasattr(self.crawler_process, 'has_exception') and self.crawler_process.has_exception):
            #     print('Command.run2')
            #     self.exitcode = 1