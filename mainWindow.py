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
from advance_form_widget import AdvancedFormWidget
from category_form_widget import CategoryFormWidget
from output_widget import OutPutWidget

os_name = platform.system()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):

        # Actions
        exitAction = QAction(QIcon('icons/exit.svg'), 'Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        font = QFont("BNazanin.ttf", 20, QFont.Bold, True)

        # Menubar
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(exitAction)

        tab_widget = QTabWidget(self)

        output = OutPutWidget(self)
        output.setFont(QFont('SansSerif', 10))

        advance_form = AdvancedFormWidget(self, output)
        advance_form.setFont(QFont('SansSerif', 10))

        advance_scroll = QScrollArea()
        advance_scroll.setWidget(advance_form)
        
        category_form = CategoryFormWidget(self, output)
        category_form.setFont(QFont('BNazanin.ttf', 15))

        category_scroll = QScrollArea()
        category_scroll.setWidget(category_form)
        category_scroll.setAlignment(Qt.AlignRight)

        tab_widget.addTab(category_scroll, "Category Mode")
        tab_widget.addTab(advance_scroll, "Advance Mode")
        tab_widget.addTab(output, "OutPuts")
        self.setCentralWidget(tab_widget)

        self.setWindowTitle('Chipsec')
        self.showMaximized()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            'Message',
            "Are you sure to quit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def main():

    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()