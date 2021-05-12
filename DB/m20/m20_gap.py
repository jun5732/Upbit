
import time
import pyupbit


intervalMinute = 30

def get_ma20(ticker,icount):
    """20봉 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute" + str(intervalMinute), count=icount)
    ma20 = df['close'].rolling(20).mean().iloc[-1]
    return ma20

def get_After20(ticker,icount):
    """20봉 전 금액 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute" + str(intervalMinute), count=icount)
    return df['close'][0]

def get_After2(ticker,icount):
    """20봉 전 금액 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute" + str(intervalMinute), count=icount + 1)
    global a20
    global a21
    
    a20  = df['close'][1]
    a21 = df['close'][0]

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

upbit = pyupbit.Upbit("LM6x7zWpGDRsx3xyQuLhAeEf4aVI22KLxtCogCfM","Pm9xi0Jl14auFBJgBq5SwICpvyTLFVRQ95IVOdzv")

while(True):
    print("START---------------")
    for ticker in pyupbit.get_tickers("KRW"):
        m20 = get_ma20(ticker,20)
        get_After2(ticker ,20)
        np = get_current_price(ticker)
        if m20 < np and  a20 < np and np < a21:
            print(ticker + " -> a20 : " + str(a20) + "  . np : " + str(np))
        time.sleep(1)
    print("---------------END")
#balances = upbit.get_balances()