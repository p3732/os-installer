from gi.repository import GnomeDesktop


class LocaleProvider:
    def __init__(self, global_state):
        self.global_state = global_state

    ### public methods ###

    def get_timezone(self):
        timezone = GnomeDesktop.WallClock().get_timezone()
        return timezone.get_identifier()

    def get_current_formats(self):
        # TODO
        return ('de_DE.utf8', 'German')

    def get_formats(self):
        # TODO
        return [('de_DE.utf8', 'German')]
