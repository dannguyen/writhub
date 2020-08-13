import logging
from rich.logging import RichHandler

LOG_FORMAT = '%(message)s'

HANDLERS = [
    RichHandler(show_path=False)
]

logging.basicConfig(
    level="DEBUG", format=LOG_FORMAT, datefmt="[%X]", handlers=HANDLERS
)


class MyLogger(object):
    def __init__(self, loglib='rich', **kwargs):
        self.logg = logging.getLogger(loglib)


    def setLevel(self, level):
        self.logg.setLevel(level)


    class Decorators(object):
        @classmethod
        def _fmt(cls, decorated):
            def wrap(cls, *args, **kwargs):
                # labeltxt = f"{kwargs['label']}: " if kwargs.get('label') else ""
                if len(args) == 1:
                    msg = args[0]
                else:
                    msg = ' '.join(str(a) for a in args)
                # msg = f"{labeltxt}{msg}"
                decorated(cls, msg, **kwargs)
            return wrap

    @Decorators._fmt
    def debug(self, *args, **kwargs):
        self.logg.debug(*args)

    @Decorators._fmt
    def info(self, *args, **kwargs):
        self.logg.info(*args)

    @Decorators._fmt
    def warning(self, *args, **kwargs):
        self.logg.warning(*args)

    @Decorators._fmt
    def error(self, *args, **kwargs):
        self.logg.error(*args)

    @Decorators._fmt
    def critical(self, *args, **kwargs):
        self.logg.critical(*args)



mylogger = MyLogger()
