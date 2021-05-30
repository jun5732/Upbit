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

vas = []
iCount = 0
while iCount < 4:
    tickers = pyupbit.get_tickers("KRW")
    for ticker in tickers:
        # ticker = "KRW-BTT"
        if ticker == "KRW-XRP":
            continue

        
        df = pyupbit.get_ohlcv(ticker, interval="minute5")
        ma3 = df['close'].rolling(5).mean()
        ma15 = df['close'].rolling(15).mean()
        ma15Dif = ma15.diff()

        print(ticker + " -> " +str(ma3[-2]) + " < " + str(ma15[-2]) + " | " + str(ma3[-1]) + " > " + str(ma15[-1]) + " | " + str(ma15Dif[-1]))
        if ma3[-2] < ma15[-2] and ma3[-1] > ma15[-1] and ma15Dif[-1] > 0:
            upbit.buy_market_order(ticker, 50000)
            iCount = iCount + 1
            if iCount == 3:
                break

        
        
        
        

        # ma3_1 = df['close'].rolling(3).mean().iloc[-2]
        # ma15_1 = df['close'].rolling(15).mean().iloc[-2]
        
        # print(ticker + " -> " +str(ma3) + " | " + str(ma3_1) + " | " + str(ma15) + " | " + str(ma15_1))
        # print("1")
        # for va in vas:
        #     if va == ticker:
        #         continue
        # inter = 5
        # df = pyupbit.get_ohlcv(ticker, interval="minute" + str(inter), count=200)
        # ohlc: pd.DataFrame = df
        # ohlc["volume"] = ohlc["volume"]
        # delta = ohlc["volume"].diff()
        # # gains, declines = delta.copy(), delta.copy()
        # ttaD = ohlc["volume"].copy()
        # evg = ttaD.abs().sum() / ttaD.count()
        # # gains[gains < 0] = 0
        # # declines[declines > 0] = 0
        
        # ttal,gains, declines = df["volume"].copy(), df["volume"].copy(), df["volume"].copy()
        # ttal[df['close'] < df['open']] = ttal * -1
        # gains[df['close'] > df['open']] = 0
        # declines[df['close'] < df['open']] = 0
        # ma1 =  get_ma(ticker,inter,5)
        # ik = 3
        
        # at = {'volume':df["volume"],'ttal':ttal,'gains':gains,'declines':declines}
        # data = pd.DataFrame(at)
        
        # # volume = round(5000 / df['close'][-1],1)
        
        # if ttaD[-1] > evg and df["close"][-1] > ma1 and df['close'][-1] > df['open'][-1]:
        #     print(ticker + "|" + str(df['volume'][-1]))
        #     if ttaD[-1] > 3000:
        #         print(ticker + "|" + str(df['volume'][-1])  + "|" +  str(df['volume'].mean()) + "|" + str(ttal[-1]) + "|" + str(ttal.sum()))
        #         upbit.buy_market_order(ticker, 10000)
        #         vas.append(ticker)
        #         time.sleep(1)

        # if df['volume'][-1] > df['volume'].mean():
        #     # if df['close'][-1] > df['open'][-1]:
        #     if ttal[-1] > 0:
        #         # if gains.sum() > abs(declines.sum()):
        #         if ttal.sum() > 0:
        #             print(ttal)
        #             print(ticker + "|" + str(df['volume'][-1])  + "|" +  str(df['volume'].mean()) + "|" + str(ttal[-1]) + "|" + str(ttal.sum()))
        #             upbit.buy_market_order(ticker, 10000)
        #             # print(upbit.buy_limit_order(ticker, df['close'][-1], volume))
        #             print(df)
                        
                    
                    

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
        
