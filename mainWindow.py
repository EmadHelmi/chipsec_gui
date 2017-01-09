import sys
import os

import chipsec_main
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from modules import modules
from functools import partial


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

        aboutMeAction = QAction(QIcon('about_me.png'), 'About Developer', self)
        aboutMeAction.setStatusTip('About project and developer')
        aboutMeAction.triggered.connect(self.showAboutMe)

        # Menubar
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(exitAction)

        helpMenu = menubar.addMenu('Help')
        helpMenu.addAction(aboutMeAction)

        form = FormWidget(self)
        form.setFont(QFont('SansSerif', 7))
        self.setCentralWidget(form)
        
        self.setWindowTitle('Chipsec')
        self.showMaximized()

    def closeEvent(self, event):
        pass
        # reply = QMessageBox.question(
        #     self,
        #     'Message',
        #     "Are you sure to quit?",
        #     QMessageBox.Yes | QMessageBox.No,
        #     QMessageBox.No
        # )
        # if reply == QMessageBox.Yes:
        #     event.accept()
        # else:
        #     event.ignore()

    def showAboutMe(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Emad Helmi")
        msg.setInformativeText(
            "Email:" + "\n" + "\t" + "s.emad.helmi@gmail.com" + "\n"
            "Telegram:" + "\n" + "\t" + "@Emad.Helmi"
        )
        msg.setWindowTitle("About the developer")
        msg.resize(800, 600)
        retval = msg.exec_()


class FormWidget(QWidget):
    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.all = False
        self.init_UI()

    def init_UI(self):
        # Main layout
        main_layout = QGridLayout()
        main_layout.setSpacing(0)

        # Top layout
        top_layout = QVBoxLayout()
        top_layout.setContentsMargins(10, 0, 0, 0)

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
        middle_layout.setSpacing(0)
        m = Modules(self)

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignRight)
        run_btn = QPushButton("Run")
        run_btn.clicked.connect(
            partial(self.call_run, m.checked_modules)
        )
        btn_layout.addWidget(run_btn)

        middle_layout.addWidget(m)
        middle_layout.addLayout(btn_layout)

        # Bottom layout
        bottom_layout = QVBoxLayout()
        bottom_layout.setSpacing(0)
        log_lable = QLabel("Output:")
        log_lable.setFont(QFont('SansSerif', 15))
        self.text_edit = QTextBrowser()
        self.text_edit.setFont(QFont('SansSerif', 10))

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignRight)
        save_btn = QPushButton("Save Results")
        save_btn.clicked.connect(
            partial(self.save)
        )
        btn_layout.addWidget(save_btn)

        bottom_layout.addWidget(log_lable)
        bottom_layout.addWidget(self.text_edit)
        bottom_layout.addLayout(btn_layout)

        main_layout.addLayout(top_layout, 0, 0)
        main_layout.addLayout(middle_layout, 1, 0)
        main_layout.addLayout(bottom_layout, 3, 0)
        self.setLayout(main_layout)

    def change_all(self, state):
        self.all = state
    
    def call_run(self, custom_modules):
        result = str()
        if os.path.exists("log.txt"):
            os.remove("log.txt")        
        if self.all:
            chipsec_main.main(['-l', 'log.txt'])
            f = open('log.txt', 'r')
            self.text_edit.setText(f.read())
            os.remove("log.txt")
            f.close()
        else:
            for custom_module in  custom_modules:
                for module in modules:
                    if custom_module['name'] == module['name']:
                        chipsec_main.main(['-m', module['cmd'], '-l', 'log.txt'])
                        f = open('log.txt', 'r')
                        t = f.read()
                        s = t.split('running module')
                        # r = s[1].split('[CHIPSEC] ***************************  SUMMARY  ***************************')
                        result += "[*] running module" + s[1] # r[0]
                        f.close()
                        os.remove("log.txt")
            self.text_edit.setText(result)

    def save(self):
        f = open("log.txt", "w")
        f.write(str(self.text_edit.toPlainText()))
        f.close()


class Modules(QWidget):
    def __init__(self, parent):
        super(Modules, self).__init__(parent)
        self.checked_modules = list()
        self.all_modules = list()
        self.args_list = list()
        self.args = list()
        self.init_UI()

    def init_UI(self):
        main_layout = QGridLayout()
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignLeft)
        list_lable = QLabel("List of Modules:")
        list_lable.setFont(QFont('SansSerif', 15))
        main_layout.addWidget(list_lable, 0, 0)
        i = 1
        for module in modules:
            # checkBox = self.creat_checkBox(
            #     module['name'],
            #     partial(self.checkBox_toggled, module['name'])
            # )
            checkBox = QCheckBox(module['name'])
            checkBox.stateChanged.connect(
                partial(self.checkBox_toggled, i-1)
            )
            self.all_modules.append(checkBox)
            
            h_group = QButtonGroup(self)
            no_args = QRadioButton("No Argument")
            no_args.clicked.connect(
                partial(self.radioButton_changed, i-1, False)
            )
            no_args.setChecked(True)
            args = QRadioButton("Arguments:")
            args.clicked.connect(
                partial(self.radioButton_changed, i-1, True)
            )

            h_group.addButton(no_args)
            h_group.addButton(args)
            self.args.append(False)
            
            # args_list = self.creat_editLine(
            #     partial(self.editLine_changed, module['name'])
            # )
            args_list = QLineEdit()
            args_list.textEdited.connect(
                partial(self.editLine_changed, i-1, module['name'])
            )
            self.args_list.append(str(args_list.text()))
            main_layout.addWidget(checkBox, i, 0)
            main_layout.addWidget(no_args, i, 5)
            main_layout.addWidget(args, i, 6)
            main_layout.addWidget(args_list, i, 7)
            i += 1
        self.setLayout(main_layout)

    def radioButton_changed(self, index, state):
        sender = self.sender()
        if self.args[index] != state:
            self.args[index] = state
            if state:
                for checked_module in self.checked_modules:
                    if checked_module['index'] == index:
                        checked_module['state'] = state
        # print self.checked_modules

    def checkBox_toggled(self, index):
        sender = self.sender()
        if sender.isChecked():
                self.checked_modules.append(
                    {
                        'name': str(sender.text()),
                        'args': self.args_list[index],
                        'index': index,
                        'state': self.args[index]
                    }
                )
        else:
            for checked_module in self.checked_modules:
                if checked_module['name'] == str(sender.text()):
                    self.checked_modules.remove(checked_module)
        # print self.checked_modules
        # QMessageBox.question(
        #     self,
        #     'Message',
        #     str(self.checked_modules),
        #     QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        #     )

    # def creat_checkBox(self, text, member):
    #     checkBox = QCheckBox(text)
    #     checkBox.stateChanged.connect(member)
    #     return checkBox

    # def creat_editLine(self, member):
    #     edit_line = QLineEdit()
    #     edit_line.textEdited.connect(member)
    #     return edit_line
    def editLine_changed(self, index, module):
        sender = self.sender()
        self.args_list[index] = str(sender.text())
        for checked_module in self.checked_modules:
            if checked_module['name'] == module:
                checked_module['args'] = str(sender.text())
        # print self.checked_modules
        # print "$" * 10
        # print "ARGS CHANGED!"
        # print "ARGS:"
        # print self.args_list
        # print "CHECKED:"
        # print self.checked_modules
        # print "$" * 10

def main():

    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()