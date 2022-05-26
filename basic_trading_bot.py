from binance.client import Client 
from config import apikey
import pandas as pd
import ta
import numpy as np
import time

api_key = apikey.API_KEY
api_secret = apikey.API_SECRET

# create a connection with API
client = Client(api_key,api_secret)


# fetch the minute data
def get_minute_data(symbol,interval,lookback):
  frame = pd.DataFrame(client.get_historical_klines(symbol,interval,lookback + ' min ago UTC'))
  frame = frame.iloc[:,:6]
  frame.columns = ['Time','Low','High','Open','Close','Volume']
  frame = frame.set_index('Time')
  frame.index = pd.to_datetime(frame.index, unit = 'ms')
  frame = frame.astype(float)
  return frame



df = get_minute_data('BTCUSDT','1m','100')

df

def technical_analysis(df):
  df['%K'] = ta.momentum.stoch(df.High,df.Low,df.Close,
                               window = 14, smooth_window = 3)
  df['%D'] = df['%K'].rolling(3).mean()
  df['RSI'] = ta.momentum.rsi(df.Close,window=14)
  df['MACD'] = ta.trend.macd_diff(df.Close)
  df.dropna(inplace=True)

  technical_analysis(df)

  df