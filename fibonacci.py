# %%
import datetime
import requests
import talib
import numpy as np
import show_and_save_log_file
import os
import configparser
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
# %%
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

# %%
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
data_symbol_less_than_seven_day_dict = {}
data_symbol_more_than_seven_day_and_less_than_twenty_five_day_dict = {}
data_symbol_usdt_list_short_line_dict = {}
data_symbol_usdt_list_median_line_dict = {}
data_symbol_usdt_list_long_line_dict = {}
data_symbol_less_than_seven_day = []


# %%
data_symbol_usdt_list
# %%
onedayklineindex_url = BASE_URL + '/api/v3/klines' + \
    '?symbol='+'GNOUSDT'+'&interval=1d&limit=1000'

# %%
resp = requests.get(onedayklineindex_url)

# %%
type(resp)
# %%
data = resp.json()
# %%
data

# %%
df = pd.DataFrame(data, columns=[
                  "open time", "open", "high", "low", "close", "volume", "close time", "1", "2", "3", "4", "5"])
# %%
df["open time"]

# %%
df['open time'] = pd.to_datetime(
    df['open time'].values, utc=True, unit='ms').tz_convert("Asia/Taipei").to_period("s")

# %%

# %%
df['close'] = df['close'].astype('float')

# %%
df['close']

# %%
plt.figure(figsize=(12.2, 4.5))  # width = 12.2in, height = 4.5
plt.plot(df['close'], color='blue')
plt.title('Stock Close Price')
plt.xlabel('Date')
plt.ylabel(' Price ($USD)')
plt.show()

# %%
maximum_price = df['close'].max()

# %%
maximum_price

# %%
minimum_price = df['close'].min()
# %%
minimum_price
# %%
difference = maximum_price - minimum_price
# %%
first_level = maximum_price - difference * 0.236

# %%
second_level = maximum_price - difference * 0.382

# %%
third_level = maximum_price - difference * 0.5
# %%
fourth_level = maximum_price - difference * 0.618
# %%
print("Level Percentage\t", "Price ($)")
print("00.0%\t\t", maximum_price)
print("23.6%\t\t", first_level)
print("38.2%\t\t", second_level)
print("50.0%\t\t", third_level)
print("61.8%\t\t", fourth_level)
print("100.0%\t\t", minimum_price)
# %%
new_df = df
plt.figure(figsize=(12.33, 4.5))
plt.title('Fibonnacci Retracement Plot SRM')
plt.plot(new_df.index, new_df['close'])
plt.axhline(maximum_price, linestyle='--', alpha=0.5, color='red')
plt.axhline(first_level, linestyle='--', alpha=0.5, color='orange')
plt.axhline(second_level, linestyle='--', alpha=0.5, color='yellow')
plt.axhline(third_level, linestyle='--', alpha=0.5, color='green')
plt.axhline(fourth_level, linestyle='--', alpha=0.5, color='blue')
plt.axhline(minimum_price, linestyle='--', alpha=0.5, color='purple')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price in USD', fontsize=18)
plt.show()

# %%
