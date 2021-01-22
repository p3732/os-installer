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

    def _can_proceed(self, needs_pin=None, pin=None):
        if needs_pin == None:
            needs_pin = self.switch.get_state()
        if pin == None:
            pin = self.pin_field.get_text()
        return not needs_pin or not pin == ''

    ### callbacks ###

    def _on_switch_flipped(self, switch, state):
        self.revealer.set_reveal_child(state)
        can_proceed = self._can_proceed(needs_pin=state)
        self.global_state.page_is_ok_to_proceed(self.__gtype_name__, can_proceed)

    def _on_pin_changed(self, editable):
        can_proceed = self._can_proceed(pin=editable.get_text())
        self.global_state.page_is_ok_to_proceed(self.__gtype_name__, can_proceed)

    ### public methods ###

    def load(self):
        return 'ok_to_proceed'

    def save(self):
        use_encryption = self.switch.get_state()
        pin = self.pin_field.get_text()
        self.global_state.set_config('use_encryption', use_encryption)
        self.global_state.set_config('encryption_pin', pin)
