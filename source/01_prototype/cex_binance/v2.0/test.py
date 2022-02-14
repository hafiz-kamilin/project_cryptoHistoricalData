# SOURCE: https://stackoverflow.com/a/11402664

from dateutil.parser import parse
import time

def is_date(string, fuzzy=False):
    
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

print(is_date("1990-12-1"))
print(is_date("2005/3"))
print(is_date("Jan 19, 1990"))
print(is_date("today is 2019-03-27"))
print(is_date("today is 2019-03-27", fuzzy=True))
print(is_date("1 Jan, 2021"))

strToDate1 = parse('1 Jan, 2021')
strToDate2 = parse('Mon Jul 09 09:20:28 +0200 2012')
print(strToDate1)
print(strToDate2)

dateToTimeStamp1 = int(time.mktime(strToDate1.timetuple()))
dateToTimeStamp2 = int(time.mktime(strToDate2.timetuple()))
print(dateToTimeStamp1)
print(dateToTimeStamp2)