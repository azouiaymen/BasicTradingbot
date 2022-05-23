from multiprocessing.connection import Client
from binance import *
from config import apikey
import pandas as pd
import ta
import numpy as np
import time

api_key = apikey.API_KEY
api_secret = apikey.API_SECRET
client = set(api_key,api_secret)

client = Client(api_key,api_secret)