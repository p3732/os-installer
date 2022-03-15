# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk

from .system_calls import reboot_system
from .page import Page


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/restart.ui')
class RestartPage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image_name = 'system-reboot-symbolic'

    spinner = Gtk.Template.Child()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

    ### public methods ###

    def load(self):
        self.spinner.start()
        reboot_system()
