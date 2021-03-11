# SPDX-License-Identifier: GPL-3.0-or-later

from .page import Page

from gi.repository import Gtk

import threading


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/install.ui')
class InstallPage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image_name = 'OS-Installer-symbolic'

    terminal_box = Gtk.Template.Child()
    terminal_button = Gtk.Template.Child()
    stack = Gtk.Template.Child()
    spinner = Gtk.Template.Child()

    def __init__(self, global_state, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

        self.global_state = global_state
        self.vte_created = False

        # UI element states
        self.stack.set_visible_child_name('spinner')

        # signals
        self.terminal_button.connect('toggled', self._on_toggled_terminal_button)

    def _setup_vte(self):
        terminal = self.global_state.terminal
        self.terminal_box.add(terminal)
        self.terminal_box.show_all()

    ### callbacks ###

    def _on_toggled_terminal_button(self, toggle_button):
        if self.stack.get_visible_child_name() == 'spinner':
            self.spinner.stop()
            if not self.vte_created:
                self._setup_vte()
                self.vte_created = True
            self.stack.set_visible_child_name('terminal')
        else:
            self.spinner.start()
            self.stack.set_visible_child_name('spinner')

    ### public methods ###

    def load_once(self):
        if self.global_state.demo_mode:
            return True

        self.spinner.start()

    def unload(self):
        self.spinner.stop()

        # in demo mode no script disables installation running flag
        if self.global_state.demo_mode:
            self.global_state.installation_running = False
