import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtGui import *
from shutil import copy, rmtree
import os
from easy_augment.utils.arguments import *
from easy_augment.utils.generate_artificial_images import perform_augmentation
from easy_augment.utils.labelme2voc import convert_to_voc
from easy_augment.utils.make_semantic_labels import generate_semantic_labels
import easy_augment.gui.progress_bar
from easy_augment.utils.preprocessing import resize_images, rename_images_labels, rename_backgrounds
from pathlib import Path
from easy_augment.gui import camera_window, aig_window_2


class MainWindow(QWidget):                           # <===
    def __init__(self):
        super().__init__()
        self.setWindowTitle("b-it-bots -- Data Augmentor")
        self.setWindowIcon(QtGui.QIcon(os.path.dirname(
            os.path.realpath(__file__))+'/data/b-it-bots.jpg'))
        self.setGeometry(100, 100, 700, 500)
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

        self.source_folder_label = QLabel(self)
        self.source_folder_label.setText('Source folder path:')
        self.source_folder_label.move(100, 200)
        self.source_folder_label.resize(200, 40)
        self.source_folder_label.hide()
        self.source_folder = QLineEdit(self)
        self.source_folder.setText(self.home_path)
        self.source_folder.move(300, 200)
        self.source_folder.resize(200, 40)
        self.source_folder.hide()
        self.button6 = QPushButton("Change", self)
        self.button6.clicked.connect(self.change_source_folder)
        self.button6.move(520, 210)
        self.button6.resize(100, 20)
        self.button6.hide()

        self.nameLabel_save_folder_2 = QLabel(self)
        self.nameLabel_save_folder_2.setText('Save folder path:')
        self.nameLabel_save_folder_2.move(100, 250)
        self.nameLabel_save_folder_2.resize(200, 40)
        self.nameLabel_save_folder_2.hide()
        self.save_folder_2 = QLineEdit(self)
        self.save_folder_2.setText(self.home_path)
        self.save_folder_2.move(300, 250)
        self.save_folder_2.resize(200, 40)
        self.save_folder_2.hide()
        self.button9 = QPushButton("Change", self)
        self.button9.clicked.connect(self.change_save_folder_2)
        self.button9.move(520, 260)
        self.button9.resize(100, 20)
        self.button9.hide()

        self.nameLabel_labels_file_path = QLabel(self)
        self.nameLabel_labels_file_path.setText('Labels.txt file path:')
        self.nameLabel_labels_file_path.move(100, 300)
        self.nameLabel_labels_file_path.resize(200, 40)
        self.nameLabel_labels_file_path.hide()
        self.labels_file_path = QLineEdit(self)
        self.labels_file_path.setText(self.home_path)
        self.labels_file_path.move(300, 300)
        self.labels_file_path.resize(200, 40)
        self.labels_file_path.hide()
        self.button10 = QPushButton("Change", self)
        self.button10.clicked.connect(self.change_labels_file_path)
        self.button10.move(520, 310)
        self.button10.resize(100, 20)
        self.button10.hide()

        self.button7 = QPushButton("Continue", self)
        self.button7.clicked.connect(self.continue_button_annotations)
        self.button7.resize(150, 20)
        self.button7.move(175, 350)
        self.button7.setEnabled(True)
        self.button7.hide()
        self.button8 = QPushButton("Back", self)
        self.button8.clicked.connect(self.back_button)
        self.button8.resize(150, 20)
        self.button8.move(375, 350)
        self.button8.setEnabled(True)
        self.button8.hide()

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

    def change_source_folder(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        self.folderpath_dlg_3 = QFileDialog()
        self.folderpath_dlg_3.setFileMode(QFileDialog.Directory)
        folderpath = self.folderpath_dlg_3.getExistingDirectory()
        self.source_folder.setText(folderpath)

    def change_save_folder_2(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        self.folderpath_dlg_3 = QFileDialog()
        self.folderpath_dlg_3.setFileMode(QFileDialog.Directory)
        folderpath = self.folderpath_dlg_3.getExistingDirectory()
        self.save_folder_2.setText(folderpath)

    def change_labels_file_path(self):
        filepath = QFileDialog.getOpenFileNames(filter='*.txt')
        self.labels_file_path.setText(filepath[0][0])

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
        self.source_folder_label.show()
        self.nameLabel_save_folder_2.show()
        self.nameLabel_labels_file_path.show()
        self.save_folder_2.show()
        self.source_folder.show()
        self.labels_file_path.show()
        self.button6.show()
        self.button7.show()
        self.button8.show()
        self.button9.show()
        self.button10.show()

        self.button1.setEnabled(False)
        self.button5.setEnabled(False)

    def back_button(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        self.nameLabel_save_folder_2.hide()
        self.nameLabel_save_folder.hide()
        self.source_folder_label.hide()
        self.nameLabel_labels_file_path.hide()
        self.save_folder_2.hide()
        self.save_folder.hide()
        self.source_folder.hide()
        self.labels_file_path.hide()
        self.button2.hide()
        self.button3.hide()
        self.button4.hide()
        self.button6.hide()
        self.button9.hide()
        self.button10.hide()
        self.button7.hide()
        self.button8.hide()

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

    def continue_button_annotations(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        convert_to_voc(self.source_folder.text(), self.save_folder_2.text(),
                       self.labels_file_path.text())
        generate_semantic_labels(self.save_folder_2.text()+"/voc_data", self.save_folder_2.text())
        generator_options = GeneratorOptions()
        generator_options.set_image_path(self.save_folder_2.text()+"/voc_data/JPEGImages")
        generator_options.set_label_path(self.save_folder_2.text()+"/semantic_labels")
        generator_options.set_labels_file_path(self.labels_file_path.text())
        self.aig_window = aig_window_2.MainWindow(generator_options)
        self.aig_window.show()
        self.hide()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
