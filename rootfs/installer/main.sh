#!/bin/bash

## Honeygain
mkdir -p /opt/honeygain 
curl -L https://github.com/technotiger/CashReaper/releases/download/bin/honeygain.tar.gz | tar -C /opt/honeygain -zxf -
if [[ `uname -m` != "x86_64" ]]
then 
    mkdir -p /etc/qemu-binfmt/x86_64/lib64/ 
    curl -L https://github.com/technotiger/CashReaper/releases/download/bin/ld64.tar.gz | tar -C /etc/qemu-binfmt/x86_64/lib64/ -zxf -
fi


# Pawns.app (IPRoyal)
curl -L https://cdn.pawns.app/download/cli/latest/linux_`uname -m`/pawns-cli > /usr/bin/pawns-cli
chmod +x /usr/bin/pawns-cli

# Traffmonetizer
mkdir -p /opt/traffmonetizer
if [[ `uname -m` == "armv7l" ]]
then 
    curl -L https://github.com/technotiger/CashReaper/releases/download/bin/traffmonetizer-arm7.tar.gz| tar -C /opt/traffmonetizer -zxf -
else
    curl -L https://github.com/technotiger/CashReaper/releases/download/bin/traffmonetizer.tar.gz | tar -C /opt/traffmonetizer -zxf -
fi

# BitPing
wget https://downloads.bitping.com/node/armv7.zip && unzip armv7.zip -d /opt/bitping && rm -rf armv7.zip
wget https://downloads.bitping.com/node/linux.zip && unzip linux.zip -d /opt/bitping && rm -rf linux.zip


# Packetstream - Installed by dockerfile
# Earnapp - Installed by service itself on first run