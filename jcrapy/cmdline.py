import sys
import os
import optparse
import inspect
import pkg_resources

from crawler import CrawlerProcess
from commands import ScrapyCommand
from utils.misc import walk_modules
from utils.project import inside_project,get_project_settings

def _iter_command_classes(module_name):
    # TODO: add `name` attribute to commands and and merge this function with
    # scrapy.utils.spider.iter_spider_classes
    for module in walk_modules(module_name):
        for obj in vars(module).values():
            if inspect.isclass(obj) and \
                    issubclass(obj, ScrapyCommand) and \
                    obj.__module__ == module.__name__ and \
                    not obj == ScrapyCommand:
                yield obj



def _get_commands_from_module(module, inproject):
    d = {}
    for cmd in _iter_command_classes(module):
        if inproject or not cmd.requires_project:
            cmdname = cmd.__module__.split('.')[-1]
            d[cmdname] = cmd()
    return d

def _get_commands_from_entry_points(inproject, group='commands'):
    cmds = {}
    for entry_point in pkg_resources.iter_entry_points(group):
        print('_get_commands_from_entry_points',entry_point)
    return cmds

def _get_commands_dict(settings, inproject):
    cmds = _get_commands_from_module('commands', inproject)
    cmds.update(_get_commands_from_entry_points(inproject))
    cmds_module = settings['COMMANDS_MODULE']
    if cmds_module:
        print('_get_commands_dict', cmds_module)
    return cmds

def _pop_command_name(argv):
    i = 0
    for arg in argv[1:]:
        if not arg.startswith('-'):
            del argv[i]
            return arg
        i += 1

def _print_header(settings, inproject):
    if inproject:
        print('In project')
    else:
        print("Scrapy %s - no active project\n" % '0.0.1')


def _print_commands(settings, inproject):
    _print_header(settings, inproject)
    print("Usage")
    print("  scrapy <command> [options] [args]\n")
    print("Available commands:")
    cmds = _get_commands_dict(settings, inproject)
    for cmdname, cmdclass in sorted(cmds.items()):
        print('Available cmds',cmds.items())
    if not inproject:
        print()
        print("  [ more ]      More commands available when run from project directory")
    print()
    print('Use "scrapy <command> -h" to see more info about a command')

def _print_unknown_command(settings, cmdname, inproject):
    _print_header(settings, inproject)
    print("Unknown command: %s\n" % cmdname)
    print('Use "scrapy" to see available commands')

def _run_print_help(parser, func, *a, **kw):
    try:
        func(*a, **kw)
    except UsageError as e:
        print('_run_print_help', func, *a, **kw)

def execute(argv=None, settings=None):
    if argv is None:
        argv = sys.argv

    if settings is None:
        settings = get_project_settings()
    inproject = inside_project()
    cmds = _get_commands_dict(settings, inproject)
    cmdname = _pop_command_name(argv)
    parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), conflict_handler='resolve')
    if not cmdname:
        _print_commands(settings, inproject)
        sys.exit(0)
    elif cmdname not in cmds:
        _print_unknown_command(settings, cmdname, inproject)
        sys.exit(2)

    cmd = cmds[cmdname]
    parser.usage = "scrapy %s %s" % (cmdname, cmd.syntax())
    parser.description = cmd.long_desc()
    settings.setdict(cmd.default_settings, priority='command')
    cmd.settings = settings
    cmd.add_options(parser)
    opts, args = parser.parse_args(args=argv[1:])
    _run_print_help(parser, cmd.process_options, args, opts)
    cmd.crawler_process = CrawlerProcess(settings)
    print('cmdline.execute',cmd.crawler_process)
