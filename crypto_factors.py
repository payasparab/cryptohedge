from datetime import time
import pandas as pd
import numpy as np
from crypto_db import CryptoDB
from tqdm import tqdm

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
        self.rets_df = None


    def calc_rolling_vol(self, coins, benchmarks, lookback, index_freq): 
        ''' 
        
        '''
        
        

    def plot_rolling_vol(self, coins, benchmarks, lookback, index_freq): 
        '''
        coins : lst(str) : Cryptocurrencies to display 
        benchmarks : lst(str) : Funds to benchmark against
        lookback : int : num
        index_freq : pd.Datetime Grouper : tracking time
        ''' 


    def calc_sharpe_table(self, coins, benchmarks, lookback, index_freq): 
        '''
        Outputs a table of Sharpe ratios for coins and benchmarks requested.
        '''
        
        pass

    
    
    

    
    
