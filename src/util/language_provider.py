from gi.repository import GnomeDesktop

from threading import Lock
import os


class LanguageProvider:
    def __init__(self, global_state):
        # load all languages/existing translations
        localedir = global_state.get_config('localedir')
        self.existing_translations_loaded = False
        self.existing_translations_lock = Lock()
        self.existing_translations = global_state.get_future_from(self._load_existing_translations, localedir=localedir)

        # load suggested languages
        config_languages = global_state.get_config('suggested_languages')
        self.suggested_languages_loaded = False
        self.suggested_languages_lock = Lock()
        self.suggested_languages = global_state.get_future_from(
            self._load_suggested_languages, config_languages=config_languages)

    def _load_existing_translations(self, localedir):
        '''
        Load all existing translations by checking for existing translations in the locale folder.
        '''
        existing_translations = set()

        for file in os.scandir(localedir):
            if file.is_dir():
                locale_folder = os.path.join(file.path, 'LC_MESSAGES')
                if os.path.isdir(locale_folder):
                    for locale_file in os.scandir(locale_folder):
                        if locale_file.name == 'os-installer.mo':
                            language = os.path.basename(file.path)
                            existing_translations.add(language)
        return existing_translations

    def _load_suggested_languages(self, config_languages):
        '''
        Load the suggested languages and filter them for those with actually existing translations.
        '''
        existing_translations = self.get_all_languages()

        suggested_languages = []
        for language in config_languages:
            name = self._get_language_name(language)
            if language in existing_translations:
                suggested_languages.append((language, name))
            else:
                print(name, " does not yet have any translations, can not provide it. (Consider contributing a translation for it.)")

        return suggested_languages

    def _get_language_name(self, language):
        return GnomeDesktop.get_language_from_code(language)

    ### public methods ###

    def get_all_languages(self):
        with self.existing_translations_lock:
            if not self.existing_translations_loaded:
                self.existing_translations = self.existing_translations.result()
                self.existing_translations_loaded = True
            return self.existing_translations

    def get_suggested_languages(self):
        with self.suggested_languages_lock:
            if not self.suggested_languages_loaded:
                self.suggested_languages = self.suggested_languages.result()
                self.suggested_languages_loaded = True
            return self.suggested_languages
