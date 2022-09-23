# about dialog needs special treatment
configure_file(input: 'about_dialog.ui.in',
               output: 'about_dialog.ui',
               configuration: {
                 'contributors': contributors,
                 'translators': translators,
                 'version': meson.project_version(),
               })
