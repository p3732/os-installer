high prio:
* handle failing installation
  * pop-up dialog followed by closing of app?
* run scripts for installation phases
    * pass settings via ENV variables
    * phases
        * system installation with bootloader
        * system configuration (user creation, additional software, anything else post-install)

* handle potentially needed EFI partition

mid prio:

* add another translation
* change licences to something GPL. maybe LGPL
* sort keyboard layouts of the actual language first

low prio:

* fix `(os-installer:16186): Gtk-WARNING **: 02:49:15.759: ../gtk/gtk/gtkwidget.c:8648: widget not within a GtkWindow` for user page
    * maybe something access gtk outside gtk thread?
* check all used library calls for needed unref()
* focus entry field when clicking on row with entry field (encrypt, user*2)
* fix focus inputs
* fix progressing with enter for user, encrypt
* correctly propagte needed size through GtkScrolledWindow/GtkViewport/GtkListbox
* allow providing minimal installl size and only accept partitions bigger than it


arch installer specific:
* Post Install configuration list (Arch)
    * copy some settings of current user
        * do not copy .mozilla cause of cache?
    * copy configured wifis
        * /etc/NetworkManager/system-connections/
    * enable all needed system daemons (homed!)
    * sanitize journald max size
    * configure paccache to only keep two versions
    * post kernel-upgrade module sanity
    * kill process before complete system lock due to too little available RAM
      * also swapfile? z-ram?
    * autoupdate if possible, preventing shutdown
