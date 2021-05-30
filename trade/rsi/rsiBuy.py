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
        Rsi7 = rsiOpen(df5,7)
        Rsi14 = rsiOpen(df5,14)

        print("---BUY--- :  " + ticker + " : " + str(Rsi7.iloc[-1]) + "  || " + str(Rsi14.iloc[-1]))

        if iCount == 0:
            if Rsi7.iloc[-2] < Rsi14.iloc[-2]:
                if Rsi7.iloc[-1] > Rsi14.iloc[-1]:
                    print(upbit.buy_market_order(ticker, 7000))
                    iCount = 1
        
        # # df3[]
        # ma1_3_Diff = df1['close'].rolling(3).mean().diff()
        # ma1_5 = df1['close'].rolling(5).mean()
        # ma1_15 = df1['close'].rolling(15).mean()
        # ma3_5 = df3['close'].rolling(5).mean()
        # ma3_15 = df3['close'].rolling(15).mean()
        
        # # ma1_3_Diff = df1['close'].rolling(3).mean().diff()
        # evg = df1['volume'].mean()
        
        

        # print("---BUY--- :  " + ticker)
        # if evg < df1['volume'].iloc[-1]:
        #     print("  "+ str(evg) + "  || " + str(df1['volume'].iloc[-1]))
        #     # 1분봉 : 15평 위에 5평이 있음
        #     if ma1_5.iloc[-1] > ma1_15.iloc[-1]:
        #         #   3분봉 : 15평 아래 5평이 있음
        #         if ma3_15.iloc[-1] > ma3_5.iloc[-1]:
        #             if df1['volume'].mean() < df1['volume'].iloc[-1]:
        #                 if iCount == 0:
        #                     print(upbit.buy_market_order(ticker, 7000))
        #                     iCount = 1        
        #                     jun.WaitSel()