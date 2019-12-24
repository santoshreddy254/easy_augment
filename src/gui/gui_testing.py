import sys
import os
import AIG_Window
from time import sleep
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtGui
from PyQt5.QtGui import *
import pytest
import pytestqt
from glob import glob
import cv2


def test_gui_1(qtbot):
    app = QApplication(sys.argv)
    window = AIG_Window.MainWindow()
    qtbot.addWidget(window)
    window.num_images.setText(str(2))
    cwd = os.getcwd()
    window.image_folder.setText(cwd+"/images")
    window.label_folder.setText(cwd+"/semantic_labels")
    window.backgrounds_folder.setText(cwd+"/backgrounds")
    window.labels_file_path.setText(cwd+"/labels.txt")
    window.image_save_path.setText(cwd)
    qtbot.waitForWindowShown(window)
    assert window.button1.isEnabled() == True
    qtbot.mouseClick(window.button1, Qt.LeftButton)
    assert os.path.exists(
        cwd+"/augmented/images/") == True and len(os.listdir(cwd+"/augmented/images/")) == 2
    assert os.path.exists(
        cwd+"/augmented/labels/") == True and len(os.listdir(cwd+"/augmented/labels/")) == 2
    assert os.path.exists(cwd+"/augmented/masks/") == True
    assert os.path.exists(cwd+"/augmented/obj_det_label/") == True


def test_gui_2(qtbot):
    app = QApplication(sys.argv)
    window = AIG_Window.MainWindow()
    qtbot.addWidget(window)
    window.num_images.setText(str(2))
    cwd = os.getcwd()
    window.image_folder.setText(cwd+"/images")
    window.label_folder.setText(cwd+"/semantic_labels")
    window.backgrounds_folder.setText(cwd+"/backgrounds")
    window.labels_file_path.setText(cwd+"/labels.txt")
    window.image_save_path.setText(cwd)
    window.rbutton3.setChecked(True)
    window.rbutton1.setChecked(True)
    qtbot.waitForWindowShown(window)
    assert window.button1.isEnabled() == True
    qtbot.mouseClick(window.button1, Qt.LeftButton)
    assert os.path.exists(
        cwd+"/augmented/images/") == True and len(os.listdir(cwd+"/augmented/images/")) == 2
    assert os.path.exists(
        cwd+"/augmented/labels/") == True and len(os.listdir(cwd+"/augmented/labels/")) == 2
    assert os.path.exists(
        cwd+"/augmented/masks/") == True and len(os.listdir(cwd+"/augmented/masks/")) == 2
    assert os.path.exists(
        cwd+"/augmented/obj_det_label/") == True and len(os.listdir(cwd+"/augmented/obj_det_label/")) == 2
