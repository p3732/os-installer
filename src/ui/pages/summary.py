# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, Gtk

from .global_state import global_state
from .installation_scripting import installation_scripting, Step
from .page import Page
#from .software_provider import get_software_suggestions
from .widgets import reset_model, SoftwareSummaryRow


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/summary.ui')
class SummaryPage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image = 'checkbox-checked-symbolic'

    # rows
    language_row = Gtk.Template.Child()
    keyboard_row = Gtk.Template.Child()
    user_row = Gtk.Template.Child()
    format_row = Gtk.Template.Child()
    timezone_row = Gtk.Template.Child()
    software_row = Gtk.Template.Child()

    # row content
    language_label = Gtk.Template.Child()
    keyboard_label = Gtk.Template.Child()
    user_label = Gtk.Template.Child()
    user_autologin = Gtk.Template.Child()
    format_label = Gtk.Template.Child()
    timezone_label = Gtk.Template.Child()

    # software list
    software_stack = Gtk.Template.Child()
    software_list = Gtk.Template.Child()
    software_model = Gio.ListStore()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)
        self.software_list.bind_model(
            self.software_model, lambda pkg: SoftwareSummaryRow(pkg.name, pkg.icon_path))
        self.language_row.set_visible(global_state.get_config('fixed_language'))
        self.software_row.set_visible(global_state.get_config('additional_software'))
        self.user_row.set_visible(not global_state.get_config('skip_user'))
        self.format_row.set_visible(not global_state.get_config('skip_locale'))
        self.timezone_row.set_visible(not global_state.get_config('skip_locale'))

    ### callbacks ###

    @Gtk.Template.Callback('continue')
    def _continue(self, button):
        global_state.advance(self, allow_return=False, cleanup=True)
        installation_scripting.set_ok_to_start_step(Step.configure)

    @Gtk.Template.Callback('summary_row_activated')
    def _summary_row_activated(self, list_box, row):
        global_state.navigate_to_page(row.get_name())

    ### public methods ###

    def load(self):
        self.language_label.set_label(global_state.get_config('language'))
        self.keyboard_label.set_label(
            global_state.get_config('keyboard_layout_ui'))
        self.user_label.set_label(global_state.get_config('user_name'))
        self.user_autologin.set_visible(
            global_state.get_config('user_autologin'))
        self.format_label.set_label(global_state.get_config('formats_ui'))
        self.timezone_label.set_label(global_state.get_config('timezone'))

        software = global_state.get_config('chosen_software')
        if len(software) > 0:
            self.software_stack.set_visible_child_name('used')
            reset_model(self.software_model, software)
        else:
            self.software_stack.set_visible_child_name('none')

        return "prevent_back_navigation"
