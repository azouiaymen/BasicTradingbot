from binance.client import Client 
from config import apikey
import pandas as pd
import ta
import numpy as np
import time

api_key = apikey.API_KEY
api_secret = apikey.API_SECRET

client = Client(api_key,api_secret)

def get_minute_data(symbol,interval,lookback):
  frame = pd.DataFrame(client.get_historical_klines(symbol,interval,lookback + ' min ago UTC'))
  frame = frame.iloc[:,:6]
  return frame