from threading import Thread
import time
import urllib


def check_connection(url):
    try:
        urllib.request.urlopen(url, timeout=50)
        return True
    except:
        return False


class InternetProvider(Thread):
    def __init__(self, global_state, callback):
        self.global_state = global_state
        self.callback = callback

        # TODO get from config
        # self.url = self.global_state.get_internet_checker_url()
        self.url = 'http://nmcheck.gnome.org/check_network_status.txt'

        # connection locking
        self.connected = False

        # start internet connection checking
        self._start_connection_checker()
        self.global_state.start_standalone_thread(self._poll, True)

    def _start_connection_checker(self):
        self.connection_checker = self.global_state.get_future_from(check_connection, url=self.url)

    def _poll(self):
        while not self.connected:
            if not self.connection_checker.done():
                time.sleep(0.5)  # wait 500ms
            else:
                self.connected = self.connection_checker.result()

                if not self.connected:
                    # restart checker
                    self._start_connection_checker()
        self.callback()
