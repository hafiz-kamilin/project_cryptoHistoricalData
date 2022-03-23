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

def time_splitter(start: str, end: str, interval_value: int, duration_limit: int, concurrent_limit: int) -> tuple[list[list[str]], list[list[str]]]:

    """
    slice the time according to the duration_limit and group as chuck 

    NOTE: we need to splice time duration specified by the user into month and
        group it as a chunk of 10 months, to prevent exceeding 1200 request
        weight allowed by binance; 10 months → 10 concurrent fetch call where
        each retrieve 1 month worth of data → 450-950 request weight
    
    """

    def list_segmenter(concurrent_limit: int, l: list) -> list[list]:

        """
        divide the splitted time (splitted_start and splitted_end) into a
        nested list, where each of the nested list has int(concurrent_limit) length

        """
        
        processed = []

        # looping till length l
        for i in range(0, len(l), concurrent_limit):
            processed.append(l[i:i + concurrent_limit])

        return processed

    # to record the splitted time
    splitted_start = []
    splitted_end = []

    timestamp_in_1m = 60

    # we specifically use UTC timezone to match with the binance API timezone
    tz = pytz.timezone("UTC")
    # convert the date time str to <class 'datetime.datetime'>
    start_time = parse(start).replace(tzinfo=pytz.UTC)
    time_duration = parse(end).replace(tzinfo=pytz.UTC)
    # convert the datetime to timestamp (utc)
    start_time = int(datetime.timestamp(start_time))
    time_duration = int(datetime.timestamp(time_duration) - start_time)

    # if the time_duration is more than duration_limit and more than the (interval_value * concurrent_limit)
    if (time_duration > duration_limit) and (time_duration > interval_value * concurrent_limit):

        # find out how many times we can divide the time_duration with the duration_limit and its remainder
        quotient = int(time_duration / duration_limit)
        remainder = time_duration % duration_limit

        for i in range(quotient * concurrent_limit):

            # append the newly calculated start time to the splitted_start
            if i == 0:
                splitted_start.append(str(datetime.fromtimestamp(start_time, tz))[:-6])
            else:
                # NOTE: smallest klines interval is 1 minute
                splitted_start.append(str(datetime.fromtimestamp(start_time + timestamp_in_1m, tz))[:-6])

            # append the newly calculated end time to the splitted_end
            start_time += duration_limit / concurrent_limit
            splitted_end.append(str(datetime.fromtimestamp(start_time, tz))[:-6])

        # if there is a remainder from the division
        if remainder != 0:

            # append the newly calculated start time to the splitted_start
            splitted_start.append(str(datetime.fromtimestamp(start_time + timestamp_in_1m, tz))[:-6])

            # append the newly calculated end time to the splitted_end
            start_time += remainder
            splitted_end.append(str(datetime.fromtimestamp(start_time, tz))[:-6])

        # create a nested list of `self.concurrent_limit` months
        splitted_start = list_segmenter(concurrent_limit, splitted_start)
        splitted_end = list_segmenter(concurrent_limit, splitted_end)

    # else if the time_duration is more more than the (interval_value * concurrent_limit)
    elif (time_duration > interval_value * concurrent_limit):

        # find out how many times we can divide the time_duration with the concurrent_limit and its remainder
        remainder = time_duration % concurrent_limit
        quotient = int(time_duration / concurrent_limit)
        number_of_loop = (concurrent_limit if (remainder == 0) else (concurrent_limit - 1))
        
        for i in range(number_of_loop):

            # append the newly calculated start time to the splitted_start
            if i == 0:
                splitted_start.append(str(datetime.fromtimestamp(start_time, tz))[:-6])
            else:
                # NOTE: smallest klines interval is 1 minute
                splitted_start.append(str(datetime.fromtimestamp(start_time + timestamp_in_1m, tz))[:-6])

            # append the newly calculated end time to the splitted_end
            start_time += quotient
            splitted_end.append(str(datetime.fromtimestamp(start_time, tz))[:-6])

        # if there is a remainder from the division
        if remainder != 0:

            # append the newly calculated start time to the splitted_start
            splitted_start.append(str(datetime.fromtimestamp(start_time + timestamp_in_1m, tz))[:-6])

            # append the newly calculated end time to the splitted_end
            start_time += remainder
            splitted_end.append(str(datetime.fromtimestamp(start_time, tz))[:-6])

        # create a nested list
        splitted_start = [splitted_start]
        splitted_end = [splitted_end]

    else:
        
        # no calculation needed
        splitted_start = [[start]]
        splitted_end = [[end]]

    return splitted_start, splitted_end