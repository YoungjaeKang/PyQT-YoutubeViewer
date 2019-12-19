# 일정 시간 간격으로 반복 작업 가능한 예제
# 스크랩핑, 클로링, 확인성 작업 ...
import threading
import time

def thread_run():
    print('=====', time.ctime(), '=====')

    ###################################
    ##### 반복하고자 하는 코드 작성 #####
    ###################################

    for i in range(1, 10000):
        print('Threading running - ', i)
    
    threading.Timer(2.5, thread_run).start() # 재귀함수, 이걸 함수 외부에서 돌리면 1번으로 끝난다.

thread_run()
# 10000을 나눠 쓰레드로 돌리면서 반복하는 중!