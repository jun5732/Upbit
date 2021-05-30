import pymysql
import os
import pyupbit
import time
import logging
import pandas as pd


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

#   자동으로 DB에서 퍼센트를 조회해서 매도 주문을 한다.
def SetPerOrder():

    balances = upbit.get_balances()
    print("-------------------------------------------------------------------------------------------")
    for b in balances:
        if b['currency'] == "KRW":
            continue
        tabkerName = "KRW-" + b['currency']

        df = pyupbit.get_ohlcv(tabkerName, interval="minute" + str(30), count=int(200))
        time.sleep(0.1)
        ma3 = df['close'].rolling(3).mean()     #   3평 
        ma5 = df['close'].rolling(5).mean()     #   5평
        ma15 = df['close'].rolling(15).mean()   #   15평
        Rsi = rsi(df, 14)
        
        print(tabkerName + " -> " + str(ma15.iloc[-1]) + " > " + str(ma5.iloc[-1]) + " || " + str(Rsi.diff()[-1]))

        if ma15.iloc[-1] > ma5.iloc[-1] and Rsi.diff()[-1] < -5:
            balance = (float(b['balance']) + float(b['locked']))
            upbit.sell_market_order(tabkerName, balance)

upbit = pyupbit.Upbit('C0Az21yejT3prbheZAUdZMCUGi9Tr1R0OlSNgIp3','ZRozlBWm55cYlLjSmf9eBzYjhpuxUWeXKPFNzf4Q')

nowPath = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(filename=nowPath + "\SelPer1.txt", level=logging.INFO)
logging.info("--------------------------------------")
logging.info("SelPer1 autotrade start")

while True :
    SetPerOrder()
    time.sleep(1)
