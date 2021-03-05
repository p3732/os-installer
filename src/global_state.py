# SPDX-License-Identifier: GPL-3.0-or-later

from .config import get_config, check_install_config, check_post_install_config

from .language_provider import LanguageProvider
from .scripting_provider import ScriptingProvider
from .system_provider import SystemProvider
from .thread_provider import ThreadProvider

import locale as Locale

from gi.repository import Vte


class GlobalState:
    def __init__(self, localedir):
        self.demo_mode = False
        self.installation_running = False
        self.stack = None
        self.terminal = Vte.Terminal()

        # configuration file loader
        self.config = get_config()
        self.set_config('localedir', localedir)
        self.set_config('disk_name', 'Test Dummy')

        # setup providers
        self.thread_provider = ThreadProvider()
        self.language_provider = LanguageProvider(self)
        self.scripting_provider = ScriptingProvider(self.terminal, self._on_installation_done)
        self.system_provider = SystemProvider(self.thread_provider)

    def _on_installation_done(self):
        self.installation_running = False
        # this can only happen if installation page is currently shown, so advancing is fine
        self.stack.advance()

    ### installation stages ###

    def apply_language_settings(self, language_info):
        self.set_config('language', language_info.name)
        self.set_config('language_short_hand', language_info.language_code)
        locale = Locale.normalize(language_info.locale)
        self.set_config('locale', locale)

        # set app language
        was_set = Locale.setlocale(Locale.LC_ALL, locale)
        if not was_set:
            print('Could not set locale to {}, falling back to English.'.format(language))
            print('Installation medium creators, check that you have correctly set up the locales',
                  'to support {}.'.format(language_info.name))
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
            self.scripting_provider.start_preparation()

    def apply_installation_confirmed(self):
        self.installation_running = True

        if not self.demo_mode:
            self.scripting_provider.start_installation(self.config)

    def apply_configuration_confirmed(self):
        if not self.demo_mode:
            self.scripting_provider.start_configuration(self.config)

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
        return self.thread_provider.get_future_from(function, **params)

    def start_standalone_thread(self, function, daemon=False, args=None):
        self.thread_provider.new_thread(function, daemon, args)

    ### stack funcitons ###

    def advance(self, name=None):
        self.stack.advance(name)

    def load_initial_page(self):
        self.stack.load_initial_page()

    def try_go_to_next(self):
        self.stack.try_go_to_next()

    def try_go_to_previous(self):
        self.stack.try_go_to_previous()

    ### system functions ###

    def has_efi_vars(self):
        return self.get_future_from(self.system_provider.has_efi_vars)

    def open_disks(self):
        self.system_provider.open_disks()

    def open_wifi_settings(self):
        self.system_provider.open_wifi_settings()
