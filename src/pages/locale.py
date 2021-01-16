from .locale_provider import LocaleProvider
from .timezone_window import TimezoneWindow
from .widgets import ProgressRow

from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/locale.ui')
class LocalePage(Gtk.Box):
    __gtype_name__ = 'LocalePage'

    stack = Gtk.Template.Child()

    overview_list = Gtk.Template.Child()
    formats_label = Gtk.Template.Child()
    timezone_label = Gtk.Template.Child()
    confirm_overview_button = Gtk.Template.Child()

    formats_list = Gtk.Template.Child()

    def __init__(self, global_state, **kwargs):
        super().__init__(**kwargs)

        self.global_state = global_state
        self.formats_list_loaded = False
        self.TimezoneMap = None
        self.timezone_window = None

        # provider
        self.locale_provider = LocaleProvider(global_state)

        # signals
        self.overview_list.connect('row-activated', self._on_overview_row_activated)
        self.formats_list.connect('row-activated', self._on_formats_row_activated)
        self.confirm_overview_button.connect("clicked", self._on_clicked_confirm_overview_button)

    def _load_formats_list(self):
        if not self.formats_list_loaded:
            formats = self.locale_provider.get_formats()
            for language, name in formats:
                row = ProgressRow(name, language)
                self.formats_list.add(row)

            self.formats_list_loaded = True
        self.stack.set_visible_child_name('formats')

    def _load_overview_list(self):
        locale, name = self.locale_provider.get_current_formats()
        self.formats_label.set_label(name)
        timezone = self.locale_provider.get_timezone()
        self.timezone_label.set_label(timezone)

        self.stack.set_visible_child_name('overview')

    def _load_timezone_map(self):
        timezone = self.locale_provider.get_timezone()
        self.global_state.set_config('timezone', timezone)

        # create timezone window
        timezone = self.locale_provider.get_timezone()
        self.timezone_window = TimezoneWindow(self, timezone, self._on_timezone_chosen, self.global_state)
        self.timezone_window.show_all()

    ### callbacks ###

    def _on_timezone_chosen(self, button):
        # set timezone
        timezone = self.timezone_window.timezone
        self.global_state.set_config('timezone', timezone)
        self.global_state.apply_timezone()

        # UI state
        self.timezone_label.set_label(timezone)
        self.stack.set_visible_child_name('overview')

        # close window
        self.timezone_window.close()

    def _on_overview_row_activated(self, list_box, row):
        if row.get_name() == 'timezone':
            self._load_timezone_map()
        elif row.get_name() == 'formats':
            self._load_formats_list()

    def _on_formats_row_activated(self, list_box, row):
        # TODO set and use format
        # locale = row.get_info()
        self._load_overview_list()

    def _on_clicked_confirm_overview_button(self, button):
        self.global_state.advance()

    ### public methods ###

    def load(self):
        self._load_overview_list()

    def save(self):
        formats = self.locale_provider.get_formats()
        self.global_state.set_config('formats', formats)
