import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from lib.YouViewerLayout import Ui_MainWindow
from lib.AuthDialog import AuthDialog

import re
import datetime



# 배포 시에는 상대경로로 해야 한다.
# import os
# os.path

# 일단 .ui 파일을 가져오고 form_class를 Main class에서 상속받으면 화면이 확인된다.
# 그 이후 .py로 변환 (pyuic5 -x you_viewer_v1.0.ui -o you_viewer_v1.0.py)하여 파이썬 파일을 import하면 된다.
# form_class = uic.loadUiType("C:/Users/Youngjae Kang/Documents/LocalProjects/section6/ui/section6.ui")[0]

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # 초기화
        self.setupUi(self)
        # 초기 잠금
        self.initAuthLock()
        # 시그널 초기화
        self.initSignal()
        # 로그인 관련 변수 선언
        self.user_id = None
        self.user_pw = None

    # 기본 UI 비활성화 (로그인하지 않은 경우)
    def initAuthLock(self):
        self.previewButton.setEnabled(False)
        self.fileNavButton.setEnabled(False)
        self.streamCombobox.setEnabled(False)
        self.streamCombobox.setEnabled(False)
        self.startButton.setEnabled(False)
        self.calendarWidget.setEnabled(False)
        self.urlTextEdit.setEnabled(False)
        self.pathTextEdit.setEnabled(False)
        self.showStatusMsg('인증되지 않음')

    # 기본 UI 활성화 (로그인한 경우)
    def initAuthActive(self):
        self.previewButton.setEnabled(True)
        self.fileNavButton.setEnabled(True)
        self.streamCombobox.setEnabled(True)
        self.streamCombobox.setEnabled(True)
        # self.startButton.setEnabled(True)
        self.calendarWidget.setEnabled(True)
        self.urlTextEdit.setEnabled(True)
        self.pathTextEdit.setEnabled(True)
        self.showStatusMsg('인증 완료')

    def showStatusMsg(self, msg):
        self.statusbar.showMessage(msg)

    def initSignal(self):
        self.loginButton.clicked.connect(self.authCheck)

    @pyqtSlot() # annotation
    def authCheck(self):
        dlg = AuthDialog()
        dlg.exec_()
        self.user_id = dlg.user_id
        self.user_pw = dlg.user_pw
        # print('test')

        # 이 부분에서 필요한 경우 실제 로컬 db 또는 구축된 서버에 call을 날려서 검증하는 과정 넣기
        # 유저 정보 및 사용 유효기간 체크하는 코드 추가
        # code
        # print('id: %s pw: %s' % (self.user_id, self.user_pw))

        if True:
            self.initAuthActive()
            self.loginButton.setText("인증 완료")
            self.loginButton.setEnabled(False)
            self.urlTextEdit.setFocus(True)
            

        else:
            QMessageBox.about(self, "인증 오류", "아이디 또는 비밀번호 오류")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    you_viewer_main = Main()
    you_viewer_main.show()
    app.exec_()