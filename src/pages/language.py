from .language_provider import LanguageProvider
from .widgets import ProgressRow

from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/language.ui')
class LanguagePage(Gtk.Box):
    __gtype_name__ = 'LanguagePage'

    stack = Gtk.Template.Child()

    suggested_list = Gtk.Template.Child()
    all_list = Gtk.Template.Child()

    def __init__(self, global_state, **kwargs):
        super().__init__(**kwargs)

        self.global_state = global_state
        self.loaded = False

        # provider
        self.language_provider = LanguageProvider(global_state)

        # UI element states
        self.stack.set_visible_child_name('suggested')

        # signals
        self.suggested_list.connect('row-activated', self._on_language_row_activated)
        self.all_list.connect('row-activated', self._on_language_row_activated)

    def _setup_suggested_list(self):
        suggested_languages = self.language_provider.get_suggested_languages()

        # insert all suggested languages before show all row
        position = 0
        for language, name in suggested_languages:
            row = ProgressRow(name, language)
            self.suggested_list.insert(row, position)
            position += 1

    def _setup_all_list(self):
        all_languages = self.language_provider.get_all_languages()

        for language, name in all_languages:
            row = ProgressRow(name, language)
            self.all_list.add(row)

    ### callbacks ###

    def _on_language_row_activated(self, list_box, row):
        if row.get_name() == 'show_all_row':
            self._setup_all_list()
            self.stack.set_visible_child_name('all')
        else:
            language = row.get_label()
            short_hand = row.get_info()
            self.global_state.set_language(language, short_hand)
            self.global_state.advance()

    ### public methods ###

    def load(self):
        if not self.loaded:
            self._setup_suggested_list()
            self.loaded = True
