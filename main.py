import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import uic
from lib.YouViewerLayout import Ui_MainWindow

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
        self.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    you_viewer_main = Main()
    you_viewer_main.show()
    app.exec_()