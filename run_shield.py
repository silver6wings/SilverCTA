from tqsdk import TqApi, TqAuth

from credentials.tq import *


if __name__ == '__main__':
    api = TqApi(auth=TqAuth(tq_username, tq_password))
    klines = api.get_kline_serial("SHFE.au2505", 10)
    print(klines)
    while api.wait_update():
        print("最后一根K线收盘价", klines.close.iloc[-1])
