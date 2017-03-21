from PySide.QtCore import *
from PySide.QtGui import *

from Widgets.ClockW import ClockW

class Radiator(QMainWindow):
    def __init__(self):
        super(Radiator, self).__init__()

        # self.setGeometry(300, 300, 180, 380)
        self.setWindowTitle('Radiator')

        self.initWidgets()

        self.initTimer()
        self.updateTime()

        self.show()

    def initWidgets(self):
        self.clock = ClockW(self)

    def initTimer(self):
        timer = QTimer(self)
        self.connect(timer, SIGNAL('timeout()'), self.updateTime)
        timer.start(1000)

    def updateTime(self):
        qtime = QTime.currentTime()
        self.clock.update_time(qtime)













