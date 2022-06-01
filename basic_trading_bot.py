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


class signal:

  def __init__(self,df,lags):
      self.df = df
      self.lags = lags

  def get_signal(self):
    dfx = pd.DataFrame()

    for i in range(self.lags + 1):
      mask = (self.df['%K'].shift(i) < 20) & (self.df['%D'].shift(i) < 20) 
      dfx = dfx.append(mask, ignore_index=True)
    
    return dfx.sum(axis=0)

  def order(self):
    self.df['Trigger'] = np.where(self.get_signal(),1,0)
    self.df['Buy'] = np.where((self.df.Trigger) & 
                              (self.df['%K'].between(20,80)) &
                              (self.df['%D'].between(20,80)) &
                              (self.df.RSI > 50) &
                              (self.df.MACD >0),1,0)

inst.order()

inst.df


def strategy(pair,qte,open_position = False):
  df = get_minute_data(pair,'1m','100')
  technical_analysis(df)
  inst = signal(df,10)
  inst.order()
  print(f'Current Close is '+str(df.Close.iloc[-1]))
  if df.Buy.iloc[-1]:
    order = client.create_order(symbol=pair,
                                side='BUY',
                                type='MARKET',
                                quantity=qte)
    print(order)
    buyprice = float(order['fills'][0]['price'])
    open_position = True
    while open_position :
      time.sleep(0.5)
      df = get_minute_data(pair,'1m','2')
      print(f'current Close '+ str(df.Close.iloc[-1]))
      print(f'current Target '+ str(df.Close.iloc[-1]*1.005))
      print(f'current Stop is '+ str(df.Close.iloc[-1]*0.997))

      if df.Close.iloc[-1] <= buyprice*0.997 & df.Close[-1] >= buyprice[-1]*1.005 :
        order = client.create_order(symbol=pair,
                                side='SELL',
                                type='MARKET',
                                quantity=qte)
        print(order)
        break



strategy("ADAUSDT",1)