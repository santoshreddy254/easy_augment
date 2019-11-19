import sys
import os
import AIG_Window
from time import sleep
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtGui import *
import pytest
import pytestqt

def test_gui(qtbot):
    # app = QApplication(sys.argv)
    window = AIG_Window.MainWindow()
    qtbot.addWidget(window)
    window.num_images.setText(str(2))
    cwd = os.getcwd()
    window.image_folder.setText(cwd+"/images")
    window.label_folder.setText(cwd+"/semantic_labels")
    window.backgrounds_folder.setText(cwd+"/backgrounds")
    window.labels_file_path.setText(cwd+"/labels.txt")
    window.show()
    qtbot.waitForWindowShown(window)
    print(window.button1.isEnabled())

    assert window.button1.isEnabled() == True
    qtbot.mouseClick(window.button1, Qt.LeftButton)
