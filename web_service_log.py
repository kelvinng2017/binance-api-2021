import logging
import logging.handlers as log_handler
import os
from colorlog import ColoredFormatter as cl

if not os.path.isdir("./log"):
    print("no file log")
    os.mkdir("./log")

format_str = "%(asctime)s -[functionName:%(funcName)s line:%(lineno)d]-[%(levelname)s]: %(message)s"
date_format = '%Y-%m-%d %H:%M:%S'
cformat = '%(log_color)s' + format_str
colors = {'DEBUG': 'green',
          'INFO': 'cyan',
          'WARNING': 'bold_yellow',
          'ERROR': 'bold_red',
          'CRITICAL': 'bold_purple'}
formatter = cl(cformat, date_format, log_colors=colors)
######################################################################################
SYSTEM_logger = logging.getLogger("SYSTEM")
SYSTEM_logger.setLevel(logging.DEBUG)

streamLogHandler = logging.StreamHandler()
streamLogHandler.setLevel(logging.DEBUG)
streamLogHandler.setFormatter(formatter)
SYSTEM_logger.addHandler(streamLogHandler)

filename = os.path.join("log", "SYSTEM.log")
LogFileHandler = log_handler.TimedRotatingFileHandler(
    filename, when='midnight', interval=1, backupCount=30, encoding="utf-8")
LogFileHandler.setLevel(logging.DEBUG)
LogFileHandler.setFormatter(logging.Formatter(
    "%(asctime)s  - [functionName:%(funcName)s line:%(lineno)d]  -[%(levelname)s]: %(message)s"))
SYSTEM_logger.addHandler(LogFileHandler)
########################################################################################
report_alive_logger = logging.getLogger("report_alive")
report_alive_logger.setLevel(logging.DEBUG)

streamLogHandler = logging.StreamHandler()
streamLogHandler.setLevel(logging.DEBUG)
streamLogHandler.setFormatter(formatter)
report_alive_logger.addHandler(streamLogHandler)

filename = os.path.join("log", "report_alive.log")
LogFileHandler = log_handler.TimedRotatingFileHandler(
    filename, when='midnight', interval=1, backupCount=30, encoding="utf-8")
LogFileHandler.setLevel(logging.DEBUG)
LogFileHandler.setFormatter(logging.Formatter(
    "%(asctime)s  - [functionName:%(funcName)s line:%(lineno)d]  -[%(levelname)s]: %(message)s"))
report_alive_logger.addHandler(LogFileHandler)
########################################################################################
database_loger = logging.getLogger("database_loger")
database_loger.setLevel(logging.DEBUG)

streamLogHandler = logging.StreamHandler()
streamLogHandler.setLevel(logging.DEBUG)
streamLogHandler.setFormatter(formatter)
report_alive_logger.addHandler(streamLogHandler)

filename = os.path.join("log", "database_loger.log")
LogFileHandler = log_handler.TimedRotatingFileHandler(
    filename, when='midnight', interval=1, backupCount=30, encoding="utf-8")
LogFileHandler.setLevel(logging.DEBUG)
LogFileHandler.setFormatter(logging.Formatter(
    "%(asctime)s  - [functionName:%(funcName)s line:%(lineno)d]  -[%(levelname)s]: %(message)s"))
database_loger.addHandler(LogFileHandler)
######################################################################################
fa12_logger = logging.getLogger("fa12_logger")
fa12_logger.setLevel(logging.DEBUG)

streamLogHandler = logging.StreamHandler()
streamLogHandler.setLevel(logging.DEBUG)
streamLogHandler.setFormatter(formatter)
fa12_logger.addHandler(streamLogHandler)

filename = os.path.join("log", "fa12_logger.log")
LogFileHandler = log_handler.TimedRotatingFileHandler(
    filename, when='midnight', interval=1, backupCount=30, encoding="utf-8")
LogFileHandler.setLevel(logging.DEBUG)
LogFileHandler.setFormatter(logging.Formatter(
    "%(asctime)s  - [functionName:%(funcName)s line:%(lineno)d]  -[%(levelname)s]: %(message)s"))
fa12_logger.addHandler(LogFileHandler)
#################################################################
fa10_logger = logging.getLogger("fa10_logger")
fa10_logger.setLevel(logging.DEBUG)

streamLogHandler = logging.StreamHandler()
streamLogHandler.setLevel(logging.DEBUG)
streamLogHandler.setFormatter(formatter)
fa10_logger.addHandler(streamLogHandler)

filename = os.path.join("log", "fa10_logger.log")
LogFileHandler = log_handler.TimedRotatingFileHandler(
    filename, when='midnight', interval=1, backupCount=30, encoding="utf-8")
LogFileHandler.setLevel(logging.DEBUG)
LogFileHandler.setFormatter(logging.Formatter(
    "%(asctime)s  - [functionName:%(funcName)s line:%(lineno)d]  -[%(levelname)s]: %(message)s"))
fa10_logger.addHandler(LogFileHandler)
