import krakenex
from pykrakenapi import KrakenAPI

if __name__ == '__main__': 
    api = krakenex.API()
    api.load_key('lowkey.txt')
    kraken = KrakenAPI(api)

