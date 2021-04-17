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
    _run_program(['gnome-disks'])


def open_internet_search():
    distribution_name = global_state.get_config('distribution_name')
    name_snippet = '"' + distribution_name + '" ' if distribution_name else ''
    search_text = '{}"failed installation" "os-installer version {}"'.format(
        name_snippet, global_state.get_config('version'))
    _run_program(['epiphany', '--search', search_text])


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


def set_system_formats(locale):
    global_state.set_config('formats', locale)
    exec_(['gsettings', 'set', 'org.gnome.system.locale', 'region', "'{}'".format(locale)])


def set_system_timezone(timezone):
    global_state.set_config('timezone', timezone)
    # TODO find correct way to set timezone without user authentication
    # _exec(['timedatectl', 'set-timezone', timezone])


def start_system_timesync():
    _exec(['gsettings', 'set', 'org.gnome.desktop.datetime', 'automatic-timezone', 'true'])
