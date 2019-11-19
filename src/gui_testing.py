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
    window.num_images.setText(str(10))
    window.image_folder.setText("/home/santosh/MAS/SDP/Data_Augmentor_With_GUI/images")
    window.label_folder.setText("/home/santosh/MAS/SDP/Data_Augmentor_With_GUI/semantic_labels")
    window.backgrounds_folder.setText("/home/santosh/MAS/SDP/Data_Augmentor_With_GUI/backgrounds")
    window.labels_file_path.setText("/home/santosh/MAS/SDP/Data_Augmentor_With_GUI/labels.txt")

    # qtbot.mouseClick(window.button2, Qt.LeftButton)
    # qtbot.mouseClick(window.folderpath_dlg,)
    window.show()
    qtbot.waitForWindowShown(window)
    # sleep(5)
    print(window.button1.isEnabled())

    assert window.button1.isEnabled() == True
    qtbot.mouseClick(window.button1, Qt.LeftButton)
