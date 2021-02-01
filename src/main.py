# SPDX-License-Identifier: GPL-3.0-or-later

import gi

# set versions for all used submodules
gi.require_version('Gdk', '3.0')           # noqa: E402
gi.require_version('Gio', '2.0')           # noqa: E402
gi.require_version('GLib', '2.0')          # noqa: E402
gi.require_version('GnomeDesktop', '3.0')  # noqa: E402
gi.require_version('Gtk', '3.0')           # noqa: E402
gi.require_version('GWeather', '3.0')      # noqa: E402
gi.require_version('Handy', '1')           # noqa: E402
gi.require_version('UDisks', '2.0')        # noqa: E402
gi.require_version('Vte', '2.91')          # noqa: E402
from gi.repository import Gdk, Gio, GLib, Gtk, Handy

import sys

# local
from .global_state import GlobalState
from .window import OsInstallerWindow

APP_ID = 'com.github.p3732.OS-Installer'


class Application(Gtk.Application):
    def __init__(self, version, localedir):
        super().__init__(application_id=APP_ID,
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE)

        # Connect app shutdown signal
        self.connect('shutdown', self._on_quit)

        # Add --hidden command line option
        self.add_main_option('demo-mode', b'd', GLib.OptionFlags.NONE,
                             GLib.OptionArg.NONE, "Run in demo mode, don't alter the system", None)

        # App window
        self.window = None

        self.global_state = GlobalState(localedir)

    def _load_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource('/com/github/p3732/os-installer/css/style.css')
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

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

    def _setup_icons(self):
        icon_theme = Gtk.IconTheme.get_default()
        icon_theme.add_resource_path('/com/github/p3732/os-installer/')
        icon_theme.add_resource_path('/com/github/p3732/os-installer/icon')

    ### parent functions ###

    def do_activate(self):
        # create window if not existing
        self.window = self.props.active_window
        if not self.window:
            self.window = OsInstallerWindow(self.global_state, application=self)
        self.window.present()

        # Grab window delete-event
        self.window.connect('delete-event', self._on_quit)

        self.global_state.window = self.window
        self.global_state.load_initial_page()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        options = options.end().unpack()

        if 'demo-mode' in options:
            self.global_state.demo_mode = True

        self.activate()
        return 0

    def do_startup(self):
        # Startup application
        Gtk.Application.do_startup(self)
        self._load_css()
        self._setup_actions()
        self._setup_icons()

        # Init Handy
        Handy.init()

    ### callbacks ###

    def _on_next_page(self, action, param):
        self.global_state.try_go_to_next()

    def _on_previous_page(self, action, param):
        self.global_state.try_go_to_previous()

    def _on_quit(self, action, param=None):
        if self.global_state.installation_running:
            # show confirm dialog
            self.window.show_confirm_quit_dialog(self.quit)
            # return True to avoid further processing of event
            return True
        else:
            self.quit()


def main(version, localedir):
    app = Application(version, localedir)
    return app.run(sys.argv)
