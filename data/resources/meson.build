pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
gnome = import('gnome')

subdir('ui')

gnome.compile_resources(
  meson.project_name(),
  meson.project_name() + '.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  dependencies: about_dialog
)
