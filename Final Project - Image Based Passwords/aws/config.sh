#!/bin/bash

PROFILE=default
REGION=us-east-1
PREAMBLE="--profile ${PROFILE} --region ${REGION}"

VPC_CDR=10.0.0.0/16
PUBLIC_CDR=10.0.1.0/24
PRIVATE_CDR=10.0.2.0/24

APP_TYPE=type
APP_TYPE_NAME=web-app
APP_TAG_NAME=APP
APP_TAG_VALUE=PicturePassword

KEY_NAME=ece455_FinalProject
KEY_FILE=~/.ssh/pems/${KEY_NAME}.pem

# for Amazon Linux 2 on x86_64
AMI_ID=ami-0ed9277fb7eb570c9
INSTANCES_COUNT=1
INSTANCE_TYPE=t2.medium
USER=ec2-user

DATABASE_FILE="~/image-based-pw/backend/db.sqlite"