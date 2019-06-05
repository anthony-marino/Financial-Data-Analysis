## Candle Stick Graph ##

#pip install mpl_finance
#pip install pandas
#pip install requests
#pip install numpy
#pip install matplotlib
#pip install numpy

## Required Modules ##
# Numpy
# Matplotlib
# Pandas
# Pandas-datareader
# BeautifulSoup4
# scikit-learn / sklearn

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web

def main():

    # plot style #
    style.use('ggplot')

    # download data #
    start = dt.datetime(2000, 1, 1)
    end = dt.datetime.now()
    df = web.DataReader("TSLA", 'yahoo', start, end)
    df.to_csv('TSLA.csv')

    # read from csv file # # index_col=0 removes numeric index #
    df = pd.read_csv('TSLA.csv', parse_dates=True, index_col=0)

    # resampling # # ohlc = open high low close #
    df_ohlc = df['Adj Close'].resample('10D').ohlc()
    df_volume = df['Volume'].resample('10D').sum()

    # reset index so that date is a column #
    df_ohlc.reset_index(inplace=True)

    # convert to mdates #
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

    # calculate moving average #
    df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()

    # initializing subplot #
    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1) 

    # display mdates #
    ax1.xaxis_date()

    # configuring up candlestick graph #
    candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')

    # displays volume in bottom plot #
    ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)


    # Testing #
    #df.index = date
    # ax1.plot(df.index, df['Adj Close'])
    # ax1.plot(df.index, df['100ma'])
    # ax2.bar(df.index, df['Volume'])
    #df['Open'].plot()

    # prints date, ohlc, volume and 100 moving average #
    print(df.tail())

    # displays candlestick graph #
    plt.show()

main()

