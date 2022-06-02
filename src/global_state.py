# SPDX-License-Identifier: GPL-3.0-or-later

from concurrent.futures import ThreadPoolExecutor
from .config import create_envs, init_config


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

    def advance(self, page):
        print('Advance called before window initalization compeleted!')

    def advance_without_return(self, page):
        print('Advance called before window initalization compeleted!')

    def send_notification(self, title, text):
        print('Notification sending called before window initalization compeleted!')

    def set_title_image(self, image_name=None, image_path=None):
        print('Setting of title image called before window initalization compeleted!')

    def installation_failed(self):
        print('Installation failed before window initalization compeleted!')

    def create_envs(self, with_install_envs=False, with_configure_envs=False):
        return create_envs(self.config, with_install_envs, with_configure_envs)


global_state = GlobalState()
