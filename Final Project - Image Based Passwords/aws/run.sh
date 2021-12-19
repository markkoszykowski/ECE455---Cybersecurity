#!/bin/bash

# fetch config from AWS for currently running infrastructure
source ./aws/config.sh

NOW=$(date '+%Y%m%d%H%M%S')
LOGFILE="./logs/run-${NOW}.log"

PROJECT_DIRECTORY="image-based-pw"

EXPORT_FLASK="export FLASK_APP=backend"
FLASK_RUN="python3 -m flask run --host 0.0.0.0"

NPM_START="npm start"

ENTER_PROJECT="cd ~/${PROJECT_DIRECTORY}/"
ENTER_FRONTEND="cd ~/${PROJECT_DIRECTORY}/frontend/"

echo "Running Full AWS infrastructure for ${APP_TAG_NAME}: ${APP_TAG_VALUE}" | tee ${LOGFILE}
echo "Running run.sh at ${NOW}" | tee -a ${LOGFILE}

# get public IP addresses of the instances (in the public subnet)
INSTANCES_IPS=$(aws ec2 describe-instances ${PREAMBLE} --filters Name=instance-state-name,Values=running Name=tag:${APP_TAG_NAME},Values=${APP_TAG_VALUE} --query 'Reservations[*].Instances[*].PublicIpAddress' --output text | tr -s '\t' ' ')
echo "Public IP addresses: ${INSTANCES_IPS}" | tee -a ${LOGFILE}

for host in ${INSTANCES_IPS}
do
    echo "(${ENTER_PROJECT} && ${EXPORT_FLASK} && ${FLASK_RUN} &) && (${ENTER_FRONTEND} && ${NPM_START} &)"
    ssh -i ${KEY_FILE} ${USER}@${host} "(${ENTER_PROJECT} && ${EXPORT_FLASK} && ${FLASK_RUN} &) && (${ENTER_FRONTEND} && ${NPM_START} &)"  | tee -a ${LOGFILE}
done

echo "Done." | tee -a ${LOGFILE}

echo "Server running at ${INSTANCES_IPS%% *}"

exit 0
