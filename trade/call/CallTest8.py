import requests
import pandas as pd
import time
import pyupbit
import numpy as np
import datetime


interval = 30

upbit = pyupbit.Upbit("C0Az21yejT3prbheZAUdZMCUGi9Tr1R0OlSNgIp3", "ZRozlBWm55cYlLjSmf9eBzYjhpuxUWeXKPFNzf4Q")

def rsi(ohlc: pd.DataFrame, period: int = 14):
    ohlc["close"] = ohlc["close"]
    delta = ohlc["close"].diff()
    raw_data = {'close' : ohlc["close"] ,'delta': delta}
    data = pd.DataFrame(raw_data)
    gains, declines = delta.copy(), delta.copy()
    gains[gains < 0] = 0
    declines[declines > 0] = 0
    _gain = gains.ewm(com=(period - 1), min_periods=period).mean()
    _loss = declines.abs().ewm(com=(period - 1), min_periods=period).mean()

    RS = _gain / _loss
    return pd.Series(100 - (100 / (1 + RS)), name="RSI")


def Sel(ticker):
    bSelect = True    
    for b in upbit.get_balances():
        if "KRW-" + b['currency'] == ticker:
            while bSelect:    
                time.sleep(1)
                time.sleep(0.1)
                ticker = "KRW-" + b['currency']
                
                df = pyupbit.get_ohlcv(ticker, interval="minute" + str(1), count=int(100))
                time.sleep(0.1)

                ma3 = df['close'].rolling(3).mean()
                ma15 = df['close'].rolling(15).mean()
                balance = (float(b['balance']) + float(b['locked']))
                print("====== SEL " + ticker)
                if ma15.iloc[-2] < ma3.iloc[-2]:
                    if ma15.iloc[-1] > ma3.iloc[-1]:
                        print(upbit.sell_market_order(ticker, balance))
                        bSelect = False

iCount = 0
while True:
    tickers = pyupbit.get_tickers("KRW")
    time.sleep(0.1)

    for ticker in tickers:
        df = pyupbit.get_ohlcv(ticker, interval="minute" + str(30), count=int(100))
        time.sleep(0.1)

        ma3 = df['close'].rolling(3).mean()
        ma5 = df['close'].rolling(5).mean()
        ma15 = df['close'].rolling(15).mean()
        print("BUY ======" + ticker)
        if ma15.iloc[-1] > ma5.iloc[-1] and ma15.iloc[-1] > ma3.iloc[-1]:
            if ma3.iloc[-2] < ma5.iloc[-2]:
                if ma3.iloc[-1] > ma5.iloc[-1]:
                    print(upbit.buy_market_order(ticker, 7000))
                    Sel(ticker)