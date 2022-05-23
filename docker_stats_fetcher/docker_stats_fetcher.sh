#!/bin/bash

# Fetch docker stat data for a $container and write it to a .json file.
# vcoopman

container_name=''

if [[ $1 != '' ]]
then
	container_name=$1
else
	echo "ERROR: Missing container."
	exit 1
fi

while true
do
	sleep 0.010
	docker stats $container_name --no-stream --format "{\"timestamp\":\"`date +%FT%T`\",\"Name\":\"{{ .Container }}\",\"MemPerc\":\"{{ .MemPerc }}\",\"CPUPerc\":\"{{ .CPUPerc }}\",\"NetIO\":\"{{ .NetIO }}\"}" >> $container_name.ouput.json
done
