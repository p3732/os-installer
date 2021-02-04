# pre-parse about dialog

conf = configuration_data()
conf.set('VERSION', meson.project_version())
conf.set('APPID', application_id)
conf.set('PACKAGE_URL', application_url)
conf.set('CONTRIBUTORS', contributors)
conf.set('TRANSLATORS', translators)

about_dialog = configure_file(
  input: 'about_dialog.ui.in',
  output: 'about_dialog.ui',
  configuration: conf,
  install_dir: pkgdatadir,
)
