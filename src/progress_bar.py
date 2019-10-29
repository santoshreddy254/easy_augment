import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtGui import *
from shutil import copy
import os
import Main_Window
import main
from arguments import *

class MainWindow(QMainWindow):                           # <===
    def __init__(self):
        super().__init__()
        self.setWindowTitle("b-it-bots -- Data Augmentor")
        self.setGeometry(100,100,550,100)
        self.progress_bar()
    def progress_bar(self):
        # self.progress_bar = QProgressBar(self)
        # self.progress_bar.setValue(val)
        self.button1 = QPushButton("Done",self)
        self.button1.clicked.connect(self.done_button)
        self.button1.resize(150,20)
        self.button1.move(200,50)
    def done_button(self):
            self.main_window = Main_Window.MainWindow()
            self.main_window.show()
            self.hide()
