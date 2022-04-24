# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk

from .global_state import global_state
from .page import Page


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/encrypt.ui')
class EncryptPage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image_name = 'dialog-password-symbolic'

    default_list = Gtk.Template.Child()
    switch = Gtk.Template.Child()

    pin_row = Gtk.Template.Child()
    pin_field = Gtk.Template.Child()

    continue_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

        # signals
        self.continue_button.connect('clicked', self._continue)
        self.default_list.connect('row-activated', self._on_row_activated)
        self.switch.connect("state-set", self._on_switch_flipped)
        self.pin_field.connect("changed", self._on_pin_changed)

    def _set_continue_button(self, needs_pin, has_pin):
        can_continue = not needs_pin or has_pin
        self.continue_button.set_sensitive(can_continue)

    ### callbacks ###

    def _continue(self, button):
        global_state.advance(self)

    def _on_row_activated(self, list_box, row):
        if row.get_name() == 'encryption':
            self.switch.activate()

    def _on_switch_flipped(self, switch, state):
        self.pin_row.set_sensitive(state)

        needs_pin = state
        has_pin = len(self.pin_field.get_text()) > 0
        self._set_continue_button(needs_pin, has_pin)

    def _on_pin_changed(self, editable):
        needs_pin = self.switch.get_state()
        has_pin = len(editable.get_text()) > 0
        self._set_continue_button(needs_pin, has_pin)

    ### public methods ###

    def unload(self):
        use_encryption = self.switch.get_state()
        pin = self.pin_field.get_text()
        global_state.set_config('use_encryption', use_encryption)
        global_state.set_config('encryption_pin', pin)
