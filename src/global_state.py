# SPDX-License-Identifier: GPL-3.0-or-later

from .config import get_config, check_install_config, check_post_install_config
from .thread_manager import ThreadManager

from .language_provider import LanguageProvider
from .system_provider import SystemProvider

import locale as Locale
import subprocess
import os
from concurrent.futures import ThreadPoolExecutor

from gi.repository import Gio, GLib, GObject, Vte


class GlobalState:
    def __init__(self, localedir):
        self.demo_mode = False
        self.installation_running = False
        self.stack = None
        self.terminal = None

        # configuration file loader
        self.config = get_config()
        self.set_config('localedir', localedir)
        self.set_config('disk_name', 'Test Dummy')

        # helper to manage proper threads
        self.thread_manager = ThreadManager()

        # for futures use built in thread pool
        self.thread_pool = ThreadPoolExecutor()

        # setup providers
        self.language_provider = LanguageProvider(self)
        self.system_provider = SystemProvider(self.thread_manager)

    ### installation stages ###

    def apply_language_settings(self, language, short_hand, locale):
        self.set_config('language', language)
        self.set_config('language_short_hand', short_hand)
        locale = Locale.normalize(locale)
        self.set_config('locale', locale)

        # set app language
        was_set = Locale.setlocale(Locale.LC_ALL, locale)
        if not was_set:
            print('Could not set locale to {}, falling back to English.'.format(language))
            print('Installation medium creators, check that you have correctly set up the locales to support {}.'.format(language))
            # fallback
            Locale.setlocale(Locale.LC_ALL, 'en_US.UTF-8')

        if not self.demo_mode:
            self.system_provider.set_system_locale(locale)

    def apply_keyboard_layout(self, keyboard_layout, short_hand):
        self.set_config('keyboard_layout', keyboard_layout)
        self.set_config('keyboard_layout_short_hand', short_hand)
        if not self.demo_mode:
            self.system_provider.set_keyboard_layout(short_hand)

    def apply_connected(self):
        if not self.demo_mode:
            self.system_provider.start_timesync()

    def apply_installation_confirmed(self):
        # create VTE with installation script
        self.terminal = Vte.Terminal()
        self.installation_running = True

        if not self.demo_mode:
            self.terminal.set_input_enabled(False)
            self.terminal.set_scroll_on_output(True)

            # TODO start the actual installation
            pty_flags = Vte.PtyFlags.DEFAULT
            spawn_flags = GLib.SpawnFlags.DEFAULT
            cancel = Gio.Cancellable()
            self.terminal.spawn_async(
                pty_flags, '/', ['sh', '/etc/os-installer/scripts/installer.sh'],
                None, spawn_flags, None, None, -1, cancel, self.terminal_callback, None)

    def terminal_callback(self, terminal, column, row, data):
        print('Terminal call ended.')

    def apply_timezone(self, timezone):
        self.set_config('timezone', timezone)
        if not self.demo_mode:
            self.system_provider.set_timezone(timezone)

    def apply_restart(self):
        if not self.demo_mode:
            self.system_provider.restart()

    def on_installation_done(self):
        self.installation_running = False
        self.stack.advance()

    ### config functions ###

    def get_config(self, setting):
        if setting in self.config:
            return self.config[setting]
        else:
            return None

    def set_config(self, setting, value):
        self.config[setting] = value

    ### thread functions ###

    def get_future_from(self, function, **params):
        return self.thread_pool.submit(function, **params)

    def start_standalone_thread(self, function, daemon=False, args=None):
        self.thread_manager.new_thread(function, daemon, args)

    ### stack funcitons ###

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

    ### system functions ###

    def open_disks(self):
        self.system_provider.open_disks()

    def open_wifi_settings(self):
        self.system_provider.open_wifi_settings()
