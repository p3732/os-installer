# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk

from .global_state import global_state
from .installation_scripting import installation_scripting
from .page import Page


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/install.ui')
class InstallPage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image = 'OS-Installer-symbolic'

    terminal_box = Gtk.Template.Child()
    stack = Gtk.Template.Child()
    spinner = Gtk.Template.Child()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

        installation_scripting.install_page_name = self.__gtype_name__

        # UI element states
        self.stack.set_visible_child_name('spinner')

    ### callbacks ###

    @Gtk.Template.Callback('terminal_button_toggled')
    def _terminal_button_toggled(self, toggle_button):
        if self.stack.get_visible_child_name() == 'spinner':
            self.spinner.stop()
            self.stack.set_visible_child_name('terminal')
        else:
            self.spinner.start()
            self.stack.set_visible_child_name('spinner')

    ### public methods ###

    def load(self):
        # setup terminal
        self.terminal_box.append(installation_scripting.terminal)
        self.spinner.start()

    def unload(self):
        self.terminal_box.remove(installation_scripting.terminal)
        self.spinner.stop()
