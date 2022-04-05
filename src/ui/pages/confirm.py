# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk

from .global_state import global_state
from .installation_scripting import installation_scripting, Step
from .page import Page


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/confirm.ui')
class ConfirmPage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image_name = 'question-round-symbolic'

    disk_label = Gtk.Template.Child()
    confirm_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

        # signals
        self.confirm_button.connect("clicked", self._on_clicked_confirm)

    ### callbacks ###

    def _on_clicked_confirm(self, button):
        installation_scripting.set_ok_to_start_step(Step.install)
        global_state.advance_without_return(self.__gtype_name__)

    ### public methods ###

    def load(self):
        # set label
        name = global_state.get_config('disk_name')
        self.disk_label.set_label(name)
