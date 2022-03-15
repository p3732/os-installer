high prio:

* GTK 4 port
* user name sanity check
* empty keyboard layout list before adding new layouts
* empty countries list before adding new countries

mid prio:

* show notification on finisehd or failed install
* fix row being selected kbd layout->same language
* handle potentially needed legacy boot partition for MBR boot + GPT
* script folder config option
* highlight current keyboard layout
* don't add "no partitions" row multiple times
* figure out why flat headerbar style does not work

low prio:

* more config options
    * fixed language
    * skip settings handled by gnome-initial-setup
      * user
      * locale + timezone
    * allow specifying additional size needed by extra packages
* focus entry field when clicking on row with entry field (encrypt, user*2)
* fix focus inputs
* fix progressing with enter for user, encrypt
