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
  'provider/disk_provider.py',
  'provider/internet_provider.py',
  'provider/keyboard_layout_provider.py',
  'provider/language_provider.py',
  'provider/locale_provider.py',
  'provider/software_provider.py',
  'ui/confirm_quit_popup.py',
  'ui/page.py',
  'ui/pages/confirm.py',
  'ui/pages/disk.py',
  'ui/pages/done.py',
  'ui/pages/encrypt.py',
  'ui/pages/failed.py',
  'ui/pages/install.py',
  'ui/pages/internet.py',
  'ui/pages/keyboard_layout.py',
  'ui/pages/language.py',
  'ui/pages/locale.py',
  'ui/pages/restart.py',
  'ui/pages/software.py',
  'ui/pages/user.py',
  'ui/pages/welcome.py',
  'ui/widgets.py',
  'ui/window.py',
  'util/installation_scripting.py',
  'util/system_calls.py',
]

install_data(os_installer_sources, install_dir: moduledir)
