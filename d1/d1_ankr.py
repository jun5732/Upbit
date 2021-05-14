import time
import pyupbit
import datetime
import logging

tickername = "ANKR"
iPer = 0.2
intervalMinute = "minute30"
access = "C0Az21yejT3prbheZAUdZMCUGi9Tr1R0OlSNgIp3"          # 본인 값으로 변경
secret = "ZRozlBWm55cYlLjSmf9eBzYjhpuxUWeXKPFNzf4Q"          # 본인 값으로 변경
iBuyPrice = 0

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval=intervalMinute, count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute" + str(intervalMinute), count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval=intervalMinute, count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

strLog =  tickername + ".log"
logging.basicConfig(filename=strLog, level=logging.INFO)

logging.info("--------------------------------------")
logging.info("Name is " + tickername)
logging.info("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time=now.replace(minute=0,second=0,microsecond=0)
        end_time = start_time + datetime.timedelta(minutes=intervalMinute)
        
        BTT = get_balance(tickername)
        if BTT is None:
            BTT = 0
        
        current_price = get_current_price("KRW-" + tickername)
        ma15 = get_ma15("KRW-" + tickername)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            
            target_price = get_target_price("KRW-" + tickername, iPer)
            
            if target_price < current_price and ma15 < current_price:
                if BTT <= 0:
                    #AllIn = get_balance("KRW") *0.9995
                    logging.info("BUY +++++ -> " + str(current_price))
                    print("BUY +++++ -> " + str(current_price))
                    iBuyPrice = current_price
                    upbit.buy_market_order("KRW-" + tickername, 50000)
        else:            
            if BTT > 0:
                logging.info("----- SEL -> " + str(current_price))
                logging.info("***** profit ==> " + str((iBuyPrice - current_price) * 0.01))
                print("----- SEL -> " + str(current_price))
                print("***** profit ==> " + str((iBuyPrice - current_price) * 0.01))
                upbit.sell_market_order("KRW-"+tickername, BTT)
        time.sleep(1)
    except Exception as e:
        print(e)
        logging.info(e)
        time.sleep(1)