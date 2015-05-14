#!/usr/bin/env python
#-*- coding:UTF-8 -*-
from boto import ec2
from boto.exception import EC2ResponseError
import boto
from pymongo import MongoClient

class MongoTool:
    db=None
    def __init__(self,host,port):
        client = MongoClient(r"mongodb://%s:%s" %(mongo_host,port))
        self.db=client.asetinfo

    #插入或者更新aws instance记录，如果已经存在则更新，如果没有则插入
    def insertOrUpdateInstances(self,instances):
        results={}
        results['error_count']=0
        results['modified_count']=0
        results['total_record']=len(instances)
        for instance in instances:
            try:
                rs=self.db.instances.update_one(
                    {'_id':instance['_id']},
                    {'$set': instance},
                    upsert=True
                )
                results['modified_count']=results['modified_count']+rs.modified_count
            except :
                results['error_count']=results['error_count']+1

        return results
    def insertOrUpdateVolumes(self,volumes):
        results={}
        results['error_count']=0
        results['modified_count']=0
        results['total_record']=len(volumes)
        for volume in volumes:
            try:
                rs=self.db.volumes.update_one(
                    {'_id':volume['_id']},
                    {'$set': volume},
                    upsert=True
                )
                results['modified_count']=results['modified_count']+rs.modified_count
            except :
                results['error_count']=results['error_count']+1

        return results

class AwsTool:
    #获取某个AWS账号下所有region的所有Instance
    def getAllInstance(self,aws_access_key_id,aws_secret_access_key):
        try:
            #尝试Key的有效性并判断属于大陆区还是海外区，并获得相应的regions列表
            conn = ec2.connect_to_region('ap-southeast-1',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
            regions = conn.get_all_regions()
            accountid = boto.connect_iam(aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key).get_user().arn.split(':')[4]
        except EC2ResponseError as e:
            print e
            
        instances=[]
        for region in regions:
            conn=ec2.connect_to_region(region.name,aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
            for instance in conn.get_only_instances():
                ins={}
                ins['_id']=instance.id
                ins['accountid']=accountid
                ins['region']=region.name
                ins['public_dns_name']=instance.public_dns_name
                ins['private_dns_name']=instance.private_dns_name
                ins['state']=instance.state
                ins['previous_state']=instance.previous_state
                ins['key_name']=instance.key_name
                ins['instance_type']=instance.instance_type
                ins['launch_time']=instance.launch_time
                ins['image_id']=instance.image_id
                ins['placement']=instance.placement
                ins['placement_group']=instance.placement_group
                ins['placement_tenancy']=instance.placement_tenancy
                ins['kernel']=instance.kernel
                ins['ramdisk']=instance.ramdisk
                ins['architecture']=instance.architecture
                ins['hypervisor']=instance.hypervisor
                ins['virtualization_type']=instance.virtualization_type
                ins['monitored']=instance.monitored
                ins['monitoring_state']=instance.monitoring_state
                ins['spot_instance_request_id']= instance.spot_instance_request_id
                ins['subnet_id']=instance.subnet_id
                ins['vpc_id']=instance.vpc_id
                ins['private_ip_address']=instance.private_ip_address
                ins['ip_address']=instance.ip_address
                ins['platform']=instance.platform
                ins['root_device_name']=instance.root_device_name
                ins['root_device_type']=instance.root_device_type

                #get tags
                ins['tags']=instance.tags

                #ins['block_device_mapping']=instance.block_device_mapping # – The Block Device Mapping for the instance.
                block_devices=[]

                for device in instance.block_device_mapping:
                    block_devices.append(device)
                ins['block_devices']=block_devices

                ins['state_reason']=instance.state_reason

                security_groups=[]
                for sgroup in instance.groups:
                    securityInfo={}
                    securityInfo['id'] = sgroup.id
                    securityInfo['name'] = sgroup.name
                    security_groups.append(securityInfo)
                ins['security_groups']=security_groups

                interfaces=[]
                for interface in instance.interfaces: # – List of Elastic Network Interfaces associated with this instance.
                    ifs={}
                    ifs['id'] = interface.id
                    ifs['subnet_id'] = interface.subnet_id
                    ifs['vpc_id'] = interface.vpc_id
                    ifs['availability_zone'] = interface.availability_zone
                    ifs['description'] = interface.description
                    ifs['owner_id'] = interface.owner_id
                    ifs['status'] = interface.status
                    ifs['mac_address'] = interface.mac_address
                    ifs['private_ip_address'] = interface.private_ip_address
                    interfaces.append(ifs)
                ins['interfaces']=interfaces
                ins['ebs_optimized']=instance.ebs_optimized
                instances.append(ins)
        return instances

    def getAllVolumes(self,aws_access_key_id,aws_secret_access_key):
        try:
            #尝试Key的有效性并判断属于大陆区还是海外区，并获得相应的regions列表
            conn = ec2.connect_to_region('ap-southeast-1',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
            regions = conn.get_all_regions()
            accountid = boto.connect_iam(aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key).get_user().arn.split(':')[4]
        except EC2ResponseError as e:
            print e
            
        volumes=[]            
        for region in regions:
            print "connect to region", region
            conn = ec2.connect_to_region(region.name,aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
            for volume in conn.get_all_volumes():                
                vol={}               
                vol['_id'] = volume.id
                vol['status'] = volume.status
                vol['attachment_state'] = volume.attachment_state()
                vol['create_time'] = volume.create_time
                vol['encrypted'] = volume.encrypted
                vol['region'] = volume.region.name
                vol['zone'] = volume.zone
                vol['size'] = volume.size
                vol['type'] = volume.type
                vol['iops'] = volume.iops
                vol['tags'] = volume.tags
                vol['snapshot_id'] = volume.snapshot_id               
                vol['accountid'] = accountid
                
                attachment = {}
                vol_attr = volume.attach_data
                attachment['_id'] = vol_attr.id
                attachment['instance_id'] = vol_attr.instance_id              
                attachment['attach_time'] = vol_attr.attach_time
                #attachment['deleteOnTermination'] = vol_attr.deleteOnTermination
                attachment['device'] = vol_attr.device
                
                vol['attach_data'] = attachment               
                volumes.append(vol)               
        return volumes

if __name__ == '__main__':
    instances = AwsTool().getAllInstance(aws_access_key_id,aws_secret_access_key)
    volumes = AwsTool().getAllVolumes(aws_access_key_id,aws_secret_access_key)
    mongoTool = MongoTool(mongo_host,port)
    mongoTool.insertOrUpdateInstances(instances)
    mongoTool.insertOrUpdateVolumes(volumes)
