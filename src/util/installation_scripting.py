# SPDX-License-Identifier: GPL-3.0-or-later

from threading import Lock
import time

from gi.repository import Gio, GLib, GObject, Vte

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
            print(f'Starting step "{script_name}"...')
            envs = global_state.create_envs(self.current_step >= 2, self.current_step == 3)
            global_state.installation_running = self.current_step >= 2

            # check config
            if envs == None:
                print(f'Not all config options set for "{script_name}". Please report this bug.')
                print('############################')
                print(global_state.config)
                print('############################')
                global_state.installation_failed()
                return

            # start script
            self.script_running, _ = self.terminal.spawn_sync(
                Vte.PtyFlags.DEFAULT, '/', ['sh', f'/etc/os-installer/scripts/{script_name}.sh'],
                envs, GLib.SpawnFlags.DEFAULT, None, None, self.cancel)
            if not self.script_running:
                print(f'Could not start {script_name} script! Ignoring.')

    ### callbacks ###

    def _on_child_exited(self, terminal, status):
        with self.lock:
            self.script_running = False
            script_name = steps[self.current_step]
            print(f'Finished step "{script_name}".')

            if not status == 0 and not global_state.demo_mode:
                global_state.installation_failed()
            elif self.current_step == 3:
                global_state.installation_running = False
                if global_state.demo_mode:
                    # allow returning in demo
                    global_state.advance(self.install_page_name)
                else:
                    global_state.advance_without_return(self.install_page_name)
            else:
                self._start_next_script()

    ### public methods ###

    def start_next_step(self):
        with self.lock:
            self.step_ready += 1
            self._start_next_script()


installation_scripting = InstallationScripting()
