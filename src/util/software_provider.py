class SoftwareProvider:
    def __init__(self, global_state):
        self.global_state = global_state

    ### public methods ###

    def get_suggestions(self):
        # TODO read from config file
        suggestions_file = {}
        suggestions_file['firefox'] = (
            'Firefox',
            'Popular Web Browser from Mozilla',
            '/usr/share/icons/hicolor/64x64/apps/firefox.png')
        suggestions_file['libreoffice-fresh'] = (
            'LibreOffice',
            'Office Suite for Documents, Tables, Presentations and more.',
            '/usr/share/icons/hicolor/64x64/apps/libreoffice-main.png')
        suggestions = []
        for package in suggestions_file:
            name, description, icon_path = suggestions_file[package]
            suggestions.append((package, name, description, icon_path))

        return suggestions
