# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, Gtk

from .global_state import global_state
from .keyboard_layout_provider import get_default_layout, get_layouts_for
from .language_provider import language_provider
from .page import Page
from .system_calls import set_system_keyboard_layout
from .widgets import reset_model, LanguageRow, SelectionRow

@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/keyboard_layout.ui')
class KeyboardLayoutPage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image_name = 'input-keyboard-symbolic'

    continue_button = Gtk.Template.Child()
    language_label = Gtk.Template.Child()
    language_list = Gtk.Template.Child()
    layout_list = Gtk.Template.Child()
    stack = Gtk.Template.Child()

    languages_model = Gio.ListStore()
    layouts_model = Gio.ListStore()

    current_row = None
    language_list_setup = False
    loaded_language = ''

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

        # models
        self.layout_list.bind_model(self.layouts_model, lambda o: SelectionRow(o.name, o.layout))
        self.language_list.bind_model(self.languages_model, lambda o: LanguageRow(o))

    def _setup_languages_list(self):
        languages = language_provider.get_all_languages_translated()
        reset_model(self.languages_model, languages)

    def _load_layout_list(self, language, short_hand):
        self.stack.set_visible_child_name('layouts')

        if self.loaded_language == short_hand:
            return

        self.loaded_language = short_hand
        self.language_label.set_label(language)

        # fill list with all keyboard layouts for given language
        layouts = get_layouts_for(short_hand, language)
        assert len(layouts) > 0, f'Language {language} has no keyboard layouts! Please report this.'
        reset_model(self.layouts_model, layouts)
        first_row = self.layout_list.get_row_at_index(0)
        self._activate_layout_row(self.layout_list, first_row)

    def _set_checkmark(self, row):
        if self.current_row:
            self.current_row.set_activated(False)
        self.current_row = row
        self.current_row.set_activated(True)
        self.continue_button.set_sensitive(True)

    ### callbacks ###

    @Gtk.Template.Callback('continue')
    def _continue(self, button):
        global_state.advance(self)

    @Gtk.Template.Callback('language_row_activated')
    def _language_row_activated(self, list_box, row):
        # show layouts for language
        language_info = row.info
        self._load_layout_list(language_info.name, language_info.language_code)
        self.can_navigate_backward = False

    @Gtk.Template.Callback('activate_layout_row')
    def _activate_layout_row(self, list_box, row):
        if self.current_row == row:
            return
        self._set_checkmark(row)

        # use selected keyboard layout
        keyboard_layout = row.get_label()
        language_code = row.info
        set_system_keyboard_layout(keyboard_layout, language_code)

    @Gtk.Template.Callback('show_language_selection')
    def _show_language_selection(self, button):
        if not self.language_list_setup:
            self.language_list_setup = True
            self._setup_languages_list()

        # show language selection
        self.stack.set_visible_child_name('languages')
        self.can_navigate_backward = True

    ### public methods ###

    def load_once(self):
        # page gets reconstructed if different app language is chosen
        language_code = global_state.get_config('language_short_hand')
        language = global_state.get_config('language')
        self._load_layout_list(language, language_code)

    def navigate_backward(self):
        self.can_navigate_backward = False
        self.stack.set_visible_child_name('layouts')
