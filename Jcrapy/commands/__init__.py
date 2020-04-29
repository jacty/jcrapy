"""
Base class for Jcrapy commands
"""
from optparse import OptionGroup

# from Jcrapy.utils.conf import arglist_to_dict

class JcrapyCommand:

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
        print("ScrapyCommand.short_desc")

    def long_desc(self):
        print('JcrapyCommand.long_desc')
        return self.short_desc()

    def help(self):
        print('ScrapyCommand.help')

    def add_options(self, parser):
        """
        Populate option parse with options available for this command
        """
        print('JcrapyCommand.add_options')
        return
        group = OptionGroup(parser, "Global Options")
        group.add_option("--logfile", metavar="FILE",
            help="log file. if omitted stderr will be used")
        group.add_option("-L", "--loglevel", metavar="LEVEL", default=None,
            help="log level (default: %s)" % self.settings['LOG_LEVEL'])
        group.add_option("--nolog", action="store_true",
            help="disable logging completely")
        group.add_option("--profile", metavar="FILE", default=None,
            help="write python cProfile stats to FILE")
        group.add_option("--pidfile", metavar="FILE",
            help="write process ID to FILE")
        group.add_option("-s", "--set", action="append", default=[], metavar="NAME=VALUE",
            help="set/override setting (may be repeated)")
        group.add_option("--pdb", action="store_true", help="enable pdb on failure")

        parser.add_option_group(group)

    def process_options(self, args, opts):
        print('JcrapyCommand.process_options')
        return
        try:
            self.settings.setdict(arglist_to_dict(opts.set), priority='cmdline')
        except ValueError:
            raise UsageError("Invalid -s value, use -s NAME=VALUE", print_help=False)

    def run(self, args, opts):
        print('ScrapyCommand.run')