import requests
import pandas as pd
import time
import pyupbit
import numpy as np
import datetime


interval = 30

upbit = pyupbit.Upbit("C0Az21yejT3prbheZAUdZMCUGi9Tr1R0OlSNgIp3", "ZRozlBWm55cYlLjSmf9eBzYjhpuxUWeXKPFNzf4Q")

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

def WaitSelAll():
    while True:    
        time.sleep(1)
        for b in upbit.get_balances():
            if b['currency'] == "KRW":
                continue
            ticker = "KRW-" + b['currency']
            df = pyupbit.get_ohlcv(ticker, interval="minute" + str(3), count=int(100))
            time.sleep(0.1)

            ma1_15 = df['close'].rolling(15).mean().diff()

            
            balance = (float(b['balance']) + float(b['locked']))

            evg = df['volume'].rolling(15).mean()

            print("" + ticker +  "-----")
            print("ma1_15.iloc[-1] : " + str(ma1_15.iloc[-1]))
            
            if ma1_15.iloc[-1] < 0:
                print(upbit.sell_market_order(ticker, balance))
                bSelect = False
                

def WaitSel(ticker):
    bSelect = True
    
    for b in upbit.get_balances():
        if "KRW-" + b['currency'] == ticker:
            while bSelect:    
                time.sleep(1)
                time.sleep(0.1)
                ticker = "KRW-" + b['currency']
                df = pyupbit.get_ohlcv(ticker, interval="minute" + str(3), count=int(100))
                time.sleep(0.1)

                ma1_15 = df['close'].rolling(15).mean().diff()

                
                balance = (float(b['balance']) + float(b['locked']))

                evg = df['volume'].rolling(15).mean()

                print("" + ticker +  "-----")
                print("ma1_15.iloc[-1] : " + str(ma1_15.iloc[-1]))
                
                if ma1_15.iloc[-1] < 0:
                    print(upbit.sell_market_order(ticker, balance))
                    bSelect = False
    

# WaitSelAll()

# ticker = "KRW-EOS"
iCount = 0
while True:
    tickers = pyupbit.get_tickers("KRW")
    time.sleep(0.1)

    for ticker in tickers:
        df = pyupbit.get_ohlcv(ticker, interval="minute" + str(1), count=int(100))
        time.sleep(0.1)

        ma1_15 = df['close'].rolling(15).mean().diff()
        evg = df['volume'].rolling(15).mean()

        print("-----" + ticker +  "-----")
        print("ma1_15.iloc[-1] : " + str(ma1_15.iloc[-1]))
        
        if ma1_15.iloc[-1] > 0:
            print(str(df['close'].iloc[-1]) +   " > " + str(df['open'].iloc[-1]))
            if df['close'].iloc[-1] > df['open'].iloc[-1]:
                print(str(evg.iloc[-1] /3 * 2) +   " < " + str(df['volume'].iloc[-1]))
                if evg.iloc[-1] /3 * 2 < df['volume'].iloc[-1]:
                    print(upbit.buy_market_order(ticker, 7000))
                    iCount = 1
                    WaitSel(ticker)
            



