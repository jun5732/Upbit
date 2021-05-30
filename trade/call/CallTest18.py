import requests
import pandas as pd
import time
import pyupbit
import numpy as np
import datetime
from bs4 import BeautifulSoup


access = "C0Az21yejT3prbheZAUdZMCUGi9Tr1R0OlSNgIp3"
secret = "ZRozlBWm55cYlLjSmf9eBzYjhpuxUWeXKPFNzf4Q"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

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
# 로그인
upbit = pyupbit.Upbit("C0Az21yejT3prbheZAUdZMCUGi9Tr1R0OlSNgIp3", "ZRozlBWm55cYlLjSmf9eBzYjhpuxUWeXKPFNzf4Q")
print("autotrade start")

# 자동매매 시작
iTime = 60
bRun = False
# bRun = True


while True:
    time.sleep(0.1)
    df = pyupbit.get_ohlcv("KRW-BTC", interval="minute" + str(iTime), count=int(1))
    time.sleep(0.1)
    now = datetime.datetime.now()
    start_time = df.index[-1]
    end_time = start_time + datetime.timedelta(minutes=iTime)        

    if start_time < now < end_time - datetime.timedelta(seconds=20):
        krw = get_balance("KRW")
        if krw is None:
            krw = 0
        # if True:
        if krw > 5000:
            tickers = FindTacker()
            for tic in tickers:
                ticker = "KRW-" + str(tic).replace('/KRW', '')
                # ticker = "KRW-RFR"
                time.sleep(0.1)
                df = pyupbit.get_ohlcv(ticker, interval="minute" + str(iTime), count=int(100))
                print(ticker)
                ma3 = df['close'].rolling(3).mean()
                ma5 = df['close'].rolling(5).mean()
                ma15 = df['close'].rolling(15).mean()
                target_price = df.iloc[-2]['close'] + (df.iloc[-2]['high'] - df.iloc[-2]['low']) * 0.2
                current_price = df.iloc[-1]['close']

                if ma15.iloc[-1] > ma15.iloc[-2] > ma15.iloc[-3]:
                    print("ma5 : " + str(ma5.iloc[-1]) +  " > " +  str(ma15.iloc[-1]))
                    if ma5.iloc[-1] > ma15.iloc[-1]:
                        print("target_price : " + str(target_price) +  " < " +  str(current_price))
                        if target_price < current_price:                    
                            time.sleep(0.1)
                            # print(upbit.buy_market_order(ticker, 7000))
                            print(upbit.buy_market_order(ticker, krw*0.9995))
    else:
        print("============== SELL ==============")
        time.sleep(0.1)
        for b in upbit.get_balances():
            if b['currency'] == "KRW":
                continue            
            ticker = "KRW-" + b['currency']
            balance = (float(b['balance']) + float(b['locked']))
            if balance * b['avg_buy_price'] > 5000:
                try:
                    print(upbit.sell_market_order(ticker, balance*0.9995))
                    time.sleep(0.1)
                except:
                    print("")