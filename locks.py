import random
from time import sleep
from threading import Thread, Lock

SCALE = 0.01

def useBathroom():
    sleep(random.uniform(30 * SCALE, 90 * SCALE))

person_id = 0

class Person:
    def __init__(self, sex):
        self.sex = sex
        global person_id
        self.name = "{} {}".format(("Homem" if sex == 'M' else "Mulher"), person_id)
        person_id += 1

bath_lock = Lock()
bathroom = []
bathroom_limit = 5

def man():
    person = Person('M')

    while True:
        bath_lock.acquire()
        if not (bathroom and bathroom[0].sex == 'W' or len(bathroom) >= bathroom_limit):
            bathroom.append(person)
            print([p.name for p in bathroom], "{} entrou".format(person.name), sep = " | ")
            bath_lock.release()
            break
        bath_lock.release()

    useBathroom()

    bath_lock.acquire()
    bathroom.remove(person)
    print([p.name for p in bathroom], "{} saiu".format(person.name), sep = " | ")
    bath_lock.release()

def woman():
    person = Person('W')

    while True:
        bath_lock.acquire()
        if not (bathroom and bathroom[0].sex == 'M' or len(bathroom) >= bathroom_limit):
            bathroom.append(person)
            print([p.name for p in bathroom], "{} entrou".format(person.name), sep = " | ")
            bath_lock.release()
            break
        bath_lock.release()

    useBathroom()

    bath_lock.acquire()
    bathroom.remove(person)
    print([p.name for p in bathroom], "{} saiu".format(person.name), sep = " | ")
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
        sleep(random.uniform(10 * SCALE, 30 * SCALE))

    for thread in threads:
        thread.join()

    print("Pronto.")
