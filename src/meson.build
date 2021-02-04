pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'os_installer')

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'os-installer.in',
  output: 'os-installer',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

os_installer_sources = [
  '__init__.py',
  'config.py',
  'global_state.py',
  'main.py',
  'ui/confirm_quit_popup.py',
  'ui/failed_installation_popup.py',
  'ui/formats_chooser.py',
  'ui/main_stack.py',
  'ui/pages/confirm.py',
  'ui/pages/disk.py',
  'ui/pages/done.py',
  'ui/pages/encrypt.py',
  'ui/pages/install.py',
  'ui/pages/internet.py',
  'ui/pages/keyboard_layout.py',
  'ui/pages/language.py',
  'ui/pages/locale.py',
  'ui/pages/restart.py',
  'ui/pages/software.py',
  'ui/pages/user.py',
  'ui/timezone_chooser.py',
  'ui/widgets.py',
  'ui/window.py',
  'util/disk_provider.py',
  'util/internet_provider.py',
  'util/keyboard_layout_provider.py',
  'util/language_provider.py',
  'util/locale_provider.py',
  'util/software_provider.py',
  'util/thread_manager.py',
]

install_data(os_installer_sources, install_dir: moduledir)
