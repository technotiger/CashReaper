#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if [ -f ./settings.conf ]
then
    source ./settings.conf
else
    echo Could not find settings.conf, exiting...
    exit 1
fi

docker run -d --restart unless-stopped --mount source=vol-picash,target=/etc/earnapp --env-file ${SCRIPT_DIR}/settings.conf --name picash technotiger/picash

if [[ "$USE_EARNAPP" == "y" ]]
then
    echo Waiting for 30 sec to stand up, will print the earnapp link when done
    sleep 30
    echo Use this link to register your worker
    docker exec -ti picash earnapp register | grep -Eo 'https.+'
fi


