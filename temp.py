# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from math import floor,ceil
from sklearn.linear_model import LinearRegression
import time
import traceback

from alpha_vantage.timeseries import TimeSeries
vintageAPIKey = "ZDNG27X5G826DEKN"
#file = open("aapl.csv","w")

# Submit our API and create a session
def predictPrice(ticker,dayUsed,dayFuture):
    alpha_ts = TimeSeries(key=vintageAPIKey, output_format='pandas')
    alpha_ts.output_format = 'pandas'
    try:
        print("starting "+ ticker)
        data,metadata = alpha_ts.get_daily(symbol="TSE:"+ticker,outputsize='full')
    except:
        print("failed2")
        return
        

    df = pd.DataFrame(data)
    df.index = df.index.astype(np.datetime64)
    colLen =len(df.columns)
    for day in range(2,dayUsed):
        for i in range(colLen):
            df[df.columns[i]+str(day)] = df[df.columns[i]].shift(day-1)
    
    df["label"]=df[df.columns[3]].shift(-(dayFuture-1))
    df = df[(dayFuture-1):-(dayFuture-1)]
    #df.to_csv("test.csv")
    numIndex = len(df)
    df.to_csv("stocks/"+ticker+".csv")
    
#    X_train = df.drop(columns="label")
#    X_train = X_train.head(floor(numIndex*0.75))
#    Y_train = df["label"]
#    Y_train = Y_train.head(floor(numIndex*0.75))
#    X_test = df.drop(columns="label")
#    X_test = X_test.tail(ceil(numIndex*0.25))
#    Y_test = df["label"]
#    Y_test = Y_test.tail(ceil(numIndex*0.25))
#    print(X_test.tail())
#    clf = LinearRegression()
#    clf.fit(X_train,Y_train)
#    #print(clf.score(X_test,Y_test))
#    #print(Y_test.iloc[[-1]])
#    #print(clf.predict(X_test.iloc[[-1]]))
#    dfStocks = pd.read_csv("WIKI_PRICES.csv")
#    dfStocks=dfStocks.set_index("ticker")
#    dfStocks.loc[ticker]["execution price"]=X_test.iloc[-8]["1. open"]
#    dfStocks.loc[ticker]["predict price"] = clf.predict(X_test.iloc[[-8]])
#    dfStocks.loc[ticker]["Friday close"] = X_test.iloc[-7]["4. close"]
#    dfStocks.loc[ticker]["%change"] = (dfStocks.loc[ticker]["predict price"]-dfStocks.loc[ticker]["execution price"])/dfStocks.loc[ticker]["execution price"]
#    dfStocks.loc[ticker]["buy price"]=X_test.iloc[-6]["1. open"]
#    dfStocks.loc[ticker]["sell price"]=X_test.iloc[-2]["4. close"]
#    dfStocks.loc[ticker]["score"]=clf.score(X_test,Y_test)
#    dfStocks.to_csv("WIKI_PRICES.csv")
#    print(dfStocks.loc[ticker]["execution price"])
#    print(dfStocks.loc[ticker]["predict price"])
#    print(dfStocks.loc[ticker]["Friday close"])
#    print(dfStocks.loc[ticker]["%change"])
#    print(dfStocks.loc[ticker]["buy price"])
#    print(dfStocks.loc[ticker]["sell price"])
#    print(dfStocks.loc[ticker]["score"])
#    print("done")
    

dayUsed = 6
dayFuture = 7
#ticker = "AAPL"
dfStocks = pd.read_csv("WIKI_PRICES.csv")
dfStocks=dfStocks.set_index("ticker")
for ticker in dfStocks.index:
    try:
        predictPrice(ticker,dayUsed,dayFuture)
    except:
        traceback.print_exc()
    time.sleep(15)

    
#predictPrice("BMO",dayUsed,dayFuture)

