import time
import pyupbit
import datetime

access = "4xmWhK3RZ5PTWHCQCNAIyx8kuBBtxEsxbyETL8ch"
secret = "IFNTt0YjO4pIScBqI2N1Ff1F5ANBCBGGv4HLBQEH"

def get_target_price(ticker, N):  #함수별로 각각 다른 df여서 가능
    """변동성 돌파 전략으로 매수 목표가 조회""" #N이 21이면 0~20 의 평균노이즈를 사용함
    df = pyupbit.get_ohlcv(ticker, interval="day", count=N+1)
    
    avarage_noise = 0
    for n in range(0, N-1):
        avarage_noise += 1 - abs((df['open'][n] - df['close'][n]) / (df['high'][n] - df['low'][n]))
    avarage_noise /= N

    target_price = df.iloc[N]['open'] + (df.iloc[N-1]['high'] - df.iloc[N-1]['low']) * avarage_noise #=k
    #df.to_excel("dd.xlsx")
    print(df.iloc[1]['open'])
    return avarage_noise #target_price

upbit = pyupbit.Upbit(access, secret)

print("k=", get_target_price("KRW-BTC", 20))