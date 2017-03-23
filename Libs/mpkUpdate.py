from PySide.QtCore import Qt
from PySide.QtGui import *
import requests
from datetime import date
import os.path

MPK_CONFIGURATION = 'Config/mpkLineList.cfg'
MPK_LOGS = 'Timetables/logs.txt'

class MpkStopInfo:
    def __init__(self, line):
        pars = line.strip().split(None, 3)
        if len(pars) < 4:
            raise ValueError("Missing line info in config file: \n\t" + MPK_CONFIGURATION + "\n\t line: " + line)

        self.line = int(pars[0])
        self.direction = int(pars[1])
        self.stop = int(pars[2])
        self.destination = pars[3]

    def getFilePath(self):
        return "Timetables/line_{0}_{1}_{2}.txt".format(self.line, self.direction, self.stop)

    def getFileHead(self):
        return "LINE {0} - DIRECTION {1} - STOP {2}".format(self.line, self.direction, self.stop)

    def getURL(self):
        return "http://rozklady.mpk.krakow.pl/?linia={0}__{1}__{2}".format(self.line, self.direction, self.stop)


class MpkUpdate:
    def __init__(self):
        self.parseConfiguration()
        if self.updatingNecesity():
            self.downloadData()

    def parseConfiguration(self):
        self.mpkStopsInfo = []
        with open(MPK_CONFIGURATION, encoding='utf-8') as f:
            for line in f:
                if line.startswith("#"):
                    continue
                else:
                    self.mpkStopsInfo.append(MpkStopInfo(line))

    def updatingNecesity(self):
        with open(MPK_LOGS) as f:
            f.readline()
            dataLine = f.readline().strip().split("-")
            self.lastUpdate = date(int(dataLine[0]), int(dataLine[1]), int(dataLine[2]))

        for mpkInfo in self.mpkStopsInfo:
            if not os.path.isfile(mpkInfo.getFilePath()):
                return True
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

        filePath = mpkInfo.getFilePath()
        f = open(filePath, 'w')

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