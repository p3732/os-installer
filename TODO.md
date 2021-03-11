high prio:
* show password field by default (autologin -> pessword protection)

* make bottom gradients bigger in some place for better scrollability discoverability

* installer scripting
    * pass settings via ENV variables
    * handle failing installation

* use python global for global state

mid prio:

* correctly store timezone and formats in config
* handle potentially needed legacy boot partition for MBR
* correctly expand terminal output window

low prio:

* OEM mode
* translation of main menu entry?
* check all used library calls for needed unref()
* focus entry field when clicking on row with entry field (encrypt, user*2)
* fix focus inputs
* fix progressing with enter for user, encrypt
* more config options
    * allow specifying additional size needed by extra packages?
