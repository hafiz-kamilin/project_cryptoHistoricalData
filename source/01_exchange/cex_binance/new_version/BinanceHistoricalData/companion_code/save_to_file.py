#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Mohd Hafizuddin Bin Kamilin"
__date__ = "7 March 2022"

# converting datetime in str into an object
from dateutil.parser import parse
# to get the current datetime
from datetime import datetime
# data processing and saving as feather
import pandas as pd
# data saving as pickle
import pickle
# timezone manipulation
import pytz
# data saving as csv
import csv
# to handle folder checking and creation
import os

def save_to_file(file_format: str, pair: str, start: str, end: str, interval: str, rearranged_klines: list) -> None:

    """
    save the downloaded klines from binance as csv/pickle/feather

    NOTE: feather have the highest compression and access time. csv option
            was added to make accessing the file outside python is easier. pickle
            option was added if feather is not usable on the host computer.
    
    """

    if (os.path.isfile("Downloaded Historical Data") is not True):

        os.mkdir("Downloaded Historical Data")

    # specify the column for the klines
    columns = [
        "open_time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_asset_volume",
        "number_of_trades",
        "taker_buy_base_asset_volume",
        "taker_buy_quote_asset_volume",
        "ignore"
    ]

    # convert the date time str to <class 'datetime.datetime'>
    start = parse(start).replace(tzinfo=pytz.UTC)
    end = parse(end).replace(tzinfo=pytz.UTC)
    # convert the datetime to timestamp (utc)
    start = int(datetime.timestamp(start))
    end = int(datetime.timestamp(end))

    if (file_format == "csv"):

        # write the column and klines as csv file
        with open(pair + "_" + interval + "_(" + str(start) + "-" + str(end) + ").csv", "w", newline="") as f:
            write = csv.writer(f)
            write.writerow(columns)
            write.writerows(rearranged_klines)

    elif (file_format == "pickle"):

        # as pickle
        # NOTE: reinsert the column as the first element in the list
        rearranged_klines.insert(0, columns)
        with open(pair + "_" + interval + "_(" + str(start) + "-" + str(end) + ").pickle", "wb") as handle:
            pickle.dump(rearranged_klines, handle, protocol=pickle.HIGHEST_PROTOCOL)

    elif (file_format == "feather"):

        # convert nested list into a dataframe
        df = pd.DataFrame(data=rearranged_klines, columns=columns)
        # write the dataframe as feather file
        df.to_feather(pair + "_" + interval + "_(" + str(start) + "-" + str(end) + ").feather", compression="zstd")
