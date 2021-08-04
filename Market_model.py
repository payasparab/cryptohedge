import requests
import pandas as pd
import numpy as np
from datetime import datetime

# get bid and ask spread
def slippage_moment(ticker, order_type, amount):
    '''
    ticker : str : cryptocurrency you want current market liq for
    order_type : str : buy / sell 
    amount : float : dollar amount to transact

    Returns: 
        pct_slippage : float 
    '''
    if order_type not in ['buy', 'sell']:
        raise ValueError('Order type arg {} is invalid'.format(order_type))

    
    resp = requests.get('https://api.kraken.com/0/public/Depth?pair={}'.format(ticker))
    response = resp.json()

    _assetcode = 'XXBTZUSD' #TODO temporary hard code need to map to asset codes csv
    asks = response['result'][_assetcode]['asks']
    bids = response['result'][_assetcode]['bids']

    cols = ['price', 'volume', 'timestamp']
    ask_df = pd.DataFrame(asks, columns=cols)
    bid_df = pd.DataFrame(bids, columns=cols)

    ask_df['vw_price'] = ask_df.apply(
            lambda x: (x.price.dot(x.volume))/(x.volume.sum())
        )
    bid_df['vw_price'] = bid_df.apply(
            lambda x: (x.price.dot(x.volume))/(x.volume.sum()), axis=1
        )

    ask_df['timestamp'] = pd.to_datetime(ask_df['timestamp'].apply(
        lambda x: datetime.fromtimestamp(x)))

    bid_df['timestamp'] = pd.to_datetime(bid_df['timestamp'].apply(
        lambda x: datetime.fromtimestamp(x)))

    ask_df[['price', 'volume']] = ask_df[['price', 'volume']].astype('float') 
    bid_df[['price', 'volume']] = bid_df[['price', 'volume']].astype('float')   
    ask_df = ask_df.sort_values('timestamp')
    bid_df = bid_df.sort_values('timestamp')
    
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
            print('Please make a smaller trade you dipshit!')
        elif volume_to_move < ask_df.iloc[0].volume:
            return (ask_df.iloc[0].price/curr_mkt_price)- 1 
        else:
            _orderbook_cleared = ask_df[(ask_df.cumul_volume < volume_to_move)]
            _full_clear =  _orderbook_cleared.iloc[:-1]
            
            _final_price = _orderbook_cleared.iloc[-1]
            _final_price['volume'] = (volume_to_move - _full_clear.volume.sum())

            _total_clear = pd.concat([_full_clear, _final_price.to_frame().T])
            exec_price = (_total_clear.price.dot(_total_clear.volume))/ _total_clear.volume.sum()
            return ((exec_price/curr_mkt_price) - 1)

    else: 
        # Sell
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
            print('Please make a smaller trade you dipshit!')
        elif volume_to_move < ask_df.iloc[0].volume:
            return (ask_df.iloc[0].price/curr_mkt_price)- 1 
        else:
            _orderbook_cleared = ask_df[(ask_df.cumul_volume < volume_to_move)]
            _full_clear =  _orderbook_cleared.iloc[:-1]
            
            _final_price = _orderbook_cleared.iloc[-1]
            _final_price['volume'] = (volume_to_move - _full_clear.volume.sum())

            _total_clear = pd.concat([_full_clear, _final_price.to_frame().T])
            exec_price = (_total_clear.price.dot(_total_clear.volume))/ _total_clear.volume.sum()
            return ((exec_price/curr_mkt_price) - 1)




#Calculate slippage

def market_slippage(crypto, amount, starttime, endtime):
    bids = []

#get max and min of bids then take average
    for bid in bids:
        max_bid = bids.max()
        min_bid = bids.min()
        current_market_price = avg(max_bid, min_bid)

# need different groupings for bid and asks and need to take for product of volume and price
    for ask in asks:
        max_ask = ask.max()
        min_ask = asks.min()
        current_market_price = avg(max_ask, min_ask)





get_data('BTCUSD')




