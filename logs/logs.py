import logging

from config import Config


def init_logging():
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)s] [%(levelname)-5.5s]: %(message)s.")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(Config.LEVEL)

    fileHandler = logging.FileHandler(Config.LOG_FILE_NAME, 'a', Config.LOG_ENCODING)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
