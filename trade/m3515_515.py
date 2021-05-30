import requests
import pandas as pd
import time
import pyupbit
import numpy as np
import time


def get_ma(ticker,intervalMinute,icount):
    df = pyupbit.get_ohlcv(ticker, interval="minute" + str(intervalMinute), count=icount)
    ma = df['close'].rolling(icount).mean().iloc[-1]
    return ma


while True:
    tickers = pyupbit.get_tickers("KRW")
    for ticker in tickers:
        ma3_5 = get_ma(ticker,3,5)
        ma3_15 = get_ma(ticker,3,15)
        time.sleep(0.1)
        ma5_5 = get_ma(ticker,5,5)
        ma5_15 = get_ma(ticker,5,15)
        time.sleep(0.1)
        ma15_5 = get_ma(ticker,15,5)
        ma15_15 = get_ma(ticker,15,15)
        time.sleep(0.1)

        if ma3_5 > ma3_15 and ma5_5 > ma5_15 and ma15_5 > ma15_15:
            print(ticker)










            