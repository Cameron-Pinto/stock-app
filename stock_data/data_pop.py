import pandas as pd
import pandas_ta as ta
import numpy as np
import yfinance as yf
from backtesting import Strategy, Backtest
import matplotlib.pyplot as plt


tickers = ["AAPL", "SPY", "XOM", "MSFT", "IBM", "CVX", "WMT", "GE", "GOOG", "PG", "T", "JNJ", "WFC", "JPM", "PFE", "KO", "PM", "ORCL", "INTC", "MRK", "QCOM", "CSCO", "VZ", "PEP", "C", "MCD", "VTI", "BAC", "V", "ABT", "COP", "SPY", "SLB", "AMZN", "CMCSA", "DIS", "HD", "UPS", "OXY", "CAT", "AXP", "GLD", "MO", "AIG", "UNH", "MMM", "EMC", "USB", "GS", "CVS", "BMY", "MA", "BA", "AMGN", "UNP", "NKE", "DD", "NWSA", "F", "LLY", "CL", "HON", "EBAY", "HPQ", "EPD", "SBUX", "LVS", "SPG", "SCO", "VWO", "MDT", "DOW", "EEM", "LOW", "SO", "GM", "MET", "TGT", "COST", "DHR",]

for ticker in tickers:
    stocks = yf.download(ticker, start="2014-01-01", group_by="tickers")
    df = pd.DataFrame(stocks)
    df.drop(["Adj Close"], axis=1, inplace=True)
    df.reset_index(inplace=True)
    df.rename(
       columns={
        "Date": "date",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume",
        "Open": "open",
    }, inplace = True)
    df.to_csv(
        r"C:\Users\Camer\OneDrive\Documents\Python-Projects\stock-app\stock_data\data\eod\{}.csv".format(
            ticker)
        )

