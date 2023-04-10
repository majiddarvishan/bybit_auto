from pybit.unified_trading import HTTP
from pybit.exceptions import *
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

session = HTTP(
    testnet=False,
    api_key=API_KEY,
    api_secret=API_SECRET,
)


def put_order(sybmol: str, side: str, usdt: str, leverage: str, tp: str, sl: str) -> str:
    resp = session.get_tickers(category="linear", symbol=sybmol)
    last_price = float(resp['result']['list'][0]['lastPrice'])
    qty = "{:.6f}".format(usdt / last_price)

    try:
        resp = session.set_leverage(
            category="linear", symbol=sybmol, buyLeverage=leverage, sellLeverage=leverage)
        print(resp)
    except InvalidRequestError as exp:
        print(f'{exp.status_code}, {exp.message}')

    try:
        resp = session.switch_margin_mode(
            category="linear", symbol=sybmol, tradeMode=0, buyLeverage=leverage, sellLeverage=leverage)
        print(resp)
    except InvalidRequestError as exp:
        print(f'{exp.status_code}, {exp.message}')

    try:
        resp = session.place_order(category="linear",
                                   symbol=sybmol,
                                   side=side,
                                   orderType="Market",
                                   qty=qty,
                                   takeProfit=tp,
                                   stopLoss=sl)
        print(resp)
        order_id = resp["result"]["orderId"]
        return order_id
    except InvalidRequestError as exp:
        print(f'{exp.status_code}, {exp.message}')

    return None


def change_stop_loss(sybmol: str, sl: str) -> None:
    try:
        resp = session.set_trading_stop(category="linear", symbol=sybmol, stopLoss=sl, positionIdx=0)
        print(resp)
    except InvalidRequestError as exp:
        print(f'{exp.status_code}, {exp.message}')

def cancel_order(sybmol: str, order_id: str) -> None:
    try:
        resp = session.cancel_order(category="linear", symbol=sybmol, orderId=order_id)
        print(resp)
    except InvalidRequestError as exp:
        print(f'{exp.status_code}, {exp.message}')

order_id = put_order("BTCUSDT", "Sell", 200, "30", "28000", "30000")
change_stop_loss("BTCUSDT", "28500")
cancel_order("BTCUSDT", "324347685434")


