#!/bin/bash
# get instance information to create motd
## wangfei

function print_help()
{
	echo "Directly use this to create /etc/motd to show instance info."
}

#check some basic configurations before running the code
function chk_config()
{
	#check if run inside an ec2-instance
	x=$(curl -s http://169.254.169.254/)
	if [ $? -gt 0 ]; then
		echo '[ERROR] Command not valid outside EC2 instance. Please run this command within a running EC2 instance.'
		exit 1
	fi
}

#print standard metric
function print_normal_metric() {
	metric_path=$2
	echo -ne "\033[33m$1:\t\033[0m" 
	RESPONSE=$(curl -fs http://169.254.169.254/latest/${metric_path}/)
	if [ $? == 0 ]; then
		echo -e "\033[35m$RESPONSE\033[0m"
	else
		echo "not available"
	fi
}

#get hostname
function print_hostname(){
	x=$(/bin/grep HOSTNAME /etc/sysconfig/network | /bin/awk -F "=" '{print $2}')
	if [ -n "$x" ]; then
		echo -e "\033[33mHostname:\t\033[0m""\033[35m$x\033[0m"
	else
		echo "not available"
	fi
}

function print_all()
{
	echo "*************************************"
	print_hostname
	print_normal_metric Location meta-data/placement/availability-zone
	print_normal_metric InstanceID meta-data/instance-id
	print_normal_metric InstanceType meta-data/instance-type
	print_normal_metric PrivateIP meta-data/local-ipv4
	print_normal_metric PublicIP meta-data/public-ipv4
	echo "*************************************"
}

#check if run inside an EC2 instance
chk_config

#command called in default mode
if [ "$#" -eq 0 ]; then
	print_all
fi
