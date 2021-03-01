# SPDX-License-Identifier: GPL-3.0-or-later

from .widgets import LanguageRow

from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/language.ui')
class LanguagePage(Gtk.Box):
    __gtype_name__ = 'LanguagePage'

    language_list = Gtk.Template.Child()
    show_all_row = Gtk.Template.Child()

    def __init__(self, global_state, **kwargs):
        super().__init__(**kwargs)

        self.global_state = global_state
        self.loaded = False

        # provider
        self.language_provider = global_state.language_provider

        # signals
        self.language_list.connect('row-activated', self._on_language_row_activated)

    def _setup_list(self):
        # insert all suggested languages before show all row
        position = 0
        for language_info in self.language_provider.get_suggested_languages():
            row = LanguageRow(language_info)
            self.language_list.insert(row, position)
            position += 1
        if self.language_provider.has_additional_languages():
            self.show_all_row.set_visible(True)

    def _show_all(self):
        self.show_all_row.set_visible(False)

        for language_info in self.language_provider.get_additional_languages():
            row = LanguageRow(language_info)
            self.language_list.add(row)

    ### callbacks ###

    def _on_language_row_activated(self, list_box, row):
        if row.get_name() == 'show_all_row':
            self._show_all()
        else:
            list_box.select_row(row)

            # set language
            self.global_state.apply_language_settings(row.info)

            self.global_state.advance()

    ### public methods ###

    def load(self):
        if not self.loaded:
            self._setup_list()
            self.loaded = True
