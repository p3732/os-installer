from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/restart.ui')
class RestartPage(Gtk.Box):
    __gtype_name__ = 'RestartPage'

    def __init__(self, global_state, **kwargs):
        super().__init__(**kwargs)

        self.global_state = global_state

    ### public methods ###

    def load(self):
        self.global_state.apply_restart()
