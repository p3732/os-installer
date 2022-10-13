# SPDX-License-Identifier: GPL-3.0-or-later

from concurrent.futures import ThreadPoolExecutor
import traceback
from .config import create_envs, init_config


class GlobalState:
    config = init_config()
    demo_mode = False
    installation_running = False

    thread_pool = ThreadPoolExecutor()  # for futures

    def __init__(self):
        self.set_config('disk_name', 'Test Dummy')

    def _uninitialized(self):
        print('Window method called before initialization.')
        traceback.print_stack()

    def get_config(self, setting):
        if setting in self.config:
            return self.config[setting]
        else:
            return None

    def set_config(self, setting, value):
        self.config[setting] = value

    def advance(self, *args):
        self._uninitialized()

    def load_translated_pages(self, *args):
        self._uninitialized()

    def navigate_to_page(self, *args):
        self._uninitialized()

    def reload_title_image(self, *args):
        self._uninitialized()

    def send_notification(self, *args):
        self._uninitialized()

    def installation_failed(self, *args):
        self._uninitialized()

    def create_envs(self, with_install_envs=False, with_configure_envs=False):
        return create_envs(self.config, with_install_envs, with_configure_envs)


global_state = GlobalState()
