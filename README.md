A simple operating system installer, intended to be used with live install systems.
Provides bootstrapping through language, keyboard, internet connection and disk selection.
Allows defining of optional additional software to be installed.

# Translations
<a href="https://hosted.weblate.org/engage/os-installer/">
<img src="https://hosted.weblate.org/widgets/os-installer/-/os-installer/multi-auto.svg" alt="Translation status" />
</a>

Help with translations is always welcome! The simplest way is via [__Weblate__](https://hosted.weblate.org/projects/os-installer/), which provides a very intuitive website.

Alternatively you could try the autonomous way:
* Fork, clone and build this repository.
* Add your [language code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) `xx` to the `po/LINGUAS` file.
* Generate a new translation file with `ninja -C build os-installer-update-po` and [edit it](https://gitlab.gnome.org/GNOME/gtranslator/).
* Test the translation, commit and push the changes to your fork and create a merge request. Thank you!

# Testing
Clone the project with [GNOME Builder](https://gitlab.gnome.org/GNOME/gnome-builder) via `https://gitlab.gnome.org/p3732/os-installer.git` and run it (this will not make changes to your system).

## Development Setup
Install the following dependencies: `gnome-desktop gtk4 libadwaita libgweather python-yaml udisks vte`.
Note that GTK4 compatible versions of `gnome-desktop` and `vte` are required.
Then clone and install OS-Installer:

```
git clone --recursive https://gitlab.gnome.org/p3732/os-installer.git
cd os-installer
meson build
sudo meson install -C build
```

To try OS-Installer, without modifying any system settings, run it in debug mode with
`os-installer -d`.
Uninstall with `sudo ninja -C build uninstall `

# Distributions
The following describes how to use this in a distribution.
## Configuration
Place a configuration and installation scripts under `/etc/os-installer`.
The file names need to match the example files found in the `example_config` folder.
The example scripts list which environment variables are made available to them.
General usage of these files is:
1) Read configuration from `config.yaml`
1) Call `prepare.sh` - can start updating mirror or package lists, potentially cache packages.
1) Call `install.sh` - can write data onto disk, installing kernel, packages, bootloader, etc.
1) Call `configure.sh` - configure the system according to selected preferences (account, locale, more packages)

Note that the installer will run scripts as the user it is started by.
If the scripts require elevated priviledges (they probably do)
these need to be granted to the script through other means.

## Dependencies
In addition to the dependencies [listed under Testing](#manually),
OS-Installer also expects these GNOME apps to be available:
`epiphany`, `gnome-disk-utility`, `gnome-control-center`

Similarly `systemd` is expected to be available, i.e. `localectl` and `timedatectl`.

# Contact
There is a matrix room https://matrix.to/#/#os-installer:matrix.org in which you can ask questions.
Response time might vary.
