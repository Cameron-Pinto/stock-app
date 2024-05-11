from polygon import RESTClient
import pandas as pd
import pandas_ta as ta
import numpy as np
from backtesting import Strategy, Backtest
import matplotlib.pyplot as plt


API_KEY = "BrJLVaynDhKd6wgaHuof4bbhfLQgdqiK"

client = RESTClient(API_KEY)

tickers = ["SPY","IVV","VOO","VTI","QQQ","VEA","IEFA","VTV","BND","VUG","AGG","IWF","VWO","IJH","IEMG","VIG","IJR","VXUS","GLD","VGT","XLK","VO","IWM","BNDX","IWD"]
aggs = []
for symbol in tickers:
    aggs = client.get_aggs(
        symbol,
        1,
        "day",
        "2018-06-04",
        "2023-12-20",
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

