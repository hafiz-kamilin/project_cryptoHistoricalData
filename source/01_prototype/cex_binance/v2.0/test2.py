from datetime import datetime
import pytz

tz = pytz.timezone('UTC')

timestamp = 1609459200000 / 1000 # 1609430400
dt_object = datetime.fromtimestamp(timestamp, tz)

print("dt_object =", str(dt_object)[:-6])
print("type(dt_object) =", type(dt_object))