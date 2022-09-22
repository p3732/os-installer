# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk

from .global_state import global_state
from .page import Page


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/user.ui')
class UserPage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image_name = 'user-symbolic'

    user_name_row = Gtk.Template.Child()
    autologin_switch = Gtk.Template.Child()
    password_row = Gtk.Template.Child()
    continue_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

    def _set_continue_button(self, autologin):
        has_user_name = not self.user_name_row.get_text().strip() == ''
        has_password = not self.password_row.get_text() == ''
        can_continue = has_user_name and (autologin or has_password)
        self.continue_button.set_sensitive(can_continue)

    ### callbacks ###

    @Gtk.Template.Callback('autologin_row_clicked')
    def _autologin_row_clicked(self, row):
        self.autologin_switch.activate()

    @Gtk.Template.Callback('autologin_switch_flipped')
    def _autologin_switch_flipped(self, autologin_switch, state):
        self._set_continue_button(state)

    @Gtk.Template.Callback('focus_password')
    def _focus_password(self, row):
        self.password_row.grab_focus()

    @Gtk.Template.Callback('entry_changed')
    def _entry_changed(self, editable):
        self._set_continue_button(self.autologin_switch.get_state())

    @Gtk.Template.Callback('continue')
    def _continue(self, object):
        if self.continue_button.get_sensitive():
            global_state.advance(self)

    ### public methods ###

    def unload(self):
        global_state.set_config('user_name', self.user_name_row.get_text().strip())
        global_state.set_config('user_password', self.password_row.get_text())
        global_state.set_config('user_autologin', self.autologin_switch.get_state())
