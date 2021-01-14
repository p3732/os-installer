from .config import get_config, check_install_config, check_post_install_config
from .thread_manager import ThreadManager

from .language_provider import LanguageProvider

import locale
import subprocess
import os
from concurrent.futures import ThreadPoolExecutor


class GlobalState:
    def __init__(self, localedir):
        self.stack = None
        self.demo_mode = False

        # configuration file loader
        self.config = get_config()
        self.set_config('localedir', localedir)

        # helper to manage proper threads
        self.thread_manager = ThreadManager()

        # for futures use built in thread pool
        self.thread_pool = ThreadPoolExecutor()

        # setup providers
        self.language_provider = LanguageProvider(self)

    ### installation stages ###

    def apply_language_settings(self):
        print('setting language to ', self.config['language'])
        # TODO assert locale exists, otherwise fallback to English
        lo = self.config['language_short_hand']
        if lo == 'en':
            l = 'en_US.utf8'
        elif lo == 'de':
            l = 'de_DE.utf8'
        else:
            l = 'en_US.utf8'
        print(l)
        locale.setlocale(locale.LC_ALL, l)

        if not self.demo_mode:
            # TODO change via localectl?
            # subprocess.run(['localectl', 'set-locale', language])
            return

    def apply_keyboard_layout(self):
        keyboard_layout = self.config['keyboard_layout_short_hand']

        if not self.demo_mode:
            # TODO change via localectl
            # subprocess.run(['localectl', 'set-keymap', short_hand])
            return

    def apply_connected(self):
        if not self.demo_mode:
            # TODO start ntp and syncing of mirrors
            # subprocess.run(['timedatectl', 'set-ntp', 'true'])
            return

    def apply_installation_confirmed(self):
        if not self.demo_mode:
            # TODO start the actual installation
            return

    def apply_installed(self):
        if not self.demo_mode:
            # TODO start copying script
            return

    def apply_restart(self):
        if not self.demo_mode:
            # TODO
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

    ### provider functions ###

    def get_language_provider(self):
        return self.language_provider

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
