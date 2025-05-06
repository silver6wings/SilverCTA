"""
https://doc.shinnytech.com/tqsdk/latest/quickstart.html
"""
import datetime

import pandas as pd
from tqsdk import TqApi, TqAuth, TqAccount, TqKq

from credentials import *
from delegate.tq_delegate import TQDelegate, UpdateType
from tools.utils_basic import pd_show_all


IS_PROD = False


def main():
    pd_show_all()

    my_symbol = "SHFE.au2506"   # 测试的品种
    my_duration_sec = 10        # 每个K线的时间长度
    my_klines_count = 50        # 订阅多少根K线

    if IS_PROD:
        my_account = TqAccount(qh_company, qh_username, qh_password)   # 实盘账户
    else:
        my_account = TqKq()  # 快期模拟账户

    def init(df):
        print(df.tail(2))

    def run(
        system_datetime: datetime.datetime,
        kline_datetime: datetime.datetime,
        kline_dataframe: pd.DataFrame,
        update_type: int,
    ):
        print(f'{system_datetime} {kline_datetime} ', end='')

        if update_type == UpdateType.PrevKLine:
            print('prev kline \n', kline_dataframe.tail(2))
        elif update_type == UpdateType.NewKLine:
            print('kline \n', kline_dataframe.tail(2))
        elif update_type == UpdateType.NewPrice:
            print('close ', kline_dataframe.tail(1).close.values[0])
        elif update_type == UpdateType.NewVolume:
            print('volume ', kline_dataframe.tail(1).volume.values[0])

    delegate = TQDelegate(
        tq_account=my_account,
        tq_username=tq_username,
        tq_password=tq_password,
        strategy_init=init,
        strategy_run=run,
        symbol=my_symbol,
        duration_seconds=my_duration_sec,
        data_length=my_klines_count,
    )

    delegate.run()


if __name__ == '__main__':
    main()
