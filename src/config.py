class Config:
    # TODO create config defaults from configurable json

    internet_checker_url = 'http://nmcheck.gnome.org/check_network_status.txt'

    formats = 'en_DA'
    language = 'English'
    language_short_hand = 'en'
    locale = 'en_US.UTF-8'
    keyboard_layout = 'English (United States)'
    keyboard_layout_short_hand = 'us'

    disk_name = 'Disk Name'
    disk_size = 'Size Gb'
    disk_device_path = '/dev/sda1'
    disk_is_partition = True

    encrypt = False
    encryption_pin = None

    user_name = 'Name'
    user_password = 'password'

    formats = 'Formats'
    timezone = 'Timezone'

    software = []
