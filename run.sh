#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if [ -f $SCRIPT_DIR/settings.conf ]
then
    source $SCRIPT_DIR/settings.conf
else
    echo Could not find settings.conf, exiting...
    exit 1
fi

clear

echo "--------------------------------------------------------------------------------
        _   _   ___   _      ___   __    __ __   ___     _____    __   
       | | | | | __| | |    / _/  /__\  |  V  | | __|   |_   _|  /__\  
       | 'V' | | _|  | |_  | \__ | \/ | | \_/ | | _|      | |   | \/ | 
       !_/ \_! |___| |___|  \__/  \__/  |_| |_| |___|     |_|    \__/  

       ▄███   ▄███  ▄██  ▄█   █▄  ▄██▄  ▄███▄   ▄███  ▄██▄ ▄███▄  ▄██▄ 
      █   █  █   █ █   ▀  █   █   █   █ █    █ █   █ █   █ █    █ █   █
      █   █▀ █   █ █      █   █   █   █ █      █   █ █   █ █      █   █
      █      █   █ ▀█▄   ▄█▄▄▄█▄ ▄█▄▄▀  ▄█▄▄▄  █   █ █   █ ▄█▄▄▄ ▄█▄▄▀ 
      █     ▀█████    █  ▀██▀▀█▀ ▀██▄   ▀█▀▀  ▀█████ ███▀  ▀█▀▀  ▀██▄ 
      █   ▄  █   █     █  █   █   █  █  █   ▄▄ █   █ █     █   ▄▄ █  █
       ███▀ ▄█   █ ▄██▀  ▄█   █▄ ▄█   █ ████▀ ▄█   █ █     ████▀ ▄█   █ 
--------------------------------------------------------------------------------"

echo "
Please read the README file before proceeding. 

To support this project, please consider using the provided links to create the required accounts.

Have you updated the settings.conf file with your login credentials? (yes/no)"
read answer

if [ "$answer" = "yes" ]; then
    echo "
    Thank you for the confirmation.
    "
else
    echo "
    Please edit the settings.conf file and run this script again.
    "
    exit 0
fi

echo -e "Building docker image... This process can take several minutes, please be patient.\n    |-"

indent_output() {
    sed 's/^/    |-/'
}

{
    docker pull -q honeygain/honeygain:latest
    docker pull -q packetstream/psclient:latest
    cd $SCRIPT_DIR
    docker build . -t technotiger/cashreaper:latest
} | indent_output

echo -e "Image built. Cleaning up...\n    |-"

{
    docker image rm honeygain/honeygain:latest
    docker image rm packetstream/psclient:latest
    docker image prune -f
} | indent_output


echo -e "Starting Container\n    |-"
{
    docker run -d --log-driver none --restart unless-stopped --tmpfs /tmp:exec --tmpfs /run:exec --tmpfs /root/.bitpingd:exec --mount source=vol-cashreaper,target=/etc/earnapp --env-file ${SCRIPT_DIR}/settings.conf --name cashreaper technotiger/cashreaper:latest
} | indent_output


if [[ "$USE_EARNAPP" == "y" ]]
then
    echo Waiting for 30 sec for the container to start up, will print the earnapp link when done
    sleep 30
    echo Use this link to register your worker
    docker exec -it cashreaper earnapp register | grep -Eo 'https.+'
fi
