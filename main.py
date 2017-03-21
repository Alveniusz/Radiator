import sys
from PySide.QtGui import QApplication

from radiator import Radiator
from Libs.mpkUpdate import MpkUpdate


def main():
    app = QApplication(sys.argv)

    mpk = MpkUpdate()

    r = Radiator()

    app.exec_()
    sys.exit()

if __name__ == '__main__':
    main()