high prio:
* don't select default keyboard layout, set continue button to sensitive accordingly

* show password field by default (autologin -> pessword protection)

* make scrollableness more noticeable

* locale navigation with back/forward is confusing, as top navigation buttons don't relate to it

* installer scripting
    * pass settings via ENV variables
    * handle failing installation

* make back navigation work for in-page, drop back navigation rows

* use python global for global state

mid prio:

* handle potentially needed legacy boot partition for MBR
* allow backwards navigation to language again?
* don't pick a keyboard by default
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
