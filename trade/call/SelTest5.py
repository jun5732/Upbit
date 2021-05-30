import requests
import pandas as pd
import time
import pyupbit
import numpy as np
import datetime


def rsi(ticker,iDTime):
    df = pyupbit.get_ohlcv(ticker, interval="minute" + str(iDTime), count=120)
    ohlc: pd.DataFrame = df
    ohlc["close"] = ohlc["close"]
    delta = ohlc["close"].diff()
    raw_data = {'close' : ohlc["close"] ,'delta': delta}
    data = pd.DataFrame(raw_data)
    gains, declines = delta.copy(), delta.copy()
    gains[gains < 0] = 0
    declines[declines > 0] = 0
    _gain = gains.ewm(com=(14 - 1), min_periods=14).mean()
    _loss = declines.abs().ewm(com=(14 - 1), min_periods=14).mean()

    RS = _gain / _loss
    return pd.Series(100 - (100 / (1 + RS)), name="RSI")

interval = 1
upbit = pyupbit.Upbit("C0Az21yejT3prbheZAUdZMCUGi9Tr1R0OlSNgIp3", "ZRozlBWm55cYlLjSmf9eBzYjhpuxUWeXKPFNzf4Q")

def WaitSel():
    bSelect = True
    
    while bSelect:    
        time.sleep(1)
        for b in upbit.get_balances():
            if b['currency'] == "KRW":
                continue
        ticker = "KRW-" + b['currency']
        balance = (float(b['balance']) + float(b['locked']))
                
        df1 = pyupbit.get_ohlcv(ticker, interval="minute" + str(1), count=int(100))
        time.sleep(0.1)
        df3 = pyupbit.get_ohlcv(ticker, interval="minute" + str(3), count=int(100))
        time.sleep(0.1)
        df5 = pyupbit.get_ohlcv(ticker, interval="minute" + str(5), count=int(100))
        time.sleep(0.1)
        df15 = pyupbit.get_ohlcv(ticker, interval="minute" + str(15), count=int(100))
        time.sleep(0.1)

        ma1_3_Diff = df1['close'].rolling(3).mean().diff()
        ma1_5 = df1['close'].rolling(5).mean()
        ma1_15 = df1['close'].rolling(15).mean()
        ma3_5 = df3['close'].rolling(5).mean()
        ma3_15 = df3['close'].rolling(15).mean()
        ma5_5 = df3['close'].rolling(5).mean()
        ma5_15 = df3['close'].rolling(15).mean()
        ma15_5 = df15['close'].rolling(5).mean()
        ma15_15 = df15['close'].rolling(15).mean()


        print("SEL :  " + ticker)

        # 1분봉 : 15평 아래 5평이 있음
        if ma1_15.iloc[-1] > ma1_5.iloc[-1]:
            #   3분봉 : 15평 아래 5평이 있음
            if ma3_15.iloc[-1] > ma3_5.iloc[-1]:
                if ma5_15.iloc[-1] > ma5_5.iloc[-1]:
                    if ma15_15.iloc[-1] > ma15_5.iloc[-1]:
                        print(upbit.sell_market_order(ticker, balance))
                        bSelect = False

WaitSel()