import pandas as pd 
import pystore
import os
from datetime import datetime
import numpy as np
from cryptohedge_config import pystore_path_local, raw_data_path_local
import krakenex
from pykrakenapi import KrakenAPI
from tqdm import tqdm

class CryptoDB:
    '''
    class CryptoDB

    Description: a pystore accessor database to quickly access time 
    series data for cryptocurrency portfolio optimization. 
    
    Key Methods: 

        - dbmap : method to access information about items held in CryptoDB
        - query : access a Pystore item directly
        

    Key Attributes:
        - metadata : dict : information about the data currently stored
    
    '''
    
    def __init__(self, 
            pystore_path=pystore_path_local, 
            raw_data_path=raw_data_path_local
        ): 
    
        pystore.set_path(pystore_path)
        api = krakenex.API()
        api.load_key('lowkey.txt')
        self.kraken_api = KrakenAPI(api)

        self.pystore_path = pystore.get_path()
        self.raw_data_path = raw_data_path
        self.store = pystore.store('CryptoDB')
        self.pairs = self.kraken_api.get_tradable_asset_pairs()
        self.assetcodes = pd.read_csv('assetcode_key.csv').set_index('asset_code')


    
    def load_raw_data(self): 
        '''
        Function to load all raw_data for transactions and load into 
        database. 
        '''
        files_lst = os.listdir(self.raw_data_path)
        files_lst = [f for f in files_lst if (('USD' in f) and ('USDT' not in  f))] 
        failed = []
        for _file in tqdm(files_lst):
            try: 
                _df = self._process_csv(_file)
            except KeyError:
                failed.append(_file)
            
            _df['crypto_name'] = _df.set_index('crypto').join(
                                        self.assetcodes.asset_name
                                    ).reset_index().asset_name
            
            _cryptoname = _df.crypto_name.iloc[0]
            _df['cash_name'] = _df.set_index('cash').join(
                                        self.assetcodes.asset_name
                                    ).reset_index().asset_name

            
            self.store.collection(
                'transactions').write(
                        _cryptoname, _df, 
                )

        print('The following tickers failed: {}'.format(
            failed
        ))
        
    def _process_csv(self, file_name): 
        '''
        Name: process_csv

        Arguments: 
            file_name: str : raw csv file name stored in

        Returns: 
            - pd.DataFrame: with cols: 
                > timestamp 
                > 

        '''
        # Pull in file #
        full_path = self.raw_data_path + '\\' + file_name
        pair_code = file_name[:-4]
        cols = ['timestamp', 'price', 'volume']
        data = pd.read_csv(full_path, names=cols, header=None)
        data['pair_code'] = pair_code
        
        # Process Dates #
        data['timestamp'] = pd.to_datetime(data['timestamp'].apply(
                lambda x: datetime.fromtimestamp(x)))

        # Asset Code Processing #
        _pairs_cut = self.pairs.loc[pair_code]
        data['crypto'] = _pairs_cut['base']
        data['cash'] = _pairs_cut['quote']

        return data
        

if __name__ == '__main__': 
    cdb = CryptoDB()
    cdb.load_raw_data(filter_curr='USD')