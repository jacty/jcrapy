ENVVAR = 'JCRAPY_SETTINGS_MODULE'


SETTINGS_PRIORITIES = {
    'default': 0,
    'command': 10,
    'project': 20,
    'spider': 30,
    'cmdline': 40,
}

valid_envvars = {
    'CHECK',
    'PICKLED_SETTINGS_TO_OVERRIDE',
    'PROJECT',
    'PYTHON_SHELL',
    'SETTINGS_MODULE',
}