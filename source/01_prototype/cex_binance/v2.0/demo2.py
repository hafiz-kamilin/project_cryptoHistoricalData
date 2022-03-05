from dateutil.parser import parse
from dateutil.tz import gettz
from datetime import datetime
import pytz
import time

class Demo:

    def __init__(self):

        self.concurrent_limit = 10
        self.divisor = 3600000
        self.start = "2022-1-1 00:00:00"
        self.end = "2022-1-2 00:00:00"
        self.timestamp_in_1m = 1

    def time_splitter(self):

        """
        slice the time according to the divisor and group as chuck 
        NOTE: we need to splice time duration specified by the user into month and
              group it as a chunk of 10 months, to prevent exceeding 1200 request
              weight allowed by binance; 10 months → 10 concurrent fetch call where
              each retrieve 1 month worth of data → 450-950 request weight
        
        """

        def divide_chunks(l):

            """
            divide the splitted time (splitted_start and splitted_end) into a
            nested list
            NOTE: the concurrent function to fetch the klines will read the nested
                  list and fetch the klines based on the defined start/end time

            """
            
            # looping till length l
            for i in range(0, len(l), self.concurrent_limit): 
                yield l[i:i + self.concurrent_limit]

        splitted_start = []
        splitted_end = []

        # 1 day     86,400 s  →  86,400 ts  →  86,400,000 binance timestamp
        # 1 hour    3,600 s   →  3,600 ts   →  3,600,000 binance timestamp
        # 1 minute  60 s      →  60 ts      →  60,000 binance timestamp

        # we only use UTC timezone to match with the binance API timezone
        tz = pytz.timezone('UTC')
        # convert the date time str to <class 'datetime.datetime'>
        calculated_time = parse(self.start).replace(tzinfo=pytz.UTC)
        time_duration = parse(self.end).replace(tzinfo=pytz.UTC)
        # convert the datetime to timestamp (utc)
        calculated_time = int(datetime.timestamp(calculated_time))
        time_duration = int(datetime.timestamp(time_duration) - calculated_time)

        # if the time_duration is larger than the divisor
        if time_duration > self.divisor:

            # find out how many times we can divide the time duration with the divisor and its remainder
            quotient = int(time_duration / self.divisor)
            remainder = time_duration % self.divisor

            for i in range(quotient):

                # append the newly calculated start time to the splitted_start
                # NOTE: after converting timestamp to datetime, remove the offset time (+00:00) with slice [:-6]
                if i == 0:
                    splitted_start.append(str(datetime.fromtimestamp(calculated_time / 100, tz))[:-6])
                else:
                    splitted_start.append(str(datetime.fromtimestamp((calculated_time + self.timestamp_in_1m) / 100, tz))[:-6])

                # append the newly calculated end time to the splitted_end
                calculated_time += self.divisor
                splitted_end.append(str(datetime.fromtimestamp(calculated_time / 100, tz))[:-6])

                print(str(splitted_start[-1]) + " - " + str(splitted_end[-1]))

            # if there is a remainder from the division
            if remainder != 0:

                # append the newly calculated start time to the splitted_start
                splitted_start.append(str(datetime.fromtimestamp((calculated_time + self.timestamp_in_1m) / 100, tz))[:-6])

                # append the newly calculated end time to the splitted_end
                calculated_time += remainder
                splitted_end.append(str(datetime.fromtimestamp(calculated_time / 100, tz))[:-6])

                print(str(splitted_start[-1]) + " - " + str(splitted_end[-1]))

        # if the time_duration is equal or less than the divisor
        else:
            
            # no calculation needed
            splitted_start.append(calculated_time)
            splitted_end.append(self.end)

        splitted_start = list(divide_chunks(splitted_start))
        splitted_end = list(divide_chunks(splitted_end))

        print(splitted_start)
        print(splitted_end)
        return splitted_start, splitted_end

demo = Demo()
_ = demo.time_splitter()
  
