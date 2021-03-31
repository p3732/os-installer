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
def has_efi_vars():
    return os.path.isdir("/sys/firmware/efi/efivars")


def open_disks():
    _run_program(['gnome-disks'])


def open_wifi_settings():
    _run_program(['gnome-control-center', 'wifi'])


def reboot_system():
    _exec(['reboot'])


def set_system_keyboard_layout(keyboard_layout, short_hand):
    global_state.set_config('keyboard_layout', keyboard_layout)
    global_state.set_config('keyboard_layout_short_hand', short_hand)

    # set system input
    _exec(['gsettings', 'set', 'org.gnome.desktop.input-sources', 'sources',
           "[('xkb','{}')]".format(short_hand)])


def set_system_language(language_info):
    global_state.set_config('language', language_info.name)
    global_state.set_config('language_short_hand', language_info.language_code)
    locale = Locale.normalize(language_info.locale)
    global_state.set_config('locale', locale)

    # set app language
    was_set = Locale.setlocale(Locale.LC_ALL, locale)
    if not was_set:
        print('Could not set locale to {}, falling back to English.'.format(language_info.name))
        print('Installation medium creators, check that you have correctly set up the locales',
              'to support {}.'.format(language_info.name))
        # fallback
        Locale.setlocale(Locale.LC_ALL, 'en_US.UTF-8')

    # set system locale
    _exec(['localectl', 'set-locale', locale])


def set_system_formats(locale):
    global_state.set_config('formats', locale)

    _exec(['localectl', 'set-locale', 'LC_NUMERIC', locale])
    _exec(['localectl', 'set-locale', 'LC_TIME', locale])
    _exec(['localectl', 'set-locale', 'LC_MONETARY', locale])
    _exec(['localectl', 'set-locale', 'LC_PAPER', locale])
    _exec(['localectl', 'set-locale', 'LC_MEASUREMENT', locale])


def set_system_timezone(timezone):
    global_state.set_config('timezone', timezone)
    _exec(['timedatectl', 'set-timezone', timezone])


def start_system_timesync():
    _exec(['timedatectl', 'set-ntp', 'true'])
