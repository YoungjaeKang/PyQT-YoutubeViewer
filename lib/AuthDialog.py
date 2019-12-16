import sys
from PyQt5.QtWidgets import *

class AuthDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

        self.user_id = None
        self.user_pw = None

    def setupUI(self):
        self.setGeometry(600, 500, 300, 100)
        self.setWindowTitle("Sign In")
        self.setFixedSize(300, 100)

        label1 = QLabel("ID:")
        label2 = QLabel("PW:")

        self.lineEdit1 = QLineEdit()
        self.lineEdit2 = QLineEdit()
        self.lineEdit2.setEchoMode(QLineEdit().Password)

        self.pushButton = QPushButton("Sign In")
        self.pushButton.clicked.connect(self.submitLogin)


        layout = QGridLayout()
        layout.addWidget(label1, 0, 0)
        layout.addWidget(self.lineEdit1, 0, 1)
        layout.addWidget(self.pushButton, 0, 2)
        layout.addWidget(label2, 1, 0)
        layout.addWidget(self.lineEdit2, 1, 1)
        
        self.setLayout(layout)

    def submitLogin(self):
        self.user_id = self.lineEdit1.text()
        self.user_pw = self.lineEdit2.text()
        # print(self.user_id, self.user_pw)

        if self.user_id is None or self.user_id == '' or not self.user_id:
            QMessageBox.about(self, "인증 오류", "ID를 입력하세요")
            self.lineEdit1.setFocus(True)
            return None

        if self.user_id is None or self.user_pw == '' or not self.user_pw:
            QMessageBox.about(self, "인증 오류", "PW를 입력하세요")
            self.lineEdit2.setFocus(True)
            return None
        
        # 이 부분에서 필요한 경우 실제 로컬 db 또는 구축된 서버에 call을 날려서 검증하는 과정 넣기
        # 유저 정보 및 사용 유효기간 체크하는 코드 추가
        # code
        # code
        # 그러나 여기서 처리하기에는 너무 복잡하고 값을 부모 요소인 main.py으로 넘겨서 하는 게 깔끔함!

        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loginDialog = AuthDialog()
    loginDialog.show()
    app.exec_()