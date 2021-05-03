import pyupbit
import logging
import configparser
from enum import Enum

access = "vqjRzy8UlElasjqXHW7tDrkjXdGuxWAfxTjBx7iw"          # 본인 값으로 변경
secret = "h9sLNV3XyVJa6pAsa8EdWlxfWiONy9o8cIc6Zdzk"          # 본인 값으로 변경

tickerName = ""
tickerNameSel = ""
iSelPrice = 0
SetGap = "minute"

gainPer = 0
lossPer = 0

gain = 5
loss = 5

iBuyPrice = 0   #   매입가

IsTestYN = False     # true 이면 LOG 만 찍는다.

class ePosition(Enum):
    PT3520 = 1
    PT3205 = 2
    PTBuy  = 3
    PT5320 = 4
    PT5203 = 5
    PTHold = 6
    PT2035 = 7
    PT2053 = 8
    PTSel  = 9

def get_MyPrice():
    """ 계좌 잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == "KRW":
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_balance():
    """ ticker 잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        print(b['currency'])
        if b['currency'] == tickerNameSel:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

#---------------------------------------------------------------------------------
# 현제평 1평전
""" 3평 구하기 """
def Get3Line1():
    minute3 = pyupbit.get_ohlcv(tickerName, SetGap,4)
    return sum(minute3['open']) / 3

""" 5평 구하기 """
def Get5Line1():
    minute5 = pyupbit.get_ohlcv(tickerName, SetGap,5)
    return sum(minute5['open']) / 5


""" 20평 구하기 """
def Get20Line1():
    minute20 = pyupbit.get_ohlcv(tickerName, SetGap,20)
    return sum(minute20['open']) / 20

""" 20평 -1 구하기 """
def Get20LineM11():    
    minute21 = pyupbit.get_ohlcv(tickerName, SetGap,21)
    sum21 = sum(minute21['open']) - minute21['open'][-1]
    return sum21 / 20
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
# 현제평
""" 3평 구하기 """
def Get3Line():
    minute3 = pyupbit.get_ohlcv(tickerName, SetGap,3)
    return sum(minute3['open']) / 3

""" 5평 구하기 """
def Get5Line():
    minute5 = pyupbit.get_ohlcv(tickerName, SetGap,5)
    return sum(minute5['open']) / 5


""" 20평 구하기 """
def Get20Line():
    minute20 = pyupbit.get_ohlcv(tickerName, SetGap,20)
    return sum(minute20['open']) / 20

""" 20평 -1 구하기 """
def Get20LineM1():    
    minute21 = pyupbit.get_ohlcv(tickerName, SetGap,21)
    sum21 = sum(minute21['open']) - minute21['open'][-1]
    return sum21 / 20
#---------------------------------------------------------------------------------
def Gap20Lin():
    if Get20Line() > Get20LineM1():
        return True
    else:
        return False

    
"""현재가 조회"""
def get_current_price(ticker):
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]


def SelOrder():
    try:
        nowPrice = get_current_price(tickerName)
        if IsTestYN == False:
            upbit.sell_market_order(tickerName, get_balance())
        writeLog("SEL BY Price : " + str(nowPrice))
        return True
    except Exception as e:
        return False
    return False

def BuyOrder():
    try:
        nowPrice = get_current_price(tickerName)
        if IsTestYN == False:
            upbit.buy_market_order(tickerName, iSelPrice)
            iBuyPrice = iSelPrice
        writeLog("BUY BY Price : " + str(nowPrice))
        return True
    except Exception as e:
        return False

def writeLog(logmsg):
    print(logmsg)
    logging.info(logmsg)

def GetNowToBuyPer():
    nowPrice = get_current_price(tickerName)

    if nowPricer > iBuyPrice + iBuyPrice * gainPer * 0.01:
        return 1
    elif nowPricer < iBuyPrice - iBuyPrice * lossPer * 0.01:
        return -1
    else:
        return 0

def GetPostion():
    Line3 = Get3Line()
    Line5 = Get5Line()
    Line20 = Get20Line()
    if Line3 > Line5 > Line20:
        return ePosition.PT3520
    elif Line3 > Line20 > Line5:
        return ePosition.PT3205
    elif Line5 > Line3 > Line20:
        return ePosition.PT5320
    elif Line5 > Line20 > Line3:
        return ePosition.PT5203
    elif Line20 > Line3 > Line5:
        return ePosition.PT2035
    elif Line20 > Line5 > Line3:
        return ePosition.PT2053

logging.basicConfig(filename='./server.log', level=logging.INFO)

config = configparser.ConfigParser()
config.read('config.ini')

tickerNameSel = config['AutoCoin']['ticker']
SetGap = "minute" + config['AutoCoin']['gap']
iSelPrice = config['AutoCoin']['Price']


gainPer = config['AutoCoin']['gain']
lossPer = config['AutoCoin']['loss']

gain = 5
loss = 5


upbit = pyupbit.Upbit(access, secret)
if int(iSelPrice) < 0:
    iSelPrice = get_MyPrice()
    writeLog("Trade is AllIn")

tickerName = "KRW-" + tickerNameSel

writeLog("Name is " + tickerName)
writeLog("GAP is " + SetGap)
writeLog("Price is " + str(iSelPrice))

writeLog("Price is " + str(get_MyPrice()))
