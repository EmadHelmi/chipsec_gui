import sys
import os

import chipsec_main
import platform
import time
import json

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from modules import modules
from functools import partial

os_name = platform.system()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):

        # Actions
        exitAction = QAction(QIcon('exit.svg'), 'Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        # Menubar
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(exitAction)

        tab_widget = QTabWidget(self)

        output = OutPutWidget(self)
        output.setFont(QFont('SansSerif', 10))

        form = FormWidget(self, output)
        form.setFont(QFont('SansSerif', 10))

        scroll = QScrollArea()
        scroll.setWidget(form)
        tab_widget.addTab(scroll, "Inputs")
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


class FormWidget(QWidget):
    def __init__(self, parent, text_edit):
        super(FormWidget, self).__init__(parent)
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

        self.b1 = QRadioButton("Custom modules")
        self.b1.setChecked(True)
        self.b1.setFont(QFont('SansSerif', 15))
        self.b1.clicked.connect(
            partial(self.change_all, False)
        )

        self.b2 = QRadioButton("All modules")
        self.b2.setFont(QFont('SansSerif', 15))
        self.b2.clicked.connect(
            partial(self.change_all, True)
        )

        top_layout.addWidget(self.b1)
        top_layout.addWidget(self.b2)

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

    def call_run(self, m_obj):
        custom_modules = m_obj.checked_exec()
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
        list_lable = QLabel("List of Modules:")
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
            args.stateChanged.connect(
                partial(self.verbose_toggled, i-1)
            )
            verbose.setFixedWidth(150)
            mdl['verbose'] = False

            debug = QCheckBox("Show Debug Output")
            args.stateChanged.connect(
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
            args.stateChanged.connect(
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
            args.stateChanged.connect(
                partial(self.driver_toggled, i-1)
            )
            mdl['driver'] = False

            ignore_platform = QCheckBox("Ignore Platform")
            args.stateChanged.connect(
                partial(self.ignore_toggled, i-1)
            )
            mdl['ignore_platfrom'] = False

            xml = QCheckBox("XML:")
            args.stateChanged.connect(
                partial(self.xml_toggled, i-1)
            )
            mdl['xml'] = False

            xml_list = QLineEdit()
            xml_list.textEdited.connect(
                partial(self.xml_editLine_changed, i-1)
            )
            mdl['xml_file'] = str()

            moduletype = QCheckBox("Module Type")
            args.stateChanged.connect(
                partial(self.module_toggled, i-1)
            )
            mdl['module_type'] = False

            list_tags = QCheckBox("List Tags")
            args.stateChanged.connect(
                partial(self.tags_toggled, i-1)
            )
            mdl['list_tags'] = False

            include = QCheckBox("Include")
            args.stateChanged.connect(
                partial(self.include_toggled, i-1)
            )
            mdl['include'] = False

            failfast = QCheckBox("Fail Fast")
            args.stateChanged.connect(
                partial(self.failFast_toggled, i-1)
            )
            mdl['fail_fast'] = False

            no_time = QCheckBox("No Time")
            args.stateChanged.connect(
                partial(self.time_toggled, i-1)
            )
            mdl['no_time'] = False

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
        # print self.checked_modules

    def checkBox_toggled(self, index):
        sender = self.sender()
        if sender.isChecked():
            self.all_modules[index]['is_selected'] = True
        else:
            self.all_modules[index]['is_selected'] = False

    def editLine_changed(self, index, module):
        sender = self.sender()
        self.all_modules[index]['args'] = str(sender.text())

    def verbose_toggled(self, index, module):
        sender = self.sender()
        if sender.isChecked():
            self.all_modules[index]['verbose'] = True
        else:
            self.all_modules[index]['verbose'] = False

    def debug_toggled(self, index, module):
        sender = self.sender()
        if sender.isChecked():
            self.all_modules[index]['debug'] = True
        else:
            self.all_modules[index]['debug'] = False

    def platform_toggled(self, index, module):
        sender = self.sender()
        if sender.isChecked():
            self.all_modules[index]['platform'] = True
        else:
            self.all_modules[index]['platform'] = False

    def menu_changed(self, index, module):
        sender = self.sender()
        self.all_modules[index]['platform_type'] = str(sender.currentText())

    def driver_toggled(self, index, module):
        sender = self.sender()
        if sender.isChecked():
            self.all_modules[index]['driver'] = True
        else:
            self.all_modules[index]['driver'] = False

    def ignore_toggled(self, index, module):
        sender = self.sender()
        if sender.isChecked():
            self.all_modules[index]['ignore_platform'] = True
        else:
            self.all_modules[index]['ignore_platform'] = False

    def xml_toggled(self, index, module):
        sender = self.sender()
        if sender.isChecked():
            self.all_modules[index]['xml'] = True
        else:
            self.all_modules[index]['xml'] = False

    def xml_editLine_changed(self, index, module):
        sender = self.sender()
        self.all_modules[index]['xml_file'] = str(sender.text())

    def module_toggled(self, index, module):
        sender = self.sender()
        if sender.isChecked():
            self.all_modules[index]['module_type'] = True
        else:
            self.all_modules[index]['module_type'] = False

    def tags_toggled(self, index, module):
        sender = self.sender()
        if sender.isChecked():
            self.all_modules[index]['list_tags'] = True
        else:
            self.all_modules[index]['list_tags'] = False

    def include_toggled(self, index, module):
        sender = self.sender()
        if sender.isChecked():
            self.all_modules[index]['include'] = True
        else:
            self.all_modules[index]['include'] = False

    def failFast_toggled(self, index, module):
        sender = self.sender()
        if sender.isChecked():
            self.all_modules[index]['fail_fast'] = True
        else:
            self.all_modules[index]['fail_fast'] = False

    def time_toggled(self, index, module):
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


def main():

    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()