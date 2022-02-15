from dateutil.parser import parse
from datetime import datetime
import time

from numpy import divide

# 1 day 86,400,000
# 1 minute 60,000

parsedStartDateTime = parse('1 Jan, 2021')
parsedEndDateTime = parse('1 Jan, 2022')

startTimeStamp = int(time.mktime(parsedStartDateTime.timetuple()))
endTimeStamp = int(time.mktime(parsedEndDateTime.timetuple()))

timeStampDifference = endTimeStamp - startTimeStamp

dividedTimeStamp = timeStampDifference / 12

timeStampList = []
for i in range(12 + 1):

    timeStampList.append(
        datetime.fromtimestamp(int(startTimeStamp + dividedTimeStamp * i))
    )

print(timeStampList) 