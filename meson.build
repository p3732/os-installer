project('OS-Installer',  
          version: '0.1.0',
    meson_version: '>= 0.50.0',
  default_options: [ 'warning_level=2',
                   ],
  license: 'MIT',
)

i18n = import('i18n')
#datadir = get_option('datadir')
application_id = 'com.github.p3732.OS-Installer'

subdir('data')
subdir('src')
subdir('po')

meson.add_install_script('build-aux/meson/postinstall.py')
