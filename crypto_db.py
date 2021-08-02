import pandas as pd 
import pystore
import os
import numpy as np
from cryptohedge_config import kraken_api_key, pystore_path_local, raw_data_path_local

pystore_path_local =  os.path.dirname(os.path.abspath(__file__)) + '\\pystore'
raw_data_path_local = os.path.dirname(os.path.abspath(__file__)) + '\\raw_data'

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
        self.pystore_path = pystore.get_path()
        self.raw_data_path = raw_data_path
        self.store = pystore.store('CryptoDB')

    def process_csv(file_name): 
        '''
        Name: process_csv

        Arguments: 
            file_name: str : raw csv file name stored in

        Returns: 
            - pd.DataFrame: 
                > contains 
        '''
        

# Function Read CSV and Convert to Data Frame #
pd.to_datetime(datetime.fromtimestamp())

# Function to Calculate Volume Weighted Price takes in time period #
