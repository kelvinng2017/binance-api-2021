
# /usr/bin/env python
# -*- coding: UTF-8 -*-
import datetime
import requests
import talib
import numpy as np
import show_and_save_log_file
import os
import configparser
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
symbol_url = BASE_URL+config['biance_api_setting']['api_url']+'ticker/price'
resp_symbol = requests.get(symbol_url)
data_symbol = resp_symbol.json()

log.logger.debug(str(len(data_symbol[0]["symbol"])))

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
                                        if(data_symbol[data_symbol_index]["symbol"][0:3] != "BCC"):
                                            if(data_symbol[data_symbol_index]["symbol"] != "BCHSVUSDT"):
                                                if(data_symbol[data_symbol_index]["symbol"] != "STORMUSDT"):
                                                    log.logger.debug(
                                                        str(data_symbol[data_symbol_index]["symbol"]))
                                                    data_symbol_usdt_list.append(
                                                        data_symbol[data_symbol_index]["symbol"])


data_symbol_less_than_seven_day_dict = {}
data_symbol_more_than_seven_day_and_less_than_twenty_five_day_dict = {}
data_symbol_usdt_list_short_line_dict = {}
data_symbol_usdt_list_median_line_dict = {}
data_symbol_usdt_list_long_line_dict = {}
data_symbol_less_than_seven_day = []
symbol_fast = {}

for data_symbol_usdt_list_index in data_symbol_usdt_list:
    log.logger.debug(str("符號:"+data_symbol_usdt_list_index))
    BASE_URL = config['biance_api_setting']['BASE_URL']
    onedayklineindex_url = BASE_URL + '/api/v3/klines' + \
        '?symbol='+data_symbol_usdt_list_index+'&interval=30m&limit=100'
    resp = requests.get(onedayklineindex_url)
    data = resp.json()
    data_symbol_usdt_list_close_list = []
    data_symbol_usdt_list_open_list = []
    for data_symbol_usdt_list_close_index in range(len(data)):
        data_symbol_usdt_list_close_list.append(
            float(data[data_symbol_usdt_list_close_index][4]))
    for data_symbol_usdt_list_open_index in range(len(data)):
        data_symbol_usdt_list_open_list.append(
            float(data[data_symbol_usdt_list_open_index][1]))

    price_rate_change = ((data_symbol_usdt_list_close_list[-1] -
                         data_symbol_usdt_list_open_list[-1])/data_symbol_usdt_list_open_list[-1])
    symbol_fast[data_symbol_usdt_list_index] = round(price_rate_change, 3)

symbol_fast_sort = sorted(symbol_fast.items(), key=lambda item: item[1])

log.logger.debug(str("1分鐘的變化:"+str(symbol_fast_sort)))
