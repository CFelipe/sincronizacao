import random
from time import sleep
from threading import Thread, BoundedSemaphore, Condition

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

bathroom_limit = 5
bath_semaphore = BoundedSemaphore(bathroom_limit)
empty = Condition()
bathroom = []

def man():
    person = Person('M')

    with empty:
        while bathroom and bathroom[0].sex == 'W':
            print("{} está esperando".format(person.name))
            empty.wait()

    bath_semaphore.acquire()
    bathroom.append(person)
    print([p.name for p in bathroom], "{} entrou".format(person.name), sep = " | ")

    useBathroom()

    bathroom.remove(person)
    print([p.name for p in bathroom], "{} saiu".format(person.name), sep = " | ")
    bath_semaphore.release()
    if not bathroom:
        with empty:
            empty.notify_all()

def woman():
    person = Person('W')

    with empty:
        while bathroom and bathroom[0].sex == 'M':
            print("{} está esperando".format(person.name))
            empty.wait()

    bath_semaphore.acquire()
    bathroom.append(person)
    print([p.name for p in bathroom], "{} entrou".format(person.name), sep = " | ")

    useBathroom()

    bathroom.remove(person)
    print([p.name for p in bathroom], "{} saiu".format(person.name), sep = " | ")
    bath_semaphore.release()
    if not bathroom:
        with empty:
            empty.notify_all()

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
