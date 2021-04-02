# SPDX-License-Identifier: GPL-3.0-or-later

import yaml

DEFAULT_CONFIG_PATH = '/etc/os-installer/config.yaml'


def _install_variables_set(config):
    return ('locale' in config and
            'disk_device_path' in config and
            'disk_is_partition' in config and
            'disk_efi_partition' in config and
            'use_encryption' in config and
            'encryption_pin' in config)


def _configure_variables_set(config):
    return ('user_name' in config and
            'user_autologin' in config and
            'user_password' in config and
            'formats' in config and
            'timezone' in config and
            'chosen_additional_software' in config)


def _get_fallback_config():
    return {
        'internet_connection_required': True,
        'internet_checker_url': 'http://nmcheck.gnome.org/check_network_status.txt',
        'suggested_languages': ['en', 'ar', 'de', 'es', 'fr', 'ja', 'ru', 'zh'],
        'minimum_disk_size': 5,
        'offer_disk_encryption': True,
        'additional_software': {}
    }


def _set_defaults_for_optional_pages(config):
    config['use_encryption'] = 'en_US.utf-8'
    config['chosen_additional_software'] = ''
    return config


### public methods ###
def init_config():
    config = _get_fallback_config()
    try:
        with open(DEFAULT_CONFIG_PATH, 'r') as file:
            config_from_file = yaml.load(file, Loader=yaml.Loader)
            for config_property in config_from_file:
                config[config_property] = config_from_file[config_property]
    except:
        print('No config provided, using fallback config.')
    return _set_defaults_for_optional_pages(config)


def create_envs(config, with_install_envs=False, with_configure_envs=False):
    if (with_install_envs and not _install_variables_set(config) or
            with_configure_envs and not _configure_variables_set(config)):
        return None
    envs = []
    if with_install_envs:
        envs += [
            'OSI_LOCALE="' + config['locale'] + '"',
            'OSI_DEVICE_PATH="' + config['disk_device_path'] + '"',
            'OSI_DEVICE_IS_PARTITION=' + str(1 if config['disk_is_partition'] else 0),
            'OSI_DEVICE_EFI_PARTITION="' + config['disk_efi_partition'] + '"',
            'OSI_USE_ENCRYPTION=' + str(1 if config['use_encryption'] else 0),
            'OSI_ENCRYPTION_PIN="' + config['encryption_pin'] + '"']
    if with_configure_envs:
        envs += [
            'OSI_USER_NAME="' + config['user_name'] + '"',
            'OSI_USER_AUTOLOGIN=' + str(1 if config['user_autologin'] else 0),
            'OSI_USER_PASSWORD="' + config['user_password'] + '"',
            'OSI_FORMATS="' + config['formats'] + '"',
            'OSI_TIMEZONE="' + config['timezone'] + '"',
            'OSI_ADDITIONAL_SOFTWARE="' + config['chosen_additional_software'] + '"']
    return envs + [None]
