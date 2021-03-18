# SPDX-License-Identifier: GPL-3.0-or-later

import threading

from gi.repository import Gtk

from .global_state import global_state
from .installation_scripting import installation_scripting
from .page import Page


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/install.ui')
class InstallPage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image_name = 'OS-Installer-symbolic'

    terminal_box = Gtk.Template.Child()
    terminal_button = Gtk.Template.Child()
    stack = Gtk.Template.Child()
    spinner = Gtk.Template.Child()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

        # UI element states
        self.stack.set_visible_child_name('spinner')

        # signals
        self.terminal_button.connect('toggled', self._on_toggled_terminal_button)

    ### callbacks ###

    def _on_toggled_terminal_button(self, toggle_button):
        if self.stack.get_visible_child_name() == 'spinner':
            self.spinner.stop()
            self.stack.set_visible_child_name('terminal')
        else:
            self.spinner.start()
            self.stack.set_visible_child_name('spinner')

    ### public methods ###

    def load_once(self):
        installation_scripting.install_window_name = self.__gtype_name__

        # setup VTE
        vte = installation_scripting.terminal
        vte.set_hexpand(True)
        vte.set_vexpand(True)
        self.terminal_box.add(vte)
        self.terminal_box.show_all()

        if global_state.demo_mode:
            return True

        self.spinner.start()

    def unload(self):
        self.spinner.stop()

        # in demo mode no script disables installation running flag
        if global_state.demo_mode:
            global_state.installation_running = False
