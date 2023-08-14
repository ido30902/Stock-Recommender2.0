import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import yfinance as yf

# Variables


def main():
    # tickers = load_tickers_list()

    test_mulitple()

    ccl = yf.download('CCL', period='max')
    snp = yf.download('^GSPC', period='max')

    ccl_frame = pd.DataFrame(ccl)
    snp_frame = pd.DataFrame(snp)

    result = pd.DataFrame(
        {'Carnival Cruise Lines': ccl_frame["Close"], 'S&P 500': snp_frame["Close"]})
    result.plot()

    plt.show()


def load_tickers_list():
    pass


def test_mulitple():
    tickers = yf.download('CCL ^GSPC GOOG TSLA AAPL ATKR',
                          period='max')

    multpl_stock_monthly_returns = tickers['Adj Close'].resample(
        'M').ffill().pct_change()

    (multpl_stock_monthly_returns + 1).cumprod().plot()
    plt.show()


if __name__ == '__main__':
    main()
