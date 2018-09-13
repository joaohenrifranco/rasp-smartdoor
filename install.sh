#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run this script as root"
  exit
fi

for file in daemon_scripts/*; do
  cp $file /etc/init.d/
  update-rc.d "$(basename "$file")" defaults
  echo "Script "$(basename "$file")" added to init.d successfully!"
done
