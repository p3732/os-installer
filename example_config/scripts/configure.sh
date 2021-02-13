#! /bin/sh

# This is an example configuration script. For OS-Installer to use it, place it at:
# /etc/os-installer/scripts/configure.sh
# The script gets called with the following environment variables set:
# OSI_LOCALE             : Locale to be used in the new system
# OSI_DEVICE_PATH        : Device path at which to install
# OSI_DEVICE_IS_PARTITON : 1 if the specified device is a partition (0 -> disk)
# OSI_USE_ENCRYPTION     : 1 if the installation is to be encrypted
# OSI_ENCRYPTION_PIN     : The encryption pin to use (if encryption is set)
# OSI_USER_NAME          : User's name. Not ASCII-fied
# OSI_USER_AUTOLOGIN     : Whether to autologin the user. If set, no password is given
# OSI_USER_PASSWORD      : User's password. Not given if autologin is set
# OSI_FORMATS            : Locale of formats to be used
# OSI_TIMEZONE           : Timezone to be used
# OSI_ADDITIONAL_SOFTWARE: Space-separated list of additional packages to install

#TODO all variables
if [ -z ${OSI_DEVICE_PATH+x} ]
then
    echo "Configuration script called without all environment variables set!"
    exit 1
fi

echo 'Configuration started.'

# Pretending to do something
echo 'Pretending to do something'

for i in {1..20}
do
    sleep 0.1
    echo -n '.'
done

echo
echo 'Configuration completed.'

exit 0