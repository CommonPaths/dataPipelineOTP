#!/bin/sh
#++++++otp-script.sh++++++
#This script contains the command to run the OTP Server. It is setup as a Daemon so that it keeps running in the background once the EC2 boots up.
# Make sure env. var. OTP_FOLDER is set prior to running the script
# Example using export set: OTP_FOLDER="/var/otp/"

java -Xmx6G -jar $otp_version --autoScan --autoReload --port 8080 --graphs $otp --basePath $otp --server
