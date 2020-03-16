import sys
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pascal_voc_writer import Writer
import cv2
from easy_augment.pc_utils import capture_data
import pyrealsense2 as rs
import numpy as np
import cv2
import pcl
import os
from easy_augment.gui import aig_window_2
import copy



class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    imagesPixmap = pyqtSignal(np.ndarray)

    def run(self):
        self.pipeline, config = capture_data.init_capture_data()
        profile = self.pipeline.start(config)
        depth_sensor = profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        clipping_distance_in_meters = 1
        clipping_distance = clipping_distance_in_meters / depth_scale
        align_to = rs.stream.color
        align = rs.align(align_to)
        while True:
            frames = self.pipeline.wait_for_frames()
            aligned_frames = align.process(frames)
            depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()
            spatial = rs.spatial_filter()
            spatial.set_option(rs.option.holes_fill, 3)
            depth_frame = spatial.process(depth_frame)
            Pixel_Coord, segmented_cloud = capture_data.get_object_points(color_frame, depth_frame)
            depth_image = np.asanyarray(depth_frame.get_data(),np.uint8)
            color_image = np.asanyarray(color_frame.get_data())
            color_image_copy = copy.deepcopy(color_image)
            if len(Pixel_Coord) > 0:
                color_image_copy, object_mask, bbox_coordinates = capture_data.get_mask(Pixel_Coord, color_image_copy)
            else:
                object_mask = np.zeros((480, 640, 3), np.uint8)
                bbox_coordinates = [0,0,640,480]
            if not depth_frame or not color_frame:
                continue
            # for i in Pixel_Coord:
            #     cv2.circle(color_image_copy, (int(i[0]), int(i[1])), 2, (0, 255, 0), -1)
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(
                depth_image, alpha=0.03), cv2.COLORMAP_JET)
            images = np.hstack((color_image_copy, object_mask))
            images_raw = np.hstack((color_image, object_mask))
            full_data = [images_raw,bbox_coordinates,segmented_cloud,depth_image]
            full_data = np.array(full_data)

            rgbImage = cv2.cvtColor(images, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QtGui.QImage(
                rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
            p = convertToQtFormat.scaled(640, 240, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)
            self.imagesPixmap.emit(full_data)


class App(QWidget):
    def __init__(self, generator_options, save_folder_path):
        super().__init__()
        self.label_list = []
        self.title = 'b-it-bots -- Data Augmentor'
        self.setWindowIcon(QtGui.QIcon(os.path.dirname(
            os.path.realpath(__file__))+'/data/b-it-bots.jpg'))
        self.left = 100
        self.top = 100
        self.width = 100
        self.height = 100
        self._image_counter = []
        self.generator_options = generator_options
        self.save_folder_path = save_folder_path
        self.initUI()
        self.show()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(np.ndarray)
    def capture_image(self, full_data):
        if self.flag:
            self._image_counter[self.label_list.index(str(self.label_box.currentText()))] += 1
            name = str(self.label_box.currentText(
            ))+"_{}.png".format(self._image_counter[self.label_list.index(str(self.label_box.currentText()))])
            annotation_name = str(self.label_box.currentText(
                        ))+"_{}.xml".format(self._image_counter[self.label_list.index(str(self.label_box.currentText()))])
            pointcloud_name = str(self.label_box.currentText(
                        ))+"_{}.ply".format(self._image_counter[self.label_list.index(str(self.label_box.currentText()))])
            frame_name = str(self.label_box.currentText(
                        ))+"_{}".format(self._image_counter[self.label_list.index(str(self.label_box.currentText()))])

            rgb_img = full_data[0][:, :640]
            mask_img = full_data[0][:, 640:]
            bbox_coordinates = full_data[1]
            obj_pixels = np.where(mask_img == 255)
            mask_img[obj_pixels] = self.label_list.index(str(self.label_box.currentText()))+1
            if self.save_rgb:
                cv2.imwrite(self.generator_options.get_image_path()+name, rgb_img)
            if self.save_semantic_label:
                cv2.imwrite(self.generator_options.get_label_path()+name, mask_img)
            if self.save_bbox:
                writer = Writer(self.generator_options.get_image_path()+name,rgb_img.shape[0],rgb_img.shape[1])
                writer.addObject(str(self.label_box.currentText()),bbox_coordinates[0],bbox_coordinates[2],bbox_coordinates[2],bbox_coordinates[3])
                writer.save(self.save_folder_path+"/captured_data/obj_det_label/"+annotation_name)
            if self.save_pointcloud:
                pcl.save(full_data[2],self.save_folder_path+"/captured_data/pointclouds/"+pointcloud_name)
            if self.save_depth:
                # print(full_data[3].get_frame_number())
                # adds frame numer at the end of filename yet to solve the issue
                # saver = rs.save_single_frameset(filename=self.save_folder_path+"/captured_data/depth_frames/"+frame_name)
                # saver.process(full_data[3])
                cv2.imwrite(self.save_folder_path+"/captured_data/depth_frames/"+name,full_data[3])
            self.flag = False
            # sleep(1)

    def initUI(self):
        # capture_data.init_capture_data()
        # images = capture_data.capture_data()
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(700, 480)
        # create a label
        self.label = QLabel(self)
        self.label.move(30, 10)
        self.label.resize(640, 240)
        self.th = Thread(self)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()
        self.button1 = QPushButton("Add", self)
        self.button1.clicked.connect(self.add_labels)
        self.button1.move(400, 260)
        self.button1.resize(80, 20)

        self.nameLabel_label = QLabel(self)
        self.nameLabel_label.setText('Labels :')
        self.nameLabel_label.move(240, 250)
        self.nameLabel_label.resize(50, 40)
        self.label_box = QComboBox(self)
        self.label_box.move(300, 260)
        for i in self.label_list:
            self.label_box.addItem(i)


        self.rgb_checkbox = QCheckBox("RGB",self)
        self.rgb_checkbox.move(50,300)
        self.rgb_checkbox.setChecked(True)
        self.save_rgb = True
        self.rgb_checkbox.stateChanged.connect(lambda:self.clickbox(self.rgb_checkbox))


        self.semantic_label_checkbox = QCheckBox("Semantic label",self)
        self.semantic_label_checkbox.move(150,300)
        self.semantic_label_checkbox.setChecked(True)
        self.save_semantic_label = True
        self.semantic_label_checkbox.stateChanged.connect(lambda:self.clickbox(self.semantic_label_checkbox))

        self.pointcloud_checkbox = QCheckBox("PointCloud",self)
        self.pointcloud_checkbox.setChecked(True)
        self.save_pointcloud = True
        self.pointcloud_checkbox.move(300,300)
        self.pointcloud_checkbox.stateChanged.connect(lambda:self.clickbox(self.pointcloud_checkbox))



        self.depth_checkbox = QCheckBox("Depth",self)
        self.depth_checkbox.setChecked(True)
        self.save_depth = True
        self.depth_checkbox.move(450,300)
        self.depth_checkbox.stateChanged.connect(lambda:self.clickbox(self.depth_checkbox))



        self.bbox_checkbox = QCheckBox("Bounding Box",self)
        self.bbox_checkbox.setChecked(True)
        self.save_bbox = True
        self.bbox_checkbox.move(550,300)
        self.bbox_checkbox.stateChanged.connect(lambda:self.clickbox(self.bbox_checkbox))


        self.timer_interval_label = QLabel("Capture interval in ms",self)
        self.timer_interval_label.move(100,340)
        self.timer_interval = QLineEdit(self)
        self.timer_interval.move(350,340)
        self.timer_interval.setText(str(1000))
        self.timer_interval.textChanged.connect(self.toggle_switch_status)
        self.onlyInt = QIntValidator()
        self.timer_interval.setValidator(self.onlyInt)


        self.toggle_switch_label = QLabel("Start continous mode",self)
        self.toggle_switch_label.move(100,370)
        self.toggle_switch = QPushButton("Start",self)
        self.toggle_switch.setEnabled(False)
        self.toggle_switch.setStyleSheet("background-color: green")
        self.toggle_switch.move(350,370)
        self.toggle_switch.clicked.connect(self.toggle_switch_status)


        self.button1 = QPushButton("Save", self)
        self.button1.setEnabled(False)
        self.button1.clicked.connect(self.capture_img)
        self.button1.move(200, 400)
        self.button1.resize(80, 20)

        self.button2 = QPushButton("Finish", self)
        self.button2.setEnabled(False)
        self.button2.clicked.connect(self.finish_button)
        self.button2.move(400, 400)
        self.button2.resize(80, 20)

    def toggle_switch_status(self):
        if self.toggle_switch.text() == "Start":
            self.toggle_switch.setText("Stop")
            self.timer = QTimer(self)
            self.timer.start(int(self.timer_interval.text()))
            self.timer.timeout.connect(self.capture_img)
            self.toggle_switch.setStyleSheet("background-color: red")
        elif self.toggle_switch.text() == "Stop":
            self.timer.stop()
            self.toggle_switch.setText("Start")
            self.toggle_switch.setStyleSheet("background-color: green")
        self.button_status()


    def add_labels(self):
        if self.toggle_switch.text()=="Stop":
            self.toggle_switch_status()
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter your name:')
        self.label_list.append(text)
        self.button_status()
        self.label_box.clear()
        for i in reversed(self.label_list):
            self.label_box.addItem(i)
        if len(self._image_counter) != len(self.label_list):
            self._image_counter.append(0)
        # print("inside add labels ", self._image_counter)

    # def continous_capture(self):


    def capture_img(self):
        self.flag = True
        if self.flag:
            self.th.imagesPixmap.connect(self.capture_image)
            # self.flag = False


    def button_status(self):
        if len(self.label_list) > 0 and (self.save_rgb or self.save_pointcloud
        or self.save_depth or self.save_bbox or self.save_semantic_label) and self.toggle_switch.text() == "Start":
            self.button1.setEnabled(True)
            self.button2.setEnabled(True)
            self.toggle_switch.setEnabled(True)
        elif len(self.label_list) > 0 and (self.save_rgb or self.save_pointcloud
        or self.save_depth or self.save_bbox or self.save_semantic_label) and self.toggle_switch.text() == "Stop":
            self.button1.setEnabled(False)
            self.button2.setEnabled(True)
        else:
            self.button1.setEnabled(False)
            self.button2.setEnabled(False)

    def finish_button(self):
        file1 = open(self.save_folder_path+"/captured_data/labels.txt", "w")
        file1.write("__ignore__ \n_background_\n")
        for i in self.label_list:
            file1.write(i+"\n")
        file1.close()
        self.generator_options.set_labels_file_path(
            self.save_folder_path+"/captured_data/labels.txt")
        self.generator_options.set_max_objects(len(self.label_list))
        self.aig_window = aig_window_2.MainWindow(self.generator_options)
        self.aig_window.show()
        self.th.pipeline.stop()
        # self.th.stop()
        self.hide()

    def clickbox(self,checkbox):
        if checkbox.text() == "RGB":
            if checkbox.isChecked() == True:
                self.save_rgb = True
            elif checkbox.isChecked() == False:
                self.save_rgb = False
        elif checkbox.text() == "Semantic label":
            if checkbox.isChecked() == True:
                self.save_semantic_label = True
            elif checkbox.isChecked() == False:
                self.save_semantic_label = False
        elif checkbox.text() == "PointCloud":
            if checkbox.isChecked() == True:
                self.save_pointcloud = True
            elif checkbox.isChecked() == False:
                self.save_pointcloud = False
        elif checkbox.text() == "Depth":
            if checkbox.isChecked() == True:
                self.save_depth = True
            elif checkbox.isChecked() == False:
                self.save_depth = False
        elif checkbox.text() == "Bounding Box":
            if checkbox.isChecked() == True:
                self.save_bbox = True
            elif checkbox.isChecked() == False:
                self.save_bbox = False
        self.button_status()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
