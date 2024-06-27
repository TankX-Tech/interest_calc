import asyncio
import datetime
import global_vars
from slack_sdk.web.async_client import AsyncWebClient

SLACK_TOKEN = None # put slack token here
CHANNEL_ID = None #put channel id here
slack_client = AsyncWebClient(token=SLACK_TOKEN)

async def log_interest_rates_usdm(leverage:float, notional_size:float):
    while(True):
        str_a = "----------------------------------------------"
        str_b = "===============USD-M FUTURES================="
        print(str_a)
        print(str_b)
        print(str_a)
        for futures_symb in global_vars.usdm_futures_symbol_to_bid_orderbook:
            #get price datas begin
            spot_eq = global_vars.futures_symbol_to_stock_symbol[futures_symb]
            if (global_vars.spot_symbol_to_bid_orderbook.get(spot_eq, -1) == -1):
                if(spot_eq.endswith("USD")):
                    spot_eq += "T"
                else:
                    continue
                continue
            base_cur, quote_cur = global_vars.spot_symbol_to_currencies[spot_eq]
            print(futures_symb)
            future_bid_price = (get_mean_price_at_volume
                            (global_vars.usdm_futures_symbol_to_bid_orderbook[futures_symb], notional_size))
            future_ask_price = (get_mean_price_at_volume
                            (global_vars.usdm_futures_symbol_to_ask_orderbook[futures_symb], notional_size))
            spot_ask_price = (get_mean_price_at_volume
                          (global_vars.spot_symbol_to_ask_orderbook[spot_eq], notional_size))
            spot_bid_price = (get_mean_price_at_volume
                            (global_vars.spot_symbol_to_bid_orderbook[spot_eq], notional_size))
            # get price datas end

            print("leverage", leverage)
            print("spot price", spot_ask_price)
            print("future price", future_bid_price)

            #calc time begin
            date_abbr = futures_symb.split("_")[1]
            year = int(date_abbr[:2]) + 2000
            month = int(date_abbr[2:4])
            day = int(date_abbr[4:])
            futuretime = datetime.datetime(year, month, day).timestamp()*1000
            now = datetime.datetime.now().timestamp()*1000
            time_diff = (futuretime - now)/86400000
            #calc time end

            print("end time", futuretime)
            print("time difference", time_diff)

            #calc interest here
            numerator = (1-1/leverage)*(future_bid_price - spot_ask_price)
            denominator = spot_ask_price
            coefficient = 365 / time_diff
            interest_rate = numerator / denominator * coefficient
            #calc interest here

            print("numerator:", numerator)
            print("denominator:", denominator)
            print("coefficient:", coefficient)
            text = f"{futures_symb} @{notional_size} {quote_cur} interest rate: {(interest_rate)*100}"
            if(interest_rate > 0.08):
                await slack_client.chat_postMessage(channel=CHANNEL_ID,
                                                text="leverage " + str(leverage) +
                                                     "\nspot price " + str(spot_ask_price) +
                                                     "\nfuture price " + str(future_bid_price) +
                                                     "\ndays till expiration " + str(time_diff) +
                                                     "\n" + text +
                                                     "\n-----------------------------------------")
            print(text)
            print("-----------------------------")


            #await slack_client.chat_postMessage(channel=CHANNEL_ID, text=text)
            # calc interest here
            numerator = (1 - 1 / leverage) * (future_ask_price - spot_bid_price)
            denominator = spot_bid_price
            coefficient = 365 / time_diff
            interest_rate = numerator / denominator * coefficient
            # calc interest here

            text = f"{futures_symb} @{notional_size} {quote_cur} interest rate: {(interest_rate) * 100}"
            if (interest_rate < 0.05):
                await slack_client.chat_postMessage(channel=CHANNEL_ID,
                                                    text="leverage " + str(leverage) +
                                                         "\nspot price " + str(spot_ask_price) +
                                                         "\nfuture price " + str(future_bid_price) +
                                                         "\ndays till expiration " + str(time_diff) +
                                                         "\n" + text +
                                                         "\n-----------------------------------------")
        await asyncio.sleep(900)

async def log_interest_rates_coinm(leverage:float, notional_size:float):
    while(True):
        str_a = "----------------------------------------------"
        str_b = "===============COIN-M FUTURES================="
        print(str_a)
        print(str_b)
        print(str_a)
        for futures_symb in global_vars.coinm_futures_symbol_to_bid_orderbook:
            #get price datas begin
            spot_eq = global_vars.futures_symbol_to_stock_symbol[futures_symb]
            if (global_vars.spot_symbol_to_ask_orderbook.get(spot_eq, -1) == -1):
                if(spot_eq.endswith("USD")):
                    spot_eq += "T"
                else:
                    continue

            base_cur, quote_cur = global_vars.spot_symbol_to_currencies[spot_eq]
            print(futures_symb)
            future_bid_price = (get_mean_price_at_volume
                                (global_vars.coinm_futures_symbol_to_bid_orderbook[futures_symb], notional_size))
            future_ask_price = (get_mean_price_at_volume
                                (global_vars.coinm_futures_symbol_to_ask_orderbook[futures_symb], notional_size))
            spot_ask_price = (get_mean_price_at_volume
                              (global_vars.spot_symbol_to_ask_orderbook[spot_eq], notional_size))
            spot_bid_price = (get_mean_price_at_volume
                              (global_vars.spot_symbol_to_bid_orderbook[spot_eq], notional_size))
            #get price datas end

            print("leverage", leverage)
            print("spot price", spot_ask_price)
            print("future price", future_bid_price)

            # calc time begin
            date_abbr = futures_symb.split("_")[1]
            year = int(date_abbr[:2]) + 2000
            month = int(date_abbr[2:4])
            day = int(date_abbr[4:])
            futuretime = datetime.datetime(year, month, day).timestamp()*1000
            now = datetime.datetime.now().timestamp()*1000
            time_diff = (futuretime - now)/86400000
            # calc time end

            print("end time", futuretime)
            print("time difference", time_diff)

            #calc interest begin
            numerator = (1-1/leverage)*(future_bid_price - spot_ask_price)
            denominator = spot_ask_price
            coefficient = 365 / time_diff
            interest_rate = numerator / denominator * coefficient
            #calc interest end

            print("numerator:", numerator)
            print("denominator:", denominator)
            print("coefficient:", coefficient)

            text = f"{futures_symb} @{notional_size} {quote_cur} interest rate: {(interest_rate) * 100}"
            if(interest_rate > 0.08):
                await slack_client.chat_postMessage(channel=CHANNEL_ID,
                                                text="leverage " + str(leverage) +
                                                     "\nspot price " + str(spot_ask_price) +
                                                     "\nfuture price " + str(future_bid_price)+
                                                     "\ndays till expiration " + str(time_diff)+
                                                     "\n"+text+
                                                    "\n-----------------------------------------")
            print(text)
            print("-----------------------------")

            # calc interest begin
            numerator = (1 - 1 / leverage) * (future_ask_price - spot_bid_price)
            denominator = spot_bid_price
            coefficient = 365 / time_diff
            interest_rate = numerator / denominator * coefficient
            # calc interest end

            text = f"{futures_symb} @{notional_size} {quote_cur} interest rate: {(interest_rate) * 100}"
            if (interest_rate < 0.05):
                await slack_client.chat_postMessage(channel=CHANNEL_ID,
                                                    text="leverage " + str(leverage) +
                                                         "\nspot price " + str(spot_ask_price) +
                                                         "\nfuture price " + str(future_bid_price) +
                                                         "\ndays till expiration " + str(time_diff) +
                                                         "\n" + text +
                                                         "\n-----------------------------------------")
            #await slack_client.chat_postMessage(channel=CHANNEL_ID, text=text)

        await asyncio.sleep(900)


def get_mean_price_at_volume(orderbook_data:list, total_notiolnal:float):
    print(orderbook_data)
    cum_price = 0
    cum_vol = 0
    for (price, volume) in orderbook_data:
        notional_at_level = price * volume
        if(cum_price + notional_at_level > total_notiolnal):
            cum_vol += (total_notiolnal - cum_price)/price
            cum_price = total_notiolnal
            break
        else:
            cum_price += notional_at_level
            cum_vol += volume
    avg_price = cum_price / cum_vol
    return avg_price