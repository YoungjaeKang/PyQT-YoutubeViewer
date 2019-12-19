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

# 데몬쓰레드 : (옵션 생략 시 기본 쓰레드)
t1 = threading.Thread(name="service-1", target=worker1)
t2 = threading.Thread(name="service-2", target=worker2, daemon=True)
t3 = threading.Thread(target=worker1, daemon=True)

if __name__ == '__main__':
    t1.start()
    t2.start()
    t3.start()


    # Join 메소드 호출로 쓰레드 종료 시 까지 대기
    t1.join() #join(시간) 시간 동안 대기
    t2.join()
    print('t3 : is_alive()', t3.is_alive()) #쓰레드가 소멸상태인지 확인
    t3.join()
    print('t1 : is_alive()', t1.is_alive()) #쓰레드가 소멸상태인지 확인