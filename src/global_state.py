from .config import get_config, check_install_config, check_post_install_config
from .thread_manager import ThreadManager

from .language_provider import LanguageProvider

import locale
import subprocess
import os
from concurrent.futures import ThreadPoolExecutor

from gi.repository import GLib, GObject, Vte


class GlobalState:
    def __init__(self, localedir):
        self.demo_mode = False
        self.stack = None

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
        # set app language
        new_locale = locale.normalize(self.config['locale'])
        print(new_locale)
        self.config['locale'] = new_locale
        was_set = locale.setlocale(locale.LC_ALL, new_locale)
        if not was_set:
            language = self.config['language']
            print('Could not set locale to {}, falling back to English.'.format(language))
            print('Installation medium creators, check that you have correctly set up the locales to support {}.'.format(language))
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

        if not self.demo_mode:
            # change system locale
            subprocess.run(['localectl', 'set-locale', new_locale])
            return

    def apply_keyboard_layout(self):
        if not self.demo_mode:
            keyboard_layout = self.config['keyboard_layout_short_hand']
            subprocess.run(['gsettings', 'set', 'org.gnome.desktop.input-sources',
                            'sources', "[('xkb','{}')]".format(keyboard_layout)])

    def apply_connected(self):
        if not self.demo_mode:
            # TODO start ntp and syncing of mirrors
            # subprocess.run(['timedatectl', 'set-ntp', 'true'])
            return

    def apply_installation_confirmed(self):
        # create VTE with installation script
        self.terminal = Vte.Terminal()

        if not self.demo_mode:
            self.terminal.set_input_enabled(False)
            self.terminal.set_scroll_on_output(True)
            # TODO start the actual installation
            # spawn_async(pty_flags, working_directory, argv, envv, spawn_flags,
            #            child_setup, timeout, cancellable, callback, *user_data)
            # self.terminal.spawn_async(Vte.PtyFlags.DEFAULT, '/', ['echo test', None], [None],
            #                          GLib.SpawnFlags.DEFAULT, None, GObject.G_MAXINT, 1, None, None)
            #self.terminal.feed_child(b'echo test')

    def apply_installed(self):
        if not self.demo_mode:
            # TODO start copying script
            return

    def apply_timezone(self):
        if not self.demo_mode:
            # TODO change system timezone
            print(self.config['timezone'])

    def apply_restart(self):
        if not self.demo_mode:
            # TODO
            return

    ### config functions ###

    def get_config(self, setting):
        if setting in self.config:
            return self.config[setting]
        else:
            return None

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
