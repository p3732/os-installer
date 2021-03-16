# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk

from .global_state import global_state
from .language_provider import language_provider
from .page import Page
from .system_calls import set_system_language
from .widgets import LanguageRow


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/language.ui')
class LanguagePage(Gtk.Overlay, Page):
    __gtype_name__ = __qualname__
    image_name = 'language-symbolic'

    language_list = Gtk.Template.Child()
    show_all_button = Gtk.Template.Child()
    show_all_revealer = Gtk.Template.Child()

    all_shown = False

    def __init__(self, **kwargs):
        Gtk.Overlay.__init__(self, **kwargs)

        language_provider.prepare()

        # signals
        self.show_all_button.connect('clicked', self._on_show_all_button_clicked)
        self.language_list.connect('row-activated', self._on_language_row_activated)

    def _setup_list(self):
        # language rows
        for language_info in language_provider.get_suggested_languages():
            self.language_list.add(LanguageRow(language_info))

        # show all button
        present_show_all = language_provider.has_additional_languages()
        self.show_all_revealer.set_reveal_child(present_show_all)

    def _show_all(self):
        for language_info in language_provider.get_additional_languages():
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
        set_system_language(row.info)
        global_state.advance()

    ### public methods ###

    def load_once(self):
        self._setup_list()
