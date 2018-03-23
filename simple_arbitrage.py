#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 23:31:44 2018

@author: hsnsd

A simple program to give you arbitrage opportunity of any input coin using cryptonator's api.
"""
import pandas as pd
import requests
import json
from matplotlib import pyplot as plt
import numpy as np

def getArbitrage(coin, curr = 'usd'):
    url = "https://api.cryptonator.com/api/full/{}-{}".format(coin,curr)
    r = requests.get(url)
    dict = json.loads(r.content)
    data = dict['ticker']['markets']
    sortedData = sorted(data, key=lambda x:x['price'])
    print ('Lowest price is: ' + sortedData[0]['price'] + ' at ' + sortedData[0]['market'])
    print ('Highest price is: ' + sortedData[len(sortedData)-1]['price'] + ' at ' + sortedData[len(sortedData)-1]['market'])
    print ('Potential arbitrage profit is ' + str(float(sortedData[len(sortedData)-1]['price']) - float(sortedData[0]['price'])) )
    df = pd.DataFrame(data)
    plt.figure(num=None, figsize=(8, 6), dpi=100)
    df['price'] = df['price'].astype(float)
    plt.scatter(df['price'], df['volume'])
    for mMkt, mRate, mVol in zip(df['market'], df['price'], df['volume']):    
        plt.annotate(mMkt,xy=(mRate, mVol), xytext=(5, -5), textcoords='offset points',fontsize=8)
    plt.title("Cryptocurrency Arbitrage Assignment")
    plt.xlabel("Price")
    plt.ylabel("Volumes")
    plt.show()
dict = getArbitrage(input('Enter coin name '))

