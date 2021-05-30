import requests
import pandas as pd
import time
import pyupbit
import numpy as np
import datetime
import SelTest2 as jun

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

interval = 3

upbit = pyupbit.Upbit("C0Az21yejT3prbheZAUdZMCUGi9Tr1R0OlSNgIp3", "ZRozlBWm55cYlLjSmf9eBzYjhpuxUWeXKPFNzf4Q")

while True:
    print("---------------------------------------------------------------------------------------")
    if len(upbit.get_balances("KRW")[0]) == 2:
        time,time.sleep(1)
        continue
    tickers = pyupbit.get_tickers("KRW")
    vas = []
    for ticker in tickers:
        df = pyupbit.get_ohlcv(ticker, interval="minute1", count=1440)
        va = ({'ticker':ticker,'volume':df['volume'].sum()})
        # va = ({'ticker':ticker,'volume':int(df['volume'].mean())})
        vas.append(va)
        time.sleep(0.1)

    data = pd.DataFrame(vas)
    data = data.sort_values(by='volume',ascending=False) #.head(50)
    
    for ticker in data['ticker']:
        if len(upbit.get_balances("KRW")[0]) == 2:
            break
        # ticker = "KRW-XEM"
        time.sleep(0.1)
        df = pyupbit.get_ohlcv(ticker, interval="minute" + str(interval), count=int(200 /interval))
        volumeS = df["volume"].copy()
        volumeS[df["close"] < df["open"]] = volumeS * -1
        
        evg = df["volume"].mean()               #   거래량 평균             
        ma5 = df['close'].rolling(5).mean()     #   5평
        ma15 = df['close'].rolling(15).mean()   #   15평
        ma5Diff = ma5.diff()                    #   5평 상승액
        ma15Diff = ma15.diff()                  #   15평 상승액
        nowPrice = df['close'][-1]
        
        Rsi = rsi(df, 14)
        nrsi = Rsi.iloc[-1]
        nrsi2 = Rsi.iloc[-2]
        nrsi3 = Rsi.iloc[-3]
        
        # print("<<<<<<<<  " + ticker + " >>>>>>>>>>>>>>>>")
        # print("EVG : " + str(evg) + "  ||  volume : " + str(df["volume"][-1]))
        # print(str(ma15Diff[-1]) + "  > : " + str(ma15Diff[-2]))
        # print(ticker + " -> " + str(df['close'][-1]))


        # if ma5Diff[-1] > ma5Diff[-2] > 0:           #   5평이 상승 추세일때
        #     print(str(ma15Diff[-1]) + "  > : " + str(ma15Diff[-2]))
        # if ma15Diff[-1] > ma15Diff[-2] > 0:     #   15평이 상승 추세일때
        #     print(ticker + " -> " + str(df['close'][-1]))

        print("<<<<<<<<  " + ticker + " >>>>>>>>>>>>>>>>")
        if df['close'][-1] > df['open'][-1]:                #   양봉일때
            print("PLUS : " + str(df['close'][-1]) + " > " + str(df['open'][-1]))
            # print("EVG : " + str(evg) + "  ||  volume : " + str(df["volume"][-1]))
            if evg < df["volume"][-1]:                      #   거래량이 평균 이상일때
                print("MA5 : " + str(ma5Diff[-1]) + "  > : " + str(ma5Diff[-2]))
                if ma5Diff[-1] > 0 and  ma5Diff[-2] > 0:           #   5평이 상승 추세일때
                    # print(str(ma15Diff[-1]) + "  > : " + str(ma15Diff[-2]))
                    print("RSI : " + str(nrsi))
                    # if ma15Diff[-1] > ma15Diff[-2] > 0:     #   15평이 상승 추세일때
                    # if nrsi - nrsi2 > 5:
                    if True:
                        if nrsi2 < 50 and nrsi > nrsi2:
                            print("<<<<<<<<  " + ticker + " >>>>>>>>>>>>>>>>")
                            print("EVG : " + str(evg) + "  ||  volume : " + str(df["volume"][-1]))
                            print(str(ma15Diff[-1]) + "  > : " + str(ma15Diff[-2]))
                            print(ticker + " -> " + str(df['close'][-1]))
                            print(ticker + " -> " + str(df['close'][-1]))                            
                            upbit.buy_market_order(ticker, 8000)
                            now = datetime.datetime.now()
                            jun.WaitSel(ticker ,now ,interval)