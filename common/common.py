import time
import pyupbit
import datetime
import logging
import pandas as pd
import queue
from collections import deque

access = "vqjRzy8UlElasjqXHW7tDrkjXdGuxWAfxTjBx7iw"          # 본인 값으로 변경
secret = "h9sLNV3XyVJa6pAsa8EdWlxfWiONy9o8cIc6Zdzk"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)
intervalMinute = 30
iHopePer = 3

# 현재가 조회
def get_current_price(ticker):    
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 3분봉이 15일봉을 상향 돌파 하는 순간을 찾는다.


# 15,60,120 정배열중 거래량 가장 많은 애를 찾는다.
def findListTarget():
        
    krw_tickers = pyupbit.get_tickers("KRW")
    arList = []

    for ticker in krw_tickers:    
        df = pyupbit.get_ohlcv(ticker , interval="minute" + str(intervalMinute))
        tVolume = sum(df['volume']) / len(df['volume'])

        close = df['close']

        ma15 = deque(maxlen=15)
        ma50 = deque(maxlen=50)
        ma120 = deque(maxlen=120)

        ma15.extend(df['close'])
        ma50.extend(df['close'])
        ma120.extend(df['close'])

        curr_ma15 = sum(ma15) / len(ma15)
        curr_ma50 = sum(ma50) / len(ma50)
        curr_ma120 = sum(ma120) / len(ma120)


        window = close.rolling(3)
        ma5 = window.mean()
        avg_ma3 = ma5[-1]
        avg_ma3_2 = ma5[-2]
        avg_ma3_3 = ma5[-3]

        window = close.rolling(15)
        ma5 = window.mean()
        avg_ma15 = ma5[-1]
        avg_ma15_2 = ma5[-2]
        avg_ma15_3 = ma5[-3]

        if curr_ma15 > curr_ma50 > curr_ma120:
            print("a")
            if avg_ma15 < avg_ma3:
                print(str(avg_ma15_3) + " > " + str(avg_ma3_3) + " , " + str(avg_ma15_2) + " > " + str(avg_ma3_2) + " , ")
                if (avg_ma15_3 > avg_ma3_3 or avg_ma15_2 > avg_ma3_2 ):
                    print("c")
                    arList.append([ticker ,tVolume])

        # if curr_ma15 > curr_ma50 > curr_ma120 and \
        #     avg_ma15 < avg_ma3 and \
        #     (avg_ma15_3 > avg_ma3_3 or avg_ma15_2 > avg_ma3_2 ):
        #     arList.append([ticker ,tVolume])
        time.sleep(0.05)

    if len(arList) > 0:
        arList.sort(reverse=True,key=lambda x:x[1])
        return arList[0][0]
    else:
        return None

# 주문된 내역 조회
def get_Totalbalance():
    balances = upbit.get_balances()
    arbalances = []
    for b in balances:
        if b['currency'] != "KRW":
            #print(b)
            if b['balance'] is not None :#and float(b['balance']) > 0:
                bKrw = b['unit_currency'] + "-" +  b['currency']
                hopePrice = pyupbit.get_tick_size(float(b['avg_buy_price']) + float(b['avg_buy_price']) * 0.01 * iHopePer)
                arbalances.append([bKrw ,hopePrice,float(b['balance'])])
    return arbalances

# 주문 내역 중에 예약 판매 조회
def get_Selbalance(arBalance):
    for balance in  arBalance:
        arOrder = upbit.get_order(balance[0], state='wait')
        for order in arOrder:
            if 'ask' == order['side']:
                if float(balance[1]) != float(order['price']):
                    print(order['ask'])

# 해당 코드의 목표가
def get_TarketPrice(target):
    bKrw = "KRW-" +  target[0][0]
    nowPrice = get_current_price(bKrw)
    bytPrice = target[1]
    print("nowPrice : " + str(nowPrice) + "  , bytPrice : " + str(bytPrice))


#print(get_Totalbalance())

arTotalbalance = get_Totalbalance()
get_Selbalance(arTotalbalance)
# tk = upbit.get_order(bKrw)

# ret = upbit.sell_limit_order(bKrw, hopePrice, b['balance'])
# print("매도주문", ret)
# print(tk)


#print(arTotalbalance)

# get_TarketPrice(arTotalbalance)

# while True:
#     print("=========================================================")
#     Target = findListTarget()
#     if Target is not None:
#         print(Target)
#         break
    #upbit.buy_market_order(Target, 10000)

# for tar in arTarget:
#     ticker = tar[0]
#     df = pyupbit.get_ohlcv(ticker , interval="minute" + str(intervalMinute))
#     close = df['close']
    
#     window = close.rolling(3)
#     ma5 = window.mean()
#     avg_ma3 = ma5[-1]
    
#     window = close.rolling(15)
#     ma5 = window.mean()
#     avg_ma15 = ma5[-1]

# #upbit.buy_market_order(target, 10000)