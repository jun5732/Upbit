import time
import pyupbit
import datetime
import logging


access = "LYkGvTftjKrUBvJ65Y0xVxVd1QJ9gkx2fpPzlKxW"          # 본인 값으로 변경
secret = "gMKxCJQsuvxjjBllBIXjkOzxt49A4BSA3Gvhd8XU"          # 본인 값으로 변경

iTargetPer = 3
sTicker = ""
fullTicker = "KRW-" + sTicker

# 원화 마켓 주문 가격 단위
# https://docs.upbit.com/docs/market-info-trade-price-detail
def get_tick_size(price):
    if price >= 2000000:
        tick_size = round(price / 1000) * 1000
    elif price >= 1000000:
        tick_size = round(price / 500) * 500
    elif price >= 500000:
        tick_size = round(price / 100) * 100
    elif price >= 100000:
        tick_size = round(price / 50) * 50
    elif price >= 10000:
        tick_size = round(price / 10) * 10
    elif price >= 1000:
        tick_size = round(price / 5) * 5
    elif price >= 100:
        tick_size = round(price / 1) * 1
    elif price >= 10:
        tick_size = round(price / 0.1) * 0.1
    else:
        tick_size = round(price / 0.01) * 0.01
    return tick_size
    
"""특정 퍼센트 가격 조회"""
def get_Per_target_price():
    balances = upbit.get_balances()
    for b in balances:
        ticker = b['currency']
        if ticker == "KRW":
            continue
        time.sleep(1)
        fullTicker = "KRW-" + ticker
        iBuyPrice = float(b['avg_buy_price'])
        iTargetPrice = iBuyPrice + (iBuyPrice * 0.01 * iTargetPer)
        iSelPrice = get_tick_size(iTargetPrice)
        if get_CancleOrder(fullTicker ,iSelPrice) > 0:
            upbit.sell_limit_order(fullTicker, iSelPrice ,float(b['balance']))

def get_CancleOrder(ticker,tPrice):
    AllOrder = upbit.get_order(ticker)
    for oder in AllOrder:
        if oder['side'] == "ask":
            if float(oder['price']) == float(tPrice):
                return 0
            else:
                upbit.cancel_order(oder['uuid'])
    return 1



def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]




# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")


#cancel_order(self, uuid, contain_req=False):
#upbit.get_order(self, ticker_or_uuid, state='wait', kind='normal', contain_req=False):

while True:
    try:
        get_Per_target_price()
        time.sleep(1)
    except Exception as e:
        print(e)
        logging.info(e)
        time.sleep(1)