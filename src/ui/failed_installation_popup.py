# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Handy


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/failed_installation_popup.ui')
class FailedInstallationPopup(Handy.Window):
    __gtype_name__ = 'FailedInstallationPopup'

    confirm_button = Gtk.Template.Child()

    error_box = Gtk.Template.Child()
    error_text = Gtk.Template.Child()
    copy_error_button = Gtk.Template.Child()

    def __init__(self, quit_callback, error_text, **kwargs):
        super().__init__(**kwargs)

        self.quit_callback = quit_callback

        # show error message if provided
        if error_text:
            self.error_text.set_label(error_text)
            self.error_box.show_all()

        # signals
        self.copy_error_button.connect('clicked', self._on_clicked_copy_error_button)
        self.confirm_button.connect('clicked', self._on_clicked_confirm_button)

    ### callbacks ###

    def _on_clicked_copy_error_button(self, button):
        self.error_text.do_copy_clipboard()

    def _on_clicked_confirm_button(self, button):
        self.quit_callback()
