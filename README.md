# OS Installer
A simple operating system installer, intended to be used with live install systems.

Provides bootstrapping through language, keyboard, internet connection and disk selection.
Allows defining of optional additional software to be installed.

# Testing

## Locally 
Clone and install OS-Installer
```
git clone --recursive https://gitlab.gnome.org/p3732/os-installer.git
cd os-installer
meson build
sudo ninja -C build install
```

To try OS-Installer, without modifying any system settings, run it in debug mode with
`os-installer -d`

Uninstall with
```
sudo ninja -C build uninstall
```

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

# Distributions
To use this in a distribution, place a configuration and installation scripts under `/etc/os-installer`.
The file names need to match the example files found in the `example_config` folder.
The example scripts list which environment variables are made available to them.
General usage of these files is:
1) Read configuration from `config.yaml`
1) Call `prepare.sh` - can start updating mirror- or package lists, potentially cache packages.
1) Call `install.sh` - can write data onto disk, installing kernel, packages, bootloader, etc.
1) Call `configure.sh` - configure the system according to selected preferences (account, locale, more packages)

Note that the installer will run scripts as the user it is started by.
If the scripts require elevated priviledges (they probably do)
these need to be granted to the script through other means.
