from PySide.QtGui import *
from PySide.QtCore import *

NOTIFICATION_FREQUENCY = 25
NOTIFICATION_SPEED = 3
MIN_CHAR_IN_NOTIFICATION_LINE = 100

from Widgets.NotificationSettings import NotificationSettings

class NotificationLine(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setThisFrameStyle()

        self.text = "Delivery stop "
        self.text = " ***        " + self.text + "       "
        self.setMinimalTextLength()

        self.initWidgets()
        self.initTimer()

    def setThisFrameStyle(self):
        self.setFrameStyle(QFrame.Box)
        self.setObjectName("NotificationFrame")
        self.setStyleSheet("QFrame#NotificationFrame{background-color: rgba(255, 255, 255, 150);}")


    def initWidgets(self):
        self.notifications = []

        palette = QPalette()
        palette.setColor(QPalette.Foreground, Qt.darkRed)

        for i in range(2):
            noti = QLabel(self.text, self)
            noti.setFont(QFont("Arial", 50, QFont.Bold))
            noti.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            noti.setPalette(palette)
            self.notifications.append(noti)

        self.setLabelsStart()

    def setLabelsStart(self):
        self.notifications[0].adjustSize()
        self.notifications[1].adjustSize()
        self.startPoints = [0, self.notifications[0].width()]

    def moveNotification(self):
        for i in range(2):
            self.notifications[i].move(self.startPoints[i], 0.1*self.height())
            self.startPoints[i] -= NOTIFICATION_SPEED
            if self.startPoints[i] + self.notifications[i].width() < 0:
                self.startPoints[i] = self.startPoints[i-1] + self.notifications[i-1].width()

    def initTimer(self):
        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL('timeout()'), self.moveNotification)
        self.timer.start(1000/NOTIFICATION_FREQUENCY)

    def setMinimalTextLength(self):
        if len(self.text) < MIN_CHAR_IN_NOTIFICATION_LINE:
            self.text = (MIN_CHAR_IN_NOTIFICATION_LINE // len(self.text) + 1) * self.text

    def mouseReleaseEvent(self, ev):
        ns = NotificationSettings()
        res = ns.exec_()
        if res:
            self.reactOnSettingsChange(ns.settings)


    def reactOnSettingsChange(self, notiSettings):
        palette = QPalette()
        palette.setColor(QPalette.Foreground, QColor(notiSettings["colorName"]))
        for i in range(2):
            self.notifications[i].setPalette(palette)

        self.text = ""
        for t in notiSettings["notifications"]:
            if len(t):
                self.text  += " ***        " + t + "       "

        self.timer.stop()
        if notiSettings["turnOff"]:
            for i in range(2):
                self.notifications[i].setText("")

        elif notiSettings["freeze"]:
            self.notifications[0].setText(self.text + " *** ")
            self.notifications[0].adjustSize()
            self.notifications[1].setText("")

            self.notifications[0].move( 0.5*(self.width() - self.notifications[0].width()),
                                        0.5*(self.height() - self.notifications[0].height()) )
        else:
            self.setMinimalTextLength()
            for i in range(2):
                self.notifications[i].setText(self.text)
            self.setLabelsStart()
            self.timer.start(1000 / NOTIFICATION_FREQUENCY)


