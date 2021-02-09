high prio:
* run scripts for installation phases
    * pass settings via ENV variables
    * phases
        * system installation with bootloader
        * system configuration (user creation, additional software, anything else post-install)
    * handle failing installation

* handle potentially needed EFI partition
    * if grub does not need one it should be fine

mid prio:

low prio:

* check all used library calls for needed unref()
* focus entry field when clicking on row with entry field (encrypt, user*2)
* fix focus inputs
* fix progressing with enter for user, encrypt
* correctly propagte needed size through GtkScrolledWindow/GtkViewport/GtkListbox
* more config options
    * make internet optional
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
