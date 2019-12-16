import sys
from PyQt5.QtWidgets import *

app = QApplication(sys.argv)
print(sys.argv)
label = QLabel("PyQT First Test!")
label.show()

print("Before Loop")
app.exec_()
print("After Loop")
#이거 pyqt는 계속 무한루프 상태라서 처음에 띄운 상태에서는 Before만 뜨고, 뭔가 이벤트가 일어나면 After가 뜬다.