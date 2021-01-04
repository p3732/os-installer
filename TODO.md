
* edit git repo in package .json file

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
    * copy settings of current user
    * enable all needed system daemons (homed!)
    * sanitize journald max size
    * configure paccache to only keep two versions
