import datetime
from datetime import timedelta as td

import dateutil.parser


def gettodaystring():
    return datetime.datetime.today().isoformat()


# return datetime objects of the given range, end points included
def datesOfRange(fromdate, todate=gettodaystring()):
    fromdate, todate = map(parse, [fromdate, todate])
    delta = todate - fromdate
    retdays = []
    for numberofdays in range(delta.days + 1):
        retdays.append(fromdate + td(days=numberofdays))
    return retdays


def deltatohours(d):
    # print d.seconds
    return d.seconds / 3600.0


def parse(str):
    return dateutil.parser.parse(str)
