# /usr/bin/env python
# -*- coding: UTF-8 -*-
import datetime
import requests
import talib
import numpy as np
import show_and_save_log_file
import os
import configparser
import logging
import logging.handlers as log_handler
import os
import json
timeStop = datetime.datetime(2021, 11, 25, 21, 10, 0)
high_hand_logger = logging.getLogger("SYSTEM")
high_hand_logger.setLevel(logging.DEBUG)

streamLogHandler = logging.StreamHandler()
streamLogHandler.setLevel(logging.DEBUG)
streamLogHandler.setFormatter(logging.Formatter(
    "%(asctime)s - [functionName:%(funcName)s line:%(lineno)d]  - [%(levelname)s]: %(message)s", "%H:%M:%S"))
high_hand_logger.addHandler(streamLogHandler)


filename = os.path.join("log", "SYSTEM.log")
LogFileHandler = log_handler.TimedRotatingFileHandler(
    filename, when='midnight', interval=1, backupCount=30, encoding="utf-8")
LogFileHandler.setLevel(logging.DEBUG)
LogFileHandler.setFormatter(logging.Formatter(
    "%(asctime)s  - [functionName:%(funcName)s line:%(lineno)d]  -[%(levelname)s]: %(message)s"))
high_hand_logger.addHandler(LogFileHandler)

timeNow = datetime.datetime.now()
file_name_time = timeNow.strftime("%Y-%m-%d_%Hh%Mm%Ss")
if not os.path.exists(os.path.join(os.getcwd(), "log_file")):
    print("creeate log file folder")
    os.makedirs(os.path.join(os.getcwd(), "log_file"))
file_name_path = os.getcwd()+"/log_file/"
log = show_and_save_log_file.Logger(file_name_path+""+os.path.basename(__file__)+" "+file_name_time +
                                    ".log", level='debug')
starttime = datetime.datetime.now()

config = configparser.ConfigParser()
config.read('config.ini')
config.sections()

BASE_URL = config['biance_api_setting']['BASE_URL']
symbol_url = BASE_URL + \
    config['biance_api_setting']['api_url']+'ticker/price'
resp_symbol = requests.get(symbol_url)
data_symbol = resp_symbol.json()

log.logger.debug("program start")


f = open('./symbol.json')
symbol_data = json.load(f)
data_symbol_usdt_list = symbol_data.get("symbol")
print(type(data_symbol_usdt_list))

count_hight_hand_first_times = {}
while datetime.datetime.now() < timeStop:
    tradces_dict = {}
    tradces_dict_use_time = {}
    tradces_dict_false = {}
    tradces_dict_true = {}
    for data_symbol_usdt_list_index in data_symbol_usdt_list:
        BASE_URL = config['biance_api_setting']['BASE_URL']
        trades_api = '/api/v3/trades'
        trades_url = BASE_URL + trades_api + '?' + \
            'symbol=' + \
            data_symbol_usdt_list_index+'&limit=1000'
        tradces_dict[data_symbol_usdt_list_index
                     ] = requests.get(trades_url).json()
        tradces_dict_use_time[data_symbol_usdt_list_index] = tradces_dict[data_symbol_usdt_list_index][-1]["time"] - \
            tradces_dict[data_symbol_usdt_list_index][0]["time"]

    tradces_dict_use_time_sort = sorted(
        tradces_dict_use_time.items(), key=lambda e: e[1], reverse=False)

    high_hand_logger.info("All:{}".format(tradces_dict_use_time_sort))
    high_hand_logger.info("==========")
    high_hand_logger.info("first:{}".format(tradces_dict_use_time_sort[0][0]))
    high_hand_logger.info("==========")
    if len(count_hight_hand_first_times.keys()) == 0:
        count_hight_hand_first_times[tradces_dict_use_time_sort[0][0]] = 1
    else:
        if tradces_dict_use_time_sort[0][0] in count_hight_hand_first_times:
            count_hight_hand_first_times[tradces_dict_use_time_sort[0][0]
                                         ] = count_hight_hand_first_times[tradces_dict_use_time_sort[0][0]]+1
        else:
            count_hight_hand_first_times[tradces_dict_use_time_sort[0][0]] = 1

    high_hand_logger.info("count:{}.".format(count_hight_hand_first_times))

print("ok")
