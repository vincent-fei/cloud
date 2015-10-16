#!/bin/bash
# get disk usage result
# wangfei 20151016

ip=$(cat ./iplist | grep -v "^#" | awk '{print $1}' | sed '/^$/d')
> disk_check_result.txt
for i in $ip
do
    ssh $i "df -h | grep dev |grep -v udev | grep -v tmpfs" | awk -v ip="$i" '{print ip"    "$0}'
done >> disk_check_result.txt
sleep 3

cat disk_check_result.txt | sort -k6 -r | head -30
