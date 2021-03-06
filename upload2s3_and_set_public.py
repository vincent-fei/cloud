import math, os
import boto
from filechunkio import FileChunkIO

# Get file info
source_path = r"Z:\test.zip"
object_name = os.path.basename(source_path)
source_size = os.stat(source_path).st_size
bucket_name = 'your-bucket-name'
bucket_dir = 'upload'
object_key = bucket_dir + "/" + object_name

# Connect to S3
c = boto.connect_s3()
b = c.get_bucket(bucket_name)

# Create a multipart upload request
mp = b.initiate_multipart_upload(object_key)

# Use a chunk size of 10 MiB (feel free to change this)
chunk_size = 10485760
chunk_count = int(math.ceil(source_size / float(chunk_size)))

print "object_key:\t" + "S3://" + bucket_name + "/" + object_key
print "source_path:\t", source_path
print "source_size:\t", source_size
print "chunk_size:\t", chunk_size
print "chunk_count:\t", chunk_count
print "Begin to multi-part upload"

for i in range(chunk_count):
    offset = chunk_size * i
    bytes = min(chunk_size, source_size - offset)
    with FileChunkIO(source_path, 'r', offset=offset,
                         bytes=bytes) as fp:
        print "uploading part number", i + 1
        mp.upload_part_from_file(fp, part_num=i + 1)
mp.complete_upload()

b.set_acl('public-read', object_key)
object_download_url = "http://" + bucket_name + ".s3.amazonaws.com/" + object_key
object_torrent_url = object_download_url + "?torrent"
print "Public Download url is :"
print object_download_url
print "Public Torrent url is :"
print object_torrent_url
