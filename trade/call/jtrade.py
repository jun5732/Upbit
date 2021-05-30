import requests
import pandas as pd
import time
import pyupbit
import numpy as np
import datetime
import threading

upbit = pyupbit.Upbit("C0Az21yejT3prbheZAUdZMCUGi9Tr1R0OlSNgIp3", "ZRozlBWm55cYlLjSmf9eBzYjhpuxUWeXKPFNzf4Q")


#   1프로에 판매
class SelClass(threading.Thread):
    def __init__(self):
        super().__init__()

    # def run(self):
    #     print("sub thread start ", threading.currentThread().getName())
    #     time.sleep(3)
    #     print("sub thread end ", threading.currentThread().getName())
            
    def run(self):
        while True:
            time.sleep(1)
            balances = upbit.get_balances()
            for b in balances:
                if b['currency'] == "KRW":
                    continue
                
                tabkerName = "KRW-" + b['currency']
                
                #   평균 매수가
                fAvgPrice = float(b['avg_buy_price'])

                # 신규 판매 예약 등록
                p1 = fAvgPrice * 1.0105

                nowPrice = pyupbit.get_current_price(tabkerName)
                oders = upbit.get_order(tabkerName)
                
                if p1 < nowPrice:
                    strPrint = upbit.sell_limit_order(tabkerName, nowPrice, b['balance'] ,True)
                    time.sleep(1)
                    oders = upbit.get_order(tabkerName)
                    time.sleep(1)
                    for oder in oders:
                        if oder['side'] == 'bid':                    
                            strPrint = upbit.cancel_order(oder['uuid'])
                            time.sleep(1)

def BuyTrade():
    t = SelClass()                # sub thread 생성
    t.start()

def MyBalanceCount():
    return len(upbit.get_balances("KRW"))

BuyTrade()