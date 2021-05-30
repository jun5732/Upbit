import pymysql
import os
import pyupbit
import time
import logging

#   자동으로 DB에서 퍼센트를 조회해서 매도 주문을 한다.
def SetPerOrder():

    balances = upbit.get_balances()
    print("-------------------------------------------------------------------------------------------")
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
        
        print(tabkerName + " || " + str(fAvgPrice) + " || " + str(p1) + " || " + str(nowPrice))  

        if p1 < nowPrice:
            logging.info("-------------------------------------------------------------------------------------------")
            strPrint = upbit.sell_limit_order(tabkerName, nowPrice, b['balance'] ,True)
            logging.info(strPrint)
            # print(upbit.sell_market_order(tabkerName, b['balance']))
            time.sleep(1)
            oders = upbit.get_order(tabkerName)
            time.sleep(1)
            for oder in oders:
                if oder['side'] == 'bid':                    
                    strPrint = upbit.cancel_order(oder['uuid'])
                    logging.info(strPrint)
                    time.sleep(1)


upbit = pyupbit.Upbit('C0Az21yejT3prbheZAUdZMCUGi9Tr1R0OlSNgIp3','ZRozlBWm55cYlLjSmf9eBzYjhpuxUWeXKPFNzf4Q')

nowPath = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(filename=nowPath + "\SelPer1.txt", level=logging.INFO)
logging.info("--------------------------------------")
logging.info("SelPer1 autotrade start")

while True :
    SetPerOrder()
    time.sleep(1)
