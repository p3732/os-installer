# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, Gtk

from .global_state import global_state
from .language_provider import language_provider
from .page import Page
from .system_calls import set_system_language
from .widgets import reset_model, ProgressRow


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/language.ui')
class LanguagePage(Gtk.Stack, Page):
    __gtype_name__ = __qualname__
    image_name = 'language-symbolic'

    default_list = Gtk.Template.Child()
    show_all_button = Gtk.Template.Child()
    all_list = Gtk.Template.Child()

    default_model = Gio.ListStore()
    all_model = Gio.ListStore()

    all_shown = False
    language_chosen = False

    def __init__(self, **kwargs):
        Gtk.Stack.__init__(self, **kwargs)

        # models
        self.default_list.bind_model(self.default_model, lambda o: ProgressRow(o.name, o))
        self.all_list.bind_model(self.all_model, lambda o: ProgressRow(o.name, o))

    def _setup_all(self):
        languages = language_provider.get_all_languages()
        reset_model(self.all_model, languages)

        self.set_visible_child_name('all')
        self.all_shown = True

    ### callbacks ###

    @Gtk.Template.Callback('show_all_button_clicked')
    def _show_all_button_clicked(self, button):
        if not self.all_shown:
            self._setup_all()

    @Gtk.Template.Callback('language_row_activated')
    def _language_row_activated(self, list_box, row):
        if (not self.language_chosen or
                global_state.get_config('language_code') != row.info.language_code):
            self.language_chosen = True
            set_system_language(row.info)
        global_state.advance(self)

    ### public methods ###

    def load_once(self):
        suggested_languages = language_provider.get_suggested_languages()
        if len(suggested_languages) > 0:
            reset_model(self.default_model, suggested_languages)
            present_show_all = language_provider.has_additional_languages()
            self.show_all_button.set_visible(present_show_all)
        else:
            self._setup_all()