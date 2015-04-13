#!/usr/bin/env python
# wangfei
import boto.ec2
from boto.ec2.blockdevicemapping import BlockDeviceMapping, BlockDeviceType

# Letter A is used for root device
# Letter B to E are used for Instance Store
# EBS starts from letter F
block_device_map = BlockDeviceMapping()
xvda = BlockDeviceType(delete_on_termination=True, size=12)
xvdb = BlockDeviceType(ephemeral_name='ephemeral0')
xvdf = BlockDeviceType(delete_on_termination=False, size=100, volume_type='gp2')
xvdg = BlockDeviceType(delete_on_termination=False, size=100, volume_type='io1', iops=1000)
block_device_map['/dev/xvda'] = xvda
block_device_map['/dev/sdb'] = xvdb
block_device_map['/dev/sdf'] = xvdf
block_device_map['/dev/sdg'] = xvdg

# then you can use block_device_map in run_instance
conn = boto.ec2.connect_to_region(ec2_region)
conn.run_instances(
    # other arguments
    block_device_map=block_device_map,
    # other arguments
    )
