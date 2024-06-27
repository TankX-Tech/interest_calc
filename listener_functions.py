from enum import Enum

import tornado.websocket


class tradetype(Enum):
    USDM = 0
    COINM = 1

def simple_print_usdm(json_data, trade_pairs:set, trade_symbols:set,
                      currencies:set, futures_to_stock_symb:dict, symbol_to_currs:dict):
    for el in json_data["symbols"]:
        if(el["contractType"] != "PERPETUAL")and(el["status"] == "TRADING"):
            trade_pairs.add(el["pair"])
            trade_symbols.add(el["symbol"])
            currencies.add(el["baseAsset"])
            currencies.add(el["quoteAsset"])
            futures_to_stock_symb[el["symbol"]] = el["pair"]
            symbol_to_currs[el["pair"]] = (el["baseAsset"], el["quoteAsset"])

def simple_print_coinm(json_data, trade_pairs:set, trade_symbols:set,
                       currencies:set, futures_to_stock_symb:dict, symbol_to_currs:dict):
    for el in json_data["symbols"]:
        if(el["contractType"] != "PERPETUAL")and(el["contractStatus"] == "TRADING"):
            trade_pairs.add(el["pair"])
            trade_symbols.add(el["symbol"])
            currencies.add(el["baseAsset"])
            currencies.add(el["quoteAsset"])
            futures_to_stock_symb[el["symbol"]] = el["pair"]
            symbol_to_currs[el["pair"]] = (el["baseAsset"], el["quoteAsset"])

