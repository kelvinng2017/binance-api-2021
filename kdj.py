# /usr/bin/env python
# -*- coding: UTF-8 -*-
# %%
import datetime
import requests
import talib
import numpy as np
import show_and_save_log_file
import os
import pandas as pd
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
                                        if(data_symbol[data_symbol_index]["symbol"][0:2] != "HC"):
                                            log.logger.debug(
                                                str(data_symbol[data_symbol_index]["symbol"]))
                                            data_symbol_usdt_list.append(
                                                data_symbol[data_symbol_index]["symbol"])

# %%
print(data_symbol_usdt_list[0])
sysmbol_kdj_k = {}
sysmbol_kdj_d = {}
sysmbol_kdj_j = {}
# %%

for data_symbol_usdt_list_index in data_symbol_usdt_list:
    BASE_URL = config['biance_api_setting']['BASE_URL']
    onedayklineindex_url = BASE_URL + '/api/v3/klines' + \
        '?symbol='+data_symbol_usdt_list_index+'&interval=1d&limit=9'
    resp = requests.get(onedayklineindex_url)
    data = resp.json()
    if(len(data) >= 9):
        print(data_symbol_usdt_list_index)
        df_kline = pd.DataFrame(data, columns={'open_time': 0, 'open': 1, 'high': 2, 'low': 3, 'close': 4, 'volume': 5,
                                               'close_time': 6, 'quote_volume': 7, 'trades': 8, 'taker_base_volume': 9, 'taker_quote_volume': 10, 'ignore': 11})
        df_kline['open_time'] = pd.to_datetime(
            df_kline['open_time'].values, utc=True, unit='ms').tz_convert("Asia/Taipei").to_period("s")
        df_kline['close'] = df_kline['close'].astype(float)
        df_kline['open'] = df_kline['open'].astype(float)
        df_kline['high'] = df_kline['high'].astype(float)
        df_kline['low'] = df_kline['low'].astype(float)
        lowList = df_kline['low'].rolling(9).min()
        lowList.fillna(value=df_kline['low'].expanding().min(), inplace=True)
        highList = df_kline['high'].rolling(9).max()
        highList.fillna(value=df_kline['high'].expanding().max(), inplace=True)
        rsv = (df_kline['close'] - lowList) / (highList - lowList) * 100
        df_kline['kdj_k'] = rsv.ewm(
            alpha=1/3, adjust=False).mean()     # ewm是指数加权函数
        df_kline['kdj_d'] = df_kline['kdj_k'].ewm(
            alpha=1/3, adjust=False).mean()
        df_kline['kdj_j'] = 3.0 * df_kline['kdj_k'] - 2.0 * df_kline['kdj_d']
        sysmbol_kdj_k[data_symbol_usdt_list_index] = df_kline['kdj_k'][8]
        sysmbol_kdj_d[data_symbol_usdt_list_index] = df_kline['kdj_d'][8]
        sysmbol_kdj_j[data_symbol_usdt_list_index] = df_kline['kdj_j'][8]

# %%
sysmbol_kdj_k_sort = sorted(sysmbol_kdj_k.items(), key=lambda item: item[1])

# %%
sysmbol_kdj_k_sort
# %%
sysmbol_kdj_d_sort = sorted(sysmbol_kdj_d.items(), key=lambda item: item[1])
# %%
sysmbol_kdj_d_sort
# %%
sysmbol_kdj_j_sort = sorted(sysmbol_kdj_j.items(), key=lambda item: item[1])
# %%
sysmbol_kdj_j_sort

# %%
