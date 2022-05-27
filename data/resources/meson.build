blueprints = custom_target('blueprints',
  input: files(
    'ui/confirm_quit_popup.blp',
    'ui/main_window.blp',
    'ui/pages/confirm.blp',
    'ui/pages/disk.blp',
    'ui/pages/done.blp',
    'ui/pages/encrypt.blp',
    'ui/pages/failed.blp',
    'ui/pages/install.blp',
    'ui/pages/internet.blp',
    'ui/pages/keyboard_layout.blp',
    'ui/pages/language.blp',
    'ui/pages/locale.blp',
    'ui/pages/restart.blp',
    'ui/pages/software.blp',
    'ui/pages/user.blp',
    'ui/pages/welcome.blp',
    'ui/widgets/device_row.blp',
    'ui/widgets/language_row.blp',
    'ui/widgets/page_wrapper.blp',
    'ui/widgets/progress_row.blp',
    'ui/widgets/selection_row.blp',
    'ui/widgets/software_row.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)
pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
gnome = import('gnome')

gnome.compile_resources(
  meson.project_name(),
  meson.project_name() + '.gresource.xml',
  gresource_bundle: true,
  dependencies: blueprints,
  install: true,
  install_dir: pkgdatadir
)
