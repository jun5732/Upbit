import time
import pyupbit
import datetime
import pandas as pd


access = "C0Az21yejT3prbheZAUdZMCUGi9Tr1R0OlSNgIp3"
secret = "ZRozlBWm55cYlLjSmf9eBzYjhpuxUWeXKPFNzf4Q"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
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

#   자동으로 DB에서 퍼센트를 조회해서 매도 주문을 한다.
def SetPerOrder(tabker):
    balances = upbit.get_balances()

    for b in balances:
        if "KRW-" + b['currency'] == tabker:            
            balance = (float(b['balance']) + float(b['locked']))                    
            #   평균 매수가
            fAvgPrice = float(b['avg_buy_price'])
            #   보유수량
            fCount = float(b['balance']) + float(b['locked'])
            # 신규 판매 예약 등록
            time.sleep(0.1)
            p1 = float(pyupbit.get_tick_size(fAvgPrice + (fAvgPrice * 0.02)))
            time.sleep(0.1)
            print(upbit.sell_limit_order(tabker, p1, fCount,True))

# 로그인
upbit = pyupbit.Upbit("C0Az21yejT3prbheZAUdZMCUGi9Tr1R0OlSNgIp3", "ZRozlBWm55cYlLjSmf9eBzYjhpuxUWeXKPFNzf4Q")
print("autotrade start")

# 자동매매 시작
iTime = 60
bRun = False
# bRun = True


arTicker = []
ttp = {}
while True:
    time.sleep(0.1)
    krw = get_balance("KRW")
    time.sleep(0.1)
    if krw is None:
        krw = 0
    # if True:
    if krw > 5000:
        tt = []
        tickers = pyupbit.get_tickers("KRW")
        for ticker in tickers:
            # ticker = "KRW-RFR"
            time.sleep(0.1)
            df = pyupbit.get_ohlcv(ticker, interval="minute" + str(iTime), count=int(100))
            print(ticker)
            ma3 = df['close'].rolling(3).mean()
            ma5 = df['close'].rolling(5).mean()
            ma15 = df['close'].rolling(15).mean()
            target_price = df.iloc[-2]['close'] + (df.iloc[-2]['high'] - df.iloc[-2]['low']) * 0.2
            current_price = df.iloc[-1]['close']
            time.sleep(0.1)

            if ma15.iloc[-1] > ma15.iloc[-2] > ma15.iloc[-3]:
                print("ma5 : " + str(ma5.iloc[-1]) +  " > " +  str(ma15.iloc[-1]))
                if ma5.iloc[-1] > ma15.iloc[-1]:
                    print("target_price : " + str(target_price) +  " < " +  str(current_price))
                    if target_price < current_price:
                        # arTicker.append(ticker)
                        # va = ({'ticker':ticker,'volume':df['volume'].sum()})
                        # tt.append(va)
                        # time.sleep(0.1)
                        print(upbit.buy_market_order(ticker, krw*0.9995))
                        time.sleep(0.1)
                        SetPerOrder(ticker)
        # print(arTicker)
        # print(tt)
        # data = pd.DataFrame(tt)
        # for ticker in data:
        #     print(ticker)

                            