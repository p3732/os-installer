# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, Gtk

from .global_state import global_state
from .page import Page
from .feature_provider import get_feature_suggestions
from .widgets import reset_model, SelectionRow


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/feature.ui')
class FeaturePage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image = 'puzzle-piece-symbolic'

    list = Gtk.Template.Child()
    list_model = Gio.ListStore()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)
        self.list.bind_model(
            self.list_model,
            lambda feat: SelectionRow(feat.name, feat.description, feat.icon_path,
                                      feat.suggested, feat, 'puzzle-piece-symbolic'))

    ### callbacks ###

    @Gtk.Template.Callback('continue')
    def _continue(self, button):
        global_state.advance(self)

    @Gtk.Template.Callback('row_activated')
    def _row_activated(self, list_box, row):
        row.flip_switch()

    ### public methods ###

    def load_once(self):
        suggestions = get_feature_suggestions()
        reset_model(self.list_model, suggestions)

    def unload(self):
        choices = [row.info for row in self.list if row.is_activated()]
        features = ' '.join([choice.feature for choice in choices])
        global_state.set_config('chosen_feature_names', choices)
        global_state.set_config('chosen_features', features)
