
* change language of app upon selection
    * add German translation

* add selection row that show check mark for selected row
    * changes language rows to selection row
        * select a default language row and make page optional
    * change keyboard layout to selection row

* use back row for keyboard layouts

* get app icon working

* make defaults configurable via json/yaml?
    * includes list of suggested languages
        * maybe even allow setting language and skipping page?

* simply run scripts for installation phases?
    * might be simplest and easily allow for portability across distributions
    * what phases are there?
        * system installation with bootloader
        * user creation
        * additional software? offer page only if supported?
        * post-install configuration

* Post Install configuration list
    * copy some settings of current user
        * do not copy .mozilla cause of cache
    * copy configured wifis
    * enable all needed system daemons (homed!)
    * sanitize journald max size
    * configure paccache to only keep two versions
