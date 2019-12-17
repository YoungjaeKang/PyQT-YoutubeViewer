import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QUrl
from lib.YouViewerLayout import Ui_MainWindow
from lib.AuthDialog import AuthDialog

from pytube import YouTube
import pytube
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
        # 재생 여부
        self.is_play = False
        # 유튜브 관련 작업
        self.youtb = None
        self.youtb_fsize = 0

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

    # 시그널 초기화
    def initSignal(self):
        self.loginButton.clicked.connect(self.authCheck)
        self.previewButton.clicked.connect(self.load_url)
        self.exitButton.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.webEngineView.loadProgress.connect(self.showProgressBrowserLoading)
        self.fileNavButton.clicked.connect(self.selectDownPath)
        self.calendarWidget.clicked.connect(self.appendDate)
        self.startButton.clicked.connect(self.downloadYoutb)

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
            self.append_log_msg("Login Success")
        else:
            QMessageBox.about(self, "인증 오류", "아이디 또는 비밀번호 오류")

    def load_url(self):
        url = self.urlTextEdit.text().strip()
        v = re.compile('http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?')
        if self.is_play:
            self.append_log_msg('Stop Playing')
            self.webEngineView.load(QUrl('about:blank'))
            self.previewButton.setText("Play")
            self.is_play = False
            self.urlTextEdit.clear()
            self.urlTextEdit.setFocus(True)
            self.startButton.setEnabled(False)
            self.streamCombobox.clear()
            self.progressBar_3.setValue(0)
            self.showStatusMsg("인증 완료")
        else:
            if v.match(url) is not None:
                self.append_log_msg('Now Playing')
                self.webEngineView.load(QUrl(url))
                self.showStatusMsg(url + " 재생 중")
                self.previewButton.setText("Stop")
                self.is_play = True
                self.startButton.setEnabled(True)
                self.initialYouWork(url)
            else:
                QMessageBox.about(self, "URL 형식 오류", "Youtube 주소 형식이 아닙니다.")
                self.urlTextEdit.clear()
                self.urlTextEdit.setFocus(True)

    def initialYouWork(self, url):
        video_list = pytube.YouTube(url)
        # 로딩바 계산
        video_list.register_on_progress_callback(self.showProgressDownLoading)
        self.youtb = video_list.streams.all()
        self.streamCombobox.clear()
        for q in self.youtb:
            # print('step1', q.itag, q.mime_type, q.abr)
            tmp_list, str_list = [], []
            tmp_list.append(str(q.mime_type or ''))
            tmp_list.append(str(q.res or ''))
            tmp_list.append(str(q.fps or ''))
            tmp_list.append(str(q.abr or ''))

            # print('setp2', tmp_list)
            str_list = [x for x in tmp_list if x != '']
            # print('step3', str_list)
            self.streamCombobox.addItem(', '.join(str_list))

    def append_log_msg(self, act):
        now = datetime.datetime.now()
        nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
        app_msg = self.user_id + ' : ' + act + ' - (' + nowDatetime + ')' 
        print(app_msg)
        self.plainTextEdit.appendPlainText(app_msg) #insertPlainText는 줄바꿈 x

        # 활동 로그 저장 (또는 DB 사용 추천)
        with open('log/log.txt', 'a') as f:
            f.write(app_msg + '\n')
    
    @pyqtSlot(int)
    def showProgressBrowserLoading(self, v):
        self.progressBar.setValue(v)

    @pyqtSlot()
    def selectDownPath(self):
        # 파일 선택하는 방법
        # fname = QFileDialog.getOpenFileName(self)
        # self.pathTextEdit.setText(fname[0])

        # 경로 선택하는 방법
        fpath = QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.pathTextEdit.setText(fpath)

    @pyqtSlot()
    def appendDate(self):
        cur_date = self.calendarWidget.selectedDate()
        # print('click date', self.calendarWidget.selectedDate().toString())
        # print('cur_date', cur_date)
        # print(str(cur_date.year()) + '-' + str(cur_date.month()) + '-' + str(cur_date.day()))
        self.append_log_msg('Calendar Click')

    @pyqtSlot()
    def downloadYoutb(self):
        down_dir = self.pathTextEdit.text().strip()
        if down_dir is None or down_dir == '' or not down_dir:
            QMessageBox.about(self, '경로 선택', '다운로드 받을 경로를 선택하세요.')
            # self.pathTextEdit.setFocus(True) 어차피 read_only라서 포커스 안됨
            return None

        self.youtb_fsize = self.youtb[self.streamCombobox.currentIndex()].filesize
        # print('fsize', self.youtb_fsize)
        self.youtb[self.streamCombobox.currentIndex()].download(down_dir)
        self.append_log_msg('Download Click')

    def showProgressDownLoading(self, stream, chunk, file_handle, bytes_remaining):
        # print(int(self.youtb_fsize - bytes_remaining))
        # print('bytes_remaining', bytes_remaining)
        self.progressBar_3.setValue(int(((self.youtb_fsize - bytes_remaining) / self.youtb_fsize) * 100))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    you_viewer_main = Main()
    you_viewer_main.show()
    app.exec_()