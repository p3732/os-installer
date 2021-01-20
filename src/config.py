import yaml

DEFAULT_CONFIG_PATH = '/etc/os-installer/config.yaml'


def get_config():
    try:
        with open(DEFAULT_CONFIG_PATH, 'r') as file:
            config = yaml.load(file, Loader=yaml.Loader)
    except:
        config = _get_fallback_config()
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
