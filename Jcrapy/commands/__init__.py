"""
Base class for Jcrapy commands
"""

class JcrapyCommand:
    # default settings for this command
    default_settings = {}
    crawler_process = None
    def __init__(self):
        self.settings = None

