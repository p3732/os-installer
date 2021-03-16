# SPDX-License-Identifier: GPL-3.0-or-later

from threading import Lock
import time

from gi.repository import Gio, GLib, GObject, Vte

from .global_state import global_state


class InstallationScripting():
    '''
    Handles all calls to scripts for installation. The installation process consists of 3 steps:
    * Preparation. Used e.g. for updating mirrors.
    * Installation. Installs an OS onto a disk.
    * Configuration. Configures an OS according to user's choices.
    '''
    terminal = Vte.Terminal()
    lock = Lock()
    preparation_done = False
    installation_ready = False
    installation_done = False
    configuration_ready = False

    def __init__(self):
        # setup terminal
        self.terminal.set_input_enabled(False)
        self.terminal.set_scroll_on_output(True)

    def _start_script(self, name, callback):
        # TODO set environment variables from config
        pty_flags = Vte.PtyFlags.DEFAULT
        spawn_flags = GLib.SpawnFlags.DEFAULT
        cancel = Gio.Cancellable()
        self.terminal.spawn_async(
            pty_flags, '/', ['sh', '/etc/os-installer/scripts/{}.sh'.format(name)],
            None, spawn_flags, None, None, -1, cancel, callback, None)

    def _start_preparation(self):
        print('Starting preparation...')
        self._start_script('prepare', self._preparation_step_done)

    def _start_installation(self):
        if self.preparation_done and self.installation_ready:
            print('Starting installation...')
            self._start_script('install', self._installation_step_done)

    def _start_configuration(self):
        if self.installation_done and self.configuration_ready:
            print('Starting configuration...')
            self._start_script('configure', self._configuration_step_done)

    ### callbacks ###

    def _preparation_step_done(self, terminal, column, row, data):
        # TODO handle return value
        with self.lock:
            print('Installation preparation done.')
            self.preparation_done = True
            self._start_installation()

    def _installation_step_done(self, terminal, column, row, data):
        # TODO handle return value
        with self.lock:
            print('Installation done.')
            self.installation_done = True
            self._start_configuration()

    def _configuration_step_done(self, terminal, column, row, data):
        # TODO handle return value
        print('Configuration done.')
        global_state.installation_running = False
        global_state.advance()

    ### public methods ###

    def start_preparation(self):
        ''' First step. Runs as soon as internet is connected or directly if internet is not required. '''
        with self.lock:
            self._start_preparation()

    def start_installation(self):
        ''' Second step. Runs when user selected disk and prepartion is done. '''
        with self.lock:
            self.installation_ready = True
            self._start_installation()

    def start_configuration(self):
        ''' Third step. Runs when both, user configuration input and installation, are done. '''
        with self.lock:
            self.configuration_ready = True
            self._start_configuration()


installation_scripting = InstallationScripting()
