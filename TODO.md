* change language of app upon selection
    * add German translation

* get app icon working


* run scripts for installation phases
    * phases
        * system installation with bootloader
        * user creation, additional software, post-install configuration

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