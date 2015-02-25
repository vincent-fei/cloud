#!/usr/bin/env python
import math, os, sys
import boto
from filechunkio import FileChunkIO

# usage
def usage():
    usage = '''
    ./s3copy.py path/to/your-file s3://your-bucket/path/
    '''
    print usage
    
# check arguments
if len(sys.argv) != 3:
    usage()
    sys.exit()

# Get info
object_name = sys.argv[1].split(os.sep)[-1]
bucket_name = sys.argv[-1].split('/')[2]

source_path = os.path.realpath(sys.argv[1])
mybucket = bucket_name

# Connect to S3
c = boto.connect_s3()
b = c.get_bucket(mybucket)
source_size = os.stat(source_path).st_size
mp = b.initiate_multipart_upload(os.path.basename(source_path))

# Use a chunk size of 10 MiB (feel free to change this)
chunk_size = 10485760
chunk_count = int(math.ceil(source_size / float(chunk_size)))

##
print mybucket
print source_path
print source_size
print str(chunk_size/1024.0/1024.0) + 'MB'
print chunk_count

# Send the file parts, using FileChunkIO to create a file-like object
# that points to a certain byte range within the original file. We
# set bytes to never exceed the original file size.
for i in range(chunk_count + 1):
    offset = chunk_size * i
    bytes = min(chunk_size, source_size - offset)
    with FileChunkIO(source_path, 'r', offset=offset,
                         bytes=bytes) as fp:
        mp.upload_part_from_file(fp, part_num=i + 1)

# Finish the upload
mp.complete_upload()
