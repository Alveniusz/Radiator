from PySide.QtGui import *
from PySide.QtCore import *

from Widgets.ClockW import ClockW
from Widgets.LineHeader import LineHeader
from Widgets.MpkLine import MpkBigLine

from Libs.mpkUpdate import MpkStopInfo, MpkTime


NUM_OF_MPK_LINE_WIDGETS = 8

class MpkListener(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.start = 0

        self.addMpkInfo()

        self.initWidgets()
        self.setWidgetsLayout()

        self.fillBigMpkFrames()

        self.initTimer()
        self.updateTime()

    def addMpkInfo(self):
        self.mpkInfoList = MpkStopInfo.parseConfiguration()
        self.mpkTimetable = []
        for mpk in self.mpkInfoList:
            for t in mpk.getTimetable():
                self.mpkTimetable.append(t)

        self.mpkTimetable.sort(key=MpkTime.minFromMidnight)

    def initWidgets(self):
        self.clockW = ClockW(self)
        self.initLineHeaders()
        self.initBigMpkFrames()

    def setWidgetsLayout(self):
        mainVerticalLayout = QVBoxLayout()
        mainVerticalLayout.setAlignment(Qt.AlignTop)

        mainVerticalLayout.addWidget(self.clockW, 1)
        mainVerticalLayout.addLayout(self.linesHeaderLayout, 1)
        mainVerticalLayout.addWidget(self.bigMpkFrames, NUM_OF_MPK_LINE_WIDGETS)

        self.setLayout(mainVerticalLayout)

    def initLineHeaders(self):
        self.linesHeaderLayout = QHBoxLayout()
        self.lineHeaders = []
        for mpk in self.mpkInfoList:
            header = LineHeader(self, mpk.line, mpk.destination, mpk.state)
            self.connect(header, SIGNAL('clicked()'), self.fillBigMpkFrames)
            self.lineHeaders.append( header )
            self.linesHeaderLayout.addWidget( header )

    def initBigMpkFrames(self):
        hLayout = QVBoxLayout()

        self.bigMpkFrames = QFrame(self)
        self.bigMpkFrames.setFrameStyle(QFrame.Box)
        self.headerLines = QLabel("Departures")
        self.headerLines.setAlignment(Qt.AlignCenter)
        self.headerLines.setFont(QFont("Arial", 27, QFont.Bold))
        pallete = QPalette()
        pallete.setColor(QPalette.Foreground, Qt.black)
        self.headerLines.setPalette(pallete)
        hLayout.addWidget(self.headerLines,1)

        self.bigMpkLines = []

        for i in range(NUM_OF_MPK_LINE_WIDGETS):
            bl = MpkBigLine(self)
            self.bigMpkLines.append(bl)
            hLayout.addWidget(bl,2)

        self.bigMpkFrames.setLayout(hLayout)


    def fillBigMpkFrames(self):
        qtime = QTime.currentTime()
        curInd = self.getCurentTimeIndex(qtime)
        acceptedTimes = 0
        maxInd = min(NUM_OF_MPK_LINE_WIDGETS, len(self.mpkTimetable) - curInd)
        while acceptedTimes < NUM_OF_MPK_LINE_WIDGETS:
            while curInd < len(self.mpkTimetable) and not self.getLineState(self.mpkTimetable[curInd].line):
                curInd += 1
            if curInd >= len(self.mpkTimetable):
                break

            mpkTime = self.mpkTimetable[curInd]
            self.bigMpkLines[acceptedTimes].fillLabels(mpkTime, self.getLineDestinationByLineNumber(mpkTime.line), qtime)
            acceptedTimes += 1
            curInd += 1

        for i in range(acceptedTimes, NUM_OF_MPK_LINE_WIDGETS):
            self.bigMpkLines[i].fillLabels(None)

    def initTimer(self):
        timer = QTimer(self)
        self.connect(timer, SIGNAL('timeout()'), self.updateTime)
        timer.start(1000)

    def updateTime(self):
        self.start += 1

        qtime = QTime.currentTime()
        self.clockW.update_time(qtime)

        if len(self.bigMpkLines):
            for bl in self.bigMpkLines:
                bl.updateTime(qtime)

            if self.bigMpkLines[0].afterDelayTime(qtime):
                self.fillBigMpkFrames()

        if qtime.hour() == 0 and qtime.minute() == 0:
            self.fillBigMpkFrames()

    def getCurentTimeIndex(self, qtime):
        qtime = QTime.currentTime()
        ind = 0
        while ind < (len(self.mpkTimetable)):
            if not self.mpkTimetable[ind].afterTime(qtime):
                return ind
            ind += 1

        return ind

    def getLineDestinationByLineNumber(self, line):
        for mpk in self.mpkInfoList:
            if mpk.line == line:
                return mpk.destination

        raise ValueError

    def getLineState(self, line):
        for head in self.lineHeaders:
            if head.line == line:
                return head.state