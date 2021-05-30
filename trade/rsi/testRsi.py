import requests
import pandas as pd
import time
import pyupbit
import numpy as np
import datetime

# DataFrame.insert( loc, column, value, allow_duplicates=False )
# loc = 추가하고 싶은 위치의 index 값을 넣는다. (3 = Name 앞)
# column = 추가하고 싶은 column의 이름을 넣는다.
# value = 추가하고자 하는 column의 값을 넣는다.
#train_data.insert( 3, 'Fare10', train_data[ 'Fare' ]/10 )

def rsi(ohlc: pd.DataFrame, period: int = 14):
    ohlc["trade_price"] = ohlc["trade_price"]
    delta = ohlc["trade_price"].diff()
    gains, declines = delta.copy(), delta.copy()
    gains[gains < 0] = 0
    declines[declines > 0] = 0

    _gain = gains.ewm(com=(period - 1), min_periods=period).mean()
    _loss = declines.abs().ewm(com=(period - 1), min_periods=period).mean()

    RS = _gain / _loss
    return pd.Series(100 - (100 / (1 + RS)), name="RSI")

def rsi7(ohlc: pd.DataFrame, period: int = 7):
    ohlc["trade_price"] = ohlc["trade_price"]
    delta = ohlc["trade_price"].diff()
    gains, declines = delta.copy(), delta.copy()
    gains[gains < 0] = 0
    declines[declines > 0] = 0

    _gain = gains.ewm(com=(period - 1), min_periods=period).mean()
    _loss = declines.abs().ewm(com=(period - 1), min_periods=period).mean()

    RS = _gain / _loss
    return pd.Series(100 - (100 / (1 + RS)), name="RSI")

inter = 1
upbit = pyupbit.Upbit("C0Az21yejT3prbheZAUdZMCUGi9Tr1R0OlSNgIp3", "ZRozlBWm55cYlLjSmf9eBzYjhpuxUWeXKPFNzf4Q")


bBuy = False
vecs = {}
vec = {}
tickers1 = pyupbit.get_tickers("KRW")


for ticker1 in tickers1:
    vec[ticker1] = 100
#   https://dev-guardy.tistory.com/89
while True:
    tickers = pyupbit.get_tickers("KRW")
    time.sleep(1)
    for ticker in tickers:
        # df = pyupbit.get_ohlcv(ticker,count=5)
        # print(np.mean(df['volume']))   # 평균 구하는식
        # print(df)
        # print(df.tail())
        # ticker = "KRW-LTC"

        # #############################################
        # df = pyupbit.get_ohlcv(ticker, interval="minute" + str(15), count=200)
        
        # sto_N=14
        # sto_m=1
        # sto_t=3
        # # 스토캐스틱 %K (fast %K) = (현재가격-N일중 최저가)/(N일중 최고가-N일중 최저가) ×100       
        
        # vec["high"]=df["high"].rolling(sto_N).max()     #   df["max%d"%sto_N]
        # vec["low"]=df["low"].rolling(sto_N).min()      #   df["min%d"%sto_N]      

        # raw_data = {'ticker':ticker,'high': vec["high"],'low': vec["low"]}
        # data = pd.DataFrame(raw_data)
        # print(data)

        # dK = pd.DataFrame(ticker, columns=['opening_price', 'high_price', 'low_price', 'trade_price',
        #                                      'candle_acc_trade_volume'])  
        # print(dK)
        # dL = pd.DataFrame('a',[vec["high"] ,vec["low"]])
        # print(dL)
        # print(vec["high"])
        # print(vec["low"])
        # print(df["close"]-vec["high"])
        # print(vec["high"]-vec["low"])
        # ret = 1 if vec["high"]-vec["low"] !=0 is 50 else 1

        # #vec["stochastic%K"] = if (vec["high"]-vec["low"])!=0 else 50,1) #df.apply(lambda x:100*(df["close"]-vec["high"]) / (vec["high"]-vec["low"]) if (vec["high"]-vec["low"])!=0 else 50,1)
        # print(ret)
        # #############################################

        url = "https://api.upbit.com/v1/candles/minutes/15"
        querystring = {"market":ticker,"count":"200"}
        response = requests.request("GET", url, params=querystring)
        data = response.json()
        df = pd.DataFrame(data)
        df=df.reindex(index=df.index[::-1]).reset_index()

        nrsi = rsi(df, 14).iloc[-1]
        nrsi2 = rsi(df, 14).iloc[-2]
        nrsi3 = rsi(df, 14).iloc[-3]
        # nrsi3 = rsi(df, 14).iloc[-3]
        # nrsi4 = rsi(df, 14).iloc[-4]

        # print(ticker + " -> " + str(nrsi2) + " -> " + str(nrsi))

        # nrsi7 = rsi(df, 7).iloc[-1]
        # nrsi72 = rsi(df, 7).iloc[-2]
        # if nrsi < nrsi7 and nrsi2 > nrsi72:
        #     print(ticker)
        #     print("")
            

        if nrsi > 31 and nrsi2 > 31 and nrsi3 < 29:
        # if nrsi > 30 and nrsi2 > 30 and nrsi3 < 30 and nrsi4 < 30:
            upbit.buy_market_order(ticker, 5000)
            abdd = 1
            
        time.sleep(1)





# import requests
# import pandas as pd
# import time
# import webbrowser
# import pyupbit




# def rsi(ohlc: pd.DataFrame, period: int = 14):
    
#     ohlc["close"] = ohlc["close"]
#     delta = ohlc["close"].diff()

#     up, down = delta.copy(), delta.copy()
#     up[up < 0] = 0
#     down[down > 0] = 0

#     _gain = up.ewm(com=(period - 1), min_periods=period).mean()
#     _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()

#     RS = _gain / _loss
#     return pd.Series(100 - (100 / (1 + RS)), name="RSI")


# while True:
#     df = pyupbit.get_ohlcv("KRW-BTC", interval="minute10", count=500)
#     rsi = rsi(df, 15).iloc[-1]
#     print('Upbit 10 minute RSI:', rsi)
#     time.sleep(1)