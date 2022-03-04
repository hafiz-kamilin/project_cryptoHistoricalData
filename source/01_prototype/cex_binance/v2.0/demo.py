start = 0
end = 50

divisor = 7

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