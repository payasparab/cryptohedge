import pandas as pd
import numpy as np
from crypto_db import CryptoDB

def _calculate_volume_weighted_price(cdb=CryptoDB(), coin='BTC', 
        time='24H'): 
    '''
    
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

    
    

    
    
    

    
    
