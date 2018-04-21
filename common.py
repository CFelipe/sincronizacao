from collections import deque
from threading import Thread
from time import sleep
import random
import argparse
import csv

SCALE = 0.01
MAX_NAME_LENGTH = 8
EMPTYSTR = MAX_NAME_LENGTH * "_"

names = {'W': deque(), 'M': deque()}

def getRandomName(gender):
    name = names[gender].popleft()
    names[gender].append(name)
    return name

def loadNames():
    with open("names.csv") as csvfile:
        reader = csv.reader(csvfile)
        for m_name, w_name in reader:
            if len(m_name) <= 5: names['M'].append(m_name)
            if len(w_name) <= 5: names['W'].append(w_name)

    random.shuffle(names['M'])
    random.shuffle(names['W'])

def useToilet():
    sleep(random.uniform(30 * SCALE, 90 * SCALE))

class Toilet:
    def __init__(self, limit):
        self.counter = 0
        # EMPTYSTR é usado pra detectar que um espaço do
        # banheiro está vazio.
        self.list = [EMPTYSTR] * limit

    def getCurrentGender(self):
        i = 0
        for p in self.list:
            i = i + 1
            if p != EMPTYSTR:
                return p.gender
        return None

    def enter(self, person):
        idx = self.list.index(EMPTYSTR) # índice do primeiro espaço vazio
        self.list[idx] = person
        print([p if p == EMPTYSTR else p.name.ljust(MAX_NAME_LENGTH) for p in self.list], "{} entrou".format(person.name), sep = " | ")
        self.counter += 1

    def leave(self, person):
        idx = self.list.index(person)
        self.list[idx] = EMPTYSTR
        print([p if p == EMPTYSTR else p.name.ljust(MAX_NAME_LENGTH) for p in self.list], "{} saiu".format(person.name), sep = " | ")
        self.counter -= 1

    def empty(self):
        return self.counter == 0

class Person:
    def __init__(self):
        self.gender = 'M' if random.randint(0, 1) else 'W'
        self.name = getRandomName(self.gender)

def main(strategy_class):
    loadNames()
    parser = argparse.ArgumentParser(description='Um banheiro mais ou menos unissex')
    parser.add_argument('-l', metavar='limite', required=False, type=int,
                        help='lotação do banheiro', default=5)

    args = parser.parse_args()

    strategy = strategy_class(limit=args.l)

    threads = []
    for _ in range(100):
        threads.append(Thread(target=strategy.personThread))

    for thread in threads:
        thread.start()
        sleep(random.uniform(10 * SCALE, 30 * SCALE))

    for thread in threads:
        thread.join()

    print("Pronto.")
