import threading
import time

def run(id):
    while True:
        print('id : {} '.format(id))
        time.sleep(0.3) # 동시에 돌아가는것을 보여주기위해 작성

a = "일"
b = "둘"
th1 = threading.Thread(target=run, args=(a))
th2 = threading.Thread(target=run, args=(b))

th1.start()
th2.start()

th1.join()
th2.join()
