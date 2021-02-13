high prio:
* installer scripting
    * pass settings via ENV variables
    * handle failing installation

* handle potentially needed EFI partition

mid prio:

low prio:

* check all used library calls for needed unref()
* focus entry field when clicking on row with entry field (encrypt, user*2)
* fix focus inputs
* fix progressing with enter for user, encrypt
* correctly propagte needed size through GtkScrolledWindow/GtkViewport/GtkListbox
* more config options
    * allow providing minimal installl size and only accept partitions bigger than it
    * allow specifying additional size needed by extra packages?

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
