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
Place a configuration and installation scripts under `/etc/os-installer` (or symlink it to another folder).
An example structure is given in the `example_config` folder.
General usage of these files is:
1) Read configuration from `config.yaml`
1) After establishing an internet connection `prepare.sh` is started.
    * Useful for starting mirror updates, getting package lists or pre-caching packages.
1) After chosing a disk and confirming the deletion of files on it, `install.sh` is started.
    * Can be used to write basic system and other data onto disk, installing kernel, packages, bootloader, etc.
    * If `install.sh` does not exist, there will be no confirmation page.
1) After giving all other information is confirmed via the summary page, `configure.sh` is started.
    * This can be used to either handle the full installation or to finish up configuring the system according to selected preferences (account, locale, additional packages and features)

Not all scripts need to exist, if one does not, this step is simply skipped.
The example scripts list which environment variables are made available to each script.

The scripts can be written in any language as long as a shell can correctly execute them.
Also, the installer will run scripts as the user it is started by.
If they require elevated priviledges (hint: they probably do),
these need to be granted to the script through other means.

## Dependencies
In addition to the dependencies [listed under Testing](#manually),
the default OS-Installer config also expects these GNOME apps to be available:
`epiphany`, `gnome-disk-utility`, `gnome-control-center`
(These can be changed via `config.yaml`)

Similarly `systemd` is expected to be available, i.e. `localectl` and `timedatectl`.

## Examples
Example configurations of distributions (experimenting) with using OS-Installer:
* https://github.com/snowflakelinux/os-installer-snowflake-config (NixOS-based)
* https://github.com/arkanelinux/pkgbuild/tree/main/os-installer-config (Arch-based)

# Contact
There is a matrix room https://matrix.to/#/#os-installer:matrix.org in which you can ask questions.
Response time might vary.
