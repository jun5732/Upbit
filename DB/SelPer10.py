import pymysql
import os
import pyupbit
import time

#   자동으로 DB에서 퍼센트를 조회해서 매도 주문을 한다.
def SetPerOrder():

    balances = upbit.get_balances()

    for b in balances:
        if b['currency'] == "KRW":
            continue
        tabkerName = "KRW-" + b['currency']
        #orders = upbit.get_order(tabkerName)
        
        print(tabkerName)  
        #   평균 매수가
        fAvgPrice = float(b['avg_buy_price'])
        #   보유수량
        fCount = float(b['balance']) + float(b['locked'])
        # 신규 판매 예약 등록
        p1 = float(pyupbit.get_tick_size(fAvgPrice + (fAvgPrice * 0.01 * 10)))

        iCancleOrderCount = 1
        # 기존 판매 예약 취소
        oders = upbit.get_order(tabkerName)
        for oder in oders:
            if oder['side'] == 'ask':
                iCancleOrderCount = 0
            # DB 평균가와 Upbit 평균가가 다를때
                if float(p1) != float(oder['price']):
                    upbit.cancel_order(oder['uuid'])
                    iCancleOrderCount = 1
                    # 현제 평균가 다시 등록
        if iCancleOrderCount == 1:
            rt = upbit.sell_limit_order(tabkerName, p1, fCount ,True)
        time.sleep(1)


upbit = pyupbit.Upbit('C0Az21yejT3prbheZAUdZMCUGi9Tr1R0OlSNgIp3','ZRozlBWm55cYlLjSmf9eBzYjhpuxUWeXKPFNzf4Q')


while True :
    SetPerOrder()
    time.sleep(1)
