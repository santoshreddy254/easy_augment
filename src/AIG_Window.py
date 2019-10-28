import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtGui import *
from shutil import copy
import os
import Main_Window
import main
from generate_artificial_images import perform_augmentation
from arguments import *

class MainWindow(QMainWindow):                           # <===
    def __init__(self):
        super().__init__()
        self.setWindowTitle("b-it-bots -- Data Augmentor")
        self.setGeometry(100,100,550,300)
        self.aig_form()
    def aig_form(self):
        self.nameLabel_num_images = QLabel(self)
        self.nameLabel_num_images.setText('Number of images:')
        self.nameLabel_num_images.move(50, 20)
        self.num_images = QLineEdit(self)
        self.onlyInt = QIntValidator()
        self.num_images.setValidator(self.onlyInt)
        self.num_images.move(300, 20)
        self.num_images.resize(200,40)

        # self.nameLabel_save_label = QLabel(self)
        # self.nameLabel_save_label.setText('Number of images:')
        # self.nameLabel_save_label.move(50, 20)
        # self.num_images = QLineEdit(self)
        # self.onlyInt = QIntValidator()
        # self.num_images.setValidator(self.onlyInt)
        # self.num_images.move(300, 20)
        # self.num_images.resize(200,40)

        button1 = QPushButton("Ok",self)
        button1.clicked.connect(self.ok_button)
        button1.resize(150,20)
        button1.move(200,100)
        return self.num_images.text()
    def ok_button(self):
        generator_options = GeneratorOptions()
        generator_options.set_num_images(int(self.num_images.text()))
        print("insise ok button")
        print(self.num_images.text())
        perform_augmentation()
