from data_pop import pd, plt, np
from data_io import load_eod_data
import yfinance as yf
import seaborn as sns



stocks = load_eod_data('AAPL')
print(stocks)
stocks.columns = stocks.columns.to_flat_index()
stocks.columns = pd.MultiIndex.from_tuples(stocks.columns)
close = stocks.loc[:, "close"].copy()
norm_close = close.div(close.iloc[0]).mul(100)
norm_close.plot(figsize=(13, 8), fontsize=12)
plt.legend(fontsize=12)
plt.style.use("seaborn-v0_8")
ret = close.pct_change().dropna()
summary = ret.describe().T.loc[:, ["mean", "std"]]
summary["mean"] = (summary["mean"] * 252).mul(100)
summary["std"] = summary["std"] * np.sqrt(252)
summary.plot.scatter(x="std", y="mean", figsize=(13, 8), fontsize=12, s=50)
for i in summary.index:
    plt.annotate(
        i, xy=(summary.loc[i, "std"] + 0.002, summary.loc[i, "mean"] + 0.002), size=12
    )
plt.xlabel("Annual Risk (Std. Dev.)", fontsize=15)
plt.ylabel("Annual Return (% Change)", fontsize=15)
plt.title("Risk/Return", fontsize=21)
plt.figure(figsize=(13, 8))
sns.set(font_scale=1.4)
sns.heatmap(
    ret.corr(), cmap="Reds", annot=True, annot_kws={"size": 15}, vmax=0.6, fmt=".2g"
)
plt.show()
