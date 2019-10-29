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
import progress_bar

class MainWindow(QMainWindow):                           # <===
    def __init__(self):
        super().__init__()
        self.setWindowTitle("b-it-bots -- Data Augmentor")
        self.setGeometry(100,100,550,500)
        self.aig_form()
    def aig_form(self):
        self.nameLabel_num_images = QLabel(self)
        self.nameLabel_num_images.setText('Number of images:')
        self.nameLabel_num_images.move(50, 20)
        self.nameLabel_num_images.resize(200,40)
        self.num_images = QLineEdit(self)
        self.onlyInt = QIntValidator()
        self.num_images.setValidator(self.onlyInt)
        self.num_images.move(300, 20)
        self.num_images.resize(200,40)

        self.nameLabel_image_type = QLabel(self)
        self.nameLabel_image_type.setText('Image format:')
        self.nameLabel_image_type.move(50, 70)
        self.nameLabel_image_type.resize(200,40)
        self.image_type = QComboBox(self)
        self.image_type.addItem(".png")
        self.image_type.addItem(".jpg")
        self.image_type.move(300, 70)

        self.nameLabel_max_objects = QLabel(self)
        self.nameLabel_max_objects.setText('Maximum objects:')
        self.nameLabel_max_objects.move(50, 120)
        self.nameLabel_max_objects.resize(200,40)
        self.max_objects = QLineEdit(self)
        self.onlyInt = QIntValidator()
        self.max_objects.setValidator(self.onlyInt)
        self.max_objects.move(300, 120)
        self.max_objects.resize(200,40)

        self.button1 = QPushButton("Ok",self)
        self.button1.clicked.connect(self.ok_button)
        self.button1.resize(150,20)
        self.button1.move(200,450)
        return self.num_images.text()
    def ok_button(self):
        generator_options = GeneratorOptions()
        generator_options.set_num_images(int(self.num_images.text()))
        generator_options.set_image_type(self.image_type.currentText())
        generator_options.set_max_objects(int(self.max_objects.text()))
        print("insise ok button")
        print(self.num_images.text())
        flag = perform_augmentation()
        if flag:
            self.progress_bar_obj = progress_bar.MainWindow()
            self.progress_bar_obj.show()
            self.hide()
