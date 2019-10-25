import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from shutil import copy
import os

# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("b-it-bots -- Data Augmentor")
        self.setGeometry(100,100,550,300)
        self.home()
        self.show()
    def home(self):
        button1 = QPushButton("Add images",self)
        button1.clicked.connect(self.browse_image_files)
        button1.resize(150,20)
        button1.move(200,100)

        button2 = QPushButton("Add labels",self)
        button2.clicked.connect(self.browse_label_files)
        button2.resize(150,20)
        button2.move(200,150)

        button3 = QPushButton("Start augmenting",self)
        button3.clicked.connect(self.close_application)
        button3.resize(150,20)
        button3.move(200,200)



    def close_application(self):
        print("Thank you")
        sys.exit()

    def browse_image_files(self):
        os.chdir("..")
        destination = os.getcwd() + '/images'
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

    # def open_progress_bar(self,num):
    #     my_progress_bar = QDialog(self)
    #     my_progress_bar.setWindowTitle("Copying")
    #     progress = QProgressBar(self)
    #     progress.setGeometry(0, 0, 300, 25)
    #     my_progress_bar.setGeometry(100,100,550,300)
    #     progress.setValue(num)
    #     my_progress_bar.show()




if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()
