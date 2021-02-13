# SPDX-License-Identifier: GPL-3.0-or-later

from .widgets import LanguageRow

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
        self.language_provider = global_state.language_provider

        # UI element states
        self.stack.set_visible_child_name('suggested')

        # signals
        self.suggested_list.connect('row-activated', self._on_language_row_activated)
        self.all_list.connect('row-activated', self._on_language_row_activated)

    def _setup_suggested_list(self):
        suggested_languages = self.language_provider.get_suggested_languages()

        # insert all suggested languages before show all row
        position = 0
        for name, language, locale in suggested_languages:
            row = LanguageRow(name, (language, locale))
            self.suggested_list.insert(row, position)
            position += 1

    def _setup_all_list(self):
        all_languages = self.language_provider.get_all_languages()

        for name, language, locale in all_languages:
            row = LanguageRow(name, (language, locale))
            self.all_list.add(row)

    ### callbacks ###

    def _on_language_row_activated(self, list_box, row):
        if row.get_name() == 'show_all_row':
            self._setup_all_list()
            self.stack.set_visible_child_name('all')
        else:
            list_box.select_row(row)

            # set language
            language = row.get_label()
            short_hand, locale = row.info
            self.global_state.apply_language_settings(language, short_hand, locale)

            self.global_state.advance()

    ### public methods ###

    def load(self):
        if not self.loaded:
            self._setup_suggested_list()
            self.loaded = True
