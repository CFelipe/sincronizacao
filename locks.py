import random
from time import sleep
from threading import Thread, Lock

SCALE = 0.01

def useBathroom():
    sleep(random.uniform(30 * SCALE, 90 * SCALE))

bath_lock = Lock()
bathroom = []
bathroom_limit = 5

def man():
    while True:
        bath_lock.acquire()
        if not (bathroom and bathroom[0] == 'W' or len(bathroom) >= bathroom_limit):
            bathroom.append('M')
            bath_lock.release()
            break
        bath_lock.release()

    useBathroom()

    bath_lock.acquire()
    bathroom.pop()
    bath_lock.release()

def woman():
    while True:
        bath_lock.acquire()
        if not (bathroom and bathroom[0] == 'M' or len(bathroom) >= bathroom_limit):
            bathroom.append('W')
            bath_lock.release()
            break
        bath_lock.release()

    useBathroom()

    bath_lock.acquire()
    bathroom.pop()
    bath_lock.release()

if __name__ == "__main__":
    threads = []
    for _ in range(50):
        if random.randint(0, 1):
            threads.append(Thread(target=man))
        else:
            threads.append(Thread(target=woman))

    for thread in threads:
        thread.start()
        print(bathroom)
        sleep(random.uniform(10 * SCALE, 30 * SCALE))

    for thread in threads:
        thread.join()

    print("Pronto.")
