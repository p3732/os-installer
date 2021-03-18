# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk

from .global_state import global_state
from .keyboard_layout_provider import get_layouts_for
from .language_provider import language_provider
from .page import Page
from .system_calls import set_system_keyboard_layout
from .widgets import LanguageRow, SelectionRow, empty_list


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/keyboard_layout.ui')
class KeyboardLayoutPage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image_name = 'input-keyboard-symbolic'

    change_language_list = Gtk.Template.Child()
    language_label = Gtk.Template.Child()

    stack = Gtk.Template.Child()
    language_list = Gtk.Template.Child()
    layout_list = Gtk.Template.Child()

    continue_button = Gtk.Template.Child()

    current_row = None
    language_list_setup = False
    loaded_language = ''

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

        # signals
        self.continue_button.connect('clicked', self._continue)
        self.change_language_list.connect('row-activated', self._show_language_selection)
        self.language_list.connect('row-activated', self._on_language_row_activated)
        self.layout_list.connect('row-activated', self._on_layout_row_activated)

    def _setup_languages_list(self):
        all_languages = language_provider.get_all_languages()

        for language_info in all_languages:
            row = LanguageRow(language_info)
            self.language_list.add(row)

    def _load_layout_list(self, language, short_hand):
        self.stack.set_visible_child_name('layouts')

        if self.loaded_language == short_hand:
            return
        self.loaded_language = short_hand

        empty_list(self.layout_list)

        self.language_label.set_label(language)

        # fill list with all keyboard layouts for given language
        layouts = get_layouts_for(short_hand, language)
        assert len(layouts) > 0, 'Language {} has no keyboard layouts! Please report this.'.format(language)
        for keyboard_layout, name in layouts:
            row = SelectionRow(name, keyboard_layout)
            self.layout_list.add(row)

    def _unselect_current_row(self):
        if self.current_row:
            self.current_row.set_activated(False)

    ### callbacks ###

    def _continue(self, button):
        global_state.advance(self.__gtype_name__)

    def _on_language_row_activated(self, list_box, row):
        self._unselect_current_row()

        # show layouts for language
        language_info = row.info
        self._load_layout_list(language_info.name, language_info.language_code)

    def _on_layout_row_activated(self, list_box, row):
        self._unselect_current_row()
        self.current_row = row
        row.set_activated(True)

        self.layout_list.select_row(row)

        # use selected keyboard layout
        keyboard_layout = row.get_label()
        short_hand = row.info
        set_system_keyboard_layout(keyboard_layout, short_hand)

        self.continue_button.set_sensitive(True)

    def _show_language_selection(self, list_box, row):
        if not self.language_list_setup:
            self.language_list_setup = True
            self._setup_languages_list()

        # show language selection
        self.stack.set_visible_child_name('languages')
        self.can_navigate_backward = True
        self.continue_button.set_sensitive(False)

    ### public methods ###

    def load_once(self):
        # page gets reconstructed if different app language is chosen
        short_hand = global_state.get_config('language_short_hand')
        language = global_state.get_config('language')
        self._load_layout_list(language, short_hand)

    def navigate_backward(self):
        self.can_navigate_backward = False
        self.stack.set_visible_child_name('layouts')
