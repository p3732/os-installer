# SPDX-License-Identifier: GPL-3.0-or-later

from threading import Condition, Lock, Thread

from concurrent.futures import ThreadPoolExecutor


class ThreadManager:
    ''' Singleton class that provides some threading utility functionality'''
    ended = False
    sync_lock = Lock()
    cv = Condition(sync_lock)
    thread_pool = ThreadPoolExecutor()  # for futures
    threads = []

    def __init__(self):
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

    def start_standalone_thread(self, function, daemon, params=None):
        with self.sync_lock:
            if params:
                args = [params]
            else:
                args = ()
            thread = Thread(target=function, daemon=daemon, args=args)
            thread.start()
            self.threads.append(thread)


thread_manager = ThreadManager()
