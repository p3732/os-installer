# SPDX-License-Identifier: GPL-3.0-or-later

from enum import Enum
from threading import Lock
import os

from gi.repository import Gio, GLib, Vte

from .global_state import global_state


class Step(Enum):
    none = 0
    prepare = 1
    install = 2
    configure = 3
    done = 4


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
    current_step = Step.none
    step_ready = Step.none
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
        if self.current_step is Step.configure:
            global_state.installation_running = False
            global_state.advance(None, allow_return=global_state.demo_mode,
                                 cleanup=not global_state.demo_mode,)

        if self.current_step.value < self.step_ready.value and not self.script_running:
            self.current_step = Step(self.current_step.value + 1)
            print(f'Starting step "{self.current_step.name}"...')

            is_installing = self.current_step is Step.install or self.current_step is Step.configure
            is_configuring = self.current_step is Step.configure
            envs = global_state.create_envs(is_installing, is_configuring)

            global_state.installation_running = is_installing

            # check config
            if envs == None:
                print(f'Not all config options set for "{self.current_step.name}". Please report this bug.')
                print('############################')
                print(global_state.config)
                print('############################')
                global_state.installation_failed()
                return

            # start script
            file_name = f'/etc/os-installer/scripts/{self.current_step.name}.sh'
            if os.path.exists(file_name):
                self.script_running, _ = self.terminal.spawn_sync(
                    Vte.PtyFlags.DEFAULT, '/', ['sh', file_name],
                    envs, GLib.SpawnFlags.DEFAULT, None, None, self.cancel)
                if not self.script_running:
                    print(f'Could not start {self.current_step.name} script! Ignoring.')
                    self._start_next_script()
            else:
                print(f'No script for step {self.current_step.name} exists.')
                self._start_next_script()

    ### callbacks ###

    def _on_child_exited(self, terminal, status):
        with self.lock:
            self.script_running = False
            print(f'Finished step "{self.current_step.name}".')

            if not status == 0 and not global_state.demo_mode:
                global_state.installation_failed()
            else:
                self._start_next_script()

    ### public methods ###

    def set_ok_to_start_step(self, step: Step):
        with self.lock:
            if self.step_ready.value < step.value:
                self.step_ready = step
                self._start_next_script()


installation_scripting = InstallationScripting()
