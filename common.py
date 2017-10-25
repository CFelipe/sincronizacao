from threading import Thread
from time import sleep
import random

person_id = 0

SCALE = 0.01

def useBathroom():
    sleep(random.uniform(30 * SCALE, 90 * SCALE))

class Person:
    def __init__(self):
        global person_id
        self.gender = 'M' if random.randint(0, 1) else 'W'
        self.name = "{} {}".format(("Homem" if self.gender == 'M' else "Mulher"), person_id)
        person_id += 1

def main(personThread):
    threads = []
    for _ in range(50):
        threads.append(Thread(target=personThread))

    for thread in threads:
        thread.start()
        sleep(random.uniform(10 * SCALE, 30 * SCALE))

    for thread in threads:
        thread.join()

    print("Pronto.")
