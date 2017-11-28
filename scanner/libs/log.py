import logging
from colorama import init, Fore, Style


class Formatter(logging.Formatter):
    """Make the log colorful."""

    def format(self, record):
        msg_prefix_dict = {
            'info': '[' + Fore.CYAN + Style.BRIGHT + '*' + Style.RESET_ALL + ']',
            'success': '[' + Fore.GREEN + Style.BRIGHT + '+' + Style.RESET_ALL + ']',
            'warning': '[' + Fore.YELLOW + Style.BRIGHT + '!' + Style.RESET_ALL + ']',
            'failure': '[' + Fore.RED + Style.BRIGHT + '-' + Style.RESET_ALL + ']'
        }

        msg = super(Formatter, self).format(record)

        msg_type = getattr(record, 'msg_type', None)

        if msg_type:
            if msg_type in msg_prefix_dict:
                prefix = msg_prefix_dict[msg_type]
                msg = prefix + ' ' + msg

        return msg


class Logger(object):
    """Customize our logger based on logging."""

    def __init__(self):
        init()

        logger = logging.getLogger(str(id(self)))
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(Formatter())
        logger.addHandler(handler)

        self._logger = logger

    def _log(self, level, msg_type, msg):
        args = []
        kwargs = {}
        extra = kwargs.get('extra', {})
        extra.setdefault('msg_type', msg_type)
        kwargs['extra'] = extra

        self._logger.log(level, msg, *args, **kwargs)

    def info(self, msg):
        self._log(logging.INFO, 'info', msg)

    def success(self, msg):
        self._log(logging.INFO, 'success', msg)

    def warning(self, msg):
        self._log(logging.WARNING, 'warning', msg)

    def failure(self, msg):
        self._log(logging.INFO, 'failure', msg)


logger = Logger()