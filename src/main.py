import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtGui import *
from shutil import copy, rmtree
import os
from utils.arguments import *
from utils.generate_artificial_images import perform_augmentation
import gui.progress_bar
from utils.preprocessing import resize_images, rename_images_labels, rename_backgrounds
from pathlib import Path
from gui import camera_window


class MainWindow(QWidget):                           # <===
    def __init__(self):
        super().__init__()
        self.setWindowTitle("b-it-bots -- Data Augmentor")
        self.setWindowIcon(QtGui.QIcon(os.path.dirname(
            os.path.realpath(__file__))+'/data/b-it-bots.jpg'))
        self.setGeometry(100, 100, 700, 300)
        self.aig_form()

    def aig_form(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        self.home_path = str(Path.home())

        self.button1 = QPushButton("Capture", self)
        self.button1.clicked.connect(self.capture_button)
        self.button1.resize(150, 20)
        self.button1.move(275, 50)
        self.button1.setEnabled(True)

        self.nameLabel_save_folder = QLabel(self)
        self.nameLabel_save_folder.setText('Save folder path:')
        self.nameLabel_save_folder.move(50, 100)
        self.nameLabel_save_folder.resize(200, 40)
        self.nameLabel_save_folder.hide()
        self.save_folder = QLineEdit(self)
        self.save_folder.setText(self.home_path)
        self.save_folder.move(300, 100)
        self.save_folder.resize(200, 40)
        self.save_folder.hide()
        self.button2 = QPushButton("Change", self)
        self.button2.clicked.connect(self.change_save_folder)
        self.button2.move(520, 110)
        self.button2.resize(100, 20)
        self.button2.hide()

        self.button3 = QPushButton("Continue", self)
        self.button3.clicked.connect(self.continue_button)
        self.button3.resize(150, 20)
        self.button3.move(175, 200)
        self.button3.setEnabled(True)
        self.button3.hide()
        self.button4 = QPushButton("Back", self)
        self.button4.clicked.connect(self.back_button)
        self.button4.resize(150, 20)
        self.button4.move(375, 200)
        self.button4.setEnabled(True)
        self.button4.hide()

        self.button5 = QPushButton("Have Annotations", self)
        self.button5.clicked.connect(self.annotations_button)
        self.button5.resize(150, 20)
        self.button5.move(275, 150)
        self.button5.setEnabled(True)

    def change_save_folder(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        self.folderpath_dlg_3 = QFileDialog()
        self.folderpath_dlg_3.setFileMode(QFileDialog.Directory)
        folderpath = self.folderpath_dlg_3.getExistingDirectory()
        self.save_folder.setText(folderpath)

    def capture_button(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        self.nameLabel_save_folder.show()
        self.save_folder.show()
        self.button2.show()
        self.button3.show()
        self.button4.show()
        self.button5.hide()

        self.button1.setEnabled(False)
        self.button5.setEnabled(False)

    def annotations_button(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        pass

    def back_button(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        self.nameLabel_save_folder.hide()
        self.save_folder.hide()
        self.button2.hide()
        self.button3.hide()
        self.button4.hide()
        self.button5.show()

        self.button1.setEnabled(True)
        self.button5.setEnabled(True)

    def continue_button(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
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

        generator_options = GeneratorOptions()
        generator_options.set_image_path(self.save_folder.text()+"/captured_data/images/")
        generator_options.set_label_path(self.save_folder.text()+"/captured_data/labels/")
        self.cam_window = camera_window.App(generator_options, self.save_folder.text())
        self.cam_window.show()
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec_()
