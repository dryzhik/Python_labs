import time
from enum import Enum


class Status(Enum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    CRITICAL = 4


class Logger(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Logger, cls).__new__(cls)
        cls.log_file = open("log_file.txt", 'a+')
        return cls.instance

    def log(self, status, message):
        self.log_file = open("log_file.txt", 'a+')
        t = time.localtime()
        output_time = time.strftime("%H:%M:%S", t)
        formatted_message = f"[{status.name}] {output_time} : {message}\n"
        self.log_file.write(formatted_message)
        self.log_file.close()

    def debug(self, message):
        self.log(Status.DEBUG, message)

    def info(self, message):
        self.log(Status.INFO, message)

    def warn(self, message):
        self.log(Status.WARN, message)

    def error(self, message):
        self.log(Status.ERROR, message)

    def critical(self, message):
        self.log(Status.CRITICAL, message)


if __name__ == "__main__":
    logger = Logger()
    logger2 = Logger()
    print(logger is logger2)  # must be True
    logger2.info("Logger2 message")
    logger.debug("Debugging message")
    logger.info("Information message")
    logger.warn("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
