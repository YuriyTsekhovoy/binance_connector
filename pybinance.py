from environs import Env
import logging
import os
import re

from binance.client import Client
from fastapi import FastAPI

env = Env()
env.read_env()

# Getting credentials from .env variable
API_KEY = env('API_KEY')
API_SECRET = env('API_SECRET')

logger = logging.getLogger(__name__)
client = Client()
app = FastAPI()


async def get_order_book(symbol):
    logger.info("Getting order book for symbol %s", symbol)
    order_book = client.get_order_book(symbol=symbol)
    return order_book


async def get_pairs(base_quote):
    symb = client.get_exchange_info()
    # Filter out symbols that are not trading
    trading_symbols = []
    for symbol in symb['symbols']:
        try:
            if symbol['status'] == 'TRADING' and not base_quote:
                trading_symbols.append(symbol['symbol'])
            elif symbol['status'] == 'TRADING' and re.search(base_quote, symbol['symbol']):
                trading_symbols.append(symbol['symbol'])

        except TypeError:
            pass
    return trading_symbols


@app.get("/order_book/{symbol}")
async def get_order_book_endpoint(symbol: str):
    order_book = await get_order_book(symbol)
    return order_book


@app.get("/pairs")
async def get_pairs_endpoint(base_quote: str = None):
    trading_symbols = await get_pairs(base_quote)
    return trading_symbols


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
