from common import *
import random
from time import sleep
from threading import Lock

bathroom_limit = 5
bath_lock = Lock()
bathroom = []

def person():
    person = Person()

    while True:
        bath_lock.acquire()
        if not (bathroom and bathroom[0].gender != person.gender or len(bathroom) >= bathroom_limit):
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
    main(person)
