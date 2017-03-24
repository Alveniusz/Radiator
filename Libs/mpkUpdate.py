from PySide.QtCore import Qt, QTime
from PySide.QtGui import *
import requests
from datetime import date
import os.path

MPK_CONFIGURATION = 'Config/mpkLineList.cfg'
MPK_LOGS = 'Timetables/logs.txt'

class MpkTime:
    def __init__(self, lineNum, stopHour, stopMin):
        self.line = lineNum
        self.hour = stopHour
        self.min = stopMin

    def minFromMidnight(self):
        return 60*self.hour + self.min

    def afterTime(self, qtime):
        return self.hour < qtime.hour() \
               or (self.hour == qtime.hour() and self.min < qtime.minute()) \
               or (self.hour == qtime.hour() and self.min == qtime.minute() and qtime.second() != 0 )

    def timeTo(self, qtime):
        min = 60 * (self.hour - qtime.hour()) + self.min - qtime.minute() - 1
        sec = 60 - qtime.second()

        if sec == 60:
            sec = 0
            min += 1

        if min < 0:
            if sec != 0:
                sec = -60 + sec
                min += 1
        return min, sec

    def __str__(self):
        return "{0:3d} - {1:2d}:{2:2d}".format(self.line, self.hour, self.min)


class MpkStopInfo:
    def __init__(self, line):
        pars = line.strip().split(None, 4)
        if len(pars) < 5:
            raise ValueError("Missing line info in config file: \n\t" + MPK_CONFIGURATION + "\n\t line: " + line)

        self.line = int(pars[0])
        self.direction = int(pars[1])
        self.stop = int(pars[2])
        if pars[3] == "T":
            self.state = True
        elif pars[3] == "F":
            self.state = False
        else:
            raise ValueError("Wrong line state in config file: \n\t" + MPK_CONFIGURATION + "\n\t line: " + line)
        self.destination = pars[4]

    def getFilePath(self):
        return "Timetables/line_{0}_{1}_{2}.txt".format(self.line, self.direction, self.stop)

    def getFileHead(self):
        return "LINE {0} - DIRECTION {1} - STOP {2}".format(self.line, self.direction, self.stop)

    def getURL(self):
        return "http://rozklady.mpk.krakow.pl/?linia={0}__{1}__{2}".format(self.line, self.direction, self.stop)

    @staticmethod
    def parseConfiguration():
        mpkStopsInfo = []
        with open(MPK_CONFIGURATION, encoding='utf-8') as f:
            for line in f:
                if line.startswith("#"):
                    continue
                else:
                    mpkStopsInfo.append(MpkStopInfo(line))

        return mpkStopsInfo

    def getTimetable(self):
        f = open(self.getFilePath(), 'r')
        f.readline()
        f.readline()

        timetable = []
        for l in f:
            t = l.split()
            timetable.append(MpkTime(self.line, int(t[0]), int(t[1])))

        return timetable



class MpkUpdate:
    def __init__(self):
        self.mpkStopsInfo = MpkStopInfo.parseConfiguration()
        if self.updatingNecesity():
            self.downloadData()



    def updatingNecesity(self):
        for mpkInfo in self.mpkStopsInfo:
            if not os.path.isfile(mpkInfo.getFilePath()):
                return True

        if not os.path.isfile(MPK_LOGS):
            return True

        with open(MPK_LOGS) as f:
            f.readline()
            dataLine = f.readline().strip().split("-")
            self.lastUpdate = date(int(dataLine[0]), int(dataLine[1]), int(dataLine[2]))

        return self.lastUpdate < date.today()

    def downloadData(self):
        for i in range(len(self.mpkStopsInfo)):
            print("\rDownload timetable {0}/{1}: ".format(i + 1, len(self.mpkStopsInfo)) + self.mpkStopsInfo[
                i].getFileHead() + " " * 20, end=" ")
            self.mpkParser(self.mpkStopsInfo[i])

        self.upadeDataInConfig()

    def upadeDataInConfig(self):
        f = open(MPK_LOGS, 'w')
        f.write('#Last update:\n')
        f.write(date.today().isoformat() + "\n")
        f.close()

    def mpkParser(self, mpkInfo):

        f = open(mpkInfo.getFilePath(), 'w')

        f.write("### " + mpkInfo.getFileHead() + "\n")
        f.write("### URL = " + mpkInfo.getURL() + "\n")

        page = requests.get(mpkInfo.getURL())
        hour = None
        for line in page.text.split("\n"):
            if line.count("white-space: nowrap;  border-bottom: dotted black 1px; padding-right: 10px;"):
                b = line.find(">") + 1
                e = line.find("<", b)

                if hour:
                    for min in line[b:e].strip().split(" "):
                        if min:
                            if not min.isdigit():
                                min = ''.join(c for c in min if c.isdigit())

                            f.write(hour + "\t" + min + "\n")
                    hour = None
                else:
                    hour = line[b:e].strip()

        f.close()

    def getMpkList(self):
        return self.mpkStopsInfo


class MpkUpdate_GUI(MpkUpdate):
    def __init__(self):
        super().__init__()

    def downloadData(self):
        progress = QProgressDialog("Update timetabless...", "Abort", 0, len(self.mpkStopsInfo))
        progress.setWindowModality(Qt.WindowModal)
        progress.setWindowTitle('Update timetabless...')
        progress.setMinimumDuration(0)
        progress.forceShow()

        for i in range(len(self.mpkStopsInfo)):
            if progress.wasCanceled():
                return
            progress.setLabelText("Download timetable {0} ({1}/{2})".format(self.mpkStopsInfo[i].line, i+1, len(self.mpkStopsInfo)))
            progress.setValue(i)
            self.mpkParser(self.mpkStopsInfo[i])

        self.upadeDataInConfig()