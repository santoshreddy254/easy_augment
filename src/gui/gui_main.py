
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from shutil import copy
import os
import Main_Window
import AIG_Window


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main_Window.MainWindow()
    window.show()

    app.exec_()
