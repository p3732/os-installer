* change language of app upon selection
    * potentially only construct remaining pages after language is set

* add test mode to disable changes to system

* sort keyboard layouts

* use GnomeDesktop for languages
    * gi.require_version('GnomeDesktop', '3.0')
    * from gi.repository import GnomeDesktop
    * GnomeDesktop.get_language_from_code('en')
    * gi.require_version('GtkSource', '4')
    * from gi.repository import GtkSource
    * a = GtkSource.Language()
    * a.get_globs()

* use UDisks for disks

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