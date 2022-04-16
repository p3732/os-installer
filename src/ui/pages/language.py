# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk

from .global_state import global_state
from .language_provider import language_provider
from .page import Page
from .system_calls import set_system_language
from .widgets import LanguageRow


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/language.ui')
class LanguagePage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image_name = 'language-symbolic'

    stack = Gtk.Template.Child()

    default_list = Gtk.Template.Child()
    show_all_button = Gtk.Template.Child()
    all_list = Gtk.Template.Child()

    all_shown = False

    def __init__(self, **kwargs):
        Gtk.Overlay.__init__(self, **kwargs)

        language_provider.prepare()

        # signals
        self.show_all_button.connect('clicked', self._on_show_all_button_clicked)
        self.default_list.connect('row-activated', self._on_language_row_activated)
        self.all_list.connect('row-activated', self._on_language_row_activated)

        self.stack.set_visible_child_name('default')

    def _setup_list(self):
        # language rows
        for language_info in language_provider.get_suggested_languages():
            self.default_list.append(LanguageRow(language_info))

        # show all button
        present_show_all = language_provider.has_additional_languages()
        self.show_all_button.set_visible(present_show_all)

    ### callbacks ###

    def _on_show_all_button_clicked(self, button):
        if not self.all_shown:
            for language_info in language_provider.get_all_languages():
                self.all_list.append(LanguageRow(language_info))

            self.stack.set_visible_child_name('all')
            self.all_shown = True

    def _on_language_row_activated(self, list_box, row):
        list_box.select_row(row)

        # set language
        set_system_language(row.info)
        global_state.advance(self.__gtype_name__)

    ### public methods ###

    def load_once(self):
        self._setup_list()
