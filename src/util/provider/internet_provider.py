# SPDX-License-Identifier: GPL-3.0-or-later

import time
from threading import Lock, Thread
from urllib.request import urlopen

from .global_state import global_state


def check_connection(url):
    try:
        urlopen(url, timeout=50)
        return True
    except:
        return False


class InternetProvider():
    callback_lock = Lock()
    callback = None

    def __init__(self):
        self.url = global_state.get_config('internet_checker_url')

        # connection locking
        self.connected = False

        # start internet connection checking
        self._start_connection_checker()
        self.thread = Thread(target=self._poll, daemon=True)
        self.thread.start()

    def _start_connection_checker(self):
        self.connection_checker = global_state.thread_pool.submit(check_connection, url=self.url)

    def _poll(self):
        connected = False
        while not connected:
            if not self.connection_checker.done():
                time.sleep(0.5)  # wait 500ms
            else:
                connected = self.connection_checker.result()

                if not connected:
                    # restart checker
                    self._start_connection_checker()

        with self.callback_lock:
            self.connected = connected
            if not self.callback is None:
                self.callback()

    ### public methods ###

    def is_connected_now_or_later(self, callback):
        ''' Returns `True` immidiately if connected. Otherwise returns False and calls callback when connected.'''
        with self.callback_lock:
            if self.connected:
                return True
            else:
                self.callback = callback
                return False


internet_provider = InternetProvider()
