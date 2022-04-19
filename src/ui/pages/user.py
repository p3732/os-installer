# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk

from .global_state import global_state
from .page import Page


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/user.ui')
class UserPage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image_name = 'user-symbolic'

    default_list = Gtk.Template.Child()
    user_name_field = Gtk.Template.Child()
    autologin_switch = Gtk.Template.Child()
    password_field = Gtk.Template.Child()

    continue_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

        # signals
        self.continue_button.connect('clicked', self._continue)
        self.default_list.connect('row-activated', self._on_row_activated)
        self.autologin_switch.connect("state-set", self._on_autologin_switch_flipped)
        self.user_name_field.connect("changed", self._on_entry_changed)
        self.password_field.connect("changed", self._on_entry_changed)

    def _set_continue_button(self, autologin):
        has_user_name = not self.user_name_field.get_text() == ''
        has_password = not self.password_field.get_text() == ''
        can_continue = has_user_name and (autologin or has_password)
        self.continue_button.set_sensitive(can_continue)

    # callbacks ###stack_manager

    def _continue(self, button):
        global_state.advance(self)

    def _on_row_activated(self, list_box, row):
        if row.get_name() == 'automatic_login':
            self.autologin_switch.activate()

    def _on_autologin_switch_flipped(self, autologin_switch, state):
        self._set_continue_button(state)

    def _on_entry_changed(self, editable):
        self._set_continue_button(self.autologin_switch.get_state())

    ### public methods ###

    def unload(self):
        global_state.set_config('user_name', self.user_name_field.get_text())
        global_state.set_config('user_password', self.password_field.get_text())
        global_state.set_config('user_autologin', self.autologin_switch.get_state())
