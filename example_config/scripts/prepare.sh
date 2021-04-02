#! /bin/sh

# This is an example preparation script. For OS-Installer to use it, place it at:
# /etc/os-installer/scripts/prepare.sh
# The script gets called when an active internet connection was established.
# The system time might not be synchronized just yet, but should be within seconds.

echo 'Preparation started.'

# Pretending to do something
echo 'Pretending to do something'

for i in {1..5}
do
    sleep 1
    echo -n '.'
done

echo
echo 'Preparation completed.'

exit 0