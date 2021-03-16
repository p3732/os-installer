# SPDX-License-Identifier: GPL-3.0-or-later

import time
from threading import Lock
from urllib.request import urlopen

from .global_state import global_state
from .thread_manager import thread_manager


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
        thread_manager.start_standalone_thread(self._poll, True)

    def _start_connection_checker(self):
        self.connection_checker = thread_manager.get_future_from(check_connection, url=self.url)

    def _poll(self):
        while not self.connected:
            if not self.connection_checker.done():
                time.sleep(0.5)  # wait 500ms
            else:
                self.connected = self.connection_checker.result()

                if not self.connected:
                    # restart checker
                    self._start_connection_checker()
        with self.callback_lock:
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
