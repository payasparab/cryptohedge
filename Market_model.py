import requests
import pandas as pd

# get bid and ask spread
def get_data(ticker):
    resp = requests.get('https://api.kraken.com/0/public/Depth?pair={}'.format(ticker))

    response = resp.json()


    print(response)
    if not response:
        return pd.Dataframe()

    r2 = pd.DataFrame(response)
    return r2

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




