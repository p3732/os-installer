# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk

from .global_state import global_state
from .installation_scripting import installation_scripting, Step
from .page import Page
from .widgets import reset_model, DeviceRow


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/confirm.ui')
class ConfirmPage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image = 'question-round-symbolic'

    disk_row = Gtk.Template.Child()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

    ### callbacks ###

    @Gtk.Template.Callback('confirmed')
    def _confirmed(self, button):
        installation_scripting.set_ok_to_start_step(Step.install)
        global_state.advance_without_return(self)

    ### public methods ###

    def load(self):
        self.disk_row.set_title(global_state.get_config('disk_name'))
        self.disk_row.set_subtitle(global_state.get_config('disk_device_path'))
