from .locale_provider import LocaleProvider
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

    timezone_map_placeholder = Gtk.Template.Child()
    timezone_map_label = Gtk.Template.Child()
    confirm_timezone_button = Gtk.Template.Child()

    def __init__(self, global_state, **kwargs):
        super().__init__(**kwargs)

        self.global_state = global_state
        self.formats_list_loaded = False
        self.timezone_map_loaded = False
        self.timezone_map = None

        # provider
        self.locale_provider = LocaleProvider(global_state)

        # signals
        self.overview_list.connect('row-activated', self._on_overview_row_activated)
        self.formats_list.connect('row-activated', self._on_formats_row_activated)
        self.confirm_overview_button.connect("clicked", self._on_clicked_confirm_overview_button)
        self.confirm_timezone_button.connect("clicked", self._on_clicked_confirm_timezone_button)

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
        if not self.timezone_map_loaded:
            # TODO
            # self.timezone_map
            self.timezone_map_loaded = True
        self.stack.set_visible_child_name('timezone_map')

    ### callbacks ###

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

    def _on_clicked_confirm_timezone_button(self, button):
        # TODO set and use timezone
        self._load_overview_list()

    ### public methods ###

    def load(self):
        self._load_overview_list()

    def save(self):
        formats = self.locale_provider.get_formats()
        timezone = self.locale_provider.get_timezone()
        self.global_state.set_config('formats', formats)
        self.global_state.set_config('timezone', timezone)
