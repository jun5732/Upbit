import requests
import pandas as pd
import time
import pyupbit
import numpy as np
import datetime
import SelTest6 as JUN

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

interval = 30

upbit = pyupbit.Upbit("C0Az21yejT3prbheZAUdZMCUGi9Tr1R0OlSNgIp3", "ZRozlBWm55cYlLjSmf9eBzYjhpuxUWeXKPFNzf4Q")

# ticker = "KRW-EOS"
iCount = 0
while True:
    tickers = pyupbit.get_tickers("KRW")
    time.sleep(0.1)
    
    for ticker in tickers:
        # ticker = "KRW-SAND"
        # df = pyupbit.get_ohlcv(ticker, interval="minute" + str(interval), count=int(200))
        # time.sleep(0.1)
        df5 = pyupbit.get_ohlcv(ticker, interval="minute" + str(5), count=int(100))
        time.sleep(0.1)
        df1 = pyupbit.get_ohlcv(ticker, interval="minute" + str(1), count=int(100))
        time.sleep(0.1)
        ma1_15 = df1['close'].rolling(15).mean().diff()

        dif = df5['close'].diff()
        print(ticker)
        if ma1_15.iloc[-1] > 0:
            print(str(df1['close'].iloc[-1]) +  "<" +  str(df1['close'].iloc[-2]) + "<" +  str(df1['close'].iloc[-3]))
            if df1['close'].iloc[-1] >  df1['close'].iloc[-2] >  df1['close'].iloc[-3]:
                print(upbit.buy_market_order(ticker, 7000))
                JUN.WaitSel()
        
