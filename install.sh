#!/bin/sh

if [ $(id -u) -ne 0 ]
  then echo "You need to run this script as root."
  exit
fi

echo "Installing Whitespace Remover..."
cp wsrm.py /usr/local/bin/wsrm
echo "Done!"