import pymysql
import os
import pyupbit
import time
import logging

id = "gaeul123"
pw = "1234"

juso_db = pymysql.connect(
    user='root', 
    passwd='@As73016463', 
    host='127.0.0.1', 
    db='coin', 
    charset='utf8'
)


cursor = juso_db.cursor(pymysql.cursors.DictCursor)

def DB_InserTacker():
    icount = 0

    sql = """SELECT * FROM tacker WHERE id = %s"""
    cursor.execute(sql, (id))
    result = cursor.fetchall()
    logging.info(sql)
    if len(result) < 1:
        balances = pyupbit.get_tickers("KRW")
        for b in balances:
            icount = icount + 1
            sql = """insert into tacker(id ,currency ,avgprice ,selper1,selper1_1 ,selper2,selper2_1 ,selper3,selper3_1) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            logging.info(sql)
            cursor.execute(sql, (id ,b ,0,1,20,2,30,3,50))
            print(cursor._executed)


def Login():
    myKey = []
    sql = "SELECT * FROM user where id = '" + id + "' and pw = '" + pw + "';"
    logging.info(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    if result is not None:
        if len(result) > 0:
            myKey = [result[0]['access'] ,result[0]['secret']]
            logging.info("Login OK")
    return myKey


#def coinInsert():

#pyupbit.get_order(self, ticker, state='wait', kind='normal', contain_req=False)

# sql = """insert into customer1(name,category,region)
#          values (%s, %s, %s)"""
# cursor.execute(sql, (1, 1, '서울'))
# cursor.execute(sql, ('이연수', 2, '서울'))
# cursor.commit()

#   자동으로 DB에서 퍼센트를 조회해서 매도 주문을 한다.
def SetPerOrder():
    ###############################
    #   신규 가입시 실행
    DB_InserTacker()
    ###############################

    balances = upbit.get_balances()

    for b in balances:
        if b['currency'] == "KRW":
            continue
        tabkerName = "KRW-" + b['currency']
        #orders = upbit.get_order(tabkerName)
        
        # DB 에 있는 평균가 조회
        sql = """SELECT * FROM tacker WHERE id = %s AND currency = %s; """
        cursor.execute(sql, (id ,tabkerName))
        logging.info(sql)
        result = cursor.fetchall()

        # DB 평균가와 Upbit 평균가가 다를때
        if float(result[0]['avgprice']) != float(b['avg_buy_price']) and float(result[0]['selper1']) > 0:
            print(tabkerName)  
            logging.info("--> " + tabkerName)
            # 기존 판매 예약 취소
            oders = upbit.get_order(tabkerName)
            for oder in oders:
                if oder['side'] == 'ask':
                    upbit.cancel_order(oder['uuid'])
                    logging.info("cancel_order --> " + tabkerName)
                    time.sleep(1)

            #   평균 매수가
            fAvgPrice = float(b['avg_buy_price'])
            #   보유수량
            fCount = float(b['balance']) + float(b['locked'])
            # 신규 판매 예약 등록
            p1 = float(pyupbit.get_tick_size(fAvgPrice + (fAvgPrice * 0.01 * float(result[0]['selper1']))))
            p2 = float(pyupbit.get_tick_size(fAvgPrice + (fAvgPrice * 0.01 * float(result[0]['selper2']))))
            p3 = float(pyupbit.get_tick_size(fAvgPrice + (fAvgPrice * 0.01 * float(result[0]['selper3']))))
            p1_1 = (fCount * 0.01 * float(result[0]['selper1_1']))
            p2_1 = (fCount * 0.01 * float(result[0]['selper2_1']))
            p3_1 = float(fCount - p1_1 - p2_1)
            
            # 현제 평균가 다시 등록
            rt = upbit.sell_limit_order(tabkerName, p1, p1_1 ,True)
            logging.info("sell_limit_order --> " + tabkerName + " : " + str(p1) + " -> " + str(p1_1))
            time.sleep(1)
            #print(rt)
            rt = upbit.sell_limit_order(tabkerName, p2, p2_1,True)
            logging.info("sell_limit_order --> " + tabkerName + " : " + str(p2) + " -> " + str(p2_1))
            time.sleep(1)
            #print(rt)
            rt = upbit.sell_limit_order(tabkerName, p3, p3_1,True)
            logging.info("sell_limit_order --> " + tabkerName + " : " + str(p3) + " -> " + str(p3_1))
            time.sleep(1)
            #print(rt)
            
            
            sql = """UPDATE tacker SET avgprice = %s WHERE id = %s AND currency = %s """
            cursor.execute(sql, (b['avg_buy_price'] ,id ,tabkerName))
            time.sleep(1)
        time.sleep(1)

myKey = Login()
upbit = pyupbit.Upbit(myKey[0], myKey[1])

logging.info("START")
strLog =  "gaeulperselPro.log"
logging.basicConfig(filename=strLog, level=logging.INFO)
logging.info("START")

while True :
    SetPerOrder()
    time.sleep(1)
