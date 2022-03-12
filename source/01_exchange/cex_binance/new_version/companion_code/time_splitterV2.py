#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Mohd Hafizuddin Bin Kamilin"
__date__ = "7 March 2022"

# converting datetime in str into an object
from dateutil.parser import parse
# to get the current datetime
from datetime import datetime
# timezone manipulation
import pytz

def time_splitter(start: str, end: str) -> tuple[list[list[str]], list[list[str]]]:

    """
    slice the time according to the divisor and group as chuck 

    NOTE: we need to splice time duration specified by the user into month and
        group it as a chunk of 10 months, to prevent exceeding 1200 request
        weight allowed by binance; 10 months → 10 concurrent fetch call where
        each retrieve 1 month worth of data → 450-950 request weight
    
    """

    def list_segmenter(concurrent_limit: int, l: list) -> list[list[str]]:

        """
        divide the splitted time (splitted_start and splitted_end) into a
        nested list

        NOTE: the concurrent function to fetch the klines will read the nested
            list and fetch the klines based on the defined start/end time

        """
        
        processed = []

        # looping till length l
        for i in range(0, len(l), concurrent_limit):
            processed.append(l[i:i + concurrent_limit])

        return processed

    # to record the splitted time
    splitted_start = []
    splitted_end = []
    # initialize the time limit
    concurrent_limit = 0

    # 1 day     86,400 s  →  86,400 timestamp  →  86,400,000 binance's timestamp
    # 1 hour    3,600 s   →  3,600 timestamp   →  3,600,000 binance's timestamp
    # 1 minute  60 s      →  60 timestamp      →  60,000 binance's timestamp

    timestamp_in_1m = 60
    # NOTE: (timestamp for 1 minute) * 60 minutes * 24 hours * 7 days * 4 weeks * 10 months
    #       based on the previous finding, we can only fetch 1 month worth of data via 10 concurrent running fetch function.
    #       thus, we will only fetch max 10 months of data with 10~20 maximum of concurrent running fetch function
    divisor = timestamp_in_1m * 60 * 24 * 7 * 4 * 10

    # we specifically use UTC timezone to match with the binance API timezone
    tz = pytz.timezone("UTC")
    # convert the date time str to <class 'datetime.datetime'>
    start_time = parse(start).replace(tzinfo=pytz.UTC)
    time_duration = parse(end).replace(tzinfo=pytz.UTC)
    # convert the datetime to timestamp (utc)
    start_time = int(datetime.timestamp(start_time))
    time_duration = int(datetime.timestamp(time_duration) - start_time)

    # if the time_duration is more than 10 months
    if time_duration > divisor:

        # set 20 concurrent running fetch function
        concurrent_limit = 20
        # find out how many times we can divide the time duration with the divisor and its remainder
        quotient = int(time_duration / divisor)
        remainder = time_duration % divisor

        for i in range(quotient * concurrent_limit):

            # append the newly calculated start time to the splitted_start
            if i == 0:
                splitted_start.append(str(datetime.fromtimestamp(start_time, tz))[:-6])
            else:
                # NOTE: smallest klines interval is 1 minute
                splitted_start.append(str(datetime.fromtimestamp(start_time + timestamp_in_1m, tz))[:-6])

            # append the newly calculated end time to the splitted_end
            start_time += divisor / concurrent_limit
            splitted_end.append(str(datetime.fromtimestamp(start_time, tz))[:-6])

        # if there is a remainder from the division
        if remainder != 0:

            # append the newly calculated start time to the splitted_start
            splitted_start.append(str(datetime.fromtimestamp(start_time + timestamp_in_1m, tz))[:-6])

            # append the newly calculated end time to the splitted_end
            start_time += remainder
            splitted_end.append(str(datetime.fromtimestamp(start_time, tz))[:-6])

    # if the time_duration is equal or less than the divisor
    else:
        
        # no calculation needed
        splitted_start.append(start)
        splitted_end.append(end)

    # create a nested list of `self.concurrent_limit` months
    splitted_start = list_segmenter(concurrent_limit, splitted_start)
    splitted_end = list_segmenter(concurrent_limit, splitted_end)

    return splitted_start, splitted_end