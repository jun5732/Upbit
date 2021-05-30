import requests
import pandas as pd
import time
import pyupbit
import numpy as np
import datetime

a = 1
a = 2
def rsi(ohlc: pd.DataFrame, period: int = 14):
    ohlc["close"] = ohlc["close"]
    delta = ohlc["close"].diff()
    raw_data = {'close' : ohlc["close"] ,'delta': delta}
    data = pd.DataFrame(raw_data)
    print(data)
    gains, declines = delta.copy(), delta.copy()
    gains[gains < 0] = 0
    declines[declines > 0] = 0
    print(gains)
    print(declines)
    _gain = gains.ewm(com=(period - 1), min_periods=period).mean()
    _loss = declines.abs().ewm(com=(period - 1), min_periods=period).mean()

    RS = _gain / _loss
    return pd.Series(100 - (100 / (1 + RS)), name="RSI")


# url = "https://api.upbit.com/v1/candles/minutes/15"
# querystring = {"market":"KRW-ATOM","count":"200"}
# response = requests.request("GET", url, params=querystring)
# data = response.json()
# df = pd.DataFrame(data)
# print(df)


def get_ma(ticker,intervalMinute,icount):
    df = pyupbit.get_ohlcv(ticker, interval="minute" + str(intervalMinute), count=icount)
    ma = df['close'].rolling(icount).mean().iloc[-1]
    return ma

upbit = pyupbit.Upbit("C0Az21yejT3prbheZAUdZMCUGi9Tr1R0OlSNgIp3", "ZRozlBWm55cYlLjSmf9eBzYjhpuxUWeXKPFNzf4Q")

while True:
    tickers = pyupbit.get_tickers("KRW")
    for ticker in tickers:
        # ticker = "KRW-BTT"
        if ticker == "KRW-XRP":
            continue
            
        df = pyupbit.get_ohlcv(ticker, interval="minute" + str(1), count=200)
        ohlc: pd.DataFrame = df
        ohlc["volume"] = ohlc["volume"]
        delta = ohlc["volume"].diff()
        # gains, declines = delta.copy(), delta.copy()
        ttaD = delta.abs().copy()
        evg = ttaD.sum() / ttaD.count()
        # gains[gains < 0] = 0
        # declines[declines > 0] = 0
        
        ttal,gains, declines = df["volume"].copy(), df["volume"].copy(), df["volume"].copy()
        ttal[df['close'] < df['open']] = ttal * -1
        gains[df['close'] > df['open']] = 0
        declines[df['close'] < df['open']] = 0

        ma = df['volume'].rolling(3).mean()
        ik = 3
        
        at = {'volume':df["volume"],'ttal':ttal,'gains':gains,'declines':declines}
        data = pd.DataFrame(at)
        
        # volume = round(5000 / df['close'][-1],1)

        # if ttaD[-1] > evg:
        #     print(str(ttaD[-1]) + " || " + evg)

        if df['volume'][-1] > ttal.mean():
        # if df['volume'][-1] > df['volume'].mean():
            # if df['close'][-1] > df['open'][-1]:
            if df['volume'][-1] > 0:
                # if gains.sum() > abs(declines.sum()):
                if df['volume'].sum() > 0:
                    print(ttal)
                    print(ticker + "|" + str(df['volume'][-1])  + "|" +  str(df['volume'].mean()) + "|" + str(ttal[-1]) + "|" + str(ttal.sum()))
                    upbit.buy_market_order(ticker, 10000)
                    # print(upbit.buy_limit_order(ticker, df['close'][-1], volume))
                    print(df)
                        
                    
                    

        # print(df['volume'].mean())
        # print(str(df['volume'][-1]))
        # ma1 = df['close'].rolling(ik).mean().iloc[-3]
        # ma2 = df['close'].rolling(ik).mean().iloc[-2]
        # ma3 = df['close'].rolling(ik).mean().iloc[-1]
        # print(str(ma1))
        # print(str(ma2))
        # print(str(ma3))
        # print("--------------------------------------------")
        time.sleep(1)
        
