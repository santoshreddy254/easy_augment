import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtGui import *
from shutil import copy, rmtree
import os
from easy_augment.utils.arguments import *
from easy_augment.utils.generate_artificial_images import perform_augmentation
import easy_augment.gui.progress_bar
from utils.preprocessing import resize_images, rename_images_labels, rename_backgrounds
from pathlib import Path
from easy_augment.gui import camera_window


class MainWindow(QWidget):                           # <===
    def __init__(self):
        super().__init__()
        self.setWindowTitle("b-it-bots -- Data Augmentor")
        self.setWindowIcon(QtGui.QIcon(os.path.dirname(
            os.path.realpath(__file__))+'/data/b-it-bots.jpg'))
        self.setGeometry(100, 100, 650, 300)
        self.aig_form()

    def aig_form(self):
        self.home_path = str(Path.home())

        self.button1 = QPushButton("Capture", self)
        self.button1.clicked.connect(self.ok_button)
        self.button1.resize(150, 20)
        self.button1.move(200, 250)
        self.button1.setEnabled(True)

        self.button2 = QPushButton("Have Annotations", self)
        self.button2.clicked.connect(self.ok_button)
        self.button2.resize(150, 20)
        self.button2.move(200, 200)
        self.button2.setEnabled(True)

    def change_save_folder(self):
        self.folderpath_dlg_3 = QFileDialog()
        self.folderpath_dlg_3.setFileMode(QFileDialog.Directory)
        folderpath = self.folderpath_dlg_3.getExistingDirectory()
        self.save_folder.setText(folderpath)

    def ok_button(self):
        if not os.path.exists(self.save_folder.text()+"/captured_data/images/"):
            os.makedirs(self.save_folder.text()+"/captured_data/images/",)
        elif os.path.exists(self.save_folder.text()+"/captured_data/images/"):
            rmtree(self.save_folder.text()+"/captured_data/images/")
            os.makedirs(self.save_folder.text()+"/captured_data/images/",)
        if not os.path.exists(self.save_folder.text()+"/captured_data/labels/"):
            os.makedirs(self.save_folder.text()+"/captured_data/labels/",)
        elif os.path.exists(self.save_folder.text()+"/captured_data/labels/"):
            rmtree(self.save_folder.text()+"/captured_data/labels/")
            os.makedirs(self.save_folder.text()+"/captured_data/labels/",)

        if not os.path.exists(self.save_folder.text()+"/captured_data/obj_det_label/"):
            os.makedirs(self.save_folder.text()+"/captured_data/obj_det_label/",)
        elif os.path.exists(self.save_folder.text()+"/captured_data/obj_det_label/"):
            rmtree(self.save_folder.text()+"/captured_data/obj_det_label/")
            os.makedirs(self.save_folder.text()+"/captured_data/obj_det_label/",)
        if not os.path.exists(self.save_folder.text()+"/captured_data/pointclouds/"):
            os.makedirs(self.save_folder.text()+"/captured_data/pointclouds/",)
        elif os.path.exists(self.save_folder.text()+"/captured_data/pointclouds/"):
            rmtree(self.save_folder.text()+"/captured_data/pointclouds/")
            os.makedirs(self.save_folder.text()+"/captured_data/pointclouds/",)

        generator_options = GeneratorOptions()
        generator_options.set_image_path(self.save_folder.text()+"/captured_data/images/")
        generator_options.set_label_path(self.save_folder.text()+"/captured_data/labels/")
        self.cam_window = Camera_Window.App(generator_options, self.save_folder.text())
        self.cam_window.show()
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec_()
