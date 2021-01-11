import sys
import gi

gi.require_version('Gtk', '3.0')           # noqa: E402
gi.require_version('Gdk', '3.0')           # noqa: E402
gi.require_version('GnomeDesktop', '3.0')  # noqa: E402
gi.require_version('Handy', '1')           # noqa: E402
gi.require_version('Json', '1.0')          # noqa: E402
gi.require_version('TimezoneMap', '1.0')   # noqa: E402

from gi.repository import Gdk, Gio, GLib, Gtk, Handy

# local
from .global_state import GlobalState
from .window import OsInstallerWindow

APP_ID = 'com.github.p3732.OS-Installer'


class Application(Gtk.Application):
    def __init__(self, version):
        super().__init__(application_id=APP_ID,
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        GLib.set_application_name(_('OS Installer'))
        GLib.set_prgname(APP_ID)

        # App window
        self.window = None

        self.global_state = GlobalState()

        # TODO would this be useful?
        # self.set_resource_base_path('/com/github/p3732/os-installer/')
        #Gtk.IconTheme.add_resource_path(Gtk.IconTheme.get_default(), '/com/github/p3732/os-installer/icons')

    def do_startup(self):
        # Startup application
        Gtk.Application.do_startup(self)
        self._setup_actions()
        self._load_css()

    def _load_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource('/com/github/p3732/os-installer/css/style.css')
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        # Init Handy
        Handy.init()

    def _setup_actions(self):
        actions = [
            {
                'name': 'next-page',
                'func': self._on_next_page,
                'accels': ['<Alt>Right']
            },
            {
                'name': 'previous-page',
                'func': self._on_previous_page,
                'accels': ['<Alt>Left']
            },
            {
                'name': 'quit',
                'func': self._on_quit,
                'accels': ['<Ctl>q']
            }
        ]

        for a in actions:
            action = Gio.SimpleAction.new(a['name'], None)
            action.connect('activate', a['func'])

            self.add_action(action)

            if 'accels' in a:
                self.set_accels_for_action('app.' + a['name'], a['accels'])

    def do_activate(self):
        self.window = self.props.active_window
        if not self.window:
            self.window = OsInstallerWindow(self.global_state, application=self)
        self.window.present()

        self.global_state.load_initial_page()

    def _on_next_page(self, action, param):
        self.global_state.try_go_to_next()

    def _on_previous_page(self, action, param):
        self.global_state.try_go_to_previous()

    def _on_quit(self, action, param):
        # TODO show warning if in installation process
        self.quit()


def main(version):
    app = Application(version)
    return app.run(sys.argv)
