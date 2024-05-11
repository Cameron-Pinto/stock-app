from polygon import RESTClient
import pandas as pd
import pandas_ta as ta
import numpy as np
from backtesting import Strategy, Backtest
import matplotlib.pyplot as plt


API_KEY = "BrJLVaynDhKd6wgaHuof4bbhfLQgdqiK"

client = RESTClient(API_KEY)

tickers = ["AAPL", "XOM", "MSFT", "IBM", "CVX"]
aggs = []
for symbol in tickers:
    aggs = client.get_aggs(
        symbol,
        1,
        "day",
        "2019-06-04",
        "2024-05-10",
        limit=1259,
    )
    df = pd.DataFrame(aggs)
    df["Date"] = pd.DatetimeIndex(
        pd.to_datetime(df["timestamp"], unit="ms").dt.normalize()
    )
    temp_cols = df.columns.tolist()
    new_cols = temp_cols[-1:] + temp_cols[:-1]
    df = df[new_cols]
    df.drop(["vwap", "timestamp", "transactions", "otc"], axis=1, inplace=True)
    df.rename(
       columns={
       "date": "Date",
       "high": "High",
       "low": "Low",
       "close": "Close",
       "volume": "Volume",
       "open": "Open"
    }, inplace = True)
    df.to_csv(
        r"C:\Users\Camer\OneDrive\Documents\Python-Projects\stock-app\stock_data\data\eod\{}.csv".format(
            symbol
        )
    )

