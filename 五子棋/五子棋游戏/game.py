from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from requests import post
from sys import argv
from start import Game
from json import load, dump


class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        # 初始化登录窗口的基本控件
        # 外观
        self.setWindowTitle('登陆')
        screen_size = [QApplication.desktop().screenGeometry().width(),
                       QApplication.desktop().screenGeometry().height()]
        self.setGeometry(screen_size[0] // 2 - 210, screen_size[1] // 2 - 125, 420, 310)
        self.setFixedSize(420, 310)
        # 设置基础控件
        self.host_label = QLabel('服务器地址', self)
        self.host_label.setFont(QFont('微软雅黑', 12, 75))
        self.host_label.setAlignment(Qt.AlignCenter)
        self.name_label = QLabel('用户id', self)
        self.name_label.setFont(QFont('微软雅黑', 12, 75))
        self.name_label.setAlignment(Qt.AlignCenter)
        self.paw_label = QLabel('密码', self)
        self.paw_label.setFont(QFont('微软雅黑', 12, 75))
        self.paw_label.setAlignment(Qt.AlignCenter)
        self.nick_label = QLabel('昵称', self)
        self.nick_label.setFont(QFont('微软雅黑', 12, 75))
        self.nick_label.setAlignment(Qt.AlignCenter)
        self.remember = QCheckBox('记住我', self)
        self.remember.setCheckable(True)
        self.remember.setChecked(True)
        self.remember.setStyleSheet("QCheckBox{color:#A020F0}")
        self.remember.setFont(QFont('微软雅黑', 13, 75))
        self.host = QLineEdit(self)
        self.name = QLineEdit(self)
        self.paw = QLineEdit(self)
        self.nick = QLineEdit(self)
        self.submit = QPushButton('提交', self)
        self.submit.clicked.connect(self.login_button)
        self.cancel = QPushButton('清空', self)
        self.cancel.clicked.connect(self.clear_text)
        self.set_login_style()
        # 添加到Layout
        self.host_label.move(50, 30)
        self.host.move(150, 30)
        self.name_label.move(50, 80)
        self.name.move(150, 80)
        self.paw_label.move(50, 130)
        self.paw.move(150, 130)
        self.nick_label.move(50, 180)
        self.nick.move(150, 180)
        self.submit.move(160, 250)
        self.cancel.move(290, 250)
        self.remember.move(70, 252)
        self.host.setText('http://127.0.0.1:5000/')
        info = self.load_info()
        if info:
            self.host.setText(info[0])
            self.name.setText(info[1])
            self.paw.setText(info[2])
            self.nick.setText(info[3])

    # 设定登陆窗口的控件style
    def set_login_style(self):
        self.host.setFixedSize(200, 30)
        self.host.setClearButtonEnabled(True)
        self.host.setToolTip('输入服务器IP地址')
        self.name.setFixedSize(200, 30)
        self.name.setClearButtonEnabled(True)
        self.name.setToolTip('输入id')
        self.paw.setFixedSize(200, 30)
        self.paw.setClearButtonEnabled(True)
        self.paw.setEchoMode(QLineEdit.Password)
        self.paw.setToolTip('输入密码')
        self.nick.setFixedSize(200, 30)
        self.nick.setClearButtonEnabled(True)
        self.nick.setToolTip('输入昵称,少于4字')
        self.submit.setFixedSize(58, 28)
        self.submit.setStyleSheet('QPushButton{background-color:lightgreen;border-radius:8px}')
        self.submit.setToolTip('登陆')
        self.cancel.setFixedSize(58, 28)
        self.cancel.setStyleSheet('QPushButton{background-color:pink;border-radius:8px}')
        self.cancel.setToolTip('清空输入')
        self.host.setFont(QFont('Microsoft YaHei', 10))
        self.name.setFont(QFont('Microsoft YaHei', 15))
        self.paw.setFont(QFont('Microsoft YaHei', 15))
        self.nick.setFont(QFont('Microsoft YaHei', 15))
        self.submit.setFont(QFont('微软雅黑', 11, 75))
        self.cancel.setFont(QFont('微软雅黑', 11, 75))

    def login_button(self):
        if self.host.text() and self.name.text() and self.paw.text() and self.nick.text():
            json = {
                'num': self.name.text(),
                'pwd': self.paw.text(),
                'nick': self.nick.text(),
            }
            response = post(self.host.text()+'login', json=json)
            if response.ok:
                if response.content.decode('utf-8') == 'ok':
                    if self.remember.isChecked():
                        self.dump_info()
                    else:
                        self.dump_info(True)
                    self.close()
                    new_game = Game(self.host.text(), self.name.text())
                    new_game.began()
                else:
                    QMessageBox.warning(self, '警告', '账号或密码错误！', QMessageBox.Ok, QMessageBox.Ok)

        else:
            QMessageBox.warning(self, '警告', '信息不能为空！', QMessageBox.Ok, QMessageBox.Ok)

    def load_info(self):
        fp = open('info.json', 'r', encoding='utf-8')
        s = load(fp)
        fp.close()
        return s

    def dump_info(self, clear=False):
        if clear:
            info = []
        else:
            info = [self.host.text(), self.name.text(), self.paw.text(), self.nick.text()]
        fp = open('info.json', 'w', encoding='utf-8')
        dump(info, fp)
        fp.close()

    def clear_text(self):
        pass


app = QApplication(argv)
c = Login()
c.show()
app.exec_()
