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

interval = 1

upbit = pyupbit.Upbit("C0Az21yejT3prbheZAUdZMCUGi9Tr1R0OlSNgIp3", "ZRozlBWm55cYlLjSmf9eBzYjhpuxUWeXKPFNzf4Q")

# ticker = "KRW-EOS"
iCount = 0
while True:
    tickers = pyupbit.get_tickers("KRW")
    time.sleep(0.1)
    
    for ticker in tickers:
        # ticker = "KRW-TFUEL"
        df = pyupbit.get_ohlcv(ticker, interval="minute" + str(interval), count=int(200))
        time.sleep(0.1)

        ma3 = df['close'].rolling(3).mean()
        ma15 = df['close'].rolling(15).mean()
        Rsi = rsi(df, 14)

        if ma3.iloc[-2] < ma15.iloc[-2] > 0 and ma15.iloc[-1] < ma3.iloc[-1]:# and Rsi.iloc[-1] < 60:
            print(upbit.buy_market_order(ticker, 7000))
            now = datetime.datetime.now()
            jun.WaitSel(ticker ,now,1)

