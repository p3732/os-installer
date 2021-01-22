from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/user.ui')
class UserPage(Gtk.Box):
    __gtype_name__ = 'UserPage'

    user_name_field = Gtk.Template.Child()
    autologin_switch = Gtk.Template.Child()

    revealer = Gtk.Template.Child()
    password_field = Gtk.Template.Child()

    def __init__(self, global_state, **kwargs):
        super().__init__(**kwargs)

        self.global_state = global_state

        # signals
        self.autologin_switch.connect("state-set", self._on_autologin_switch_flipped)
        self.user_name_field.connect("changed", self._on_user_name_changed)
        self.password_field.connect("changed", self._on_password_changed)

    def _can_continue_(self, switch_state=None):
        has_user_name = not self.user_name_field.get_text() == ''
        has_password = not self.password_field.get_text() == ''
        if switch_state == None:
            needs_password = not self.autologin_switch.get_state()
        else:
            needs_password = not switch_state

        # can not continue if no auto-login and no password given
        return has_user_name and ((not needs_password) or has_password)

    def _set_navigation(self, switch_state=None):
        ok_to_proceed = self._can_continue_(switch_state)
        self.global_state.page_is_ok_to_proceed(self.__gtype_name__, ok_to_proceed)

    ### callbacks ###

    def _on_autologin_switch_flipped(self, autologin_switch, state):
        self.revealer.set_reveal_child(not state)
        self._set_navigation(state)

    def _on_user_name_changed(self, editable):
        self._set_navigation()

    def _on_password_changed(self, editable):
        self._set_navigation()

    ### public methods ###

    def load(self):
        if self._can_continue_():
            return 'ok_to_proceed'

    def save(self):
        password = self.password_field.get_text()
        user_name = self.user_name_field.get_text()
        self.global_state.set_config('password', password)
        self.global_state.set_config('user_name', user_name)
