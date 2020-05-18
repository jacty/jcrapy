import sys
import inspect
import optparse

import Jcrapy
from Jcrapy.crawler import CrawlerProcess
from Jcrapy.commands import JcrapyCommand
from Jcrapy.utils.project import inside_project, get_project_settings
from Jcrapy.utils.misc import walk_modules

def _iter_command_classes(module_name):
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
    cmds =_get_commands_from_module('Jcrapy.commands', inproject)
    cmds_module = settings['COMMANDS_MODULE']
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
        print('-'*20 + " Jcrapy %s - project: %s " % (Jcrapy.__version__,settings['BOT_NAME'])+'-'*20)
    else:
        print('-'*20 + " Jcrapy %s - no active project " % Jcrapy.__version__ + '-'*20)


def execute():
    argv = sys.argv
    settings = get_project_settings()
    inproject = inside_project()
    _print_header(settings, inproject)
    cmds = _get_commands_dict(settings, inproject)
    cmdname = _pop_command_name(argv)
    parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), conflict_handler='resolve')

    #default command
    if cmdname not in cmds:
        cmdname = 'crawl'

    cmd = cmds[cmdname]    
    cmd.settings = settings
    args = parser.parse_args(args=argv[1:])[1]

    cmd.crawler_process = CrawlerProcess(settings)
    _run_command(cmd, args)
    sys.exit(0)

def _run_command(cmd, args):
    cmd.run(args)



if __name__ == '__main__':
    execute()