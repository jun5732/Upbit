import time
import datetime
import pyupbit
import threading

intervalTime = "minute30"

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval=intervalTime, count=1)
    start_time = df.index[0]
    return start_time

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


def TradeRun(ticker):
    try:
        start_time = get_start_time(ticker)
        now = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(minutes=5)
        
        nowPrice = get_current_price(ticker)

        BTT = get_balance(ticker[4:])
        if BTT is None:
            BTT = 0
            
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            time.sleep(1)
            df = pyupbit.get_ohlcv(ticker, interval=intervalTime,count=10)

            ma15 = df['volume'].rolling(10).mean().iloc[-1]
            nw = df['volume'][-1]

            if nw > ma15 and df['close'][-1] - df['open'][-1] > 1:
                print(ticker + " ->  BUY :" + str(get_current_price(ticker)))
                
                if BTT <= 0:
                    if iCount < 3:
                        print("BUY-----> " + ticker + " : " + str(iCount))
                        #upbit.buy_market_order(ticker, 100000)
                        iCount = iCount + 1
                    #upbit.buy_limit_order(ticker, 10000, volume)
                    #upbit.sell_market_order(ticker, nowPrice)
        else:            
            if BTT > 0:
                print("----->SEL " + ticker + " : " + str(iCount))
                #upbit.sell_limit_order(ticker, nowPrice, BTT ,True)
                iCount = iCount - 1
    except Exception as e:
        print(e) 
        time.sleep(1)     

def run(ticker):
    while True:               
        TradeRun(ticker)

# 로그인
access = "C0Az21yejT3prbheZAUdZMCUGi9Tr1R0OlSNgIp3"          # 본인 값으로 변경
secret = "ZRozlBWm55cYlLjSmf9eBzYjhpuxUWeXKPFNzf4Q"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

iCount = 0

th1 = threading.Thread(target=run, args=("KRW-BTT"))
th1.start()
th1.join()

# try:
#     tickers = pyupbit.get_tickers(fiat="KRW")
#     time.sleep(1)
#     for ticker in tickers:
#         th1 = threading.Thread(target=run, args=(ticker))
#         th1.start()
#         th1.join()
        
#         t = Worker(ticker)                # sub thread 생성
#         t.start()                       # sub thread의 run 메서드를 호출


        
#         start_time = get_start_time(ticker)
#         now = datetime.datetime.now()
#         end_time = start_time + datetime.timedelta(minutes=5)
        
#         nowPrice = get_current_price(ticker)

#         BTT = get_balance(ticker[4:])
#         if BTT is None:
#             BTT = 0
            
#         if start_time < now < end_time - datetime.timedelta(seconds=10):
#             time.sleep(1)
#             df = pyupbit.get_ohlcv(ticker, interval=intervalTime,count=10)

#             ma15 = df['volume'].rolling(10).mean().iloc[-1]
#             nw = df['volume'][-1]

#             if nw > ma15 and df['close'][-1] - df['open'][-1] > 1:
#                 print(ticker + " ->  BUY :" + str(get_current_price(ticker)))                
#                 if BTT <= 0:
#                     if iCount < 3:
#                         upbit.buy_market_order(ticker, 100000)
#                     #upbit.buy_limit_order(ticker, 10000, volume)
#                     #upbit.sell_market_order(ticker, nowPrice)
#         else:            
#             if BTT > 0:
#                 upbit.sell_limit_order(ticker, nowPrice, BTT ,True)
# except Exception as e:
#     print(e) 
#     time.sleep(1)



 