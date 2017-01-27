# -*- coding: utf-8 -*-
import sys
import os

import platform
import time
import json

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from module_list import modules
from category_list import categories
from functools import partial

class Cagtegories(QWidget):
    def __init__(self, parent):
        super(Cagtegories, self).__init__(parent)
        self.all_categories = list()
        self.init_UI()

    def init_UI(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(5)
        list_lable = QLabel(u"دسته بندی ها:")
        list_lable.setFont(QFont('SansSerif', 15))
        main_layout.addWidget(list_lable)
        i = 1
        for category in categories:
            horizontal_line = QFrame()
            horizontal_line.setFrameStyle(QFrame.HLine)
            horizontal_line.setSizePolicy(1000, 200)
            # checkBox = self.creat_checkBox(
            #     module['name'],
            #     partial(self.checkBox_toggled, module['name'])
            # )
            mdl = {}
            mdl['name'] = category['name']
            mdl['index'] = i-1

            table = QHBoxLayout()
            table.setAlignment(Qt.AlignRight | Qt.AlignLeading)

            right = QHBoxLayout()
            checkBox = QCheckBox()
            checkBox.stateChanged.connect(
                partial(self.checkBox_toggled, i-1)
            )
            lbl = QLabel(category['name'])
            mdl['is_selected'] = False

            info = QPushButton('')
            info.setIcon(QIcon("icons/info.png"))
            info.setIconSize(QSize(15, 15))
            info.clicked.connect(
                partial(self.show_info, i-1)
            )

            mdl['is_selected'] = False

            right.addWidget(lbl)
            right.addWidget(checkBox)
            right.addWidget(info)
            self.all_categories.append(mdl)

            table.addLayout(right)
            # table.addLayout(right)            

            main_layout.addLayout(table)
            i += 1
        self.setLayout(main_layout)

    def show_info(self, index):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(
            "<p align='justify'>%s</p>" % categories[index]['info'])
        msg.setWindowTitle("More details about the category")
        msg.exec_()

    def checkBox_toggled(self, index):
        sender = self.sender()
        if sender.isChecked():
            self.all_categories[index]['is_selected'] = True
        else:
            self.all_categories[index]['is_selected'] = False

    def checked_exec(self):
        self.checked_categories = list()
        for category in self.all_categories:
            if category['is_selected']:
                self.checked_categories.append(category)
        return self.checked_categories