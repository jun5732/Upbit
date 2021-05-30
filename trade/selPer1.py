import pymysql
import os
import pyupbit
import time
import logging


#   자동으로 DB에서 퍼센트를 조회해서 매도 주문을 한다.
def SetPerOrder():
    balances = upbit.get_balances()

    for b in balances:
        if b['currency'] == "KRW":
            continue
        # print(b)
        tabkerName = "KRW-" + b['currency']
        balance = (float(b['balance']) + float(b['locked']))
        
        # DB 평균가와 Upbit 평균가가 다를때
        # if float(result[0]['avgprice']) != float(b['avg_buy_price']) and float(result[0]['selper1']) > 0:
        print(tabkerName)  
        logging.info("--> " + tabkerName)
        
        #   평균 매수가
        fAvgPrice = float(b['avg_buy_price'])
        #   보유수량
        fCount = float(b['balance']) + float(b['locked'])
        # 신규 판매 예약 등록
        p1 = float(pyupbit.get_tick_size(fAvgPrice * 1.018))

        print(upbit.sell_limit_order(tabkerName, p1, fCount,True))

upbit = pyupbit.Upbit("C0Az21yejT3prbheZAUdZMCUGi9Tr1R0OlSNgIp3", "ZRozlBWm55cYlLjSmf9eBzYjhpuxUWeXKPFNzf4Q")

logging.info("START")
strLog =  "gaeulperselPro.log"
logging.basicConfig(filename=strLog, level=logging.INFO)
logging.info("START")

while True :
    SetPerOrder()
    time.sleep(1)
