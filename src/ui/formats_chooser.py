from .widgets import empty_list, ProgressRow

from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/formats_chooser.ui')
class FormatsChooser(Gtk.Box):
    __gtype_name__ = 'FormatsChooser'

    current_formats_row_list = Gtk.Template.Child()
    formats_list = Gtk.Template.Child()

    def __init__(self, locale_provider, callback, **kwargs):
        super().__init__(**kwargs)

        self.locale_provider = locale_provider
        self.callback = callback
        self.formats_list_loaded = False

        # signals
        self.current_formats_row_list.connect('row-activated', self._on_formats_row_activated)
        self.formats_list.connect('row-activated', self._on_formats_row_activated)

    def _load_formats_list(self):
        # current formats row list
        empty_list(self.current_formats_row_list)
        name, locale = self.locale_provider.get_current_formats()
        row = ProgressRow(name, locale)
        self.current_formats_row_list.add(row)

        # all formats list
        if not self.formats_list_loaded:
            formats = self.locale_provider.get_formats()
            for name, locale in formats:
                row = ProgressRow(name, locale)
                self.formats_list.add(row)

            self.formats_list_loaded = True

    ### callbacks ###

    def _on_formats_row_activated(self, list_box, row):
        formats = row.info
        name = row.get_label()
        self.callback(name, formats)

    ### public methods ###

    def load(self):
        self._load_formats_list()
