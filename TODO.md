* sort keyboard layouts

* pass locales in config, not language codes
    * needed to translate language names into respective language

* allow explicitly setting backward navigation for sections (keyboard -> language)

* use UDisks for disks

* add translation hints

* run scripts for installation phases
    * pass settings via ENV variables?
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

* overall setup progress indicator in headerbar?
    * list of circles that become checkmarks? or filled?