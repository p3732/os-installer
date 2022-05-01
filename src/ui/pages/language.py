# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, Gtk

from .global_state import global_state
from .language_provider import language_provider
from .page import Page
from .system_calls import set_system_language
from .widgets import reset_model, LanguageRow


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/language.ui')
class LanguagePage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image_name = 'language-symbolic'

    stack = Gtk.Template.Child()

    default_list = Gtk.Template.Child()
    show_all_button = Gtk.Template.Child()
    all_list = Gtk.Template.Child()

    default_model = Gio.ListStore()
    all_model = Gio.ListStore()

    all_shown = False

    def __init__(self, **kwargs):
        Gtk.Overlay.__init__(self, **kwargs)

        language_provider.prepare()

        # models
        self.default_list.bind_model(self.default_model, lambda o: LanguageRow(o))
        self.all_list.bind_model(self.all_model, lambda o: LanguageRow(o))

    def _setup_default(self):
        suggested_languages = language_provider.get_suggested_languages()
        if len(suggested_languages) > 0:
            reset_model(self.default_model, suggested_languages)
            present_show_all = language_provider.has_additional_languages()
            self.show_all_button.set_visible(present_show_all)
        else:
            self._setup_all()

    def _setup_all(self):
        languages = language_provider.get_all_languages()
        reset_model(self.all_model, languages)

        self.stack.set_visible_child_name('all')
        self.all_shown = True

    ### callbacks ###

    @Gtk.Template.Callback('show_all_button_clicked')
    def _show_all_button_clicked(self, button):
        if not self.all_shown:
            self._setup_all()

    @Gtk.Template.Callback('language_row_activated')
    def _language_row_activated(self, list_box, row):
        set_system_language(row.info)
        global_state.advance(self)

    ### public methods ###

    def load_once(self):
        self._setup_default()
