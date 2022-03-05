class Demo:

    def __init__(self):

        self.concurrent_limit = 10
        self.divisor = 7
        self.start = 0
        self.end = 100
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

        time_duration = self.end - self.start

        # if the time_duration is larger than the divisor
        if time_duration > self.divisor:

            # find out how many times we can divide the time duration with the divisor and its remainder
            quotient = int(time_duration / self.divisor)
            remainder = time_duration % self.divisor

            for i in range(quotient):

                # append the newly calculated start time to the splitted_start
                if i == 0:
                    splitted_start.append(self.start)
                else:
                    splitted_start.append(self.start + self.timestamp_in_1m)

                # append the newly calculated end time to the splitted_end
                self.start += self.divisor
                splitted_end.append(self.start)

                print(str(splitted_start[i]) + " - " + str(splitted_end[i]))

            # if there is a remainder from the division
            if remainder != 0:

                # append the newly calculated start time to the splitted_start
                splitted_start.append(self.start + self.timestamp_in_1m)

                # append the newly calculated end time to the splitted_end
                self.start += remainder
                splitted_end.append(self.start)

                print(str(splitted_start[-1]) + " - " + str(splitted_end[-1]))

        # if the time_duration is equal or less than the divisor
        else:
            
            # no calculation needed
            splitted_start.append(self.start)
            splitted_end.append(self.end)

        splitted_start = list(divide_chunks(splitted_start))
        splitted_end = list(divide_chunks(splitted_end))

        return splitted_start, splitted_end

demo = Demo()
_ = demo.time_splitter()
  
