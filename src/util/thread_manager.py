from threading import Condition, Lock, Thread


class ThreadManager:
    def __init__(self):
        # for managment thread syncronization
        self.sync_lock = Lock()
        self.cv = Condition(self.sync_lock)
        self.ended = False

        self.threads = []
        self.manager_thread = Thread(target=self._manage)

    def __del__(self):
        print("thread mgmt deleter got called")
        with self.sync_lock:
            self.ended = True
        self.cv.notify()
        self.manager_thread.join()

    def _manage(self):
        with self.cv:
            while not self.ended:
                # check if any thread stopped meanwhile
                for index, thread in enumerate(self.threads):
                    if not thread.is_alive():
                        thread.join()
                        del self.threads[index]

                # rest for half a second
                self.cv.wait(0.5)

    ### public methods ###

    def new_thread(self, function, daemon, params=()):
        with self.sync_lock:
            thread = Thread(target=function, daemon=daemon, args=params)
            thread.start()
            self.threads.append(thread)
