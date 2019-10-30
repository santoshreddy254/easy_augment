import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from shutil import copy
import os
import AIG_Window

# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.setWindowTitle("b-it-bots -- Data Augmentor")
        self.setGeometry(100,100,550,300)
        self.home()
        self.show()
    def home(self):

        button1 = QPushButton("Add images",self)
        button1.clicked.connect(self.browse_image_files)
        button1.resize(150,20)
        button1.move(200,10)

        button2 = QPushButton("Add labels",self)
        button2.clicked.connect(self.browse_label_files)
        button2.resize(150,20)
        button2.move(200,60)

        button3 = QPushButton("Add backgrounds",self)
        button3.clicked.connect(self.browse_background_files)
        button3.resize(150,20)
        button3.move(200,110)

        button4 = QPushButton("Start augmenting",self)
        button4.clicked.connect(self.augment_data)
        button4.resize(150,20)
        button4.move(200,160)


    def close_application(self):
        print("Thank you")
        sys.exit()

    def augment_data(self):
        self.agi_window = AIG_Window.MainWindow()
        self.agi_window.show()
        self.hide()
    def browse_image_files(self):
        os.chdir("..")
        destination = os.getcwd() + '/images'
        print(destination)
        filepaths = QFileDialog.getOpenFileNames()
        self.copy_files(filepaths[0],destination)
    def browse_background_files(self):
        os.chdir("..")
        destination = os.getcwd() + '/backgrounds'
        print(destination)
        filepaths = QFileDialog.getOpenFileNames()
        self.copy_files(filepaths[0],destination)

    def browse_label_files(self):
        os.chdir("..")
        destination = os.getcwd() + '/semantic_labels'
        filepaths = QFileDialog.getOpenFileNames()
        self.copy_files(filepaths[0],destination)


    def copy_files(self,filepaths,destination):
        val = 100/len(filepaths)
        # progress_bar = ProgressWindow()
        for i,f_name in enumerate(filepaths):
            copy(f_name,destination)
            # self.open_progress_bar(val*i)





# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#
#     app.exec_()
