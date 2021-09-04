# /usr/bin/env python
# -*- coding: UTF-8 -*-
import datetime
import requests
import talib
import numpy as np
import show_and_save_log_file
import os
import configparser
timeStop = datetime.datetime(2021, 9, 4, 21, 10, 0)


while datetime.datetime.now() < timeStop:
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

    data_symbol_usdt_list = []

    for data_symbol_index in range(len(data_symbol)):
        if(len(data_symbol[data_symbol_index]["symbol"][-4:]) >= 4):
            if(data_symbol[data_symbol_index]["symbol"][-4:] == "USDT"):
                if(data_symbol[data_symbol_index]["symbol"].find("DOWN") == -1):
                    if(data_symbol[data_symbol_index]["symbol"].find("UP") == -1):
                        if(data_symbol[data_symbol_index]["symbol"].find("BEAR") == -1):
                            if(data_symbol[data_symbol_index]["symbol"].find("BULL") == -1):
                                if(data_symbol[data_symbol_index]["symbol"][0:3] != "VEN"):
                                    if(data_symbol[data_symbol_index]["symbol"][0:3] != "MCO"):
                                        if(data_symbol[data_symbol_index]["symbol"][0:3] != "BCC"):
                                            if(data_symbol[data_symbol_index]["symbol"][0:2] != "HC"):
                                                # log.logger.debug(str(data_symbol[data_symbol_index]["symbol"]))
                                                data_symbol_usdt_list.append(
                                                    data_symbol[data_symbol_index]["symbol"])

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
        # log.logger.debug("顯示第一個回傳結果:"+str(tradces_dict[data_symbol_usdt_list_index][0]))
        # log.logger.debug(str(tradces_dict[data_symbol_usdt_list_index][0]["time"]))
        # log.logger.debug(str(tradces_dict[data_symbol_usdt_list_index][-1]["time"]))
        tradces_dict_use_time[data_symbol_usdt_list_index] = tradces_dict[data_symbol_usdt_list_index][-1]["time"] - \
            tradces_dict[data_symbol_usdt_list_index][0]["time"]
        count_false = 0
        count_true = 0

        for tradces_index in range(len(tradces_dict[data_symbol_usdt_list_index])):
            # log.logger.debug(tradces_dict[data_symbol_usdt_list_index][tradces_index])
            if(tradces_dict[data_symbol_usdt_list_index][tradces_index]["isBuyerMaker"] == False):
                count_false = count_false + 1
            if(tradces_dict[data_symbol_usdt_list_index][tradces_index]["isBuyerMaker"] == True):
                count_true = count_true + 1

        tradces_dict_false[data_symbol_usdt_list_index] = count_false
        tradces_dict_true[data_symbol_usdt_list_index] = count_true

    tradces_dict_use_time_sort = sorted(
        tradces_dict_use_time.items(), key=lambda e: e[1], reverse=False)
    tradces_dict_false_sort = sorted(
        tradces_dict_false.items(), key=lambda e: e[1], reverse=True)
    tradces_dict_true_sort = sorted(
        tradces_dict_true.items(), key=lambda e: e[1], reverse=True)
    log.logger.debug("\n交易使用時間:\n"+str(tradces_dict_use_time_sort[0:9]))
    log.logger.debug("\ntradec false first ten:\n" +
                     str(tradces_dict_false_sort[0:9]))
    log.logger.debug("\ntradec true first ten:\n" +
                     str(tradces_dict_true_sort[0:9]))
    radces_dict_use_time_sort_short = tradces_dict_use_time_sort[0:10]
    tradces_dict_false_sort_short = tradces_dict_false_sort[0:10]
    tradces_dict_true_sort_short = tradces_dict_true_sort[0:10]
    print(radces_dict_use_time_sort_short[0][0])
    print(tradces_dict_false_sort_short[0][0])
    time_and_false_same_dict = {}
    time_and_true_same_dict = {}
    radces_dict_use_time_sort_short_index = 0
    tradces_dict_false_sort_short_index = 0
    time_and_false_same_dict_index = 0
    for radces_dict_use_time_sort_short_index in range(len(radces_dict_use_time_sort_short)):
        for tradces_dict_false_sort_short_index in range(len(tradces_dict_false_sort_short)):
            if(radces_dict_use_time_sort_short[radces_dict_use_time_sort_short_index][0] == tradces_dict_false_sort_short[tradces_dict_false_sort_short_index][0]):
                time_and_false_same_dict[time_and_false_same_dict_index] = tradces_dict_false_sort_short[tradces_dict_false_sort_short_index]
                time_and_false_same_dict_index = time_and_false_same_dict_index + 1
            tradces_dict_false_sort_short_index = tradces_dict_false_sort_short_index + 1
        radces_dict_use_time_sort_short_index = radces_dict_use_time_sort_short_index + 1

    radces_dict_use_time_sort_short_index = 0
    tradces_dict_true_sort_short_index = 0
    time_and_true_same_dict_index = 0
    for radces_dict_use_time_sort_short_index in range(len(radces_dict_use_time_sort_short)):
        for tradces_dict_true_sort_short_index in range(len(tradces_dict_true_sort_short)):
            if(radces_dict_use_time_sort_short[radces_dict_use_time_sort_short_index][0] == tradces_dict_true_sort_short[tradces_dict_true_sort_short_index][0]):
                time_and_true_same_dict[time_and_true_same_dict_index] = tradces_dict_true_sort_short[tradces_dict_true_sort_short_index]
                time_and_true_same_dict_index = time_and_true_same_dict_index + 1
            tradces_dict_true_sort_short_index = tradces_dict_true_sort_short_index + 1
        radces_dict_use_time_sort_short_index = radces_dict_use_time_sort_short_index + 1

    log.logger.debug("fast false"+str(time_and_false_same_dict))
    log.logger.debug("fast true"+str(time_and_true_same_dict))
print("ok")
