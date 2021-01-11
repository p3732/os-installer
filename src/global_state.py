from .config import get_config, check_install_config, check_post_install_config
from .thread_manager import ThreadManager

import subprocess
import os
from concurrent.futures import ThreadPoolExecutor


class GlobalState:
    def __init__(self):
        self.stack = None

        # configuration file loader
        self.config = get_config()

        # helper to manage proper threads
        self.thread_manager = ThreadManager()

        # for futures use built in thread pool
        self.thread_pool = ThreadPoolExecutor()

    ### installation stages ###

    def apply_language_settings(self):
        print('setting language to ', self.config['language'])
        # TODO
        # change via localectl?
        # At least load respective translations
        # subprocess.run(['localectl', 'set-locale', language])

    def apply_keyboard_layout(self, keyboard_layout, short_hand):
        keyboard_layout = self.config['keyboard_layout_short_hand']
        # change via localectl
        # subprocess.run(['localectl', 'set-keymap', short_hand])

    def apply_connected(self):
        # TODO start ntp and syncing of mirrors
        # subprocess.run(['timedatectl', 'set-ntp', 'true'])
        return

    def apply_installation_confirmed(self):
        # TODO start the actual installation
        return

    def apply_installed(self):
        # TODO start copying script
        return

    ### config functions ###

    def get_config(self, setting):
        return self.config[setting]

    def set_config(self, setting, value):
        self.config[setting] = value

    ### general helper functions ###

    def get_future_from(self, function, **params):
        return self.thread_pool.submit(function, **params)

    def open_disks(self):
        self.thread_manager.new_thread(subprocess.run, True, ['gnome-disks'])

    def open_settings(self, page):
        # open respective section of 'gnome-control-center'
        # TODO use correct language setting
        self.thread_manager.new_thread(subprocess.run, True, ['gnome-control-center', page])

    def start_standalone_thread(self, function, daemon=False, args=None):
        self.thread_manager.new_thread(function, daemon, args)

    ### stack funcitons ###

    def set_stack(self, stack):
        self.stack = stack

    def advance(self):
        self.stack.advance()

    def load_initial_page(self):
        self.stack.load_initial_page()

    def page_can_proceed_automatically(self, name):
        self.stack.page_can_proceed_automatically(name)

    def page_is_ok_to_proceed(self, name, ok=True):
        self.stack.page_is_ok_to_proceed(name, ok)

    def try_go_to_next(self):
        self.stack.try_go_to_next()

    def try_go_to_previous(self):
        self.stack.try_go_to_previous()
