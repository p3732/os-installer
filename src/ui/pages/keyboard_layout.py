# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, Gtk

from .global_state import global_state
from .keyboard_layout_provider import get_default_layout, get_layouts_for
from .language_provider import language_provider
from .page import Page
from .system_calls import set_system_keyboard_layout
from .widgets import reset_model, ProgressRow


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/keyboard_layout.ui')
class KeyboardLayoutPage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image = 'input-keyboard-symbolic'

    stack = Gtk.Template.Child()

    # overview
    chosen_layouts = Gtk.Template.Child()
    continue_button = Gtk.Template.Child()
    primary_layout_row = Gtk.Template.Child()

    # layouts
    language_label = Gtk.Template.Child()
    layout_list = Gtk.Template.Child()

    # languages
    language_list = Gtk.Template.Child()

    languages_model = Gio.ListStore()
    layouts_model = Gio.ListStore()

    current_row = None
    language_list_setup = False
    loaded_language = ''

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

        # models
        self.layout_list.bind_model(self.layouts_model, lambda o: ProgressRow(o.name, o))
        self.language_list.bind_model(self.languages_model, lambda o: ProgressRow(o.name, o))

    def _setup_languages_list(self):
        languages = language_provider.get_all_languages_translated()
        reset_model(self.languages_model, languages)

    def _load_overview(self, keyboard_info):
        self.stack.set_visible_child_name('overview')
        self.primary_layout_row.set_title(keyboard_info.name)
        set_system_keyboard_layout(keyboard_info.name, keyboard_info.layout)

    def _load_layout_list(self, language, language_code):
        self.stack.set_visible_child_name('layouts')

        if self.loaded_language == language_code:
            return

        self.loaded_language = language_code
        self.language_label.set_label(language)

        # fill list with all keyboard layouts for given language
        layouts = get_layouts_for(language_code, language)
        reset_model(self.layouts_model, layouts)


    ### callbacks ###

    @Gtk.Template.Callback('continue')
    def _continue(self, button):
        global_state.advance(self)

    @Gtk.Template.Callback('language_row_activated')
    def _language_row_activated(self, list_box, row):
        # show layouts for language
        language_info = row.info
        self._load_layout_list(language_info.name, language_info.language_code)

    @Gtk.Template.Callback('layout_row_activated')
    def _layout_row_activated(self, list_box, row):
        # use selected keyboard layout
        keyboard_info = row.info
        self._load_overview(keyboard_info)
        self.can_navigate_backward = False

    @Gtk.Template.Callback('show_language_selection')
    def _show_language_selection(self, row):
        if not self.language_list_setup:
            self.language_list_setup = True
            self._setup_languages_list()

        # show language selection
        self.stack.set_visible_child_name('languages')
        self.can_navigate_backward = True

    @Gtk.Template.Callback('show_layout_selection')
    def _show_layout_selection(self, row):
        if self.loaded_language == '':
            self._load_layout_list(self.default_language, self.default_language_code)
        else:
            self.stack.set_visible_child_name('layouts')
        self.can_navigate_backward = True

    ### public methods ###

    def load_once(self):
        # page gets reconstructed if different app language is chosen
        self.default_language = global_state.get_config('language')
        self.default_language_code = global_state.get_config('language_code')
        keyboard_info = get_default_layout(self.default_language_code)
        self._load_overview(keyboard_info)

    def navigate_backward(self):
        match self.stack.get_visible_child_name():
            case 'layouts':
                self.stack.set_visible_child_name('overview')
                self.can_navigate_backward = False
            case 'languages':
                self.stack.set_visible_child_name('layouts')
