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
  'main_stack.py',
  'pages/confirm.py',
  'pages/disk.py',
  'pages/done.py',
  'pages/encrypt.py',
  'pages/install.py',
  'pages/internet.py',
  'pages/keyboard_layout.py',
  'pages/language.py',
  'pages/locale.py',
  'pages/restart.py',
  'pages/software.py',
  'pages/user.py',
  'ui/timezone_choser.py',
  'util/disk_provider.py',
  'util/internet_provider.py',
  'util/keyboard_layout_provider.py',
  'util/language_provider.py',
  'util/locale_provider.py',
  'util/software_provider.py',
  'util/thread_manager.py',
  'widgets.py',
  'window.py',
]

install_data(os_installer_sources, install_dir: moduledir)
