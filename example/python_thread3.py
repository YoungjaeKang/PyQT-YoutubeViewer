# 로깅(Logging) 패키지를 활용한 예제
# 웹 개발, 서버 운영 os에서의 로그를 잘 쌓아놔야
import logging
import threading
import time

logging.basicConfig(   # INFO fatl error debug
    level = logging.DEBUG, format='[%(levelname)s (%(threadName)-8s) %(message)s]',
)

def worker1():
    logging.debug('Starting')
    time.sleep(0.5)
    logging.debug('Exiting')

def worker2():
    logging.debug('Starting')
    time.sleep(0.5)
    logging.debug('Exiting')

t1 = threading.Thread(name="service-1", target=worker1)
t2 = threading.Thread(name="service-2", target=worker2)
t3 = threading.Thread(target=worker1)
t4 = threading.Thread(target=worker2)


t1.start()
t2.start()
t3.start()
t4.start()

