#!/bin/sh

if [ $(id -u) -ne 0 ]
  then echo "You need to run this script as root."
  exit
fi

echo "Uninstalling Whitespace Remover..."
rm -f /usr/local/bin/wsrm
echo "Done!"