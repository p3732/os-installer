# TODO necessary?
from pathlib import Path
from pathlib import os

import json
from threading import Lock


class LanguageProvider:
    def __init__(self, global_state):
        self.json_loaded = False
        # TODO get real file path
        self.json_file_path = '/home/p3732/Projects/os-installer/data/resources/json/supported_languages.json'
        self.json_load_lock = Lock()

        self.json_data = global_state.get_future_from(
            self._load_json)

    def _load_json(self):
        with open(self.json_file_path, 'r') as file:
            json_data = json.load(file)
        return json_data

    def _assert_json_loaded(self):
        with self.json_load_lock:
            if not self.json_loaded:
                self.json_data = self.json_data.result()
                self.json_loaded = True

    ### public methods ###

    def get_suggested_languages(self):
        self._assert_json_loaded()

        suggested_languages = []
        for language in self.json_data['suggested']:
            name = self.json_data[language]
            suggested_languages.append((language, name))

        return suggested_languages

    def get_all_languages(self):
        self._assert_json_loaded()

        all_languages = []
        for language in self.json_data:
            if not language == 'suggested':
                name = self.json_data[language]
                all_languages.append((language, name))

        return all_languages
