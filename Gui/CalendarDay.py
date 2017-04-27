from PySide.QtGui import *
from PySide.QtCore import *

FORENAMES_FILE = "Calendar/Forenames_PL.txt"
HOLIDAY_FILE_PART = "Calendar/Holiday_PL_"

class CalendarDay(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initWidgets()
        self.formatLabels()

        self.formatBackground()

        self.updateCalendar()

        QTimer.singleShot(2000, self.initTimer)

    def initWidgets(self):
        self.dateLabel = QLabel("26 Mai 2017")
        self.holidayText = QLabel("Mother Day")
        self.weekDayName = QLabel("Friday")
        self.weekNumber = QLabel("Week num: 14")
        self.namesLabel = QLabel("Today celebrate")
        self.namesText = QLabel("Łucja, Tomasz,\nJoanna")

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
        print("Date updated")
        date = QDate.currentDate()

        # TODO: use locale
        months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
        self.dateLabel.setText(months[date.month()-1] + " " + str(date.day()) +", " + str(date.year()))

        days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
        self.weekDayName.setText(days[date.dayOfWeek()])
        self.weekNumber.setText("Week num: " + str(date.weekNumber()[0]))

        # TODO: move to lib file
        monthsRome = ["I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII"]
        dateRome = str(date.day()) + " " +  monthsRome[date.month()-1] + ";"

        forenames = ""
        forenamesNum = 0
        with open(FORENAMES_FILE, encoding='utf-8') as f:
            for line in f:
                if line.count(dateRome):
                    if forenamesNum:
                        forenames += ", "
                    if forenamesNum == 2:
                        forenames += "\n"

                    forenamesNum += 1
                    forenames += line.split()[0]

        if forenamesNum == 0:
            forenames = "-"

        holidayFile = HOLIDAY_FILE_PART + str(date.year()) + ".txt"
        holiday = ""
        with open(holidayFile, encoding='utf-8') as f:
            for line in f:
                if line.count(dateRome):
                    holiday = line.split(";")[1].strip()

        self.namesText.setText(forenames)
        self.holidayText.setText(holiday)

    def initTimer(self):
        print("Timer started")
        timer = QTimer(self)
        self.connect(timer, SIGNAL('timeout()'), self.updateCalendar)
        # timer.start(24*60*60*1000)
        timer.start(1000)