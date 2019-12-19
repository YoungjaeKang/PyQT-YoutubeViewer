import threading

# 쓰레드 실행 - 함수형

def thread_run():
    print("Thread Running - F")

def thread_run_msg(msg):
    print("Thread Running - F", msg)

for i in range(1000):
    t1 = threading.Thread(target=thread_run)
    t2 = threading.Thread(target=thread_run_msg, args=('service',))

    t1.start()
    t2.start()
    