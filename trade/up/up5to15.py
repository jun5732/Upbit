import requests
import pandas as pd
import time
import pyupbit



upbit = pyupbit.Upbit("C0Az21yejT3prbheZAUdZMCUGi9Tr1R0OlSNgIp3", "ZRozlBWm55cYlLjSmf9eBzYjhpuxUWeXKPFNzf4Q")
intervalMinute = 1

tickers = pyupbit.get_tickers("KRW")
for ticker in tickers:    
    df15 = pyupbit.get_ohlcv(ticker, interval="minute" + str(intervalMinute), count=16)
    time.sleep(1)
    ma15 = df15['close'].rolling(15).mean().iloc[-2]
    ma5 = df15['close'].rolling(5).mean().iloc[-2]
    
    ma15_1 = df15['close'].rolling(15).mean().iloc[-1]
    ma5_1 = df15['close'].rolling(5).mean().iloc[-1]

    print(ticker + " IS 15 -> " + str(ma15) + "  => "+ str(ma5) + " || 15_1 -> " + str(ma15_1) + "  => "+ str(ma5_1))
    if ma15 > ma5 and ma15_1 < ma5_1 and ma15_1 > ma15:
        upbit.buy_market_order(ticker, 10000)
