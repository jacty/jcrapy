import sys

import Jcrapy
from utils.project import inside_project, get_project_settings

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
    print('execute')
    # cmds = _get_commands_dict(settings, inproject)
    # cmdname = _pop_command_name(argv)
    # parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), conflict_handler='resolve')

    # cmd = cmds[cmdname]    

    # parser.usage = "Jcrapy %s %s" % (cmdname, cmd.syntax()) ##??
    # parser.description = cmd.long_desc() ##?? Usage? No usage, should be removed.
     
    # settings.update(cmd.default_settings, priority='command')
    # cmd.settings = settings
    # cmd.add_options(parser)
    # opts, args = parser.parse_args(args=argv[1:])
    # #resolve command options.
    # _run_print_help(parser, cmd.process_options, args, opts)
    # cmd.crawler_process = CrawlerProcess(settings)
    # _run_print_help(parser, _run_command, cmd, args, opts)
    # sys.exit(cmd.exitcode)



if __name__ == '__main__':
    execute()