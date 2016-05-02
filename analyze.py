import copy
import csv
import datetime
from datetime import timedelta as td

import utils

reportname = "newreport.csv"


# todo 1: switch on/off tracked or untracked time mode
# todo 2: pie chart


def firstolastActivities():
    """returns first and last activities in a list"""
    ret = []
    for first in [True, False]:
        with open(reportname, 'rb') as cfile:
            report = csv.reader(cfile)
            counter = 0
            pivot = 0
            for row in report:
                if counter == 0:
                    pivot = row[2]
                    counter += 1
                else:
                    if first:
                        if row[2] < pivot: pivot = row[2]
                    else:
                        if row[3] > pivot: pivot = row[3]
            if pivot:
                print "add"
                ret.append(ret.append(pivot))
    return [ret[0], ret[2]]


def getActivities(fromdate, todate=utils.gettodaystring()):
    """get activities between two given date/time, given in string"""
    fromdate, todate = map(utils.parse, [fromdate, todate])
    # print fromdate, todate
    with open(reportname, 'rb') as file:
        report = csv.reader(file)
        pivot = 0
        ret = []
        for row in report:
            mrow = map(utils.parse, row[2:4])
            if mrow[0] < fromdate < mrow[1]:
                a1, a2 = cutActivity(row)
                ret.append(a2)
            elif mrow[0] > fromdate and mrow[1] < todate:
                ret.append(row)
            elif mrow[0] < todate < mrow[1]:
                a1, a2 = cutActivity(row)
                ret.append(a1)
        return ret


def getDayActivity(fromdate=utils.gettodaystring()):
    fromdate = utils.parse(fromdate).date()
    return getActivities(fromdate.isoformat(), (fromdate + td(days=1)).isoformat())


def getWeekActivity(fromdate=(datetime.datetime.today()).date().isoformat()):
    # first get this monday
    # if after or equal to this monday, this week
    # otherwise, previous weeks
    fromdate = utils.parse(fromdate)
    today = datetime.datetime.today()
    d1 = today.day - today.weekday()
    thismonday = datetime.datetime.today().replace(day=d1)
    if fromdate > thismonday:
        return getActivities(thismonday.date().isoformat(), fromdate.isoformat())
    else:
        thatmonday = (fromdate - td(days=(fromdate.weekday())))
        return getActivities(thatmonday.date().isoformat(), (thatmonday + td(days=7)).date().isoformat())


# this is assuming that no activity goes across three days
def cutActivity(row):
    fromdate = utils.parse(row[2])
    todate = utils.parse(row[3])
    # print fromdate, todate
    if (todate.date() - fromdate.date()).days != 1:
        print "error cutting activity: wrong date range"
        return [0, 0]
    else:
        middate = copy.deepcopy(todate).replace(hour=0, minute=0, second=0)
        firsthalf = [row[0], utils.deltatohours(middate - fromdate), fromdate.isoformat(' '), middate.isoformat(' ')]
        secondhalf = [row[0], utils.deltatohours(todate - middate), middate.isoformat(' '), todate.isoformat(' ')]
        # print firsthalf, secondhalf
        return [firsthalf, secondhalf]


def trackedCheck(fromdate, todate=utils.gettodaystring()):
    fromdate, todate = map(utils.parse, [fromdate, todate])
    # want to include the end dates
    nd = (todate - fromdate).days + 1
    time = sumTime(getActivities(fromdate.isoformat(), todate.isoformat()))
    return nd, time, time / (24.0 * nd)


def sumTime(acts):
    time = 0.0
    for activity in acts:
        time += float(activity[1]) * 1.0
    return time


def piechart():
    pass


def getActivitiesByType(acts):
    """Returns activities grouped by type in a dictionary"""
    retdict = {}
    for activity in acts:
        if activity[0] in retdict.keys():
            retdict[activity[0]].append(activity)
        else:
            retdict[activity[0]] = [activity]
    return retdict


def getTimeByType(acts):
    """Returns summed time grouped by activities in a dictionary"""
    actsbytype = getActivitiesByType(acts)
    return {k: sumTime(v) for k, v in actsbytype.items()}


if __name__ == '__main__':
    # print trackedCheck("3/22")
    print getTimeByType(getActivities("3/22")).items()
