# SPDX-License-Identifier: GPL-3.0-or-later

from threading import Condition, Lock, Thread

from concurrent.futures import ThreadPoolExecutor


class ThreadProvider:
    def __init__(self):
        # for futures use built in thread pool
        self.thread_pool = ThreadPoolExecutor()

        # for manager thread syncronization
        self.sync_lock = Lock()
        self.cv = Condition(self.sync_lock)
        self.ended = False

        # manager thread
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

    def get_future_from(self, function, **params):
        return self.thread_pool.submit(function, **params)

    def new_thread(self, function, daemon, params=None):
        with self.sync_lock:
            if params:
                args = [params]
            else:
                args = ()
            thread = Thread(target=function, daemon=daemon, args=args)
            thread.start()
            self.threads.append(thread)
