import queue
import threading
import time

class Factory:
    def __init__(self, func, tasks, workers = 16):
        assert type(tasks) == list
        self.func = func
        self.tasks = queue.deque(tasks)
        self.workers = [threading.Thread(target=self._job) for _ in range(0,workers)]
        self.done = False
        self.lock = threading.Lock()

    def _job(self):
        while True:
            try:
                task = self.tasks.pop()
                self.func(*task)
            except IndexError:
                return
            except KeyboardInterrupt:
                self.tasks = queue.deque([])
                return
            except Exception as e:
                self.log_error(str(e))

    def _job_monitor(self):
        while not self.done:
            alive = 0
            for worker in self.workers:
                if worker.is_alive():
                    alive += 1
            print(f"\rWorkers: {alive} Remaining: {len(self.tasks)}                                  ",end='')
            time.sleep(1)
        print()
        
    def log_error(self, message):
        self.lock.acquire()
        #open("error.log","a").write(message+'\n')
        print(message)
        self.lock.release()

    def start(self, wait=True):
        self.stop = False
        monitor = threading.Thread(target=self._job_monitor)
        monitor.start()
        for worker in self.workers:
            worker.start()
        for worker in self.workers:
            worker.join()
        self.done = True
        monitor.join()
   