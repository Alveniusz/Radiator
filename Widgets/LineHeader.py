from PySide.QtGui import *
from PySide.QtCore import *

class LineHeader(QLabel):
    def __init__(self, parent, lineNum, lineDestination):
        super().__init__(parent)
        self.setLineAndDestination(lineNum,lineDestination)

        f = QFont("Arial", 9, QFont.Bold)
        self.setFont(f)
        self.setAlignment(Qt.AlignCenter)
        self.setFrameStyle(QFrame.StyledPanel)
        self.colorThisLabel(1)

    def setLineAndDestination(self, lineNum, lineDestination):
        self.line = lineNum
        self.destination = lineDestination

        self.setText("<font color=blue size=7>{0}</font><br>{1}".format(self.line, self.destination))
        self.setObjectName( "LineLabel{0}".format(self.line) )

    def colorThisLabel(self, styleColor):
        style = "QLabel#" + self.objectName() +" { "
        style += "border-style: solid; border: 2px solid gray; border-radius: 8px; "

        if styleColor == 0: # cyan
            style += "background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #eff, stop: 1 #1ff)"
        elif styleColor == 1: # green
            style += "background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #efe, stop: 1 #1f1)"
        elif styleColor == 2: # red
            style += "background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fee, stop: 1 #f11)"
        else: # black
            style += "background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #eee, stop: 1 #111)"

        style += " }"
        self.setStyleSheet(style)