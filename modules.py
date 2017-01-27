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

class Modules(QWidget):
    def __init__(self, parent):
        super(Modules, self).__init__(parent)
        self.checked_modules = list()
        self.all_modules = list()
        self.args_list = list()
        self.args = list()
        self.platforms = "SNB IVB KBL JKT BYT QRK BDW IVT AVN CHT HSW SKL HSX".split(" ")

        self.init_UI()

    def init_UI(self):
        main_layout = QVBoxLayout()
        list_lable = QLabel(u"ماژول ها:")
        list_lable.setFont(QFont('SansSerif', 15))
        main_layout.addWidget(list_lable)
        i = 1
        for module in modules:
            horizontal_line    =  QFrame()
            horizontal_line.setFrameStyle(QFrame.HLine)
            horizontal_line.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
            # checkBox = self.creat_checkBox(
            #     module['name'],
            #     partial(self.checkBox_toggled, module['name'])
            # )
            mdl = {}
            mdl['name'] = module['name']

            table = QHBoxLayout()

            left = QVBoxLayout()
            checkBox = QCheckBox(module['name'])
            checkBox.stateChanged.connect(
                partial(self.checkBox_toggled, i-1)
            )
            checkBox.setFixedWidth(460)
            mdl['is_selected'] = False

            left.addWidget(checkBox)

            right = QVBoxLayout()
            right.setContentsMargins(200, 0, 0, 0)

            right_top = QHBoxLayout()

            args = QCheckBox("Arguments:")
            args.stateChanged.connect(
                partial(self.args_toggled, i-1)
            )
            mdl['has_arg'] = False

            args_list = QLineEdit()
            args_list.textEdited.connect(
                partial(self.editLine_changed, i-1)
            )
            args.setFixedWidth(150)
            args_list.setFixedWidth(150)
            mdl['args'] = str()

            verbose = QCheckBox("VerboseMode")
            verbose.stateChanged.connect(
                partial(self.verbose_toggled, i-1)
            )
            verbose.setFixedWidth(150)
            mdl['verbose'] = False

            debug = QCheckBox("Show Debug Output")
            debug.stateChanged.connect(
                partial(self.debug_toggled, i-1)
            )
            debug.setFixedWidth(150)
            mdl['debug'] = False

            right_top.addWidget(verbose)
            right_top.addWidget(debug)
            right_top.addWidget(args)
            right_top.addWidget(args_list)

            right_middle = QHBoxLayout()
            right_bottom = QHBoxLayout()

            platform = QCheckBox("Platform")
            platform.stateChanged.connect(
                partial(self.platform_toggled, i-1)
            )
            mdl['platform'] = False

            menu = QComboBox()
            for pf in self.platforms:
                menu.addItem(pf)
            menu.currentIndexChanged.connect(
                partial(self.menu_changed, i-1)
            )
            mdl['platform_type'] = "SNB"

            no_driver = QCheckBox("No Driver")
            no_driver.stateChanged.connect(
                partial(self.driver_toggled, i-1)
            )
            mdl['driver'] = False

            ignore_platform = QCheckBox("Ignore Platform")
            ignore_platform.stateChanged.connect(
                partial(self.ignore_toggled, i-1)
            )
            mdl['ignore_platform'] = False

            xml = QCheckBox("XML:")
            xml.stateChanged.connect(
                partial(self.xml_toggled, i-1)
            )
            mdl['xml'] = False

            xml_list = QLineEdit()
            xml_list.textEdited.connect(
                partial(self.xml_editLine_changed, i-1)
            )
            mdl['xml_file'] = str()

            moduletype = QCheckBox("Module Type")
            moduletype.stateChanged.connect(
                partial(self.module_toggled, i-1)
            )
            mdl['module_type'] = False

            list_tags = QCheckBox("List Tags")
            list_tags.stateChanged.connect(
                partial(self.tags_toggled, i-1)
            )
            mdl['list_tags'] = False

            failfast = QCheckBox("Fail Fast")
            failfast.stateChanged.connect(
                partial(self.failFast_toggled, i-1)
            )
            mdl['fail_fast'] = False

            no_time = QCheckBox("No Time")
            no_time.stateChanged.connect(
                partial(self.time_toggled, i-1)
            )
            mdl['no_time'] = False

            include = QCheckBox("Include")
            include.stateChanged.connect(
                partial(self.include_toggled, i-1)
            )
            mdl['include'] = False

            self.all_modules.append(mdl)

            right_middle.addWidget(platform)
            right_middle.addWidget(menu)
            right_middle.addWidget(no_driver)
            right_middle.addWidget(ignore_platform)
            right_middle.addWidget(xml)
            right_middle.addWidget(xml_list)
            right_bottom.addWidget(moduletype)
            right_bottom.addWidget(list_tags)
            right_bottom.addWidget(include)
            right_bottom.addWidget(failfast)
            right_bottom.addWidget(no_time)

            right.addLayout(right_top)
            right.addLayout(right_middle)
            right.addLayout(right_bottom)

            table.addLayout(left)
            table.addLayout(right)            

            main_layout.addLayout(table)
            main_layout.addWidget(horizontal_line)
            i += 1
        self.setLayout(main_layout)

    def args_toggled(self, index):
        sender = self.sender()
        if sender.isChecked():
            self.all_modules[index]['has_arg'] = True
        else:
            self.all_modules[index]['has_arg'] = False

    def checkBox_toggled(self, index):
        sender = self.sender()
        if sender.isChecked():
            self.all_modules[index]['is_selected'] = True
        else:
            self.all_modules[index]['is_selected'] = False

    def editLine_changed(self, index):
        sender = self.sender()
        self.all_modules[index]['args'] = str(sender.text())

    def verbose_toggled(self, index):
        sender = self.sender()
        print "Hi"
        if sender.isChecked():
            self.all_modules[index]['verbose'] = True
        else:
            self.all_modules[index]['verbose'] = False

    def debug_toggled(self, index):
        sender = self.sender()
        if sender.isChecked():
            self.all_modules[index]['debug'] = True
        else:
            self.all_modules[index]['debug'] = False

    def platform_toggled(self, index):
        sender = self.sender()
        if sender.isChecked():
            self.all_modules[index]['platform'] = True
        else:
            self.all_modules[index]['platform'] = False

    def menu_changed(self, index):
        sender = self.sender()
        self.all_modules[index]['platform_type'] = str(sender.currentText())

    def driver_toggled(self, index):
        sender = self.sender()
        if sender.isChecked():
            self.all_modules[index]['driver'] = True
        else:
            self.all_modules[index]['driver'] = False

    def ignore_toggled(self, index):
        sender = self.sender()
        if sender.isChecked():
            self.all_modules[index]['ignore_platform'] = True
        else:
            self.all_modules[index]['ignore_platform'] = False

    def xml_toggled(self, index):
        sender = self.sender()
        if sender.isChecked():
            self.all_modules[index]['xml'] = True
        else:
            self.all_modules[index]['xml'] = False

    def xml_editLine_changed(self, index):
        sender = self.sender()
        self.all_modules[index]['xml_file'] = str(sender.text())

    def module_toggled(self, index):
        sender = self.sender()
        if sender.isChecked():
            self.all_modules[index]['module_type'] = True
        else:
            self.all_modules[index]['module_type'] = False

    def tags_toggled(self, index):
        sender = self.sender()
        if sender.isChecked():
            self.all_modules[index]['list_tags'] = True
        else:
            self.all_modules[index]['list_tags'] = False

    def include_toggled(self, index):
        sender = self.sender()
        if sender.isChecked():
            self.all_modules[index]['include'] = True
        else:
            self.all_modules[index]['include'] = False

    def failFast_toggled(self, index):
        sender = self.sender()
        if sender.isChecked():
            self.all_modules[index]['fail_fast'] = True
        else:
            self.all_modules[index]['fail_fast'] = False

    def time_toggled(self, index):
        sender = self.sender()
        if sender.isChecked():
            self.all_modules[index]['no_time'] = True
        else:
            self.all_modules[index]['no_time'] = False

    def checked_exec(self):
        self.checked_modules = list()
        for module in self.all_modules:
            if module['is_selected']:
                self.checked_modules.append(module)
        # for checked_module in self.checked_modules:
        #     print json.dumps(checked_module, indent=1)
        return self.checked_modules