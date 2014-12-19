#!/usr/bin/env python
## get usefull information of instances in all regions
## wangfei

import boto.ec2

regions = [
    'ap-southeast-1',
    'ap-northeast-1',
    'ap-southeast-2',
    'sa-east-1',
    'us-east-1',
    'us-west-2',
    'us-west-1',
    'eu-west-1',
    'eu-central-1'
    ]

for region in regions:
    print "Print instance information in %s" % region
    conn = boto.ec2.connect_to_region(region)
    reservations = conn.get_all_reservations()
    for ec2_list in reservations:
        instances = ec2_list.instances
        inst = instances[0]
        print "%s\t%s\t%s\t%s\t%s\t%s" % (
                                inst.id,
                                inst._state,
                                inst._placement,
                                inst.private_ip_address,
                                inst.ip_address,
                                inst.tags['Name'])
print "end"
