from tqsdk import TqApi, TqAuth

from credentials import *


SYMBOL = "SHFE.au2506"


def run(symbol: str):
    api = TqApi(auth=TqAuth(tq_username, tq_password))
    klines = api.get_kline_serial(symbol, 10)
    print(klines)
    while api.wait_update():

        print("最后一根K线收盘价", klines.close.iloc[-1])

        # https://doc.shinnytech.com/tqsdk/latest/reference/tqsdk.objs.html#tqsdk.objs.Position
        position = api.get_position(symbol=symbol)
        print(position.open_price_long)
        print(position.open_price_short)
        print(position.position_cost_long)
        print(position.position_cost_short)


if __name__ == '__main__':
    run(symbol=SYMBOL)
