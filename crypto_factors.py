from datetime import time
import pandas as pd
import numpy as np
from crypto_db import CryptoDB
from tqdm import tqdm
import matplotlib.pyplot as plt



def calc_vm_price(coin, cdb=CryptoDB(),time='24H'): 
    '''
    Args: 
        - coin : str : currency pair/name
        - cdb : CrypCtoDB obj : database to query for price data
        - time : pd time str : rebalance time period for calculating price
    
    Returns: pd.DF: cols: 
        - wv_price : float : volume weighted price
        - traded_volume : float : total traded volume
        - rets : float : returns of 
    '''
    transactions = cdb.query('transactions', coin)
    wv_price = transactions.groupby(pd.Grouper(
        key='timestamp',
        freq=time)).apply(
            lambda x: (x.price.dot(x.volume))/(x.volume.sum())
        )
    
    traded_volume = transactions.groupby(pd.Grouper(
        key='timestamp',
        freq=time)).apply(
            lambda x: (x.volume.sum())
        )

    wv_price = wv_price.rename('wv_price')
    traded_volume = traded_volume.rename('traded_volume')
    output = pd.concat([wv_price, traded_volume], axis=1)
    output['rets'] = output.wv_price.pct_change()
    output['currency'] = coin
    output = output.reset_index().set_index(
        ['timestamp', 'currency']
    )
    return output


def generate_returns_db(time_period='24H'): 
    '''
    Creates pystore returns for processing 
    database. 
    '''
    #TODO : move this to crypto_db to keep all reads and writes in one place
    cdb = CryptoDB()
    to_collection = cdb.store.collection('returns')
    coins = cdb.store.collection('transactions').list_items()
    rets_dfs = []
    for coin in tqdm(coins): 
        _rets_df = calc_vm_price(coin, cdb, time_period)
        rets_dfs.append(_rets_df)
    
    returns_df = pd.concat(rets_dfs)
    returns_df = returns_df.reset_index()
    returns_df = returns_df.dropna()
    to_collection.write(time_period, returns_df, overwrite=True)

class CryptoRiskAnalyzer: 
    def __init__(self, cdb=CryptoDB()):
        self.cdb = cdb
        self.rets_collect = self.cdb.store.collection('returns')


    def calc_rolling_vol(self, coins, lookback, index_freq): 
        ''' 
        coins : lst(str) : Cryptocurrencies to display 
        benchmarks : lst(str) : Funds to benchmark against
        lookback : int : num : how many periods for distribution
        index_freq : pd.Datetime Grouper : tracking time for returns
        '''
        rets = self.rets_collect.item(index_freq).to_pandas().set_index(
                            ['timestamp', 'currency']).rets
        _rets = rets.unstack()[coins]
        _vol = _rets.rolling(lookback).std().dropna()
        print(_rets.dropna().describe())
        _vol.plot(title='Annualized Volatility')
        
    '''
    def what_time_to_trade(self):
        rets = self.rets_collect.item('3H').to_pandas().set_index(
                            ['timestamp', 'currency']).rets
        
        rets = rets.to_frame().reset_index()
        
        rets['hour'] = rets.timestamp.dt.hour
    '''



    def calc_sharpe_table(self, coins): 
        '''
        Outputs a table of Sharpe ratios for coins and benchmarks requested.
        '''
        rets = self.rets_collect.item('24H').to_pandas().set_index(
                            ['timestamp', 'currency']).rets
        years = [1, 3, 5]


def kraken_index(frequency):
    cdb = CryptoDB()
    rets = cdb.store.collection('returns').item(frequency).to_pandas()
    rets = rets.set_index(['timestamp', 'currency'])

    rets['traded_dollars'] = rets.wv_price.mul(rets.traded_volume)
    vw_index = rets.reset_index().groupby('timestamp').apply(
        lambda x: ((x.traded_dollars/x.traded_dollars.sum()) * x.rets).sum()
    )

    vw_index = vw_index.cumsum() + 1
    vw_index = vw_index * 100
    
    fig, axes = plt.subplots(nrows=2, ncols=1)


    vw_index.cumsum().plot(ax=axes[0], title='Kraken Exchange Returns Index')

    print('Number of cryptocurrencies on Kraken:')
    rets.groupby('timestamp').rets.count().rolling(30).mean().plot(
                    ax=axes[1], 
                    title='Number of cryptocurrencies on Kraken'
                )




        
        

    
    
    

    
    
