import logging
import logging.handlers
import config


def get_logger():
    if config.PROD_LOGGER:
        logger = logging.getLogger('song-feed-worker')
        logger.setLevel(logging.ERROR)
        handler = logging.handlers.SysLogHandler('/dev/log')
        formatter = logging.Formatter('Python: { "loggerName":"%(name)s", "asciTime":"%(asctime)s", "pathName":"%(pathname)s", "logRecordCreationTime":"%(created)f", "functionName":"%(funcName)s", "levelNo":"%(levelno)s", "lineNo":"%(lineno)d", "time":"%(msecs)d", "levelName":"%(levelname)s", "message":"%(message)s"}')
        handler.formatter = formatter
        logger.addHandler(handler)
        return logger
    return logging
