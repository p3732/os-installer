# SPDX-License-Identifier: GPL-3.0-or-later

import os
import subprocess


class SystemProvider:
    '''
    All calls to other programs are encapsulated here.
    '''

    def __init__(self, thread_provider):
        self.thread_provider = thread_provider

    ### public methods ###

    def has_efi_vars(self):
        return os.path.isdir("/sys/firmware/efi/efivars")

    def open_disks(self):
        # TODO use correct language setting
        self.thread_provider.new_thread(subprocess.run, True, ['gnome-disks'])

    def open_wifi_settings(self):
        # TODO use correct language setting
        self.thread_provider.new_thread(subprocess.run, True, ['gnome-control-center', 'wifi'])

    def restart(self):
        subprocess.run(['reboot'])

    def set_keyboard_layout(self, keyboard_layout):
        subprocess.run(['gsettings', 'set', 'org.gnome.desktop.input-sources',
                        'sources', "[('xkb','{}')]".format(keyboard_layout)])

    def set_system_locale(self, new_locale):
        subprocess.run(['localectl', 'set-locale', new_locale])

    def set_timezone(self, timezone):
        subprocess.run(['timedatectl', 'set-timezone', timezone])

    def start_timesync(self):
        subprocess.run(['timedatectl', 'set-ntp', 'true'])
