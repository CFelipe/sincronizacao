from common import *
import random
from time import sleep
from threading import Thread, BoundedSemaphore, Condition

class SemaphoreStrategy:
    """Resolve o problema usando um semáforo e uma variável de condição"""

    def __init__(self, limit):
        self.toilet_limit = limit
        self.toilet_semaphore = BoundedSemaphore(self.toilet_limit)
        self.empty = Condition()
        self.toilet = Toilet(self.toilet_limit)

    def personThread(self):
        person = Person()

        with self.empty:
            while (not self.toilet.empty()) and self.toilet.getCurrentGender() != person.gender:
                print("{} está esperando".format(person.name))
                self.empty.wait()

        self.toilet_semaphore.acquire()
        self.toilet.enter(person)

        useToilet()

        self.toilet.leave(person)
        self.toilet_semaphore.release()
        if self.toilet.empty():
            with self.empty:
                self.empty.notify_all()

if __name__ == "__main__":
    main(SemaphoreStrategy)
