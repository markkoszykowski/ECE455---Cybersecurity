#!/bin/bash

# fetch config from AWS for currently running infrastructure
source ./aws/config.sh

NOW=$(date '+%Y%m%d%H%M%S')
LOGFILE="./logs/deploy-${NOW}.log"

PACKAGE_UPDATE="sudo yum update -y"
GIT_INSTALL="sudo yum install git -y"

GIT_REPO="https://github.com/RebeccaGartenberg/image-based-pw"
GIT_CLONE="git clone ${GIT_REPO}"

PROJECT_DIRECTORY="image-based-pw"
PIP_INSTALL="pip3 install -r ${PROJECT_DIRECTORY}/requirements.txt"

ENTER_FRONTEND="cd ~/${PROJECT_DIRECTORY}/frontend/"
DOWNLOAD_NPM="curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash"
ACTIVATE_NPM=". ~/.nvm/nvm.sh"

NVM_INSTALL="nvm install 16.13.0"
REACT_INSTALL="npm install react-scripts"

echo "Deploying Full AWS infrastructure for ${APP_TAG_NAME}: ${APP_TAG_VALUE}" | tee ${LOGFILE}
echo "Running deploy.sh at ${NOW}" | tee -a ${LOGFILE}

# get public IP addresses of the instances (in the public subnet)
INSTANCES_IPS=$(aws ec2 describe-instances ${PREAMBLE} --filters Name=instance-state-name,Values=running Name=tag:${APP_TAG_NAME},Values=${APP_TAG_VALUE} --query 'Reservations[*].Instances[*].PublicIpAddress' --output text | tr -s '\t' ' ')
echo "Public IP addresses: ${INSTANCES_IPS}" | tee -a ${LOGFILE}

for host in ${INSTANCES_IPS}
do
  	# adds host to trusted ssh hosts so that it does not wait on request
 	ssh-keyscan -H ${host} >> ~/.ssh/known_hosts | tee -a ${LOGFILE}
	ssh -i ${KEY_FILE} ${USER}@${host} ${PACKAGE_UPDATE}  | tee -a ${LOGFILE}
	ssh -i ${KEY_FILE} ${USER}@${host} ${GIT_INSTALL}  | tee -a ${LOGFILE}
	ssh -i ${KEY_FILE} ${USER}@${host} ${GIT_CLONE}  | tee -a ${LOGFILE}
	ssh -i ${KEY_FILE} ${USER}@${host} ${PIP_INSTALL}  | tee -a ${LOGFILE}
	ssh -i ${KEY_FILE} ${USER}@${host} ${PIP_INSTALL}  | tee -a ${LOGFILE}
	ssh -i ${KEY_FILE} ${USER}@${host} "${ENTER_FRONTEND} && ${DOWNLOAD_NPM}"  | tee -a ${LOGFILE}
	ssh -i ${KEY_FILE} ${USER}@${host} "${ACTIVATE_NPM}"  | tee -a ${LOGFILE}
	ssh -i ${KEY_FILE} ${USER}@${host} "${ENTER_FRONTEND} && ${NVM_INSTALL}"  | tee -a ${LOGFILE}
	ssh -i ${KEY_FILE} ${USER}@${host} "${ENTER_FRONTEND} && ${REACT_INSTALL}"  | tee -a ${LOGFILE}
done

echo "Done." | tee -a ${LOGFILE}

exit 0
