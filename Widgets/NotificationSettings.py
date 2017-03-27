from PySide.QtGui import *
from PySide.QtCore import *

import json

NOTIFICATION_INPUT_LINES = 3
NOTIFICATIONS_SETTINGS_FILE = "Config/notificationsSettings.cfx"

class NotificationSettings(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Notifications settings...")
        self.setMinimumWidth(400)
        self.setFocus()

        self.initSettings()

        self.initWidgets()
        self.connectSignals()

        self.loadSettings()

    def initWidgets(self):
        self.okButton = QPushButton("Ok")
        self.okButton.setDefault(True)
        self.okButton.setAutoDefault(True)
        self.cancelButton = QPushButton("Cancel")

        self.setFreezeBox = QCheckBox("Freeze notification")
        self.setTurnOffBox = QCheckBox("Turn off this")

        self.notificationInputs = []
        for i in range(NOTIFICATION_INPUT_LINES):
            notifi = QLineEdit()
            notifi.setPlaceholderText("Notification " + str(i + 1))
            self.notificationInputs.append(notifi)

        self.colorButton = QPushButton("Set notification color")
        self.frameColor = QFrame()
        self.frameColor.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.frameColor.setLineWidth(2)
        self.frameColor.setObjectName("FrameSettingsColor")

        mainLayout = QVBoxLayout()
        for n in self.notificationInputs:
            mainLayout.addWidget(n)
        hLayout = QHBoxLayout()
        hLayout.addStretch(1)
        hLayout.addWidget(self.colorButton, 2)
        hLayout.addStretch(1)
        hLayout.addWidget(self.frameColor, 1)
        hLayout.addStretch(1)
        mainLayout.addLayout(hLayout)
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.setFreezeBox,1)
        hLayout.addWidget(self.setTurnOffBox,1)
        mainLayout.addLayout(hLayout)
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.okButton)
        hLayout.addWidget(self.cancelButton)
        mainLayout.addLayout(hLayout)

        self.setLayout(mainLayout)

    def connectSignals(self):
        self.connect(self.cancelButton, SIGNAL('clicked()'), self.reject)
        self.connect(self.okButton, SIGNAL('clicked()'), self.accept)
        self.connect(self.colorButton, SIGNAL('clicked()'), self.selectColor)

    def accept(self):
        self.saveSettings()
        super().accept()

    def setSettings(self):
        try:
            for i in range(NOTIFICATION_INPUT_LINES):
                self.settings["notifications"][i] = self.notificationInputs[i].text()
                self.settings["freeze"] = self.setFreezeBox.isChecked()
                self.settings["turnOff"] = self.setTurnOffBox.isChecked()
        except (KeyError, IndexError, ValueError):
            self.initSettings()

    def setWidgets(self):
        try:
            for i in range(NOTIFICATION_INPUT_LINES):
                self.notificationInputs[i].setText( self.settings["notifications"][i] )
            self.frameColor.setStyleSheet(
                "QFrame { background-color: %s; }" % self.settings["colorName"])
            self.setFreezeBox.setChecked(self.settings["freeze"])
            self.setTurnOffBox.setChecked(self.settings["turnOff"])
        except (KeyError, IndexError, ValueError):
            self.initSettings()

    def selectColor(self):
        col = QColorDialog.getColor()
        if col.isValid():
            print(col.name())
            self.settings["colorName"] = col.name()
            self.frameColor.setStyleSheet(
                "QFrame { background-color: %s; }" % self.settings["colorName"])

    def loadSettings(self):
        try:
            with open(NOTIFICATIONS_SETTINGS_FILE, 'r') as infile:
                self.settings = json.load(infile)
        except (FileNotFoundError, ValueError):
            self.initSettings()

        self.setWidgets()

    def saveSettings(self):
        self.setSettings()
        with open(NOTIFICATIONS_SETTINGS_FILE, 'w') as outfile:
            json.dump(self.settings, outfile, ensure_ascii=False)

    def initSettings(self):
        self.settings = { "notifications":["" for i in range(NOTIFICATION_INPUT_LINES)],
                          "colorName":"",
                          "freeze":False,
                          "turnOff":False}
