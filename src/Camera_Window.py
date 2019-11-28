import sys
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
from pc_utils import capture_data


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        # pipeline = rs.pipeline()
        # config = rs.config()
        # config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        # config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        #
        # # Start streaming
        # pipeline.start(config)
        #
        # # Get stream profile and camera intrinsics
        # profile = pipeline.get_active_profile()
        # depth_profile = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
        # depth_intrinsics = depth_profile.get_intrinsics()
        # w, h = depth_intrinsics.width, depth_intrinsics.height
        # try:
        #     count = 0
        #     while True:
        #
        #         # Wait for a coherent pair of frames: depth and color
        #         frames = pipeline.wait_for_frames()
        #         depth_frame = frames.get_depth_frame()
        #         color_frame = frames.get_color_frame()
        #         spatial = rs.spatial_filter()
        #         spatial.set_option(rs.option.holes_fill, 3)
        #         depth_frame = spatial.process(depth_frame)
        #         if not depth_frame or not color_frame:
        #             continue
        #         # Convert images to numpy arrays
        #         depth_image = np.asanyarray(depth_frame.get_data())
        #         color_image = np.asanyarray(color_frame.get_data())
        #         # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        #         depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(
        #             depth_image, alpha=0.03), cv2.COLORMAP_JET)
        #
        #         # Stack both images horizontally
        #         images = np.hstack((color_image, depth_colormap))
        #         rgbImage = cv2.cvtColor(images, cv2.COLOR_BGR2RGB)
        #         h, w, ch = rgbImage.shape
        #         bytesPerLine = ch * w
        #         convertToQtFormat = QtGui.QImage(
        #             rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
        #         p = convertToQtFormat.scaled(100, 100, Qt.KeepAspectRatio)
        #         self.changePixmap.emit(p)
        #         count += 1
        #         # break
        #
        # finally:
        #
        #     # Stop streaming
        #     pipeline.stop()
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                # https://stackoverflow.com/a/55468544/6622587
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QtGui.QImage(
                    rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
                p = convertToQtFormat.scaled(100, 100, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.label_list = []
        self.title = 'PyQt5 Video'
        self.left = 100
        self.top = 100
        self.width = 100
        self.height = 100
        self.initUI()
        self.show()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        # capture_data.init_capture_data()
        # images = capture_data.capture_data()
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(640, 480)
        # create a label
        self.label = QLabel(self)
        self.label.move(280, 0)
        self.label.resize(100, 100)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        self.button1 = QPushButton("Add", self)
        self.button1.clicked.connect(self.add_labels)
        self.button1.move(400, 90)
        self.button1.resize(100, 40)

        self.nameLabel_label = QLabel(self)
        self.nameLabel_label.setText('Labels :')
        self.nameLabel_label.move(50, 90)
        self.nameLabel_label.resize(200, 40)
        self.label_box = QComboBox(self)
        self.label_box.move(300, 90)
        for i in self.label_list:
            self.label_box.addItem(i)

    def add_labels(self):
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter your name:')
        self.label_list.append(text)
        self.label_box.clear()
        for i in self.label_list:
            self.label_box.addItem(i)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
