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
from output_widget import OutPutWidget

os_name = platform.system()


class AdvancedFormWidget(QWidget):
    def __init__(self, parent, text_edit):
        super(AdvancedFormWidget, self).__init__(parent)
        self.all = False
        self.text_edit = text_edit.text_edit
        self.init_UI()

    def init_UI(self):
        # Main layout
        main_layout = QGridLayout()
        main_layout.setSpacing(0)

        # Top layout
        top_layout = QVBoxLayout()
        top_layout.setContentsMargins(5, 0, 0, 0)

        self.b1 = QRadioButton(u"ماژول های انتخابی")
        self.b1.setChecked(True)
        self.b1.setFont(QFont('SansSerif', 15))
        self.b1.clicked.connect(
            partial(self.change_all, False)
        )

        path_layout = QHBoxLayout()
        lable = QLabel(u"دایرکتوری برای بارگذاری ماژول ها:")
        self.location = QLabel()
        additional_path = QPushButton(u"انتخاب دایرکتوری")
        additional_path.clicked.connect(self.path)
        
        path_layout.addWidget(additional_path)
        path_layout.addWidget(self.location, alignment=Qt.AlignRight)
        path_layout.addWidget(lable, alignment=Qt.AlignRight)

        self.b2 = QRadioButton(u"همه ماژول ها")
        self.b2.setFont(QFont('SansSerif', 15))
        self.b2.clicked.connect(
            partial(self.change_all, True)
        )

        top_layout.addWidget(self.b1, alignment=Qt.AlignRight)
        top_layout.addWidget(self.b2, alignment=Qt.AlignRight)
        top_layout.addLayout(path_layout)

        # Middle layout
        middle_layout = QVBoxLayout()
        m = Modules(self)

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignRight)
        run_btn = QPushButton("Run")
        run_btn.clicked.connect(
            partial(self.call_run, m)
        )
        btn_layout.addWidget(run_btn)

        middle_layout.addWidget(m)
        middle_layout.addLayout(btn_layout)

        main_layout.addLayout(top_layout, 0, 0)
        main_layout.addLayout(middle_layout, 1, 0)
        self.setLayout(main_layout)

    def change_all(self, state):
        self.all = state

    def path(self):
        directory = str(
            QFileDialog.getExistingDirectory(
                self,
                "Open a folder",
                ".",
                QFileDialog.ShowDirsOnly
            )
        )
        self.location.setText(directory)

    def call_run(self, m_obj):
        import chipsec_main
        custom_modules = m_obj.checked_exec()
        print json.dumps(custom_modules[0], indent=1)
        result = str()
        if os.path.exists("log.txt"):
            if os_name.lower() != 'linux':
                f = open("log.txt", 'w')
                f.write("")
                f.close()
            else:
                os.remove("log.txt")        
        if self.all:
            try:
                chipsec_main.main(['-l', 'log.txt'])
            except:
                result = "Operation not permitted! Please make sure you are admin"
                self.text_edit.setText(result)
                return
            f = open('log.txt', 'r+')
            self.text_edit.setText(f.read())
            if os_name.lower() != 'linux':
                f.write("")
                f.close()
            else:
                f.close()
                os.remove("log.txt")                    
        else:
            for custom_module in  custom_modules:
                command = list()
                for module in modules:
                    if custom_module['name'] == module['name']:
                        command.append('-m')
                        command.append(module['cmd'])

                        if custom_module['has_arg']:
                            command.append('-a')
                            command.append(custom_module['args'])

                        command.append('-l')
                        command.append('log.txt')

                        if custom_module['xml']:
                            command.append('-x')
                            command.append(custom_module['xml_file'])

                        if custom_module['ignore_platform']:
                            command.append('-i')

                        if custom_module['no_time']:
                            command.append('--no_time')

                        if custom_module['verbose']:
                            command.append('-v')

                        if custom_module['driver']:
                            command.append('-n')

                        if custom_module['fail_fast']:
                            command.append('--failfast')

                        if custom_module['platform']:
                            command.append('-p')
                            command.append(custom_module['platform_type'])

                        if custom_module['module_type']:
                            command.append('-t')
                            # Moonde

                        if custom_module['debug']:
                            command.append('-d')

                        if custom_module['list_tags']:
                            command.append('--list_tags')

                        if custom_module['include']:
                            command.append('-I')
                            command.append(str(self.location.text()))

                        print "Command: chipsec_main.main(%s)" %str(command)
                        chipsec_main.main(command)
                        f = open('log.txt', 'r+')
                        t = f.read()
                        s = t.split('running module')
                        # r = s[1].split('[CHIPSEC] ***************************  SUMMARY  ***************************')
                        try:
                            result += "[*] running module" + s[1] # r[0]
                        except:
                            result = "Operation not permitted! Please make sure you are admin"
                            self.text_edit.setText(result)
                            return
                        if os_name.lower() != 'linux':
                            f.write("")
                            f.close()
                        else:
                            f.close()
                            os.remove('log.txt')
            self.text_edit.setText(result)