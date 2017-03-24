from datetime import datetime
from PySide import QtGui


class ClockW(QtGui.QLCDNumber):
    def __init__(self, parent = None):
        super(ClockW, self).__init__(8,parent)
        self.setSegmentStyle(QtGui.QLCDNumber.Filled)
        self.configure_layout()

    def configure_layout(self):
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.WindowText,QtGui.QColor(230,0,0))
        self.setPalette(palette)

    def update_time(self, qtime):
        text = qtime.toString("hh:mm:ss")
        self.display(text)