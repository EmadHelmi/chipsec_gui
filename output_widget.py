# -*- coding: utf-8 -*-
import sys
import os

import platform
import time
import json

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from module_list import modules
from functools import partial
from modules import Modules

class OutPutWidget(QWidget):
    def __init__(self, parent):
        super(OutPutWidget, self).__init__(parent)
        self.all = False
        self.init_UI()

    def init_UI(self):
        # Bottom layout
        bottom_layout = QVBoxLayout()
        log_lable = QLabel("Output:")
        log_lable.setFont(QFont('SansSerif', 15))
        self.text_edit = QTextBrowser()
        self.text_edit.setFont(QFont('SansSerif', 10))

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignRight)

        sv_layout = QHBoxLayout()
        sv_layout.setAlignment(Qt.AlignRight)
        save_btn = QPushButton("Save Results")
        save_btn.clicked.connect(
            partial(self.save)
        )
        btn_layout.addWidget(save_btn)

        bottom_layout.addWidget(log_lable)
        bottom_layout.addWidget(self.text_edit)
        bottom_layout.addLayout(btn_layout)

        self.setLayout(bottom_layout)

    def save(self):
        directory = str(
            QFileDialog.getSaveFileName(
                self,
                'Select a file for saving the result',
                '.',
                selectedFilter='*.txt'
            )
        )
        if directory:
            f = open(directory, "w")
            f.write(str(self.text_edit.toPlainText()))
            f.close()