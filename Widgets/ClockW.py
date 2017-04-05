from datetime import datetime
from PySide import QtGui
from PySide.QtCore import Qt


class ClockW(QtGui.QLCDNumber):
    def __init__(self, parent = None):
        super(ClockW, self).__init__(8,parent)
        self.setSegmentStyle(QtGui.QLCDNumber.Filled)
        self.configure_layout()

    def configure_layout(self):
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.WindowText,QtGui.QColor(230,0,0))
        self.setObjectName("ClockLCDFrame")
        self.setStyleSheet("QLCDNumber#ClockLCDFrame{background-color: rgba(255, 255, 255, 150);}")

        self.setPalette(palette)

    def update_time(self, qtime):
        if qtime.second()%2:
            text = qtime.toString("hh:mm:ss")
        else:
            text = qtime.toString("hh mm ss")
        self.display(text)