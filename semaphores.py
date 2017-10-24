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
men_condition = Condition()
women_condition = Condition()
bathroom = []

def man():
    person = Person('M')

    with men_condition:
        while bathroom and bathroom[0].sex == 'W':
            men_condition.wait()

        bath_semaphore.acquire()
        bathroom.append(person)
        print([p.name for p in bathroom], "{} entrou".format(person.name), sep = " | ")

    useBathroom()

    with men_condition:
        with women_condition:
            bathroom.remove(person)
            print([p.name for p in bathroom], "{} saiu".format(person.name), sep = " | ")
            bath_semaphore.release()
            if not bathroom:
                men_condition.notify()
                women_condition.notify()

def woman():
    person = Person('W')

    with women_condition:
        while bathroom and bathroom[0].sex == 'M':
            women_condition.wait()

        bath_semaphore.acquire()
        bathroom.append(person)
        print([p.name for p in bathroom], "{} entrou".format(person.name), sep = " | ")

    useBathroom()

    with women_condition:
        with men_condition:
            bathroom.remove(person)
            print([p.name for p in bathroom], "{} saiu".format(person.name), sep = " | ")
            bath_semaphore.release()
            if not bathroom:
                men_condition.notify()
                women_condition.notify()

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
