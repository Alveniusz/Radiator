from PySide.QtGui import *
from PySide.QtCore import *

from Widgets.ClockW import ClockW
from Widgets.LineHeader import LineHeader

from Libs.mpkUpdate import MpkStopInfo

class MpkListener(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.addMpkInfo()

        self.initWidgets()
        self.setWidgetsLayout()

        self.initTimer()
        self.updateTime()

    def addMpkInfo(self):
        self.mpkInfoList = []
        self.mpkInfoList.append( MpkStopInfo("11  2   24   Mały Płaszów"))
        self.mpkInfoList.append( MpkStopInfo("23  1   2   Nowy Bieżanów"))
        self.mpkInfoList.append( MpkStopInfo("18  1   2   Krowodrza Górka"))
        self.mpkInfoList.append( MpkStopInfo("52  1   2   Osiedle Piastów"))
        self.mpkInfoList.append( MpkStopInfo("194 1   3   Krowodrza Górka"))


    def initWidgets(self):
        self.clockW = ClockW(self)
        self.initLineHeaders()


    def setWidgetsLayout(self):
        mainVerticalLayout = QVBoxLayout()
        mainVerticalLayout.setAlignment(Qt.AlignTop)

        mainVerticalLayout.addWidget(self.clockW, 1)
        mainVerticalLayout.addLayout(self.linesHeaderLayout, 1)
        mainVerticalLayout.addStretch(8)

        self.setLayout(mainVerticalLayout)


    def initLineHeaders(self):
        self.linesHeaderLayout = QHBoxLayout()
        self.lineHeaders = []
        for mpk in self.mpkInfoList:
            header = LineHeader(self, mpk.line, mpk.destination)
            self.lineHeaders.append( header )
            self.linesHeaderLayout.addWidget( header )


    def initTimer(self):
        timer = QTimer(self)
        self.connect(timer, SIGNAL('timeout()'), self.updateTime)
        timer.start(1000)

    def updateTime(self):
        qtime = QTime.currentTime()
        self.clockW.update_time(qtime)
