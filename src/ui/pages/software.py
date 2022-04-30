# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk

from .global_state import global_state
from .page import Page
from .software_provider import get_software_suggestions
from .widgets import SoftwareRow


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/software.ui')
class SoftwarePage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image_name = 'system-software-install-symbolic'

    software_list = Gtk.Template.Child()


    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

    def _setup_software(self):
        suggestions = get_software_suggestions()
        for package in suggestions:
            row = SoftwareRow(package)
            self.software_list.append(row)

    ### callbacks ###

    @Gtk.Template.Callback('continue')
    def _continue(self, button):
        global_state.advance(self)

    @Gtk.Template.Callback('software_row_activated')
    def _software_row_activated(self, list_box, row):
        new_state = not row.is_activated()
        row.set_activated(new_state)

    ### public methods ###

    def load_once(self):
        self._setup_software()

    def unload(self):
        to_install = ''
        for row in self.software_list:
            if row.is_activated():
                to_install += ' ' + row.package_name

        global_state.set_config('chosen_additional_software', to_install.strip())
