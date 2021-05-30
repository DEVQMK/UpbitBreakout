import time
import pyupbit
import datetime

access = "4xmWhK3RZ5PTWHCQCNAIyx8kuBBtxEsxbyETL8ch"
secret = "IFNTt0YjO4pIScBqI2N1Ff1F5ANBCBGGv4HLBQEH"

def dog_logic(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=1)
    #MaginoLine = (df['close'][0] + df['open'][0]) / 2
    return df['close'][0] - df['open'][0]

def get_target_price(ticker, N):  #함수별로 각각 다른 df여서 가능
    """변동성 돌파 전략으로 매수 목표가 조회""" #N이 21이면 0~20 의 평균노이즈를 사용함
    df = pyupbit.get_ohlcv(ticker, interval="day", count=N+1)
    
    avarage_noise = 0
    for n in range(0, N-1):
        avarage_noise += 1 - abs((df['open'][n] - df['close'][n]) / (df['high'][n] - df['low'][n]))
    avarage_noise /= N

    target_price = df.iloc[N]['open'] + (df.iloc[N-1]['high'] - df.iloc[N-1]['low']) * avarage_noise #=k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma(ticker, DN):    #MoveAvarageDayN
    """DN일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=DN)
    maDN = df['close'].rolling(DN).mean().iloc[-1]
    return maDN

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

# 자동매매 시작
while True:
    try:
        #current_price = get_current_price("KRW-BTC")
        if get_current_price("KRW-BTC") > get_target_price("KRW-BTC", 20):
            print(get_current_price("KRW-BTC"), " 딱 대 ㅋㅋ 매수각")
            krw = get_balance("KRW")
            if krw >= 0:
                magino_line = get_current_price("KRW-BTC")
                upbit.buy_market_order("KRW-BTC", krw*0.9995)
                while get_current_price("KRW-BTC") >= magino_line * 0.95:
                    if get_current_price("KRW-BTC") >= magino_line:
                        magino_line = get_current_price("KRW-BTC")
                    time.sleep(1)
                btc = get_balance("BTC")
                if btc > 0.00008:
                    upbit.sell_market_order("KRW-BTC", btc*0.9995)
                print(get_current_price("KRW-BTC"), " 떡락하네 매도각")
        
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)