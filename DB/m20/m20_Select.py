import time
import pyupbit
import datetime
import logging

tickername = "ETC"
iPer = 0.5
intervalMinute = 60
access = "vqjRzy8UlElasjqXHW7tDrkjXdGuxWAfxTjBx7iw"          # 본인 값으로 변경
secret = "h9sLNV3XyVJa6pAsa8EdWlxfWiONy9o8cIc6Zdzk"          # 본인 값으로 변경
iBuyPrice = 0

def get_ma20(ticker):
    """20일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute" + str(intervalMinute), count=20)
    ma15 = df['close'].rolling(20).mean().iloc[-1]
    return ma15

""" 20일 전 가격 구하기"""
def getAfter20(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute" + str(intervalMinute), count=20)
    ma15 = df['close'][0]
    return ma15


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

# 로그인
upbit = pyupbit.Upbit(access, secret)
print(getAfter20("KRW-BTT"))


#자동매매 시작
while True:
    try:
        tickers = pyupbit.get_tickers()
        for ticker in tickers:
            ma20 = get_ma20(ticker)
            After20 = getAfter20(ticker)
            nowPrice = get_current_price(ticker)

            """매수 타이밍"""
            if nowPrice > ma20 and nowPrice > ma20:
                upbit.buy_market_order(ticker, 100000)
            """매도 타이밍"""
            if nowPrice < ma20 and nowPrice < ma20:
                BTT = get_balance(ticker)
                if BTT > 0:
                    upbit.sell_market_order(ticker, BTT)
        time.sleep(1)
    except Exception as e:
        print(e)
        logging.info(e)
        time.sleep(1)