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
        self.data_load_fail = None


    def query(self, db, coin, return_dask=False):
        '''
        Args: 

            coin : str : can contain asset_name or asset_code or werd exceptions
        ''' 
        if db not in self.store.list_collections(): 
            print('Invalid collection argument'.format(db))
        
        if coin in self.assetcodes.index: 
            search_term = self.assetcodes.asset_name[coin]
            _item = self.store.collection(db).item(search_term)
        elif self.assetcodes.asset_name.str.contains(coin).any():
            _item = self.store.collection(db).item(coin)
        else: 
            e_msg = 'Invalid coin argument: {}'.format(coin)
            raise ValueError(e_msg)

        if return_dask:
            return _item.data
        else:
            return _item.to_pandas(parse_dates=False)
    
    def load_raw_data(self, currency='USD'): 
        '''
        Function to load all raw_data for transactions and load into 
        database. 
        '''
        files_lst = os.listdir(self.raw_data_path)
        files_lst = [f for f in files_lst if (
                (currency in f) 
                and ('USDT' not in  f) 
                and ('USDC' not in f))] 
        failed = []
        for _file in tqdm(files_lst):
            ignores = ['REPV2USD.csv', 'WAVESUSD.csv']

            if _file in ignores: 
                continue
            
            try: 
                _df = self._process_csv(_file)
            except (KeyError, FileNotFoundError):
                failed.append(_file)
            
            
            x_add = [
                # Currency pairs that need an X for some stupid ass reason
                'ETCUSD', 'ETHUSD', 'LTCUSD', 'MLNUSD', 'REPUSD', 
                'XBTUSD', 'XLMUSD', 'XMRUSD', 'XRPUSD', 'ZECUSD', 
                'XTZUSD', 'XDGUSD'
            ] 
            
            z_add = [
                # Currency pairs that need an X for some stupid ass reason
                'EURUSD', 'GBPUSD', 'AUDUSD', 'JPYUSD'
            ]


            pair_code = _df.pair_code.iloc[0]

            if pair_code in x_add:
                pair_code = 'X' + pair_code

            if pair_code in z_add:
                pair_code = 'Z' + pair_code 

            _df['pair_code'] = pair_code
            _df['cash'] = currency
            _df['crypto'] = pair_code.replace(currency, '')

            
            _cryptoname = _df.crypto.iloc[0]
            _cryptoname_full = self.assetcodes.loc[_cryptoname].asset_name
            _df['asset_name_full'] = _cryptoname_full
 
            try: 
                self.store.collection(
                    'transactions').write(
                            _cryptoname_full, _df, overwrite=True
                    )
            except:
                failed.append('Pystore_fail: {}'.format(_file))

        print('The following tickers failed: {}'.format(
            failed
        ))
        self.data_load_fail = failed
        

        
        


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
        #TODO : temporary knocking out asset codes to make life easier
        '''
        
        _pairs_cut = self.pairs.loc[pair_code]
        data['crypto'] = _pairs_cut['base']
        data['cash'] = _pairs_cut['quote']
        '''
        return data

if __name__ == '__main__': 
    cdb = CryptoDB()
