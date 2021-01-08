from .config import Config
from .thread_manager import ThreadManager


from concurrent.futures import ThreadPoolExecutor
import os
import subprocess


class GlobalState:
    def __init__(self):
        self.config = Config()
        self.stack = None

        # helper to manage proper threads
        self.thread_manager = ThreadManager()
        # for futures use built in thread pool
        self.thread_pool = ThreadPoolExecutor()

    ### language page ###

    def set_language(self, language, short_hand):
        self.config.language = language
        self.config.language_short_hand = short_hand
        print('setting language to ', language)
        # TODO
        # change via localectl?
        # At least load respective translations
        # subprocess.run(['localectl', 'set-locale', language])

    ### keyboard layout page ###

    def get_language(self):
        return (self.config.language, self.config.language_short_hand)

    def set_keyboard_layout(self, keyboard_layout, short_hand):
        self.config.keyboard_layout = keyboard_layout
        self.config.keyboard_layout_short_hand = short_hand
        # change via localectl
        # subprocess.run(['localectl', 'set-keymap', short_hand])

    ### internet page ###

    def get_internet_checker_url(self):
        return self.config.internet_checker_url

    def set_connected(self):
        subprocess.run(['timedatectl', 'set-ntp', 'true'])
        # TODO start syncing of mirrors

    ### disks page ###

    def open_disks(self):
        self.thread_manager.new_thread(subprocess.run, True, ['gnome-disks'])

    def set_disk(self, name, size, device_path, is_partition):
        self.config.disk_name = name
        self.config.disk_size = size
        self.config.disk_device_path = device_path
        self.config.disk_is_partition = is_partition

    ### encrypt page ###

    def set_encryption(self, state, pin=None):
        self.config.encrypt = state
        if pin:
            self.config.encryption_pin = pin

    ### confirm page ###

    def get_disk_name(self):
        return self.config.disk_name

    ### user page ###

    def set_user_name(self, user_name):
        self.config.user_name = user_name

    def set_password(self, password):
        self.config.password = password

    ### general helper functions ###

    def get_future_from(self, function, **params):
        return self.thread_pool.submit(function, **params)

    def open_settings(self, page):
        # open respective section of 'gnome-control-center'
        # TODO use correct language setting
        self.thread_manager.new_thread(subprocess.run, True, ['gnome-control-center', page])

    def start_standalone_thread(self, function, daemon=False, args=None):
        self.thread_manager.new_thread(function, daemon, args)

    ### stack methods ###

    def set_stack(self, stack):
        self.stack = stack

    def page_can_proceed_automatically(self, name):
        self.stack.page_can_proceed_automatically(name)

    def advance(self):
        self.stack.advance()

    def load_initial_page(self):
        self.stack.load_initial_page()

    def set_waiting(self, waiting, able_to_continue=True):
        self.stack.set_waiting(waiting, able_to_continue)

    def page_is_ok_to_proceed(self, name, ok=True):
        self.stack.page_is_ok_to_proceed(name, ok)

    def try_go_to_next(self):
        self.stack.try_go_to_next()

    def try_go_to_previous(self):
        self.stack.try_go_to_previous()
