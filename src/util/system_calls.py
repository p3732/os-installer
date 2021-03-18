# SPDX-License-Identifier: GPL-3.0-or-later

''' All calls to other programs are encapsulated here. '''

import os
import subprocess
import locale as Locale

from .global_state import global_state
from .thread_manager import thread_manager


def _exec(args):
    if not global_state.demo_mode:
        subprocess.run(args)


### public methods ###
def has_efi_vars():
    return os.path.isdir("/sys/firmware/efi/efivars")


def open_disks():
    # TODO use correct language setting
    thread_manager.start_standalone_thread(subprocess.run, True, ['gnome-disks'])


def open_wifi_settings():
    # TODO use correct language setting
    thread_manager.start_standalone_thread(subprocess.run, True, ['gnome-control-center', 'wifi'])


def reboot_system():
    _exec(['reboot'])


def set_system_keyboard_layout(keyboard_layout, short_hand):
    global_state.set_config('keyboard_layout', keyboard_layout)
    global_state.set_config('keyboard_layout_short_hand', short_hand)

    # set system input
    _exec(['gsettings', 'set', 'org.gnome.desktop.input-sources sources',
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


def set_system_timezone(timezone):
    global_state.set_config('timezone', timezone)
    _exec(['timedatectl', 'set-timezone', timezone])


def start_system_timesync():
    _exec(['timedatectl', 'set-ntp', 'true'])
