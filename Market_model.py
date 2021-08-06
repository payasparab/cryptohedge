import requests
import pandas as pd
import numpy as np
from datetime import datetime

# get bid and ask spread
def crypto_slippage(ticker, order_type, amount):
    '''
    ticker : str : cryptocurrency you want current market liq for
    order_type : str : buy / sell 
    amount : float : dollar amount to transact

    Returns: 
        pct_slippage : float 
    '''
    if order_type not in ['buy', 'sell']:
        raise ValueError('Order type arg {} is invalid'.format(order_type))

    if ticker == 'ANT': 
        ticker = 'ANTUSD'
        _assetcode = 'ANTUSD'

    resp = requests.get('https://api.kraken.com/0/public/Depth?pair={}'.format(ticker))
    response = resp.json()

    #TODO temporary hard code need to map to asset codes csv
    if ticker == 'BTCUSD':
        _assetcode = 'XXBTZUSD' 
    
    asks = response['result'][_assetcode]['asks']
    bids = response['result'][_assetcode]['bids']

    cols = ['price', 'volume', 'timestamp']
    ask_df = pd.DataFrame(asks, columns=cols)
    bid_df = pd.DataFrame(bids, columns=cols)
    ask_df[['price', 'volume']] = ask_df[['price', 'volume']].astype('float') 
    bid_df[['price', 'volume']] = bid_df[['price', 'volume']].astype('float')   

    ask_df['timestamp'] = pd.to_datetime(ask_df['timestamp'].apply(
        lambda x: datetime.fromtimestamp(x)))

    bid_df['timestamp'] = pd.to_datetime(bid_df['timestamp'].apply(
        lambda x: datetime.fromtimestamp(x)))


    ask_df['cumul_volume'] = ask_df.volume.cumsum()
    bid_df['cumul_volume'] = bid_df.volume.cumsum()

    curr_mkt_price = np.mean([max(bid_df.price), min(ask_df.price)])
    
    volume_to_move = amount/curr_mkt_price
    if order_type == 'buy': 
        order_book_max  = ask_df.volume.sum() 
        if volume_to_move > order_book_max:
            print(('trade of {} amount results in {} of {} shares' +  
            'which exceeds order book volume of {}').format(
                    amount, 
                    order_type, 
                    volume_to_move,
                    order_book_max
                )
            )
            return (max(ask_df.price)/curr_mkt_price) -1 
        elif volume_to_move < ask_df.iloc[0].volume:
            return (ask_df.iloc[0].price/curr_mkt_price) - 1 
        else:
            _full_clear = ask_df[(ask_df.cumul_volume < volume_to_move)]
            
            _final_price = ask_df.iloc[(_full_clear.index.max() + 1)]
            _final_price['volume'] = (volume_to_move - _full_clear.volume.sum())

            _total_clear = pd.concat([_full_clear, _final_price.to_frame().T])
            exec_price = (_total_clear.price.dot(_total_clear.volume))/ _total_clear.volume.sum()
            return ((exec_price/curr_mkt_price) - 1)

    else: 
        # Sell
        order_book_max  = bid_df.volume.sum() 
        if volume_to_move > order_book_max:
            print(('trade of {} amount results in {} of {} shares' +  
            'which exceeds order book volume of {}').format(
                    amount, 
                    order_type, 
                    volume_to_move,
                    order_book_max
                )
            )
            return (min(bid_df.price)/curr_mkt_price) - 1
        elif volume_to_move < bid_df.iloc[0].volume:
            return np.abs((bid_df.iloc[0].price/curr_mkt_price)- 1)
        else:
            _full_clear = bid_df[(bid_df.cumul_volume < volume_to_move)]
            
            _final_price = bid_df.iloc[(_full_clear.index.max() + 1)]
            _final_price['volume'] = (volume_to_move - _full_clear.volume.sum())

            _total_clear = pd.concat([_full_clear, _final_price.to_frame().T])
            exec_price = (_total_clear.price.dot(_total_clear.volume))/ _total_clear.volume.sum()
            return np.abs((exec_price/curr_mkt_price) - 1)






