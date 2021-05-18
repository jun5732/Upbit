import numpy as np
import pandas as pd
import pyupbit
import datetime
    

#   14봉의 이득의 합
#   14봉의 손해의 합

def get_rsiM(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

# dms = pyupbit.get_ohlcv("KRW-BTT", interval="minute1", count=15)

df = pyupbit.get_ohlcv("KRW-BTT")
print(df.tail())


# iSumP = 0
# iSumM = 0
# for dm in dms:
#     print(dm)

#     dmGap = dm['close'] - dm['open']
#     if dmGap > 0:    #   상승
#         iSumP = iSumP + dmGap
#     else:
#         iSumM = iSumM + abs(dmGap)


# print(str(iSumP) + "   <-->  " + str(iSumM))