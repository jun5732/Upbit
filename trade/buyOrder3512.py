import time
import pyupbit
import datetime
import logging


intervalMinute = 3

def get_ma15(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute" + str(intervalMinute), count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_ma5(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute" + str(intervalMinute), count=5)
    ma5 = df['close'].rolling(5).mean().iloc[-1]
    return ma5

def get_ma3(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute" + str(intervalMinute), count=3)
    ma3 = df['close'].rolling(3).mean().iloc[-1]
    return ma3
    
def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if "KRW" + b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
    return 0

upbit = pyupbit.Upbit('C0Az21yejT3prbheZAUdZMCUGi9Tr1R0OlSNgIp3','ZRozlBWm55cYlLjSmf9eBzYjhpuxUWeXKPFNzf4Q')

iType = 0
while True :
    # tickers = pyupbit.get_tickers("KRW")
    # for ticker in tickers:
    ticker = "KRW-ADA"
    ma3 = get_ma3(ticker)
    ma5 = get_ma5(ticker)
    ma15 = get_ma15(ticker)
    time.sleep(1)
    
    if ma3 > ma5 > ma15 and iType > 0:
        print(ticker)
        if get_balance(ticker) < 1:
            upbit.buy_market_order(ticker, 5000)
            iType = 0
    if ma5 < ma15 or ma3 < ma15:
        iType = 1
