#!/usr/bin/env python
import os
import sys
import time
import math
import numpy as np
from PIL import Image
from matplotlib import colors

from qtmodern import styles, windows
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QLabel, QFileDialog, QPushButton, QSlider, QGridLayout, QHBoxLayout, QVBoxLayout


def time_dec(func):
    def wrapper(*args):
        start_time = time.time()
        func(args[0])
        print(f"Execution time for {func.__name__} is {time.time() - start_time}s")
    return wrapper


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """
        Initialize user interface
        """
        self.label = QLabel(self)
        self.pixmap = QPixmap()
        self.img = ''

        self.grid = QGridLayout()
        self.grid.setVerticalSpacing(10)
        self.setLayout(self.grid)

        self.init_choose_button()
        self.init_save_button()
        self.init_to_grey_button()
        self.init_to_red_button()
        self.init_to_green_button()
        self.init_to_blue_button()
        self.init_h_view()
        self.init_s_view()
        self.init_v_view()
        self.init_to_hsv_button()
        #self.init_to_hsv_button()

        self.init_sliders_view()
        self.fill_grid()
        
        self.set_start_picture()
        self.center()
        
    def init_choose_button(self):
        self.choose_img = QPushButton('Open', self)
        self.choose_img.clicked.connect(self.open_on_click)

    def init_save_button(self):
        self.save_img = QPushButton('Save', self)
        self.save_img.clicked.connect(self.save_on_click)
        self.save_img.setStyleSheet("background-color: #9a37ff; color:black")
        self.save_img.setAutoFillBackground(True)

    def init_to_grey_button(self):
        self.to_grey = QPushButton('to Grey', self)
        self.to_grey.clicked.connect(self.to_grey_on_click)

    def init_to_red_button(self):
        self.to_red = QPushButton('to Red', self)
        self.to_red.clicked.connect(self.to_red_on_click)

    def init_to_green_button(self):
        self.to_green = QPushButton('to Green', self)
        self.to_green.clicked.connect(self.to_green_on_click)

    def init_to_blue_button(self):
        self.to_blue = QPushButton('to Blue', self)
        self.to_blue.clicked.connect(self.to_blue_on_click)

    def init_to_hsv_button(self):
        self.to_hsv = QPushButton('to HSV', self)
        self.to_hsv.clicked.connect(self.rgb_to_hsv)
        #self.to_hsv.clicked.connect(self.hsv)

    def init_h_view(self):
        self.h_label = QLabel('H', self)
        self.h_sld = QSlider(Qt.Horizontal, self)
        self.h_min_label = QLabel('0', self)
        self.h_max_label = QLabel('360', self)
        self.h_sld.setRange(0, 360)
        self.h_sld.setPageStep(1)
        self.h_sld.setValue(180)
        self.h_diff = 0
        
    def init_s_view(self):
        self.s_label = QLabel('S', self)
        self.s_sld = QSlider(Qt.Horizontal, self)
        self.s_min_label = QLabel('-50', self)
        self.s_max_label = QLabel('50', self)
        self.s_sld.setRange(-50, 50)
        self.s_sld.setPageStep(1)
        self.s_sld.setValue(0)
        self.s_diff = 0
        # self.s_sld.valueChanged.connect(self.s_slider_change)

    def init_v_view(self):
        self.v_label = QLabel('V', self)
        self.v_sld = QSlider(Qt.Horizontal, self)
        self.v_min_label = QLabel('-50', self)
        self.v_max_label = QLabel('50', self)
        self.v_sld.setRange(-50, 50)
        self.v_sld.setValue(0)
        self.v_sld.setPageStep(1)
        self.v_diff = 0
    
    def refresh_sliders(self):
        self.h_sld.setValue(180)
        self.s_sld.setValue(0)
        self.v_sld.setValue(0)

    def init_sliders_view(self):
        self.slid_v = QVBoxLayout()
        self.slid_v.addSpacing(15)
        hbox = QHBoxLayout()
        hbox.addWidget(self.h_label)
        hbox.addSpacing(30)
        hbox.addWidget(self.h_min_label)
        hbox.addWidget(self.h_sld)
        hbox.addWidget(self.h_max_label)
        hbox.setSpacing(5)
        self.slid_v.addLayout(hbox)
        self.slid_v.addSpacing(25)

        hbox = QHBoxLayout()
        hbox.addWidget(self.s_label)
        hbox.addSpacing(20)
        hbox.addWidget(self.s_min_label)
        hbox.addSpacing(7)
        hbox.addWidget(self.s_sld)
        hbox.addSpacing(15)
        hbox.addWidget(self.s_max_label)
        self.slid_v.addLayout(hbox)
        self.slid_v.addSpacing(25)

        hbox = QHBoxLayout()
        hbox.addWidget(self.v_label)
        hbox.addSpacing(20)
        hbox.addWidget(self.v_min_label)
        hbox.addSpacing(7)
        hbox.addWidget(self.v_sld)
        hbox.addSpacing(15)
        hbox.addWidget(self.v_max_label)
        self.slid_v.addLayout(hbox)

    def fill_grid(self):
        self.grid.addWidget(self.choose_img, 1, 0)
        self.grid.addWidget(self.save_img, 1, 1)
        self.grid.addWidget(self.to_grey, 2, 0)
        self.grid.addWidget(self.to_red, 2, 1)
        self.grid.addWidget(self.to_green, 3, 0)
        self.grid.addWidget(self.to_blue, 3, 1)
        self.grid.addLayout(self.slid_v, 4, 0, 1, 2)
        self.grid.addWidget(self.to_hsv, 5, 0, 1, 2)
        self.grid.addWidget(self.label, 0, 5, 11, 1)

    def set_start_picture(self):
        self.filename = 'images/ФРУКТЫ.jpg'
        pixmap = QPixmap(self.filename)
        self.image_size = pixmap.size()
        self.label.resize(pixmap.size().width(), pixmap.size().height())
        self.label.setPixmap(pixmap)
        self.show()
        
    def pixels_to_grey(self, pixels, weights=None):
        dtype = pixels.dtype
        #print(pixels.shape)
        mod_pixels = np.average(pixels, axis=2, weights=weights)
        # reshaped_pixels = np.repeat(mod_pixels, 3).reshape(pixels.shape)
        reshaped_pixels = np.dstack((mod_pixels, mod_pixels, mod_pixels))
        return reshaped_pixels.astype(dtype)

    @time_dec
    def to_grey_on_click(self):
        # convert image to array
        img = Image.open(self.filename).resize((self.image_size.width(), self.image_size.height()))
        pixels = np.array(img, dtype=np.uint8)

        equal_weigths = [.33] * pixels.shape[-1]
        equal_pixels = self.pixels_to_grey(pixels, equal_weigths)
        # convert array to image
        equal_img = Image.fromarray(equal_pixels)
        equal_img.save('images/Equal_weights.jpg')

        # human_weigths = [.299, .587, .114]
        human_weigths = [.2126, .7152, .0722] 
        human_pixels = self.pixels_to_grey(pixels, human_weigths)
        human_img = Image.fromarray(human_pixels)
        human_img.save('images/Human_weights.jpg')

        min_ = np.min((equal_pixels - human_pixels).astype(np.int8))
        sub_pixels = (equal_pixels - human_pixels).astype(np.int8) + abs(min_)
        sub_img = Image.fromarray(sub_pixels.astype(np.uint8))
        sub_img.save('images/Sub_weights.jpg')

        self.label.setPixmap(QPixmap('images/Human_weights.jpg').scaled(self.image_size.width(), self.image_size.height()))


    def to_red_on_click(self):
        img = Image.open(self.filename).resize((self.image_size.width(), self.image_size.height()))
        pixels = np.array(img, dtype=np.uint8)
        pixels = (pixels * [1, 0, 0]).astype(pixels.dtype)
        img = Image.fromarray(pixels.astype(np.uint8))
        filename = f"{self.to_red_on_click.__name__.split('_')[1]}.jpg"
        img.save(filename)
        self.label.setPixmap(QPixmap(filename).scaled(self.image_size.width(), self.image_size.height()))
#        try:
#            os.remove(filename) 
#        except Exception as e:
#            print('FileNotFound')

    def to_green_on_click(self):
        img = Image.open(self.filename).resize((self.image_size.width(), self.image_size.height()))
        pixels = np.array(img, dtype=np.uint8)
        pixels = (pixels * [0, 1, 0]).astype(pixels.dtype)
        img = Image.fromarray(pixels)
        filename = f"{self.to_green_on_click.__name__.split('_')[1]}.jpg"
        img.save(filename)
        self.label.setPixmap(QPixmap(filename).scaled(self.image_size.width(), self.image_size.height()))
#        try:
#            os.remove(filename) 
#        except Exception as e:
#            print('FileNotFound')

    def to_blue_on_click(self):
        img = Image.open(self.filename).resize((self.image_size.width(), self.image_size.height()))
        pixels = np.array(img, dtype=np.uint8)
        pixels = (pixels * [0, 0, 1]).astype(pixels.dtype)
        img = Image.fromarray(pixels)
        filename = f"{self.to_blue_on_click.__name__.split('_')[1]}.jpg"
        img.save(filename)
        self.label.setPixmap(QPixmap(filename).scaled(self.image_size.width(), self.image_size.height()))
#        try:
#            os.remove(filename) 
#        except Exception as e:
#            print('FileNotFound')

    def open_file_name_dialog(self):
        dialog = QFileDialog()
        filename, _ = dialog.getOpenFileName(self, filter="Images (*.jpg *.jpeg *.png)")
        self.filename = filename if filename else self.filename
        self.pixmap = QPixmap(self.filename).scaled(self.image_size.width(), 
                                                    self.image_size.height())

    def rgb_to_hsv(self):
        img = Image.open(self.filename).resize((self.image_size.width(), self.image_size.height()))
        pixels = np.array(img, dtype=np.uint8)
        hsv = colors.rgb_to_hsv(pixels / 256)

        dh = self.h_sld.value() - self.h_diff
        ds = (self.s_sld.value() - self.s_diff) * 0.01
        dv = (self.v_sld.value() - self.v_diff) * 0.01
        h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]

        h1 = (h + dh) % 360
        s1 = np.maximum(np.minimum(s + ds, 1), 0)
        v1 = np.maximum(np.minimum(v + dv, 1), 0)
        self.refresh_sliders()
        self.h_diff = self.h_sld.value()
        self.s_diff = self.s_sld.value()
        self.v_diff = self.v_sld.value()
        hsv = np.dstack((h1, s1, v1))

        rgb = colors.hsv_to_rgb(hsv) * 255
        img = Image.fromarray(rgb.astype(np.uint8))
        filename = f"{self.rgb_to_hsv.__name__.split('_')[1]}.jpg"
        img.save(filename)
        self.label.setPixmap(QPixmap(filename).scaled(self.image_size.width(), self.image_size.height()))
        try:
            os.remove(filename) 
        except Exception as e:
            print('FileNotFound')

        #maxs = np.max(pixels, axis=2)
        #mins = np.min(pixels, axis=2)
        #delta = maxs - mins
        
        #r, g, b = pixels[:, :, 0], pixels[:, :, 1], pixels[:, :, 2]

        ## fill h values
        #h = np.zeros(shape=pixels[..., 0].shape, dtype=pixels.dtype)
        #h = np.where(maxs == mins, 0, h)
        #h = np.where((maxs == r) & (g >= b),
        #             60 * (g - b) / delta, h)
        #h = np.where((maxs == r) & (g < b),
        #             60 * (g - b) / delta + 360, h) 
        #h = np.where(maxs == g,
        #             60 * (b - r) / delta + 120, h)
        #h = np.where(maxs == b,
        #             60 * (r - g) / delta + 240, h)

        ## fill s values
        #s = np.where(maxs != 0, 1 - (mins / maxs), 0)
        
        ## fill v values
        #v = np.max(pixels, axis=2)

        #np.set_printoptions(suppress=True)
        #hsv = np.dstack((h, s, v))
        
        #hsv[:, :, 2] /= 255 
        ##print(hsv)
        #self.hsv_to_rgb(hsv)


    def open_on_click(self):
        self.open_file_name_dialog()
        self.label.setPixmap(self.pixmap)


    def save_on_click(self):
        self.save_file_dialog()


    def save_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "Images (*.jpg *.jpeg *.png)", options=options)
        if filename:
            self.label.pixmap().save(filename)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def eqweights(self, r, g, b):
        pixel = int(0.33 * (r + g + b))
        return pixel, pixel, pixel

    def difweights(self, r, g, b):
        pixel = int(r * 0.299 + g * 0.587 + b * 0.114)
        return pixel, pixel, pixel


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    styles.dark(app)
    mw = windows.ModernWindow(win)
    mw.show()
    sys.exit(app.exec_())
