import requests
from datetime import date
import os.path

MPK_CONFIGURATION = 'Config/mpkLineList.cfg'


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
            f.readline()
            dataLine = f.readline().strip().split("-")
            self.lastUpdate = date(int(dataLine[0]), int(dataLine[1]), int(dataLine[2]))

            for line in f:
                if line.startswith("#"):
                    continue
                else:
                    self.mpkStopsInfo.append(MpkStopInfo(line))

    def updatingNecesity(self):
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
        f = open(MPK_CONFIGURATION, 'r')
        s = f.readlines();
        f.close()
        s[1] = date.today().isoformat() + "\n"
        f = open(MPK_CONFIGURATION, 'w')
        f.write(''.join(s))
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
