import datetime
from typing import Optional, Union, Callable

import pandas as pd

from tqsdk import TqApi, TqAuth, TqMultiAccount
from tqsdk.api import UnionTradeable
# from tqsdk.objs import Order


def timestamp_us_to_datetime(timestamp_us):
    return datetime.datetime.fromtimestamp((timestamp_us / 10 ** 9).astype(float))


def remove_earliest_one_rows(df: pd.DataFrame):
    df = df.drop(df.index[0])
    return df


def add_one_row(df: pd.DataFrame, row_df: pd.DataFrame):
    df = pd.concat([df, row_df], ignore_index=True)
    return df


def update_latest_one_row(df: pd.DataFrame, row_df: pd.DataFrame):
    df = df.drop(df.index[-1])
    df = pd.concat([df, row_df], ignore_index=True)
    return df


class TQDelegate:
    def __init__(
        self,
        tq_account: Optional[Union[TqMultiAccount, UnionTradeable]],
        tq_username: str,
        tq_password: str,
        strategy_init: Callable,
        strategy_run: Callable,
        symbol: str,
        duration_seconds: int,
        data_length: int,
    ):
        self.tq_account = tq_account
        self.tq_username = tq_username
        self.tq_password = tq_password
        self.strategy_init = strategy_init
        self.strategy_run = strategy_run

        self.symbol = symbol
        self.duration_seconds = duration_seconds
        self.data_length = data_length

        self.df = None

    def run(self):
        with TqApi(
            account=self.tq_account,
            auth=TqAuth(self.tq_username, self.tq_password),
        ) as my_api:
            self.subscribe_kline(
                api=my_api,
                symbol=self.symbol,
                duration_seconds=self.duration_seconds,
                kline_period=self.data_length,
            )

    def subscribe_kline(
        self,
        api: TqApi,
        symbol: str,
        duration_seconds: int,
        kline_period: int,
    ):
        df = api.get_kline_serial(
            symbol=self.symbol,
            duration_seconds=self.duration_seconds,
            data_length=self.data_length,
        )
        self.df = df.copy()
        self.strategy_init(self.df)

        # 逐行补足数据
        last_datetime = self.df['datetime'].iloc[-1]

        # 更新最后一行
        last_df = df[df['datetime'] == last_datetime]
        self.df = update_latest_one_row(self.df, last_df)
        self.strategy_run(df=self.df, overdue=True)

        # 添加多出来的行
        diff_rows = df[df['datetime'] > last_datetime]
        for index, row in diff_rows.iterrows():
            self.df = remove_earliest_one_rows(self.df)
            row_df = pd.DataFrame([row], columns=self.df.columns)
            self.df = add_one_row(self.df, row_df)
            self.strategy_run(df=self.df, overdue=True)

        while True:
            api.wait_update()
            print(0)

            # 监测量价状态
            if api.is_changing(df.iloc[-1], 'datetime'):
                self.df = update_latest_one_row(self.df, df.tail(2).head(1))
                self.strategy_run(self.df, overdue=True)

                self.df = remove_earliest_one_rows(self.df)
                self.df = add_one_row(self.df, df.tail(1))

                print(f'>>>{datetime.datetime.now()} 新的 KLine 更新 '
                      f'Date Time: {timestamp_us_to_datetime(self.df.tail(1).datetime.values[0])}')

                self.strategy_run(self.df, overdue=False)

            elif api.is_changing(df.iloc[-1], 'close'):
                self.df = update_latest_one_row(self.df, df.tail(1))

                print(f'>>> {datetime.datetime.now()} 新的 Price 更新 '
                      f'Date Time: {timestamp_us_to_datetime(self.df.tail(1).datetime.values[0])} '
                      f'Close: {self.df.tail(1).close.values[0]}')
                self.strategy_run(self.df, overdue=False)

            elif api.is_changing(df.iloc[-1], 'volume'):
                print(f'>>> {datetime.datetime.now()} 新的 Volume 更新 无操作')
