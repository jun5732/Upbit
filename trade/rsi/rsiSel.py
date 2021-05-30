import requests
import pandas as pd
import time
import pyupbit
import numpy as np
import datetime

def rsiOpen(ohlc: pd.DataFrame, period: int = 14):
    ohlc["open"] = ohlc["open"]
    delta = ohlc["open"].diff()
    raw_data = {'open' : ohlc["open"] ,'delta': delta}
    data = pd.DataFrame(raw_data)
    gains, declines = delta.copy(), delta.copy()
    gains[gains < 0] = 0
    declines[declines > 0] = 0
    _gain = gains.ewm(com=(period - 1), min_periods=period).mean()
    _loss = declines.abs().ewm(com=(period - 1), min_periods=period).mean()

    RS = _gain / _loss
    return pd.Series(100 - (100 / (1 + RS)), name="RSI")
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

interval = 5

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
        
        df5 = pyupbit.get_ohlcv(ticker, interval="minute" + str(5), count=int(100))
        time.sleep(0.1)
        Rsi7 = rsiOpen(df5,7)
        Rsi14 = rsiOpen(df5,14)

        print(ticker + " : " + str(Rsi7.iloc[-2]) + "  || " + str(Rsi14.iloc[-2]))
        print("---SEL--- :  " + ticker + " : " + str(Rsi7.iloc[-1]) + "  || " + str(Rsi14.iloc[-1]))

        # if Rsi7.iloc[-2] > Rsi14.iloc[-2]:
        if Rsi7.iloc[-1] < Rsi14.iloc[-1]:
            print(upbit.sell_market_order(ticker, balance))
            # bSelect = False
WaitSel()                