#!/usr/bin/env python
## wangfei@cyou-inc.com
## created at 2014-12-24

import boto.ec2
region = 'ap-southeast-1'
'''
Wrapping the raw boto api to make them more friendly to use.
In boto raw api, public_ip is used in Classic domain, and 
allocation_id is used in VPC domain
'''
def eip_allocation(domain='vpc'):
    conn = boto.ec2.connect_to_region(region)
    allocation = conn.allocate_address(domain='vpc', dry_run=False)
    return {'public_ip':allocation.public_ip,
            'allocation_id':allocation.allocation_id}

def eip_association(instance_id,public_ip):
    '''Notice: need InstanceID and PublicIP to make association'''
    conn = boto.ec2.connect_to_region(region)
    ##make sure input ip is valid EIP
    try:
        address = conn.get_all_addresses(addresses=[public_ip])
    except boto.exception.EC2ResponseError:
        print "Error: IP not found or not EIP"
    else:
        allocation_id = address[0].allocation_id
    ## to call boto associate_address func
    conn.associate_address(
        instance_id=instance_id,
        public_ip=None,
        allocation_id=allocation_id,
        network_interface_id=None,
        private_ip_address=None,
        allow_reassociation=False,
        dry_run=False)

def eip_disassociation(public_ip):
    conn = boto.ec2.connect_to_region(region)
    '''Notice: use public_ip to get network_interface_id
    and use network_interface_id to get association_id'''
    ##make sure input ip is valid EIP
    try:
        address = conn.get_all_addresses(addresses=[public_ip])
    except boto.exception.EC2ResponseError:
        print "Error: IP not found or not EIP"
    else:
        association_id = address[0].association_id
    #network_interface_id = address[0].network_interface_id    
    conn.disassociate_address(
        public_ip=None,
        association_id=association_id,
        dry_run=False)

def eip_release(public_ip):
    conn = boto.ec2.connect_to_region(region)
    ##make sure input ip is valid EIP
    try:
        address = conn.get_all_addresses(addresses=[public_ip])
    except boto.exception.EC2ResponseError:
        print "Error: IP not found or not EIP"
    else:
        association_id = address[0].association_id
        allocation_id = address[0].allocation_id
    ## only release EIP that not associated to any instance
    if association_id == None:
        conn.release_address(
            public_ip=None,
            allocation_id=allocation_id)
    else:
        print "IP %s is in use, cannot be released" % public_ip

def eip_change(instance_id):
    conn = boto.ec2.connect_to_region(region)
    reservations = conn.get_all_reservations([instance_id])
    instances = reservations[0].instances
    inst = instances[0]
    old_public_ip = inst.ip_address
    ##make sure the public ip is valid EIP
    try:
        address = conn.get_all_addresses(addresses=[old_public_ip])
    except boto.exception.EC2ResponseError:
        print "Error: Old public IP not found or not EIP"
    else:
        eip_disassociation(old_public_ip)
        eip_release(old_public_ip)
    ## add new IP 
    allocation = eip_allocation()
    public_ip = allocation['public_ip']
    eip_association(instance_id,public_ip)
    
    
def main():
    #usage demos
    #eip_disassociation('54.xx.xx.xx')
    #eip_association('i-xxxxxxxx','54.xx.xx.xx')
    #eip_release('54.xx.xx.xx')
    #eip_change('i-xxxxxxxx')
     
if __name__ == '__main__':
    main()
