# THIS IS STILL UNDER DEVELOPMENT
It can not yet be used to actually install anything.

# OS Installer
A simple operating system installer, intended to be used with live install systems.

Provides bootstrapping through language, keyboard, internet connection and disk selection.
Allows defining of optional additional software to be installed.

# Testing
To try out OS-Installer, without making any changes to your system, run it in debug mode:

```
meson build
sudo ninja -C build install
os-installer -d
```

# Translating
* Get the source code by cloning the repository with `git clone git@gitlab.gnome.org:p3732/os-installer.git` or by [downloading it](https://gitlab.gnome.org/p3732/os-installer/-/archive/master/os-installer-master.zip)
* In the folder containg the source code first prepare the build with `meson build`
* Add your [language code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) `xx` to the `po/LINGUAS` file
* Generate a new translation file with `ninja -C build os-installer-update-po`
* Edit the new translation file `po/xx.po` with an editor of your choice (e.g. a normal text editor or [Translator Editor](https://gitlab.gnome.org/GNOME/gtranslator/))
* Try out your new translation by following the 'Testing' intructions
* If everything works, you can submit your translation by simply [opening a new issue](https://gitlab.gnome.org/p3732/os-installer/-/issues/new) and attaching the added .po file or with a [merge request](https://mattstauffer.com/blog/how-to-contribute-to-an-open-source-github-project-using-your-own-fork/) from your forked repository.
