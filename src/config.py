import yaml

DEFAULT_CONFIG_PATH = '/etc/os-installer/config.yaml'


def _get_fallback_config():
    return {
        'internet_checker_url': 'http://nmcheck.gnome.org/check_network_status.txt',
        'suggested_languages': ['en', 'ar', 'de', 'es', 'fr', 'ja', 'ru', 'zh'],
        'additional_software': {}
    }


### public methods ###

def get_config():
    config = _get_fallback_config()
    try:
        with open(DEFAULT_CONFIG_PATH, 'r') as file:
            config_from_file = yaml.load(file, Loader=yaml.Loader)
            for config_property in config_from_file:
                config[config_property] = config_from_file[config_property]
    except:
        print('No config provided, using fallback config.')
    return config


def check_install_config(config):
    return ('locale' in config and
            'disk_device_path' in config and
            'disk_is_partition' in config and
            'use_encryption' in config and
            'encryption_pin' in config)


def check_post_install_config(config):
    return ('user_name' in config and
            'user_password' in config and
            'locale' in config and
            'formats' in config and
            'timezone' in config and
            'additional_software' in config)
