#!/usr/bin/env python
## wangfei 2014-12-18
import requests
import time
import boto.ec2
from boto.ec2.blockdevicemapping import BlockDeviceMapping, BlockDeviceType
from boto.ec2.networkinterface import NetworkInterfaceSpecification, NetworkInterfaceCollection

ec2_region = 'ap-southeast-1'
ami_id = 'ami-d6e7c084' # Ubuntu Server 14.04 LTS (HVM)
instance_type = 't2.micro'
subnet_id = 'subnet-xxxxxxx'
groups = ['sg-xxxxxx']
tags = {'Name':'wangfei-test','PROJECT':'test'}
key_name = 'xxxxx-test-20141218'
block_device_map = BlockDeviceMapping()
block_dev_type = BlockDeviceType(delete_on_termination=True, size=100)
block_device_map['/dev/sda1'] = block_dev_type
user_data = "sudo apt-get -y htop"

networks = NetworkInterfaceSpecification(
    subnet_id = subnet_id, 
    groups = groups,
    associate_public_ip_address = True)
    
network_interfaces = boto.ec2.networkinterface.NetworkInterfaceCollection(networks)

conn = boto.ec2.connect_to_region(ec2_region)
reservation = conn.run_instances(
    ami_id,
    key_name = key_name,
    network_interfaces = network_interfaces,
    instance_type = instance_type,
    min_count=1,
    max_count=1,
    block_device_map=block_device_map,
    user_data=user_data,
    )

instance = reservation.instances[0]
## add tags
instance.add_tags(tags)
## allocate eip
allocate_address = conn.allocate_address(domain='vpc', dry_run=False)
eip = allocate_address.public_ip
allocation_id = allocate_address.allocation_id

## get instance information
print "Instance is launching, Please wait..."
time_init = 0
time_total = 300
time_interval = 5       
while time_init < time_total:
    status = instance.update()   
    if status == 'running':
        conn.associate_address(
            instance_id=instance.id,
            public_ip=eip,
            allocation_id=allocation_id,
            network_interface_id=None,
            private_ip_address=None,
            allow_reassociation=False,
            dry_run=False)
        print "InstanceID:\t%s" % instance.id
        print "Placement:\t%s" % instance.placement
        print "InstanceType:\t%s" % instance.instance_type
        print "PrivateIp:\t%s" % instance.private_ip_address
        print "PublicIp:\t%s" % instance.ip_address
        print "ElasticIp:\t%s" % eip
        break
    else:
        time.sleep(time_interval)
        time_init += time_interval
