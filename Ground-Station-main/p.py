import sys
import time
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi


class Main_UI(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        loadUi("UI_V3.ui", self)
        self.count = 0
        self.styleSheet = "QFrame#circular_progress{\n border-radius:150;\n background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(0, 0, 0, 255), stop:{STOP_2} rgba(85, 85, 255, 255));\n}"

        # SET THE TİMER
        self.timerbar = QTimer(self)
        self.timerbar.start(35)
        self.timerbar.timeout.connect(self.get)

    def get(self):
        if self.count >= 100:
            self.timerbar.stop()
        else:
            self.count += 1
            self.progressbar(self.count)

    def progressbar(self, value):
        time.sleep(1)
        value = (100 - value) / 100.0
        self.styleSheet = self.styleSheet.replace("{STOP_1}", str(value - 0.001)).replace("{STOP_2}", str(value))
        self.temperature_visual.setStyleSheet(self.styleSheet)


def run():
        app = QtWidgets.QApplication([])
        window = Main_UI()
        window.show()
        app.exec_()


run()