from pytestqt import qtbot
import AIG_Window
from time import sleep
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtGui import *
import sys

def test_myapp(qtbot):
    app = QApplication(sys.argv)
    window = AIG_Window.MainWindow()
    window.show()
    qtbot.mouseClick(window.button1, Qt.LeftButton)
    sleep(30)
test_myapp(qtbot)
