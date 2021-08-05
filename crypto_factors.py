import pandas as pd
import numpy as np
from crypto_db import CryptoDB


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




    
    
    

    
    
