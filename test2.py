import sys
sys.path.append('C:\\Users\\tkddb\\AppData\\Roaming\\Python\\Python310\\site-packages')
import pyupbit
import time

access = "wxq5NTdxETrvUVO4vOnx2ul7GwCQt9ozNl2qVp2n"
secret = "awn3q0Fs1zOJhFfKHnTo6idqMjxdndDDfCdrxDpP"
upbit = pyupbit.Upbit(access, secret)

def get_target_price(ticker):
    """목표 매수가를 반환합니다."""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=5)
    # 전일 종가 대비 변동성 돌파 전략 적용
    target_price = df.iloc[-2]['close'] + (df.iloc[-2]['high'] - df.iloc[-2]['low']) * 0.5
    return target_price

def buy_crypto_currency(ticker, krw):
    """KRW로 암호화폐를 매수합니다."""
    # 매수 가격
    orderbook = pyupbit.get_orderbook(ticker)
    sell_price = orderbook['asks'][0]['price']
    buy_price = sell_price * 1.01
    # 매수 가격으로 매수량 계산
    buy_volume = krw / float(sell_price)
    # 시장가 주문으로 매수
    upbit.buy_market_order(ticker, buy_volume)
    print(f"매수 완료 - 가격: {buy_price}, 수량: {buy_volume}")
    return buy_price

buy_price = None

while True:
    try:
        # KRW-BTC 현재가를 가져옵니다.
        price = pyupbit.get_current_price("KRW-BTC")
        # 현재 잔고 조회
        krw = upbit.get_balance("KRW")
        btc = upbit.get_balance("BTC")
        # 목표 매수가 계산
        target_price = get_target_price("KRW-BTC")
        # 목표 매수가보다 현재가가 높으면 매수 진행
        if price >= target_price and krw > 5000:
            buy_price = buy_crypto_currency("KRW-BTC", krw*0.9995)
        # 현재가가 손절매가보다 낮으면 시장가 매도
        else:
            if buy_price is not None:
                # 손절매가 (현재 매수가보다 3% 하락한 가격)
                loss_cut_price = buy_price * 0.97
                # 현재가가 손절매가보다 낮으면 시장가 매도
                if price <= loss_cut_price and btc > 0.0001:
                    upbit.sell_market_order("KRW-BTC", btc)
                    print(f"매도 완료 - 가격: {price}, 수량 {btc}")
        # 매수 또는 매도 주문 후 대기
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)