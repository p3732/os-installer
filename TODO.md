* fix `(os-installer:16186): Gtk-WARNING **: 02:49:15.759: ../gtk/gtk/gtkwidget.c:8648: widget not within a GtkWindow` for user page
    * maybe something access gtk outside gtk thread?

* add another translation

* toggle switch on row activation for encrypt and user

* check all used library calls for needed unref()

* sort keyboard layouts of the actual language first

* run scripts for installation phases
    * pass settings via ENV variables?
    * phases
        * system installation with bootloader
        * user creation, additional software, post-install configuration

* fix focus inputs

* fix progressing with enter for user, encrypt

* Post Install configuration list (Arch)
    * copy some settings of current user
        * do not copy .mozilla cause of cache?
    * copy configured wifis
        * /etc/NetworkManager/system-connections/
    * enable all needed system daemons (homed!)
    * sanitize journald max size
    * configure paccache to only keep two versions

* handle potentially needed EFI partition

* allow providing minimal installl size and only accept partitions bigger than it

* overall setup progress indicator in headerbar?
    * list of circles that become checkmarks? or filled?