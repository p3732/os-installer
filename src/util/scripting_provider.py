# SPDX-License-Identifier: GPL-3.0-or-later

from threading import Lock
import time
from gi.repository import Gio, GLib, GObject, Vte


class ScriptingProvider():
    '''
    All calls to other programs are encapsulated here.
    '''

    def __init__(self, terminal, callback):
        self.terminal = terminal
        self.terminal.set_input_enabled(False)
        self.terminal.set_scroll_on_output(True)

        self.callback = callback
        self.config = {}
        self.lock = Lock()

        self.preparation_done = False
        self.installation_ready = False
        self.installation_done = False
        self.configuration_ready = False

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
        self._start_script('prepare', self._on_preparation_done)

    def _start_installation(self):
        if self.preparation_done and self.installation_ready:
            print('Starting installation...')
            self._start_script('install', self._on_installation_done)

    def _start_configuration(self):
        if self.installation_done and self.configuration_ready:
            print('Starting configuration...')
            self._start_script('configure', self._on_configuration_done)

    ### callbacks ###

    def _on_preparation_done(self, terminal, column, row, data):
        # TODO handle return value
        with self.lock:
            print('Installation preparation done.')
            self.preparation_done = True
            self._start_installation()

    def _on_installation_done(self, terminal, column, row, data):
        # TODO handle return value
        with self.lock:
            print('Installation done.')
            self.installation_done = True
            self._start_configuration()

    def _on_configuration_done(self, terminal, column, row, data):
        # TODO handle return value
        print('Configuration done.')
        self.callback()

    ### public methods ###

    def start_configuration(self, config):
        with self.lock:
            self.config = config
            self.configuration_ready = True
            self._start_configuration()

    def start_installation(self, config):
        with self.lock:
            self.config = config
            self.installation_ready = True
            self._start_installation()

    def start_preparation(self):
        with self.lock:
            self._start_preparation()
