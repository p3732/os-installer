# SPDX-License-Identifier: GPL-3.0-or-later

from concurrent.futures import ThreadPoolExecutor
from .config import init_config


class GlobalState:
    config = init_config()
    demo_mode = False
    installation_running = False

    thread_pool = ThreadPoolExecutor()  # for futures

    def __init__(self):
        self.set_config('disk_name', 'Test Dummy')

    def get_config(self, setting):
        if setting in self.config:
            return self.config[setting]
        else:
            return None

    def set_config(self, setting, value):
        self.config[setting] = value

    def advance(self, name):
        print('Advance called before window initalization done!')

    def advance_without_return(self, name):
        print('Advance called before window initalization done!')


global_state = GlobalState()
