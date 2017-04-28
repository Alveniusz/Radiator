from PySide.QtGui import *
from PySide.QtCore import *

from Libs.calendarReader import readCalendar

FORENAMES_FILE = "Calendar/Forenames_PL.txt"
HOLIDAY_FILE_PART = "Calendar/Holiday_PL_"

class CalendarDay(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initWidgets()
        self.formatLabels()
        self.formatBackground()

        self.initFirstTimer()

    def initWidgets(self):
        self.dateLabel = QLabel("")
        self.holidayText = QLabel("")
        self.weekDayName = QLabel("")
        self.weekNumber = QLabel("")
        self.namesLabel = QLabel("Today celebrate:")
        self.namesText = QLabel("")

        verLeftLayout = QVBoxLayout()
        verLeftLayout.addWidget(self.weekDayName, 1)
        verLeftLayout.addWidget(self.weekNumber, 4)

        verMedLayout = QVBoxLayout()
        verMedLayout.addWidget(self.holidayText, 1)
        verMedLayout.addStretch(4)

        verRightLayout = QVBoxLayout()
        verRightLayout.addWidget(self.namesLabel, 1)
        verRightLayout.addWidget(self.namesText, 4)

        horBottonLayout = QHBoxLayout()
        horBottonLayout.addLayout(verLeftLayout,1)
        horBottonLayout.addLayout(verMedLayout,1)
        horBottonLayout.addLayout(verRightLayout,1)

        verLayout = QVBoxLayout()
        verLayout.addWidget(self.dateLabel, 2)
        verLayout.addLayout(horBottonLayout,3)

        self.setLayout(verLayout)

    def formatLabels(self):
        palette = QPalette()

        palette.setColor(QPalette.WindowText,QColor(200,20,20))
        font = QFont("Arial", 56, QFont.Bold)
        self.dateLabel.setAlignment(Qt.AlignCenter)
        self.dateLabel.setFont(font)
        self.dateLabel.setPalette(palette)


        palette.setColor(QPalette.WindowText,QColor(140,0,0))
        font = QFont("Times New Roman", 20)
        self.holidayText.setAlignment(Qt.AlignCenter)
        self.holidayText.setFont(font)
        self.holidayText.setPalette(palette)


        font = QFont("Arial", 20, QFont.Bold)
        self.weekDayName.setFont(font)
        self.weekDayName.setAlignment(Qt.AlignCenter)

        palette.setColor(QPalette.WindowText,QColor(20,20,105))
        font = QFont("Arial", 40, QFont.Bold)
        self.weekNumber.setAlignment(Qt.AlignCenter)
        self.weekNumber.setFont(font)
        self.weekNumber.setPalette(palette)
        self.weekNumber.setObjectName("WeekNumberCalendar")
        self.weekNumber.setStyleSheet("QLabel#WeekNumberCalendar{background-color: rgba(50, 250, 50, 70);border-radius: 30px;}")

        font = QFont("Arial", 20, QFont.Bold)
        self.namesLabel.setAlignment(Qt.AlignCenter)
        self.namesLabel.setFont(font)
        font = QFont("Times New Roman", 25, QFont.Bold)
        self.namesText.setAlignment(Qt.AlignCenter)
        self.namesText.setFont(font)
        self.namesText.setPalette(palette)
        self.namesText.setObjectName("WeekNumberCalendar")
        self.namesText.setStyleSheet("QLabel#WeekNumberCalendar{background-color: rgba(50, 250, 50, 70);border-radius: 30px;}")

    def formatBackground(self):
        self.setObjectName("CalendarDayWidget")
        self.setStyleSheet("QFrame#CalendarDayWidget{background-color: rgba(255, 255, 255, 100);border-radius: 40px;}")


    def updateCalendar(self):
        date = QDate.currentDate()

        # TODO: use locale
        months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
        self.dateLabel.setText(months[date.month()-1] + " " + str(date.day()) +", " + str(date.year()))

        days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
        self.weekDayName.setText(days[date.dayOfWeek()])
        self.weekNumber.setText("Week num: " + str(date.weekNumber()[0]))

        forenames, holiday = readCalendar()

        self.namesText.setText(forenames)
        self.holidayText.setText(holiday)

    def initFirstTimer(self):
        self.updateCalendar()
        current = QTime.currentTime()
        secondsToMidnight = 3600*(24-current.hour()) - 60*current.minute() - current.second()
        QTimer.singleShot(1000*(secondsToMidnight + 10), self.initTimer)

    def initTimer(self):
        timer = QTimer(self)
        self.connect(timer, SIGNAL('timeout()'), self.updateCalendar)
        timer.start(24*60*60*1000)
