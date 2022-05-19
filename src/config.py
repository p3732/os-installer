# SPDX-License-Identifier: GPL-3.0-or-later

import yaml

DEFAULT_CONFIG_PATH = '/etc/os-installer/config.yaml'


def _bool_to_int(b: bool):
    return 1 if b else 0


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
        'additional_software': {},

        'version': -1,
        'distribution_name': None
    }


def _set_defaults_for_optional_pages(config):
    config['use_encryption'] = 'en_US.utf-8'
    config['chosen_additional_software'] = ''
    config['disk_name'] = 'Test Dummy'  # for testing


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
    _set_defaults_for_optional_pages(config)
    return config


def create_envs(config, with_install_envs, with_configure_envs):
    if (with_install_envs and not _install_variables_set(config) or
            with_configure_envs and not _configure_variables_set(config)):
        return None
    envs = []
    if with_install_envs:
        envs += [
            f'OSI_LOCALE="{config["locale"]}"',
            f'OSI_DEVICE_PATH="{config["disk_device_path"]}"',
            f'OSI_DEVICE_IS_PARTITION={_bool_to_int(config["disk_is_partition"])}',
            f'OSI_DEVICE_EFI_PARTITION="{config["disk_efi_partition"]}"',
            f'OSI_USE_ENCRYPTION={_bool_to_int(config["use_encryption"])}',
            f'OSI_ENCRYPTION_PIN="{config["encryption_pin"]}"',
        ]
    if with_configure_envs:
        envs += [
            f'OSI_USER_NAME="{config["user_name"]}"',
            f'OSI_USER_AUTOLOGIN={_bool_to_int(config["user_autologin"])}',
            f'OSI_USER_PASSWORD="{config["user_password"]}"',
            f'OSI_FORMATS="{config["formats"]}"',
            f'OSI_TIMEZONE="{config["timezone"]}"',
            f'OSI_ADDITIONAL_SOFTWARE="{config["chosen_additional_software"]}"',
        ]
    return envs + [None]
