from .locale_provider import LocaleProvider

from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/locale.ui')
class LocalePage(Gtk.Box):
    __gtype_name__ = 'LocalePage'

    formats_label = Gtk.Template.Child()
    formats_button = Gtk.Template.Child()

    timezone_label = Gtk.Template.Child()
    timezone_button = Gtk.Template.Child()

    def __init__(self, global_state, **kwargs):
        super().__init__(**kwargs)

        self.global_state = global_state

        self.locale_provider = LocaleProvider(global_state)

        # signals
        self.formats_button.connect("clicked", self._on_clicked_formats_button)
        self.timezone_button.connect("clicked", self._on_clicked_timezone_button)

    def _set_formats(self):
        formats = self.locale_provider.get_formats()
        self.formats_label.set_label(formats)

    def _set_timezone(self):
        timezone = self.locale_provider.get_timezone()
        self.timezone_label.set_label(timezone)

    ### callbacks ###

    def _on_clicked_formats_button(self, button):
        # TODO enable passing callback that gets called after closing settings
        self.global_state.open_settings('region')

    def _on_clicked_timezone_button(self, button):
        # TODO enable passing callback that gets called after closing settings
        self.global_state.open_settings('datetime')

    ### public methods ###

    def load(self):
        self._set_formats()
        self._set_timezone()
        return 'ok_to_proceed'

    def save(self):
        formats = self.locale_provider.get_formats()
        timezone = self.locale_provider.get_timezone()
        self.global_state.set_locales(formats, timezone)
