import numpy as np
import pandas as pd
import pyupbit
import datetime
import time

#   5,10,15분봉을 볼것
#   15는 2봉 10분은 3봉 5분은 6봉

#   14봉의 이득의 합
#   14봉의 손해의 합

def get_rsiM(ticker, inter):
    time.sleep(1)
    dms = pyupbit.get_ohlcv(ticker, interval="minute" + str(inter), count=15)
    
    U1 = U2 = 0
    D1 = D2 = 0

    countU1 = 0
    countD1 = 0
    countU2 = 0
    countD2 = 0

    for i in range(14,1,-1):
        #dmGap1 = dms['close'][i-1] - dms['open'][i-1]
        #dmGap2 = dms['close'][i] - dms['open'][i]
        
        dmGap1 = dms['close'][i-1] - dms['open'][i-2]
        dmGap2 = dms['close'][i] - dms['close'][i-1]


        if dmGap1 > 0:    #   상승
            U1 = U1 + dmGap1
            countU1 = countU1 + 1
        else:
            D1 = D1 + abs(dmGap1)
            countD1 = countD1 + 1
            
        if dmGap2 > 0:    #   상승
            U2 = U2 + dmGap2
            countU2 = countU2 + 1
        else:
            D2 = D2 + abs(dmGap2)
            countD2 = countD2 + 1

    countU1 = countD1 = countU2 = countD2 = 14
    U11 = U1 / countU1 
    D11 = D1 / countD1
    Rs1 = U11 / D11
    RSI3 = Rs1 / (1+Rs1) * 100

    U21 = U2 / countU2 
    D21 = D2 / countD2
    Rs2 = U21 / D21
    RSI4 = Rs2 / (1+Rs2) * 100

    print(str(RSI3) + " | " + str(RSI4))
    
    if RSI3 < 30 and RSI4 > 30:
        return True
    else:
        return False

def get_rsiM15(ticker):
    dms = pyupbit.get_ohlcv(ticker, interval="minute15", count=15)
    
    U1 = U2 = 0
    D1 = D2 = 0

    for i in range(14,1,-1):
        dmGap1 = dms['close'][i] - dms['close'][i-1]
        dmGap2 = dms['close'][i] - dms['open'][i]

        if dmGap1 > 0:    #   상승
            U1 = U1 + dmGap1
        else:
            D1 = D1 + abs(dmGap1)
            
        if dmGap2 > 0:    #   상승
            U2 = U2 + dmGap2
        else:
            D2 = D2 + abs(dmGap2)

    U11 = U1 / 14 
    D11 = D1 / 14
    Rs1 = U11 / D11
    RSI3 = Rs1 / (1+Rs1) * 100

    U21 = U2 / 14 
    D21 = D2 / 14
    Rs2 = U21 / D21
    RSI4 = Rs2 / (1+Rs2) * 100

    print(str(RSI3) + " | " + str(RSI4))

    if RSI3 < 30 and RSI4 > 30:
        return True

#get_rsiM15("KRW-BTT")
# dms = pyupbit.get_ohlcv("KRW-BTT", interval="minute1", count=14)
# print(dms)


def get_rsi(ticker, inter):
    time.sleep(1)
    dms = pyupbit.get_ohlcv(ticker, interval="minute" + str(inter), count=14)
    
    clo = sum(dms['close']) / 14
    ga = sum(dms['close'] - dms['open']) / 14

    print (str(clo))
    up, down = dms.copy(), dms.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    _gain = up.ewm(com=(14 - 1), min_periods=14).mean()
    _loss = down.abs().ewm(com=(14 - 1), min_periods=14).mean()

    print (_gain)
    print (up)
    print (str(dms['close'].diff() / 14))

tickers = pyupbit.get_tickers("KRW")
get_rsi("KRW-BTC",15)
for ticker in tickers:
    time.sleep(1)
    print(ticker)
    if get_rsiM(ticker,15) == True:
        print("15")
        if get_rsiM(ticker,10) == True:
            print("10")
        if get_rsiM(ticker,5) == True:
            print("5")

# dms = pyupbit.get_ohlcv("KRW-BTT", interval="minute15", count=14)
# dms.to_excel("dd.xlsx")

# AU = 0
# AD = 0
# cU = 0
# cD = 0
# for i in range(0,13,1):
#     gap = dms['close'][i] - dms['open'][i]
#     #dmGap = dms['close'][i] - dms['close'][i+1]


#     if gap > 0:    #   양봉
#         AU = AU + dms['close'][i]
#         cU = cU + 1
#     else:
#         AD = AD + dms['close'][i]
#         cD = cD + 1

# Rs = (AU /cU) / (AD/cD)
# RSI = Rs / (1+Rs)
# print(str(AU) + " | " + str(AD) + " | " + str(Rs) + " | " + str(RSI))
# get_rsiM15("KRW-BTT")
