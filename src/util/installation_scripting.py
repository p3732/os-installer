# SPDX-License-Identifier: GPL-3.0-or-later

from threading import Lock
import time

from gi.repository import Gio, GLib, GObject, Vte

from .config import create_envs
from .global_state import global_state


steps = [None, 'prepare', 'install', 'configure']


class InstallationScripting():
    '''
    Handles all calls to scripts for installation. The installation process consists of 3 steps:
    * Preparation. Used e.g. for updating mirrors.
    * Installation. Installs an OS onto a disk.
    * Configuration. Configures an OS according to user's choices.
    '''

    terminal = Vte.Terminal()
    cancel = Gio.Cancellable()

    lock = Lock()
    current_step = 0
    step_ready = 0
    script_running = False

    # set by installation page
    install_page_name = None

    def __init__(self):
        # setup terminal
        self.terminal.set_input_enabled(False)
        self.terminal.set_scroll_on_output(True)
        self.terminal.set_hexpand(True)
        self.terminal.set_vexpand(True)
        self.terminal.connect('child-exited', self._on_child_exited)

    def _start_next_script(self):
        if self.current_step < self.step_ready and not self.script_running:
            self.current_step += 1
            script_name = steps[self.current_step]
            print('Starting step "{}"...'.format(script_name))
            envs = create_envs(global_state.config, self.current_step >= 2, self.current_step == 3)

            # check config
            if envs == None:
                print('Not all config options set for "{}". Please report this bug.'.format(script_name))
                print('############################')
                print(global_state.config)
                print('############################')
                global_state.installation_failed()
                return

            # start script
            self.script_running, _ = self.terminal.spawn_sync(
                Vte.PtyFlags.DEFAULT, '/', ['sh', '/etc/os-installer/scripts/{}.sh'.format(script_name)],
                envs, GLib.SpawnFlags.DEFAULT, None, None, self.cancel)
            if not self.script_running:
                print('Could not start {} script! Ignoring.'.format(script_name))

    ### callbacks ###

    def _on_child_exited(self, terminal, status):
        with self.lock:
            self.script_running = False
            script_name = steps[self.current_step]
            print('Finished step "{}".'.format(script_name))

            if not status == 0 and not global_state.demo_mode:
                global_state.installation_failed()
            elif self.current_step == 3:
                global_state.advance_without_return(self.install_page_name)
            else:
                self._start_next_script()

    ### public methods ###

    def start_next_step(self):
        with self.lock:
            self.step_ready += 1
            self._start_next_script()


installation_scripting = InstallationScripting()
