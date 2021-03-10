# SPDX-License-Identifier: GPL-3.0-or-later

from .page import Page
from .widgets import LanguageRow
from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/language.ui')
class LanguagePage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image_name = 'language-symbolic'

    language_list = Gtk.Template.Child()
    show_all_button = Gtk.Template.Child()
    show_all_revealer = Gtk.Template.Child()

    all_shown = False
    loaded = False

    def __init__(self, global_state, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

        self.global_state = global_state

        # provider
        self.language_provider = global_state.language_provider

        # signals
        self.show_all_button.connect('clicked', self._on_show_all_button_clicked)
        self.language_list.connect('row-activated', self._on_language_row_activated)

    def _setup_list(self):
        # language rows
        for language_info in self.language_provider.get_suggested_languages():
            self.language_list.add(LanguageRow(language_info))

        # show all button
        present_show_all = self.language_provider.has_additional_languages()
        self.show_all_revealer.set_reveal_child(present_show_all)

    def _show_all(self):
        for language_info in self.language_provider.get_additional_languages():
            self.language_list.add(LanguageRow(language_info))

    ### callbacks ###

    def _on_show_all_button_clicked(self, button):
        if not self.all_shown:
            self.all_shown = True

            self.show_all_revealer.set_reveal_child(False)
            self._show_all()

    def _on_language_row_activated(self, list_box, row):
        list_box.select_row(row)

        # set language
        self.global_state.apply_language_settings(row.info)

        self.global_state.advance()

    ### public methods ###

    def load(self):
        if not self.loaded:
            self._setup_list()
            self.loaded = True
