# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk

from .global_state import global_state
from .installation_scripting import installation_scripting, Step
from .page import Page
from .widgets import reset_model, DeviceRow


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/welcome.ui')
class WelcomePage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image_name = 'weather-clear-symbolic'

    description = Gtk.Template.Child()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)
        text = self.description.get_label()
        text = text.format(global_state.get_config('distribution_name'))
        self.description.set_label(text)

    ### callbacks ###

    @Gtk.Template.Callback('continue')
    def _continue(self, button):
        global_state.advance(self)
