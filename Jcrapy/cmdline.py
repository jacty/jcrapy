
import sys
import os
import optparse #TD:replace with argparse due to deprecation
import inspect
import pkg_resources

import Jcrapy
from Jcrapy.crawler import CrawlerProcess
from Jcrapy.commands import JcrapyCommand
from Jcrapy.exceptions import UsageError
from Jcrapy.utils.misc import walk_modules
from Jcrapy.utils.project import get_project_settings,inside_project

def _iter_command_classes(module_name):
    # TODO: add `name` attribute to commands and merge this function with
    # jcrapy.utils.spider.iter_spider_classes
        
    for module in walk_modules(module_name):
        for obj in vars(module).values():
            if inspect.isclass(obj) and \
                    issubclass(obj, JcrapyCommand) and \
                    obj.__module__ == module.__name__ and \
                    not obj == JcrapyCommand:

                yield obj


def _get_commands_from_module(module, inproject):
    d = {}

    for cmd in _iter_command_classes(module):
        if inproject or not cmd.requires_project:
            cmdname = cmd.__module__.split('.')[-1]
            d[cmdname] = cmd()
    return d


def _get_commands_dict(settings, inproject):
    cmds = _get_commands_from_module('commands', inproject)
    cmds_module = settings['COMMANDS_MODULE']

    if cmds_module:
        cmds.update(_get_commands_from_module(cmds_module, inproject))
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
        print('-'*20 + " Jcrapy %s - project: %s " % (Jcrapy.__version__, settings['BOT_NAME']) + '-'*20 +'\n')
    else:
        print('-'*20 + " Jcrapy %s - no active project" % (Jcrapy.__version__) + '-'*20 +'\n')


def _run_print_help(parser, func, *a, **kw):
    try:
        func(*a, **kw)
    except UsageError as e:
        if str(e):
            parser.error(str(e))
        if e.print_help:
            parser.print_help()
        sys.exit(2)

def execute(argv=None, settings=None):
    if argv is None:
        argv = sys.argv

    if settings is None:
        settings = get_project_settings()
 
    inproject = inside_project()
    _print_header(settings, inproject)
    cmds = _get_commands_dict(settings, inproject)
    cmdname = _pop_command_name(argv)
    parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), conflict_handler='resolve')

    cmd = cmds[cmdname]    

    parser.usage = "Jcrapy %s %s" % (cmdname, cmd.syntax()) ##??
    parser.description = cmd.long_desc() ##?? Usage? No usage, should be removed.
     
    settings.update(cmd.default_settings, priority='command')
    cmd.settings = settings
    cmd.add_options(parser)
    opts, args = parser.parse_args(args=argv[1:])
    #resolve command options.
    _run_print_help(parser, cmd.process_options, args, opts)
    cmd.crawler_process = CrawlerProcess(settings)
    _run_print_help(parser, _run_command, cmd, args, opts)
    sys.exit(cmd.exitcode)

def _run_command(cmd, args, opts):
    if opts.profile:
        _run_command_profiled(cmd, args, opts)
    else:
        cmd.run(args, opts)

if __name__ == '__main__':
    try:
        print('cmdline.__main__')
        execute()
    finally:
        # Twisted prints errors in DebugInfo.__del__, but PyPy does not run gc.collect()
        # on exit: http://doc.pypy.org/en/latest/cpython_differences.html?highlight=gc.collect#differences-related-to-garbage-collection-strategies
        garbage_collect()