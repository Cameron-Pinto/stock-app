from polygon import RESTClient
import pandas as pd
import pandas_ta as ta
import numpy as np
from backtesting import Strategy, Backtest
import matplotlib.pyplot as plt
import glob
from multiprocessing import Pool
import os

path = (
    "C:\\Users\\Camer\\OneDrive\\Documents\\Python-Projects\\stock-app\\stock_data\\data\\eod"
)
# def read_csv(filename):
#    return pd.read_csv(filename)
#
# def main():
#    files = os.listdir(path)
#    file_list = [filename for filename in files if filename.split('.')[1]=="csv"]
#    print(files)
#
#    with Pool() as p:
#        df_list = p.map(read_csv, file_list)
#        print(df_list)
#
# if __name__ == '__main__':
#    main()


class Willr(Strategy):
    upper_bound = -25
    lower_bound = -75

    def init(self):
        self.willr = self.I(
            ta.willr,
            pd.Series(self.data.High),
            pd.Series(self.data.Low),
            pd.Series(self.data.Close),
        )

    def next(self):
        if self.willr <= self.lower_bound:
            if not self.position:
                self.buy()
        if self.willr >= self.upper_bound:
            if self.position:
                self.position.close()


def do_backtest(filename):
    df = pd.read_csv(f"{path}/{filename}")
    df["EMA"] = ta.ema(df.Close, length=20)
    df["EMA2"] = ta.ema(df.Close, length=50)
    df["Change"] = ta.percent_return(df.Close).mul(100)
    df["Prev_Low"] = df.Low.shift()
    df["Prev_High"] = df.High.shift()
    df = df.dropna()
    df.reset_index(inplace=True)
    ordersignal = [0] * len(df)
    for i in range(len(df)):
        if df.Low[i] < df.Prev_Low[i] and df.Close[i] < df.EMA2[i] and df.Change[i] < 0:
            ordersignal[i] = 1
        if df.Close[i] > df.EMA[i]:
            ordersignal[i] = -1
    df["ordersignal"] = ordersignal
    # emasignal = [0] * len(df)
    bt = Backtest(df, Willr, cash=10000, commission=0.00)
    stat = bt.run()
    bt.plot()
    #stat = bt.optimize(
    #   upper_bound=list(np.arange(0, -40, -1)),
    #   lower_bound=list(np.arange(-50, -90, -1)),
    #   maximize="Equity Final [$]",
    #)
    sym = filename.split(".")[0]
    return (sym, stat["Return [%]"], stat["Buy & Hold Return [%]"])
    dfp1 = pd.DataFrame(sym, stat["Return [%]"], stat["Buy & Hold Return [%]"])
    headers = ['Ticker', 'Return', 'Buy and Hold']
    dfp1.to_excel('data.xlsx', index=False, na_rep='N/A', header='headers', index_label='ID')


# def buysignal(df):
#    ordersignal = [0] * len(df)
#    for i in range(len(df)):
#        if df.Low[i] < df.Prev_Low[i] and df.Close[i] < df.EMA[i] and df.Change[i] < 0:
#            ordersignal[i] = 1
#        if df.Close[i] > df.EMA[i]:
#            ordersignal[i] = -1
#    df["ordersignal"] = ordersignal


# buysignal(df)
#
#
# def SIGNAL():
#    return df.ordersignal


# class Momentum(Strategy):
#    def init(self):
#        super().init()
#        self.signal = self.I(SIGNAL)
#
#    def next(self):
#        super().next
#        current_signal = self.data.ordersignal[-1]
#        if current_signal == 1:
#            if not self.position:
#                self.sell()
#        if current_signal == -1:
#            if self.position:
#                self.position.close()


if __name__ == "__main__":
    with Pool() as p:
        results = p.map(do_backtest, os.listdir(path))
    print(results)
