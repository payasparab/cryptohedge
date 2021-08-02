import pandas as pd 
import pystore
import os
from datetime import datetime
import numpy as np
from cryptohedge_config import pystore_path_local, raw_data_path_local
import krakenex
from pykrakenapi import KrakenAPI

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
        self.assetcodes = pd.read_csv('assetcode_key.csv')

    def process_csv(self, file_name): 
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
        

        return data
        

    def dump_to_pystore(self): 
        pass


# Function to Calculate Volume Weighted Price takes in time period #
