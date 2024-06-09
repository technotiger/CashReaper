#!/bin/bash

# Honeygain - Installed by dockerfile

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
update_json=$(curl --silent "https://releases.bitping.com/bitpingd/update.json")
tag=$(echo "$update_json" | grep '"version":' | sed -E 's/.*"([^"]+)".*/\1/')
base_url="https://releases.bitping.com/$tag"
OS=$(uname -s)
ARCH=$(uname -m)
if [[ "$ARCH" == "x86_64" ]]; then
    file="bitpingd-x86_64-unknown-linux-gnu-$tag.tar.gz"
elif [[ "$ARCH" == "armv7l" ]]; then
    file="bitpingd-armv7-unknown-linux-gnueabihf-$tag.tar.gz"
elif [[ "$ARCH" == "aarch64" ]]; then
    file="bitpingd-aarch64-unknown-linux-musl-$tag.tar.gz"
else
    echo "Unsupported architecture"
    exit 1
fi
curl -L "$base_url/$file" -o $file
tar -xf "$file"
rm -f $file
mv bitpingd "/opt/bitpingd"
chmod +x "/opt/bitpingd"
setcap 'cap_net_raw=ep' "/opt/bitpingd"
echo "Successfully installed Bitpingd"

# Packetstream - Installed by dockerfile

# Earnapp
wget -qO- https://brightdata.com/static/earnapp/install.sh > /tmp/earnapp.sh && bash /tmp/earnapp.sh -y
rm /tmp/earnapp.sh
