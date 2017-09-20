
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QLabel, QFileDialog, QPushButton, QSlider


class Colors(QWidget):

    def __init__(self):
        super().__init__()
        self.img = ''
        self.label = QLabel(self.window())
        self.label.resize(670, 500)
        self.label.move(25, 25)
        self.pixmap = QPixmap()
        self.init_ui()

    def init_ui(self):
        self.resize(1200, 850)
        self.center()
        self.setWindowTitle('Center')

        self.h_label = QLabel('H', self)
        self.h_label.move(30, 766)
        self.h_sld = QSlider(Qt.Horizontal, self)
        self.h_sld.setRange(0, 360)
        self.h_sld.setPageStep(1)
        self.h_sld.move(50, 750)
        self.h_sld.resize(500, 50)
        # self.h_sld.valueChanged[int].connect(self.h_slider_change)

        self.s_label = QLabel('S', self)
        self.s_label.move(30, 801)
        self.s_sld = QSlider(Qt.Horizontal, self)
        self.s_sld.setRange(0, 100)
        self.s_sld.setPageStep(1)
        self.s_sld.move(50, 785)
        self.s_sld.resize(500, 50)
        # self.s_sld.valueChanged.connect(self.s_slider_change)

        self.v_label = QLabel('V', self)
        self.v_label.move(30, 836)
        self.v_sld = QSlider(Qt.Horizontal, self)
        self.v_sld.setRange(0, 100)
        self.v_sld.setPageStep(1)
        self.v_sld.move(50, 820)
        self.v_sld.resize(500, 50)
        # self.v_sld.valueChanged.connect(self.v_slider_change)

        choose_img = QPushButton('Открыть', self)
        choose_img.move(700, 50)
        choose_img.clicked.connect(self.open_on_click)

        save_img = QPushButton('Сохранить', self)
        save_img.move(800, 50)
        save_img.clicked.connect(self.save_on_click)

        to_grey = QPushButton('RGB -> Grey', self)
        to_grey.move(700, 85)
        to_grey.clicked.connect(self.to_grey_on_click)

        to_red = QPushButton('RGB -> Red', self)
        to_red.move(800, 85)
        to_red.clicked.connect(self.to_red_on_click)

        to_green = QPushButton('RGB -> Green', self)
        to_green.move(700, 120)
        to_green.clicked.connect(self.to_green_on_click)

        to_blue = QPushButton('RGB -> Blue', self)
        to_blue.move(800, 120)
        to_blue.clicked.connect(self.to_blue_on_click)

        to_hsv = QPushButton('To HSV', self)
        to_hsv.move(700, 800)
        to_hsv.clicked.connect(self.to_hsv)

        self.show()


    def to_grey_on_click(self):
        img = self.pixmap.toImage()
        for x in range(img.width()):
            for y in range(img.height()):
                r = QColor(img.pixel(x, y)).red()
                g = QColor(img.pixel(x, y)).green()
                b = QColor(img.pixel(x, y)).blue()
                a = (0.2126 * r + 0.7152 * g + 0.0722 * b)
                img.setPixel(x, y, QColor(a, a, a).rgb())
        self.label.setPixmap(QPixmap(img))
        self.show()

    def to_red_on_click(self):
        img = self.pixmap.toImage()
        for x in range(img.width()):
            for y in range(img.height()):
                r = QColor(img.pixel(x, y)).red()
                img.setPixel(x, y, QColor(r, 0, 0).rgb())
        self.label.setPixmap(QPixmap(img))
        self.show()

    def to_green_on_click(self):
        img = self.pixmap.toImage()
        for x in range(img.width()):
            for y in range(img.height()):
                g = QColor(img.pixel(x, y)).green()
                img.setPixel(x, y, QColor(0, g, 0).rgb())
        self.label.setPixmap(QPixmap(img))
        self.show()

    def to_blue_on_click(self):
        img = self.pixmap.toImage()
        for x in range(img.width()):
            for y in range(img.height()):
                b = QColor(img.pixel(x, y)).blue()
                img.setPixel(x, y, QColor(0, 0, b).rgb())
        self.label.setPixmap(QPixmap(img))
        self.show()

    def refresh(self):
        print("refresh")

    def open_file_name_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Images (*.jpg *.jpeg *.png)", options=options)
        if filename:
            self.pixmap = QPixmap(filename).scaled(670, 500)

    # def h_slider_change(self, value):
        # self.hsv()

    # def s_slider_change(self, value):
        # self.hsv()

    # def v_slider_change(self, value):
        # self.hsv()

    def to_hsv(self):
        self.hsv()

    def hsv(self):
        img = self.pixmap.toImage()
        for x in range(img.width()):
            for y in range(img.height()):
                r = QColor(img.pixel(x, y)).red()
                g = QColor(img.pixel(x, y)).green()
                b = QColor(img.pixel(x, y)).blue()
                h, s, v = self.rgb2hsv(r, g, b)
                img.setPixel(x, y, QColor(h, s, v).rgb())
        self.label.setPixmap(QPixmap(img))
        self.show()

    def rgb2hsv(self, r, g, b):
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / df) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / df) + 120) % 360
        elif mx == b:
            h = (60 * ((r - g) / df) + 240) % 360
        if mx == 0:
            s = 0
        else:
            s = df / mx
        v = mx
        return h, s, v

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


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Colors()
    sys.exit(app.exec_())