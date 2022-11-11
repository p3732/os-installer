# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, Gtk

from .global_state import global_state
from .page import Page
from .software_provider import get_software_suggestions
from .widgets import reset_model, SelectionRow


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/software.ui')
class SoftwarePage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image = 'system-software-install-symbolic'

    software_list = Gtk.Template.Child()
    software_model = Gio.ListStore()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)
        self.software_list.bind_model(
            self.software_model,
            lambda pkg: SelectionRow(pkg.name, pkg.description, pkg.icon_path,
                                     pkg.suggested, pkg, 'application-x-executable-symbolic'))

    def _setup_software(self):
        suggestions = get_software_suggestions()
        reset_model(self.software_model, suggestions)

    ### callbacks ###

    @Gtk.Template.Callback('continue')
    def _continue(self, button):
        global_state.advance(self)

    @Gtk.Template.Callback('software_row_activated')
    def _software_row_activated(self, list_box, row):
        row.flip_switch()

    ### public methods ###

    def load_once(self):
        self._setup_software()

    def unload(self):
        choices = [row.info for row in self.software_list if row.is_activated()]
        packages = ' '.join([choice.package for choice in choices])
        global_state.set_config('chosen_software_packages', packages)
        global_state.set_config('chosen_software', choices)
