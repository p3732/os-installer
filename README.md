# OS Installer
A simple operating system installer, intended to be used with live install systems.

Provides bootstrapping through language, keyboard, internet connection and disk selection.
Allows defining of optional additional software to be installed.

# Build and Install
```
meson build
sudo ninja -C build install
```

# Test
To try OS-Installer, without making any changes to your system, run it in debug mode with `os-installer -d`

# Translating
## Simple Way
* Create an issue [on Github](https://github.com/p3732/os-installer/issues/new) or [on Gitlab](https://gitlab.gnome.org/p3732/os-installer/-/issues/new) stating what language you want to translate `OS-Installer` into
* A file will be provided to you. Add the translation underneath the English text [like in this example](https://gitlab.gnome.org/p3732/os-installer/-/blob/master/po/de.po)
* Upload the translated file back into the issue. Thank you!

## Autonomous Way
* Fork this repository, clone the source code and create a build folder with `meson build`
* Add your [language code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) `xx` to the `po/LINGUAS` file
* Generate a new translation file with `ninja -C build os-installer-update-po`
* Edit the translation file `po/xx.po` with an editor of your choice (normal text editor or a [Translator Editor](https://gitlab.gnome.org/GNOME/gtranslator/))
* Try your new translation by following the '__Testing__' intructions
* If everything works, commit your changes, push them to your repository and create a merge request. Thank you!
