import requests
import pandas as pd
import time
import pyupbit
import numpy as np
import datetime
from bs4 import BeautifulSoup

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
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

iTime = 30
# iTime = 60

upbit = pyupbit.Upbit("C0Az21yejT3prbheZAUdZMCUGi9Tr1R0OlSNgIp3", "ZRozlBWm55cYlLjSmf9eBzYjhpuxUWeXKPFNzf4Q")

def FindTacker():
    # 데이터 스크래핑
    url = "https://www.coingecko.com/ko/거래소/upbit"
    resp = requests.get(url)

    # 데이터 선택
    bs = BeautifulSoup(resp.text,'html.parser')
    selector = "tbody > tr > td > a"
    columns = bs.select(selector)

    # TOP 5 추출    
    ticker_in_krw = [x.text.strip() for x in columns if x.text.strip()[-3:] == "KRW"]
    return ticker_in_krw

while True:
    print("---------------------------------------------------------------------------------------")
    tickers = FindTacker()
    vas = []
    for tic in tickers:
        time.sleep(0.1)
        ticker = "KRW-" + str(tic).replace('/KRW', '')
        print(ticker)
        df = pyupbit.get_ohlcv(ticker, interval="minute" + str(iTime), count=int(100))
        
        # evg = df["volume"].mean()               #   거래량 평균    
        # print(evg)
        
        # volumeS = df["volume"].copy()
        # volumeS[df["close"] < df["open"]] = volumeS * -1
        # print(volumeS[-1])

        ma3 = df['close'].rolling(3).mean()
        ma5 = df['close'].rolling(5).mean()
        ma15 = df['close'].rolling(15).mean()
        ma15Def = ma15.diff()

        if ma3.iloc[-2] < ma5.iloc[-2]:
            if ma3.iloc[-1] > ma5.iloc[-1]:
                if df["close"].iloc[-1] - df["open"].iloc[-1] > 0 :
                    if df["volume"].mean() < df["volume"].iloc[-1]:
                        print(upbit.buy_market_order(ticker, 7000))

        
        # print("ma5 : " + str(ma5.iloc[-1]) +  " > " +  str(ma5.iloc[-2]) + " > " + str(ma5.iloc[-3]))
        # if ma5.iloc[-1] > ma5.iloc[-2] > ma5.iloc[-3]:
        #     print("ma15 : " + str(ma15.iloc[-1]) +  " > " +  str(ma15.iloc[-2]) + " > " + str(ma15.iloc[-3]))
        #     if ma15.iloc[-1] > ma15.iloc[-2] > ma15.iloc[-3]:
        #     # print("ma15Def : " + str(ma15Def.iloc[-1]) +  " > " +  str(ma15Def.iloc[-2]) + " > " + str(ma15Def.iloc[-3]))
        #     # if ma15Def.iloc[-1] > ma15Def.iloc[-2] > ma15Def.iloc[-3]:
        #         krw = get_balance("KRW")
        #         time.sleep(0.1)
        #         if krw is None:
        #             krw = 0
        #         # if True:
        #         if krw > 5000:
        #             print(upbit.buy_market_order(ticker, 7000))
                    # print(upbit.buy_market_order(ticker, krw*0.9995))
        
    # print(data)
    # if len(data) > 0:
    #         print(data['ticker'][0])