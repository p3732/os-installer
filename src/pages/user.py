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

    def _can_continue_(self, user_name=None, password=None):
        if not user_name:
            user_name = self.user_name_field.get_text()
        if not password:
            password = self.password_field.get_text()
        has_user_name = not user_name == ''
        needs_password = self.user_name_field.get_state()
        has_password = not password == ''
        # TODO remove
        print(user_name)
        print(password)
        if has_user_name and (not needs_password or has_password):
            return True
        else:
            return False

    def _set_navigation(self, user_name=None, password=None):
        # disable forward navigation if no auto-login and no password given
        ok_to_proceed = self._can_continue_(user_name, password)
        self.global_state.set_ok_to_proceed(ok_to_proceed)

    ### callbacks ###

    def _on_autologin_switch_flipped(self, autologin_switch, state):
        self.revealer.set_reveal_child(not state)
        self._set_navigation()

    def _on_user_name_changed(self, editable):
        user_name = editable.get_chars(0, -1)
        self.global_state.set_user_name(True, user_name)
        self._set_navigation(user_name=user_name)

    def _on_password_changed(self, editable):
        password = editable.get_chars(0, -1)
        self.global_state.set_password(True, user_name)
        self._set_navigation(password=password)

    ### public methods ###

    def load(self):
        if self._can_continue_():
            return 'ok_to_proceed'
