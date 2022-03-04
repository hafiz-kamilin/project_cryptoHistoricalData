start = 0
end = 100

divisor = 7

concurrent_limit = 10

quotient = int(end / divisor)
remainder = end % divisor

divided_start = []
divided_end = []

if quotient != 0:

    for i in range(quotient):

        if i == 0:
            divided_start.append(start)
        else:
            divided_start.append(start + 1)

        start += divisor
        divided_end.append(start)

        print(str(divided_start[i]) + " - " + str(divided_end[i]))

    if remainder != 0:

        divided_start.append(start + 1)

        start += remainder
        divided_end.append(start)

        print(str(divided_start[-1]) + " - " + str(divided_end[-1]))

else:

    divided_start.append(start)

    start += remainder
    divided_end.append(start)
    print(str(divided_start[0]) + " - " + str(divided_end[0]))




# source: https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
def divide_chunks(l, n):
      
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]
  
# How many elements each
# list should have
n = 5
  
x = list(divide_chunks(divided_start, n))
print (x)