
class ScrapyCommand:

    requires_project = False
    crawler_process = None

    # default settings to be used for this command instead of global defaults
    default_settings = {}

    exitcode = 0

    def __init__(self):
        self.settings = None

    def set_crawler(self, crawler):
        print('ScrapyCommand.set_crawler')

    def syntax(self):
        print('ScrapyCommand.syntax')

    def short_desc(self):
        print('ScrapyCommand.short_desc')

    def long_desc(self):
        print('ScrapyCommand.long_desc')

    def help(self):
        print('ScrapyCommand.help')

    def add_options(self, parser):
        print('ScrapyCommand.add_options')

    def process_options(self, args, opts):
        print('ScrapyCommand.process_options')

    def run(self, args, opts):
        print('ScrapyCommand.run')