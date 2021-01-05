from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/encrypt.ui')
class EncryptPage(Gtk.Box):
    __gtype_name__ = 'EncryptPage'

    switch = Gtk.Template.Child()

    revealer = Gtk.Template.Child()
    pin_field = Gtk.Template.Child()

    def __init__(self, global_state, **kwargs):
        super().__init__(**kwargs)

        self.global_state = global_state

        # signals
        self.switch.connect("state-set", self._on_switch_flipped)
        self.pin_field.connect("changed", self._on_pin_changed)

    ### callbacks ###

    def _on_switch_flipped(self, switch, state):
        self.revealer.set_reveal_child(state)
        self.global_state.set_encryption(state)

    def _on_pin_changed(self, editable):
        pin = editable.get_chars(0, -1)
        self.global_state.set_encryption(True, pin)

    ### public methods ###

    def load(self):
        return 'ok_to_proceed'
