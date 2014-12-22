#!/usr/bin/env python
## wangfei@cyou-inc.com 

import boto.ec2
conn = boto.ec2.connect_to_region('ap-southeast-1')

##public_ip is used in Classic domain
##allocation_id is used in VPC domain

def eip_allocation(domain='vpc'):
    allocation = conn.allocate_address(domain='vpc', dry_run=False)
    return {'public_ip':allocation.public_ip,
            'allocation_id':allocation.allocation_id}

def eip_association(instance_id,allocation_id):
    conn.associate_address(
        instance_id=instance_id,
        public_ip=None,
        allocation_id=allocation_id,
        network_interface_id=None,
        private_ip_address=None,
        allow_reassociation=False,
        dry_run=False)

def eip_disassociation(association_id):
    conn.disassociate_address(
        public_ip=None,
        association_id=association_id,
        dry_run=False)
    
    
def eip_release(allocation_id):
    conn.release_address(
        public_ip=None,
        allocation_id=allocation_id)

def main(instance_id):
    allocation = eip_allocation()
    public_ip = allocation['public_ip']
    allocation_id = allocation['allocation_id']
    eip_association(instance_id,allocation_id)
    print public_ip
     
if __name__ == '__main__':
    main('i-xxxxxxxx')
