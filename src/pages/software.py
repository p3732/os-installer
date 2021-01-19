from .software_provider import SoftwareProvider
from .widgets import SoftwareRow

from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/software.ui')
class SoftwarePage(Gtk.Box):
    __gtype_name__ = 'SoftwarePage'

    software_list = Gtk.Template.Child()

    def __init__(self, global_state, **kwargs):
        super().__init__(**kwargs)

        self.global_state = global_state
        self.loaded = False
        self.always_skip = False

        self.software_provider = SoftwareProvider(global_state)

    def _setup_software(self):
        suggestions = self.software_provider.get_suggestions()
        if len(suggestions) == 0:
            self.always_skip = True
        else:
            for package_name, default, name, description, icon_path in suggestions:
                row = SoftwareRow(name, description, package_name, default, icon_path)
                self.software_list.add(row)

    ### public methods ###

    def load(self):
        if not self.loaded:
            self._setup_software()
            self.loaded = True
        if self.always_skip:
            return 'automatic'
        else:
            return 'ok_to_proceed'

    def save(self):
        to_install = []
        for row in self.software_list:
            if row.is_activated():
                package_name = row.package_name
                to_install.append(package_name)
        self.global_state.set_config('additional_software', to_install)
