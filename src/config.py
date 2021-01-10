import yaml

DEFAULT_CONFIG_PATH = '/etc/os-installer/config.yaml'


def get_config():
    try:
        with open(DEFAULT_CONFIG_PATH, 'r') as file:
            config = yaml.load(file, Loader=yaml.Loader)
    except:
        config = _get_fallback_config()
    return config


def _get_fallback_config():
    return {
        'internet_checker_url': 'http://nmcheck.gnome.org/check_network_status.txt',
        'suggested_languages': ["en", "ar", "de", "es", "fr", "ja", "ru", "zh"],
        'additional_software': {}
    }


def check_install_config(config):
    return (hasattr(config, 'formats') and
            hasattr(config, 'disk_device_path') and
            hasattr(config, 'disk_is_partition') and
            hasattr(config, 'use_encryption') and
            hasattr(config, 'encryption_pin'))


def check_post_install_config(config):
    return (hasattr(config, 'user_name') and
            hasattr(config, 'user_password') and
            hasattr(config, 'locale') and
            hasattr(config, 'formats') and
            hasattr(config, 'timezone') and
            hasattr(config, 'additional_software'))
