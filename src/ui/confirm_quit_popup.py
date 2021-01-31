from gi.repository import Gtk, Handy


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/confirm_quit_popup.ui')
class ConfirmQuitPopup(Handy.Window):
    __gtype_name__ = 'ConfirmQuitPopup'

    stop_button = Gtk.Template.Child()
    continue_button = Gtk.Template.Child()

    def __init__(self, confirm_callback, **kwargs):
        super().__init__(**kwargs)

        self.confirm_callback = confirm_callback

        # signals
        self.continue_button.connect('clicked', self._on_clicked_continue_button)
        self.stop_button.connect('clicked', self._on_clicked_stop_button)

    ### callbacks ###

    def _on_clicked_stop_button(self, button):
        self.confirm_callback()

    def _on_clicked_continue_button(self, button):
        self.close()
