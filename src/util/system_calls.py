# SPDX-License-Identifier: GPL-3.0-or-later

''' All calls to other programs are encapsulated here. '''

import os
from subprocess import Popen
import subprocess
import locale as Locale

from .global_state import global_state


def _exec(args):
    if not global_state.demo_mode:
        subprocess.run(args)


def _run_program(args):
    env = os.environ.copy()
    env["LANG"] = global_state.get_config('locale')
    Popen(args, env=env)


### public methods ###
def is_booted_with_uefi():
    return os.path.isdir("/sys/firmware/efi/efivars")


def open_disks():
    _run_program(global_state.get_config('disks_cmd').split())


def open_internet_search():
    browser_cmd = global_state.get_config('browser_cmd').split()
    failure_help_url = global_state.get_config('failure_help_url')
    version = global_state.get_config("version")
    browser_cmd.append(failure_help_url.format(version))
    _run_program(browser_cmd)


def open_wifi_settings():
    _run_program(global_state.get_config('wifi_cmd').split())


def reboot_system():
    _exec(['reboot'])


def set_system_keyboard_layout(keyboard_layout, short_hand):
    global_state.set_config('keyboard_layout_ui', keyboard_layout)
    global_state.set_config('keyboard_layout', short_hand)

    # set system input
    _exec(['gsettings', 'set', 'org.gnome.desktop.input-sources', 'sources',
           f"[('xkb','{short_hand}')]"])


def set_system_language(language_info):
    global_state.set_config('language', language_info.name)
    global_state.set_config('language_code', language_info.language_code)
    locale = Locale.normalize(language_info.locale)
    global_state.set_config('locale', locale)

    # set app language
    was_set = Locale.setlocale(Locale.LC_ALL, locale)
    if not was_set:
        print(f'Could not set locale to {language_info.name}, falling back to English.')
        print('Installation medium creators, check that you have correctly set up the locales',
              f'to support {language_info.name}.')
        # fallback
        Locale.setlocale(Locale.LC_ALL, 'en_US.UTF-8')

    # TODO find correct way to set system locale without user authentication
    _exec(['localectl', '--no-ask-password', 'set-locale', f'LANG={locale}'])


def set_system_formats(locale, formats_label):
    global_state.set_config('formats_locale', locale)
    global_state.set_config('formats_ui', formats_label)
    _exec(['gsettings', 'set', 'org.gnome.system.locale', 'region', f"'{locale}'"])


def set_system_timezone(timezone):
    global_state.set_config('timezone', timezone)
    # TODO find correct way to set timezone without user authentication
    _exec(['timedatectl', '--no-ask-password', 'set-timezone', timezone])


def start_system_timesync():
    # TODO find correct way to set enable time sync without user authentication
    _exec(['timedatectl', '--no-ask-password', 'set-ntp', 'true'])
    _exec(['gsettings', 'set', 'org.gnome.desktop.datetime', 'automatic-timezone', 'true'])
