import requests
import pandas as pd
from datetime import datetime

# Define the base URL for the Binance API
BASE_URL = "https://api.binance.com/api/v3/klines"


def get_historical_data(symbol, interval, start_str, end_str):
    """
    Fetch historical Kline data from Binance API.

    :param symbol: Trading pair symbol (e.g., 'BTCUSDT')
    :param interval: Kline interval (e.g., '1d', '1h', '15m')
    :param start_str: Start time in string format (e.g., '1 Jan, 2020')
    :param end_str: End time in string format (e.g., '1 Jan, 2021')
    :return: DataFrame with historical data
    """
    dataframes = []
    # Convert start and end times to milliseconds
    start_time = int(datetime.strptime(start_str, "%d %b %Y").timestamp() * 1000)
    end_time = int(datetime.strptime(end_str, "%d %b %Y").timestamp() * 1000)
    print(start_time)
    print(end_time)
    current_end_time = 0
    if(interval.endswith("m")):
        increase_amount = int(interval[:-1])*60*1000
    elif(interval.endswith("h")):
        increase_amount = int(interval[:-1])*60*60*1000
    elif(interval.endswith("d")):
        increase_amount = int(interval[:-1])*24*60*60*1000
    elif(interval.endswith("w")):
        increase_amount = int(interval[:-1])*7*24*60*60*1000
    elif(interval.endswith("M")):
        increase_amount = int(interval[:-1])*30*7*24*60*60*1000
    else:
        print("invalid interval")
        raise Exception
    while(True):
        current_end_time = start_time + increase_amount * 900
        if(current_end_time > end_time):
            break

        # Define the parameters for the API request
        params = {
            'symbol': symbol,
            'interval': interval,
            'startTime': start_time,
            'endTime': current_end_time,
            "limit": 1000
        }

        # Send the GET request to the Binance API
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        start_time = current_end_time + increase_amount

        for elem in data:
            print(elem)
        print(data)

        # Process the response data
        df = pd.DataFrame(data, columns=[
            'Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time',
            'Quote asset volume', 'Number of trades', 'Taker buy base asset volume',
            'Taker buy quote asset volume', 'Ignore'
        ])
        # Convert timestamp columns to datetime
        df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
        df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')

        dataframes.append(df)


    return dataframes


if __name__ == '__main__':
    # Example usage
    symbol = 'BTCUSDT_240628'
    interval = '1h'
    start_str = '1 Apr 2024'
    end_str = '1 May 2024'

    df = get_historical_data(symbol, interval, start_str, end_str)
    print(df)