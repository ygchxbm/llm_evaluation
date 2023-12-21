from datetime import datetime


class Log:

    log_level_map = {
        'INFO': 1,
        'DEBUG': 2,
        'WARNING': 3,
        'ERROR': 4,
    }
    LOG_LEVEL = 1

    @staticmethod
    def init_app(level):
        if level not in Log.log_level_map:
            raise Exception('log level error')
        Log.LOG_LEVEL = Log.log_level_map[level]

    @staticmethod
    def print_log(msg):
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        print('info-{}-{}'.format(date_time, msg))

    @staticmethod
    def info(msg):
        if Log.LOG_LEVEL < Log.log_level_map['INFO']:
            return
        Log.print_log(msg)

    @staticmethod
    def debug(msg):
        if Log.LOG_LEVEL < Log.log_level_map['DEBUG']:
            return
        Log.print_log(msg)

    @staticmethod
    def warning(msg):
        if Log.LOG_LEVEL < Log.log_level_map['WARNING']:
            return
        Log.print_log(msg)

    @staticmethod
    def error(msg):
        if Log.LOG_LEVEL < Log.log_level_map['ERROR']:
            return
        Log.print_log(msg)