# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/about_dialog.ui')
class AboutDialog(Gtk.AboutDialog):
    __gtype_name__ = 'AboutDialog'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # TODO set via .ui file
        self.set_license_type(Gtk.License.GPL_3_0)
