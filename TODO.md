high prio:
* installer scripting
    * pass settings via ENV variables
    * handle failing installation

mid prio:

* handle potentially needed legacy boot partition for MBR

low prio:

* check all used library calls for needed unref()
* focus entry field when clicking on row with entry field (encrypt, user*2)
* fix focus inputs
* fix progressing with enter for user, encrypt
* correctly propagte needed size through GtkScrolledWindow/GtkViewport/GtkListbox
* more config options
    * allow specifying additional size needed by extra packages?
