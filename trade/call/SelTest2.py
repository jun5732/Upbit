import requests
import pandas as pd
import time
import pyupbit
import numpy as np
import datetime


def rsi(ticker,iDTime):
    df = pyupbit.get_ohlcv(ticker, interval="minute" + str(iDTime), count=120)
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

def WaitSel(ticker,now, inter):
    now = str(now)[0:str(now).find(".")]
    balance = 0
    bWhile = True
    bSelect = False
    iDTime = inter
    buyrsi = 0
    while bWhile:
        time.sleep(1)
        for b in upbit.get_balances():
            if "KRW-" + b['currency'] == ticker:
                balance += (float(b['balance']) + float(b['locked']))
                bSelect = True
                bWhile = False
    bSelect = True
    while bSelect:
        
        time.sleep(0.1)
        
        nTime = datetime.datetime.now()
        btime = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
        date_diff = nTime - btime
        delTime = int(date_diff.seconds / (60 * iDTime))

        if delTime < 1:
            delTime = 1
        
        url = "https://api.upbit.com/v1/candles/minutes/" + str(iDTime)
        querystring = {"market":ticker,"from":now,"count":delTime}
        response = requests.request("GET", url, params=querystring)
        data = response.json()
        df = pd.DataFrame(data)
        df=df.reindex(index=df.index[::-1]).reset_index()
        
        volumeS = df["candle_acc_trade_volume"].copy()
        volumeS[df["trade_price"] < df["opening_price"]] = volumeS * -1

        time.sleep(0.1)
        nrsi = rsi(ticker,iDTime).diff()
        
        if buyrsi == 0:
            buyrsi = nrsi.iloc[-1]

        rsiSum = nrsi.tail(delTime).sum()
        evg = df["candle_acc_trade_volume"].mean()               #   ????????? ??????    

        print(str(rsiSum) + " || " + str(evg * 2 / 3) + " < " + str(df["candle_acc_trade_volume"].iloc[-1]))
        
        # if True:
        if evg * 2 / 3 < df["candle_acc_trade_volume"].iloc[-1]:                      #   ???????????? ?????? ????????????
            if nrsi.iloc[-1] < -3 :
                # if rsiSum < buyrsi :
                upbit.sell_market_order(ticker, balance)
                print(df["trade_price"].iloc[-1])
                bSelect = False

# WaitSel("KRW-XRP" ,"2021-05-26 15:26:00.1456782",3)