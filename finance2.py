# S&P 500 Data Fetcher - Web Scraping with Beautiful Soup and Pickle #

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

import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests

def save_sp500_tickers():
    # gets source code # 
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

    # Beautiful Soup Object
    soup = bs.BeautifulSoup(resp.text, 'lxml')

    # finds table of S&P 500 companies in source code
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []

    # iteratte through table in source code and add to list #
    for row in table.findAll('tr')[1:]: # "1 onward"
        ticker = row.findAll('td')[0].text
        ticker= ticker[:-1] 
        #ticker = row.findAll('td')[0].text.replace('.','-')
        tickers.append(ticker)

     # saving list #
    with open("sp500tickers.pickle", "wb") as f:
        # dumping tickers to file f 
        pickle.dump(tickers, f)
    
    print(tickers)
    
    return tickers

# already stored #
#save_sp500_tickers()

def get_data_from_yahoo(reload_sp500=False):
    # if you want to refetch the data 
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    
    # if directory does not already exist, make it # 
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    
    # start and end dates #
    start = dt.datetime(2010, 1, 1)
    end = dt.datetime.now()

    for ticker in tickers[:25]: # get the first 25
        # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            #df = df.drop("Symbol", axis=1)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))


get_data_from_yahoo()
