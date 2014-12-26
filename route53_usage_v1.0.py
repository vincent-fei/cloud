#!/usr/bin/env python
# -*- coding: utf-8 -*-
# wangfei 2014-12-26

import boto.route53
import os

def add_record_to_zone(domain_name,type,sub_domain,value,ttl=300):
    ## check domain_name ends with dot or not
    input = domain_name
    if input.endswith('.'):
        hosted_zone_name = input
    else:
        hosted_zone_name = input + '.'
        
    conn = boto.route53.connect_to_region('ap-southeast-1')
    zone = conn.get_zone(hosted_zone_name)
    record_type = type
    record_set = sub_domain + '.' + hosted_zone_name
    record_value = value
    record_ttl = int(ttl)
    if zone.find_records(record_set,record_type):
        print "ERROR, record set already exists"
    else:
        zone.add_record(record_type, record_set, record_value,record_ttl)
        print "record set added successfully"
        print record_set,record_value
    
def delete_record_from_zone(domain_name,type,sub_domain):
    ## check input ends with dot or not
    input = domain_name
    if input.endswith('.'):
        hosted_zone_name = input
    else:
        hosted_zone_name = input + '.'
        
    conn = boto.route53.connect_to_region('ap-southeast-1')
    zone = conn.get_zone(hosted_zone_name)
    record_type = type
    record_set = sub_domain + '.' + hosted_zone_name
    record_find_result = zone.find_records(record_set,record_type)
    if not record_find_result:
        print "ERROR, record set does NOT exists"
    else:
        zone.delete_record(record_find_result)
        print "record set %s deleted" % record_set

def export_zone_to_file(domain_name,type,sub_domain):
    '''
    Route53 serive has no region, it works across all region.
    But you have to give a region to let boto to make connection
    to AWS route53 service endpoint, so just give one
    '''
    ## check input ends with dot or not
    ## zone name have to be domain name ends with dot
    input = domain_name
    if input.endswith('.'):
        hosted_zone_name = input
    else:
        hosted_zone_name = input + '.'
    # make connection to route53   
    conn = boto.route53.connect_to_region('ap-southeast-1')
    zone = conn.get_zone(hosted_zone_name)
    records = zone.get_records()
    # write output to file
    output_fle = os.sys.path[0] + os.sep + hosted_zone_name + 'records.txt'
    f = open(output_fle,'w')
    for record in records:
        output = "%s\tIN\t%s\t%s\t%s" % (record.name,record.type,record.ttl, ",".join(record.resource_records))
        f.writelines(str(output) + "\n")
    f.close()
  

def main():
    # useage demos
    #export_zone_to_file('imbusy.me')
    #add_record_to_zone('cypay.internal','A','www','10.0.1.175')
    #add_record_to_zone('cypay.internal','CNAME','web','www.cypay.internal')
    #delete_record_from_zone('cypay.internal','A','www')

if __name__ == '__main__':
    main()
