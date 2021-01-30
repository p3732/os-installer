#! /bin/sh

# This is an example installer script. For OS-Installer to use it, place it at:
# /etc/os-installer/scripts/installer.sh
# The script gets called with the following environment variables set:
# OSI_LOCALE             : Locale to be used in the new system
# OSI_DEVICE_PATH        : Device path at which to install
# OSI_DEVICE_IS_PARTITON : 1 if the specified device is a partition (0 -> disk)
# OSI_USE_ENCRYPTION     : 1 if the installation is to be encrypted
# OSI_ENCRYPTION_PIN     : The encryption pin to use (if encryption is set)

if [ -z ${OSI_DEVICE_PATH+x} ]
then
    echo "Installer script called without all environment variables set!"
    exit 1
fi

echo 'Installation started'

# Pretending to do something
echo 'Pretending to do something'

for i in {1..20}
do
    sleep 0.1
    echo -n '.'
done

echo
echo 'Installation completed!'

exit 0