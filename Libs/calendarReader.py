from PySide.QtCore import QDate

FORENAMES_FILE = "Calendar/Forenames_PL.txt"
HOLIDAY_FILE_PART = "Calendar/Holiday_PL_"

def readCalendar():
    date = QDate.currentDate()

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

    return forenames, holiday

