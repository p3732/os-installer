artists = run_command(
  'cat', files('artists'),
).stdout().strip()

contributors = run_command(
  'cat', files('contributors'),
).stdout().strip()

documenters = run_command(
  'cat', files('documenters'),
).stdout().strip()

translators = run_command(
  'cat', files('translators'),
).stdout().strip()

if get_option('flatpak')
  # start in demo mode when using flatpak through wrapper
  demo_script = files('os-installer-demo')

  install_data(demo_script,
    install_dir: get_option('bindir')
  )
endif
