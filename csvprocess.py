import csv
from datetime import timedelta as td

import utils


# todo 1: aggregate arbitrary number of files
# todo 2: automation of picking start and to date/time
# todo 3: generate new report instead of writing into any specific one
# todo 4: get rid of repeated entries
# TODO: get rid of the last comma in original lines: o/w incompatible lengths

# range format: ex: 3/20/2000.  actually anything parsable by dateutil would be fine
def collectSleepActivityWithinRange(fromdate, to=utils.gettodaystring()):
    # should convert the result to the format of target file
    # example data: ['2016-03-23 02:01:09', '2016-03-23 09:22:06', '86%', '7:20', '', '', '', '13335'] len=8
    to = utils.parse(to)
    fromdate = utils.parse(fromdate)
    # usually don't sleep past 12pm?
    # try to capture an entire day's sleep
    fromdate = fromdate.replace(hour=12)
    with open("sleepdata.csv", 'rb') as cfile:
        sleepdata = csv.reader(cfile, delimiter=';')
        data1 = []
        counter = 0
        for row in sleepdata:
            if counter == 0:
                counter += 1
            else:
                # structure: (from,to)
                sleepfrom = utils.parse(row[0])
                sleepto = utils.parse(row[1])
                if fromdate < sleepfrom and to > sleepto:
                    data1.append((sleepfrom, sleepto))
                # examplerow = row
                counter += 1
        # print examplerow[0]
        # print type(utils.parse(examplerow[0]))
        return data1


def convertReportTimeFormat():
    # example data: ['Classwork', '0.6', 'Mar 21 08:12 pm', 'Mar 21 08:46 pm', ''] len = 5
    filename = 'report.csv'
    writename = "newreport.csv"
    with open(filename, 'rb') as cfile:
        with open(writename, 'wb') as writefile:
            writer = csv.writer(writefile, delimiter=',')
            report = csv.reader(cfile)
            counter = 0
            for row in report:
                if counter == 0:
                    counter += 1
                elif len(row) == 5:
                    row = row[0:4]
                    # get rid of zero time activities
                    if row[1] == '0':
                        pass
                    else:
                        row[2:4] = map(quickfn, row[2:4])
                        writer.writerow(row)
                        # else:
                        #    writer.writerow(row)


def quickfn(str):
    return utils.parse(str).isoformat(' ')


def putSleepsToReport():
    sdata = collectSleepActivityWithinRange("3/20/2016")
    writename = "newreport.csv"
    with open(writename, 'ab') as writefile:
        writer = csv.writer(writefile, delimiter=',')
        for row in sdata:
            writer.writerow(
                ["Sleep", utils.deltatohours(row[1] - row[0]), row[0].isoformat(' '), row[1].isoformat(' ')])


def addClasses(fromdate, schd="MWF, 12,1;TTH,9.35,2.35", todate=utils.gettodaystring()):
    schd = schd.split(';')
    schd = map(quick1, schd)
    # data now: [['MWF', ' 12', '1'], ['TTH', '9.35', '2.35']]
    # print schd
    rows = []
    for theday in utils.datesOfRange(fromdate, todate):
        if theday.isoweekday() in [1, 3, 5]:
            for i in range(1, len(schd[0])):
                classstart = theday.replace(hour=int(schd[0][i]), minute=10)
                rows.append(["Class", utils.deltatohours(td(minutes=50)), classstart.isoformat(' '),
                             (classstart + td(minutes=50)).isoformat(' ')])
                rows.append(
                    ["Transportation", utils.deltatohours(td(minutes=10)), (classstart + td(minutes=50)).isoformat(' '),
                     (classstart + td(minutes=60)).isoformat(' ')])
                if i == 1: rows.append(
                    ["Transportation", utils.deltatohours(td(minutes=10)),
                     (classstart + td(minutes=-10)).isoformat(' '),
                     classstart.isoformat(' ')])
        elif theday.isoweekday() in [2, 4]:
            for i in range(1, len(schd[1])):
                ct = schd[1][i].split('.')
                ct = map(int, ct)
                classstart = theday.replace(hour=ct[0], minute=ct[1])
                rows.append(["Class", utils.deltatohours(td(minutes=75)), classstart.isoformat(' '),
                             (classstart + td(minutes=75)).isoformat(' ')])
                rows.append(
                    ["Transportation", utils.deltatohours(td(minutes=10)), (classstart + td(minutes=75)).isoformat(' '),
                     (classstart + td(minutes=85)).isoformat(' ')])
                if i == 1: rows.append(
                    ["Transportation", utils.deltatohours(td(minutes=10)),
                     (classstart + td(minutes=-10)).isoformat(' '),
                     classstart.isoformat(' ')])
    writename = "newreport.csv"
    with open(writename, 'ab') as writefile:
        writer = csv.writer(writefile, delimiter=',')
        writer.writerows(rows)


def quick1(str):
    return str.split(',')


if __name__ == '__main__':
    convertReportTimeFormat()
    putSleepsToReport()
    addClasses("3/21/2016")
