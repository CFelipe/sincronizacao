from common import *
import random
from time import sleep
from threading import Lock

class LockStrategy:
    """Resolve o problema usando uma variável lock"""

    def __init__(self, limit):
        self.toilet_limit = limit
        self.toilet_lock = Lock()
        self.toilet = Toilet(self.toilet_limit)

    def personThread(self):
        person = Person()

        while True:
            self.toilet_lock.acquire()
            if not (not self.toilet.empty() and self.toilet.getCurrentGender() != person.gender or self.toilet.counter >= self.toilet_limit):
                self.toilet.enter(person)
                self.toilet_lock.release()
                break
            self.toilet_lock.release()

        useToilet()

        self.toilet_lock.acquire()
        self.toilet.leave(person)
        self.toilet_lock.release()

if __name__ == "__main__":
    main(LockStrategy)
