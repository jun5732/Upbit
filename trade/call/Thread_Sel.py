import requests
import pandas as pd
import time
import pyupbit
import numpy as np
import datetime
import threading


def rsi(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute" + str(1), count=120)
    ohlc: pd.DataFrame = df
    ohlc["close"] = ohlc["close"]
    delta = ohlc["close"].diff()
    raw_data = {'close' : ohlc["close"] ,'delta': delta}
    data = pd.DataFrame(raw_data)
    gains, declines = delta.copy(), delta.copy()
    gains[gains < 0] = 0
    declines[declines > 0] = 0
    _gain = gains.ewm(com=(14 - 1), min_periods=14).mean()
    _loss = declines.abs().ewm(com=(14 - 1), min_periods=14).mean()

    RS = _gain / _loss
    return pd.Series(100 - (100 / (1 + RS)), name="RSI")

interval = 1
upbit = pyupbit.Upbit("C0Az21yejT3prbheZAUdZMCUGi9Tr1R0OlSNgIp3", "ZRozlBWm55cYlLjSmf9eBzYjhpuxUWeXKPFNzf4Q")


class SelClass(threading.Thread):
    def __init__(self,name,now):
        super().__init__()
        self.name = name
        self.now = now

    # def run(self):
    #     print("sub thread start ", threading.currentThread().getName())
    #     time.sleep(3)
    #     print("sub thread end ", threading.currentThread().getName())
            
    def run(self):
        balance = 0
        bWhile = True
        bSelect = False
        ticker = self.name
        now = self.now

        while bWhile:
            time.sleep(1)
            for b in upbit.get_balances():
                if "KRW-" + b['currency'] == ticker:
                    balance += (float(b['balance']) + float(b['locked']))
                    bSelect = True
                    bWhile = False
        bSelect = True
        while bSelect:            
            time.sleep(1)
            
            nTime = datetime.datetime.now()
            btime = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
            date_diff = nTime - btime
            delTime = int(date_diff.seconds / 60)
            
            url = "https://api.upbit.com/v1/candles/minutes/1"
            querystring = {"market":ticker,"from":now,"count":delTime}
            response = requests.request("GET", url, params=querystring)
            data = response.json()
            df = pd.DataFrame(data)
            df=df.reindex(index=df.index[::-1]).reset_index()
            
            volumeS = df["candle_acc_trade_volume"].copy()
            volumeS[df["trade_price"] < df["opening_price"]] = volumeS * -1

            nrsi = rsi(ticker).diff()
            nrsi1 = nrsi.iloc[-1]
            RsiSum = nrsi.tail(delTime).sum()
            print(RsiSum)

            if RsiSum < 0:
                upbit.sell_market_order(ticker, balance)
                print(df["trade_price"].iloc[-1])
                bSelect = False