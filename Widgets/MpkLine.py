from PySide.QtGui import *
from PySide.QtCore import *

from Libs.mpkUpdate import MpkTime

class MpkBigLine(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.mpkTime = None
        self.destination = ""

        self.setFrameOptions()

        self.initLabels()
        self.fillLabels(None)

    def initLabels(self):
        horLayout = QHBoxLayout()

        self.lineLabel = QLabel()
        self.colorlLineLabel()
        horLayout.addWidget(self.lineLabel, 4)

        self.destinationLabel = QLabel()
        self.colorDestinationLabel()
        horLayout.addWidget(self.destinationLabel, 12)

        self.timeToLabel = QLabel()
        self.colorTimeToLabel()
        horLayout.addWidget(self.timeToLabel, 7)

        self.timetableLabel = QLabel()
        self.colorTimetableLabel()
        horLayout.addWidget(self.timetableLabel, 5)

        self.setLayout(horLayout)


    def fillLabels(self, mpkTime, destination = "", qtime = None):
        self.mpkTime = mpkTime
        self.destination = destination

        if mpkTime:
            self.lineLabel.setText(str(self.mpkTime.line))
            self.destinationLabel.setText(self.destination)

            text = "["
            if self.mpkTime.hour < 10:
                text += "0"
            text += "{0:d}:".format(self.mpkTime.hour)
            if self.mpkTime.min < 10:
                text += "0"
            text += "{0:d}]".format(self.mpkTime.min)
            self.timetableLabel.setText(text)
            self.updateTime(qtime)

            self.colorThisLabel(1)
        else:
            self.lineLabel.setText("")
            self.destinationLabel.setText("")
            self.timetableLabel.setText("[--:--]")
            self.updateTime(None)

            self.colorThisLabel(0)

    def setFrameOptions(self):
        self.setObjectName("MpkBigFrame")
        self.setFrameStyle(QFrame.StyledPanel)

    def colorlLineLabel(self):
        f = QFont("Arial", 27, QFont.Bold)
        self.lineLabel.setFont(f)
        self.lineLabel.setAlignment(Qt.AlignCenter)
        palette = QPalette()
        palette.setColor(QPalette.Foreground, Qt.darkRed)
        self.lineLabel.setPalette(palette)

    def colorDestinationLabel(self):
        f = QFont("Arial", 16, QFont.Bold)
        self.destinationLabel.setFont(f)
        self.destinationLabel.setAlignment(Qt.AlignCenter)
        self.destinationLabel.setObjectName("MpkBigFrame_Destination")
        style = "QLabel#" + self.destinationLabel.objectName() +" { "
        style += "border-radius: 8px; "
        style += "background: #fff"
        style += " }"
        self.destinationLabel.setStyleSheet(style)

    def colorTimeToLabel(self):
        f = QFont("Arial", 10, QFont.Bold)
        self.timeToLabel.setFont(f)
        self.timeToLabel.setAlignment(Qt.AlignCenter)
        palette = QPalette()
        palette.setColor(QPalette.Foreground, Qt.darkGray)
        self.timeToLabel.setPalette(palette)


    def colorTimetableLabel(self):
        f = QFont("Arial", 20, QFont.Bold)
        self.timetableLabel.setFont(f)
        self.timetableLabel.setAlignment(Qt.AlignCenter)
        palette = QPalette()
        palette.setColor(QPalette.Foreground, Qt.darkGray)
        self.timetableLabel.setPalette(palette)

    def colorThisLabel(self, styleColor):
        style = "QFrame#" + self.objectName() +" { "
        style += "border-style: solid; border: 2px solid gray; border-radius: 8px; "

        if styleColor == 0: # cyan
            style += "background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fff, stop: 1 #1ff)"
        elif styleColor == 1: # green
            style += "background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fff, stop: 1 #1f1)"
        elif styleColor == 2: # red
            style += "background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fff, stop: 1 #f11)"
        else: # black
            style += "background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fff, stop: 1 #111)"

        style += " }"
        self.setStyleSheet(style)

    def updateTime(self, qtime):
        if qtime and self.mpkTime:
            min, sec = self.mpkTime.timeTo(qtime)
            if sec < 0:
                self.timeToLabel.setText("Departure <br> <font color=blue size=5 style=Consolas> Time up! </font>".format(min,sec))
            elif sec < 10:
                self.timeToLabel.setText("Departure <br> <font color=blue size=5 style=Consolas> {0:2d} min 0{1:d} s</font>".format(min,sec))
            else:
                self.timeToLabel.setText("Departure <br> <font color=blue size=5 style=Consolas> {0:2d} min {1:d} s</font>".format(min,sec))

            if min < 16:
                self.colorThisLabelAfterTime(min)
        else:
            self.timeToLabel.setText("Departure <br> <font color=blue size=5 style=Consolas> -- min -- s</font>")

    def afterDelayTime(self, qtime):
        if self.mpkTime:
            min, sec = self.mpkTime.timeTo(qtime)
            return min < 1 and sec < -15
        else:
            return True

    def colorThisLabelAfterTime(self, min):
        step = 15
        if min < 15:
            step = min
        elif min < 0:
            step = 0

        style = "QFrame#" + self.objectName() +" { "
        style += "border-style: solid; border: 2px solid gray; border-radius: 8px; "
        style += "background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fff, stop: 1 #{1:x}{0:x}1)".format(step,15-step)
        style += " }"
        self.setStyleSheet(style)