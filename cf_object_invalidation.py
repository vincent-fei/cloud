#!/usr/bin/env python
## wangfei@cyou-inc.com 
import boto
import sys, os

distribution_id = 'xxxxxxx'
#paths = ['/path/7eleven.png', '/path/alipay.png', '/path/Braintree.png']
# make object list from file
input_fle = os.sys.path[0] + os.sep + 'purge-object.txt'
f = open(input_fle,'r')
paths = []
for line in f:
    line = line.strip()
    paths.append(line)
#print paths

c = boto.connect_cloudfront()
inval_req = c.create_invalidation_request(distribution_id, paths)
#print inval_req.paths
invals = c.get_invalidation_requests(distribution_id)

for inval in invals:
    print 'Object: %s, ID: %s, Status: %s' % (inval, inval.id, inval.status)
