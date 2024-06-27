import requests
import binance_info
import hmac
import hashlib
import binance
import asyncio
import global_vars
import ujson


def send_simple_get_order(url, callback, *args):
    resp = requests.get(url)
    callback(resp.json(), *args)

def get_simple_earn_rates(target_currencies: set, interest_rates: dict):
    # Make the request
    response = get_default_simple_earn()
    got_currencies = set()

    for elem in response.json()["rows"]:
        interest_rates[elem["asset"]] = float(elem["latestAnnualPercentageRate"])
        got_currencies.add(elem["asset"])

    for currency in target_currencies:
        if currency not in got_currencies:
            data = get_default_simple_earn(currency, True).json()["rows"]
            if(data == []):
                continue
            data = data[0]
            interest_rates[data["asset"]] = float(data["latestAnnualPercentageRate"])

def get_default_simple_earn(currency="", isspecified = False):
    resp = requests.get("https://api.binance.com/api/v3/time")
    timeServer = resp.json()["serverTime"]
    api_secret = binance_info.api_secret
    api_key = binance_info.api_key
    url = "https://api.binance.com/sapi/v1/simple-earn/flexible/list"

    if not isspecified:
        params = {
            'timestamp': timeServer,
            'size': 100
        }
    else:
        params = {
            'timestamp': timeServer,
            'size': 100,
            'asset':currency
        }

    # Create the query string
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])

    # Signature for the request
    signature = hmac.new(
        api_secret.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    # Add the signature to the parameters
    params['signature'] = signature

    # Headers for the request
    headers = {
        'X-MBX-APIKEY': api_key
    }

    # Make the request
    response = requests.get(url, headers=headers, params=params)
    return response

async def get_all_prices():
    client = binance.client.Client(binance_info.api_key, binance_info.api_secret)
    while(True):
        data = client.get_all_tickers()
        for el in data:
            global_vars.spot_symbol_to_value[el["symbol"]] = float(el["price"])
        await asyncio.sleep(3600)

async def get_usdm_prices(symbols:set):
    while(True):
        url = "https://fapi.binance.com/fapi/v1/ticker/price"
        resp = requests.get(url)
        data = resp.json()
        for coindata in data:
            if not(coindata["symbol"] in symbols):
                continue
            global_vars.usdm_futures_symbol_to_value[coindata["symbol"]] = float(coindata["price"])
        print(symbols)
        print(data)
        await asyncio.sleep(3600)

async def get_coinm_prices(symbols:set):
    while(True):
        url = "https://dapi.binance.com/dapi/v1/ticker/price"

        response = requests.get(url)
        data = response.json()
        for coindata in data:
            if not(coindata["symbol"] in symbols) :
                continue
            global_vars.coinm_futures_symbol_to_value[coindata["symbol"]] = float(coindata["price"])

        await asyncio.sleep(3600)

async def get_spot_orderbooks(symbols:set):
    while(True):
        url = "https://api.binance.com/api/v3/depth"
        for symbol in symbols:
            print(symbol)
            params = {"symbol":symbol,"limit":1000}
            response = requests.get(url, params=params)

            biddata = response.json()["bids"]
            askdata = response.json()["asks"]
            bid_data_sorted = []
            ask_data_sorted = []
            for bid in biddata:
                bid_data_sorted.append((float(bid[0]), float(bid[1])))
            for ask in askdata:
                ask_data_sorted.append((float(ask[0]), float(ask[1])))
            ask_data_sorted = sorted(ask_data_sorted, reverse=False)
            bid_data_sorted = sorted(bid_data_sorted, reverse=True)
            print("ask_data_sorted:", ask_data_sorted)
            print("bid_data_sorted:", bid_data_sorted)
            global_vars.spot_symbol_to_bid_orderbook[symbol] = bid_data_sorted
            global_vars.spot_symbol_to_ask_orderbook[symbol] = ask_data_sorted
        await asyncio.sleep(900)

async def get_future_orderbooks(symbols:set, is_usdm=True):
    if(is_usdm):
        url = "https://fapi.binance.com/fapi/v1/depth"
        store_bid_data = global_vars.usdm_futures_symbol_to_bid_orderbook
        store_ask_data = global_vars.usdm_futures_symbol_to_ask_orderbook
    else:
        url = "https://dapi.binance.com/dapi/v1/depth"
        store_bid_data = global_vars.coinm_futures_symbol_to_bid_orderbook
        store_ask_data = global_vars.coinm_futures_symbol_to_ask_orderbook
    while(True):
        for symbol in symbols:
            print(symbol)
            params = {"symbol":symbol, "limit":1000}
            response = requests.get(url, params=params)

            biddata = response.json()["bids"]
            askdata = response.json()["asks"]
            bid_data_sorted = []
            ask_data_sorted = []
            for bid in biddata:
                bid_data_sorted.append((float(bid[0]), float(bid[1])))
            for ask in askdata:
                ask_data_sorted.append((float(ask[0]), float(ask[1])))

            ask_data_sorted = sorted(ask_data_sorted, reverse=False)
            bid_data_sorted = sorted(bid_data_sorted, reverse=True)
            print("ask_data_sorted", ask_data_sorted)
            print("bid_data_sorted", bid_data_sorted)
            store_bid_data[symbol] = bid_data_sorted
            store_ask_data[symbol] = ask_data_sorted
        await asyncio.sleep(900)




#if __name__ == "__main__":
#    asyncio.run(get_future_orderbooks({"BTCUSDT_240628"}, True))