from cmath import pi
from multiprocessing import Condition, Lock, Manager, Semaphore

class Table:
    def __init__(self, nphil, manager):
        self.mutex = Lock()
        self.size = nphil
        self.manager = manager
        self.phils = self.manager.list([False]*self.size)
        self.freefork = Condition(self.mutex)

    def set_current_phil(self, pid):
        self.curr_phil = pid

    def check_forks(self):
        return not self.phils[(self.curr_phil - 1) % self.size] and not self.phils[(self.curr_phil + 1) % self.size]

    def wants_eat(self, pid):
        self.mutex.acquire()
        self.freefork.wait_for(self.check_forks)
        self.phils[pid] = True
        self.mutex.release()

    def wants_think(self, pid):
        self.mutex.acquire()
        self.phils[pid] = False
        self.freefork.notify_all()
        self.mutex.release()

# Por que es necesario el mutex (?) (aparte de para la variable condicion)

class CheatMonitor:
    def __init__(self):
        self.mutex = Lock()
        self.manager = Manager()
        self.cheaters = self.manager.list([False]*2)
        self.other_eating = Condition(self.mutex)

    def is_eating(self, pid):
        self.mutex.acquire()
        self.cheaters[pid//2] = True
        self.other_eating.notify_all()
        self.mutex.release()

    def wants_think(self, pid):
        self.mutex.acquire()
        self.other_eating.wait_for(lambda: self.cheaters[1 if pid == 0 else 0])
        self.cheaters[pid//2] = False
        self.mutex.release()

# Sin empezar vvv

class AnticheatTable:
    def __init__(self, nphil, manager):
        self.mutex = Lock()
        self.size = nphil
        self.manager = manager
        self.phils = self.manager.list([False]*self.size)
        self.freefork = Condition(self.mutex)

    def set_current_phil(self, pid):
        self.curr_phil = pid

    def check_forks(self):
        return not self.phils[(self.curr_phil - 1) % self.size] and not self.phils[(self.curr_phil + 1) % self.size]

    def wants_eat(self, pid):
        self.mutex.acquire()
        self.freefork.wait_for(self.check_forks)
        self.phils[pid] = True
        self.mutex.release()

    def wants_think(self, pid):
        self.mutex.acquire()
        self.phils[pid] = False
        self.freefork.notify_all()
        self.mutex.release()