import rest_requests
import listener_functions
import utils
import websocket_stream
import asyncio
import binance
import binance_info
import global_vars

async def get_async_gather(leverage, spot_trade_symbols, usdm_trade_symbols, coinm_trade_symbols):

    task1 = asyncio.create_task(rest_requests.get_spot_orderbooks(spot_trade_symbols))
    print(spot_trade_symbols)

    task2 = asyncio.create_task(rest_requests.get_future_orderbooks(usdm_trade_symbols, True))
    print(usdm_trade_symbols)

    task3 = asyncio.create_task(rest_requests.get_future_orderbooks(coinm_trade_symbols, False))
    print(coinm_trade_symbols)

    task4 = asyncio.create_task(utils.log_interest_rates_usdm(leverage=leverage, notional_size=1000))

    task5 = asyncio.create_task(utils.log_interest_rates_coinm(leverage=leverage, notional_size=1000))

    await asyncio.gather(task1, task2, task3, task4, task5)

if __name__ == '__main__':
    trade_pairs = set()
    usdm_trade_symbols = set()
    coinm_trade_symbols = set()
    currencies = set()
    rest_requests.send_simple_get_order("https://fapi.binance.com/fapi/v1/exchangeInfo",
                                        listener_functions.simple_print_usdm, trade_pairs,
                                        usdm_trade_symbols, currencies,
                                        global_vars.futures_symbol_to_stock_symbol, global_vars.spot_symbol_to_currencies)
    rest_requests.send_simple_get_order("https://dapi.binance.com/dapi/v1/exchangeInfo",
                                        listener_functions.simple_print_coinm, trade_pairs,
                                        coinm_trade_symbols, currencies,
                                        global_vars.futures_symbol_to_stock_symbol, global_vars.spot_symbol_to_currencies)

    add_tr_pairs = []
    rem_tr_pairs = []
    for trade_pair in trade_pairs:
        if(trade_pair.endswith("USD")):
            add_tr_pairs.append(trade_pair + "T")
            rem_tr_pairs.append(trade_pair)
    for add_pair in add_tr_pairs:
        trade_pairs.add(add_pair)
        cur1, cur2 = global_vars.spot_symbol_to_currencies[add_pair[:-1]]
        global_vars.spot_symbol_to_currencies[add_pair] = (cur1, cur2+"T")
    for rem_pair in rem_tr_pairs:
        trade_pairs.remove(rem_pair)

    asyncio.run(get_async_gather(10, trade_pairs, usdm_trade_symbols ,coinm_trade_symbols))





