import requests
import pandas as pd
import time
import pyupbit
import numpy as np
import datetime
import SelTest4 as jun

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
        # ticker = "KRW-TFUEL"
        # df = pyupbit.get_ohlcv(ticker, interval="minute" + str(interval), count=int(200))
        # time.sleep(0.1)
        df1 = pyupbit.get_ohlcv(ticker, interval="minute" + str(1), count=int(200))
        time.sleep(0.1)
        df3 = pyupbit.get_ohlcv(ticker, interval="minute" + str(3), count=int(200))
        time.sleep(0.1)
        df5 = pyupbit.get_ohlcv(ticker, interval="minute" + str(5), count=int(200))
        time.sleep(0.1)

        # df3[]
        ma1 = df1['close'].rolling(15).mean().diff()        #   3평 
        ma3 = df3['close'].rolling(15).mean().diff()        #   5평
        ma5 = df5['close'].rolling(15).mean().diff()        #   15평
        
        ma13 = df1['close'].rolling(3).mean()           #   3평 
        ma115 = df1['close'].rolling(15).mean()         #   3평 

        print(ticker)
        print(ma1.iloc[-1])
        print(ma3.iloc[-1])
        print(ma5.iloc[-1])
        if ma1.iloc[-1] > 0 and ma3.iloc[-1] > 0:# and ma5.iloc[-1] > 0:
            if ma115.iloc[-2] > ma13.iloc[-2] and ma115.iloc[-1] < ma13.iloc[-1]:
                if df3['volume'].mean() < df3['volume'].iloc[-1]:
                    if iCount == 0:
                        print(upbit.buy_market_order(ticker, 7000))
                        now = datetime.datetime.now()
                        jun.WaitSel(ticker ,now,1)
                        iCount = 1

