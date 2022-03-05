class Demo:

    def __init__(self):

        self.concurrent_limit = 10
        self.divisor = 7
        self.start = 0
        self.end = 100

    def time_splitter(self):

        """
        slice the time according to the divisor and group it as chuck 
        
        """

        def divide_chunks(l):

            """
            divide the splitted time (splitted_start and splitted_end) into a
            nested list; the concurrent function to fetch the klines will read
            the nested list and fetch the klines based on the defined start/end
            time

            """
            
            # looping till length l
            for i in range(0, len(l), self.concurrent_limit): 
                yield l[i:i + self.concurrent_limit]

        quotient = int(self.end / self.divisor)
        remainder = self.end % self.divisor

        splitted_start = []
        splitted_end = []

        if quotient != 0:

            for i in range(quotient):

                if i == 0:
                    splitted_start.append(self.start)
                else:
                    splitted_start.append(self.start + 1)

                self.start += self.divisor
                splitted_end.append(self.start)

                print(str(splitted_start[i]) + " - " + str(splitted_end[i]))

            if remainder != 0:

                splitted_start.append(self.start + 1)

                self.start += remainder
                splitted_end.append(self.start)

                print(str(splitted_start[-1]) + " - " + str(splitted_end[-1]))

        else:

            splitted_start.append(start)

            start += remainder
            splitted_end.append(start)
            print(str(splitted_start[0]) + " - " + str(splitted_end[0]))

        splitted_start = list(divide_chunks(splitted_start))
        splitted_end = list(divide_chunks(splitted_end))

        print(splitted_start)
        print(splitted_end)

demo = Demo()
_ = demo.time_splitter()
  
