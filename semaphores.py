from common import *
import random
from time import sleep
from threading import Thread, BoundedSemaphore, Condition

bathroom_limit = 5
bath_semaphore = BoundedSemaphore(bathroom_limit)
empty = Condition()
bathroom = []

def person():
    person = Person()

    with empty:
        while bathroom and bathroom[0].gender != person.gender:
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
    main(person)
