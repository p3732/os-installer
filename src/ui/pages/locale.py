from .formats_chooser import FormatsChooser
from .locale_provider import LocaleProvider
from .timezone_chooser import TimezoneChooser
from .widgets import ProgressRow

from gi.repository import GLib, Gtk


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/locale.ui')
class LocalePage(Gtk.Box):
    __gtype_name__ = 'LocalePage'

    stack = Gtk.Template.Child()

    overview_list = Gtk.Template.Child()
    formats_label = Gtk.Template.Child()
    timezone_label = Gtk.Template.Child()
    confirm_overview_button = Gtk.Template.Child()

    def __init__(self, global_state, **kwargs):
        super().__init__(**kwargs)

        self.global_state = global_state
        self.timezone_chooser_setup = False
        self.formats_chooser_setup = False

        # provider
        self.locale_provider = LocaleProvider(global_state)

        # signals
        self.overview_list.connect('row-activated', self._on_overview_row_activated)
        self.confirm_overview_button.connect('clicked', self._on_clicked_confirm_overview_button)

    def _load_formats_list(self):
        if not self.formats_chooser_setup:
            self.formats_chooser = FormatsChooser(self.locale_provider, self._on_formats_chosen)
            self.stack.add_named(self.formats_chooser, 'formats')
            self.formats_chooser_setup = True
        self.formats_chooser.load()
        self.stack.set_visible_child_name('formats')

    def _load_timezone_chooser(self):
        if not self.timezone_chooser_setup:
            self.timezone_chooser = TimezoneChooser(self._on_timezone_chosen)
            self.stack.add_named(self.timezone_chooser, 'timezone')
            self.timezone_chooser_setup = True
        self.timezone_chooser.load()
        self.stack.set_visible_child_name('timezone')

    ### callbacks ###

    def _on_timezone_chosen(self, timezone):
        # set timezone
        self.global_state.set_config('timezone', timezone)
        self.global_state.apply_timezone()

        # UI state
        self.timezone_label.set_label(timezone)
        self.stack.set_visible_child_name('overview')

    def _on_formats_chosen(self, name, formats):
        print(name, formats)
        self.global_state.set_config('formats', formats)

        # UI state
        self.formats_label.set_label(name)
        self.stack.set_visible_child_name('overview')

    def _on_overview_row_activated(self, list_box, row):
        if row.get_name() == 'timezone':
            self._load_timezone_chooser()
        elif row.get_name() == 'formats':
            self._load_formats_list()

    def _on_clicked_confirm_overview_button(self, button):
        self.global_state.advance()

    ### public methods ###

    def load(self):
        name, _ = self.locale_provider.get_current_formats()
        self.formats_label.set_label(name)
        timezone = self.locale_provider.get_timezone()
        self.timezone_label.set_label(timezone)

        self.stack.set_visible_child_name('overview')
