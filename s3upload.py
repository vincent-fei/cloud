#!/usr/bin/env python
import getopt
import sys
import os
import boto

from boto.compat import six

try:
    import math
    import mimetypes
    from multiprocessing import Pool
    from boto.s3.connection import S3Connection
    from filechunkio import FileChunkIO
    multipart_capable = True
    usage_flag_multipart_capable = ''' [--multipart]'''
    usage_string_multipart_capable = '''
        multipart - Upload files as multiple parts. This needs filechunkio.
                    Requires ListBucket, ListMultipartUploadParts,
                    ListBucketMultipartUploads and PutObject permissions.'''
except ImportError as err:
    multipart_capable = False
    usage_flag_multipart_capable = ''' [--multipart]'''
    if six.PY2:
        attribute = 'message'
    else:
        attribute = 'msg'
    usage_string_multipart_capable = '\n\n     "' + \
        getattr(err, attribute)[len('No module named '):] + \
        '" is missing for multipart support '


DEFAULT_REGION = 'ap-southeast-1'
usage_string = '''
Usgae:
s3upload  [-a/--access_key <access_key>] [-s/--secret_key <secret_key>]
          -b/--bucket <bucket_name> [-c/--callback <num_cb>]
          [-d/--debug <debug_level>] [-i/--ignore <ignore_dirs>]
          [-n/--no_op] [-p/--prefix <prefix>] [-k/--key_prefix <key_prefix>]
          [-q/--quiet] [-g/--grant grant] [-w/--no_overwrite] [-r/--reduced]
          [--header] [--region <name>] [--host <s3_host>]''' + \
          usage_flag_multipart_capable + ''' path [path...]
'''

def usage(status=1):
    print(usage_string)
    sys.exit(status)

def submit_cb(bytes_so_far, total_bytes):
    print('%d bytes transferred / %d bytes total' % (bytes_so_far, total_bytes))

def get_key_name(fullpath, prefix, key_prefix):
    if fullpath.startswith(prefix):
        key_name = fullpath[len(prefix):]
    else:
        key_name = fullpath
    l = key_name.split(os.sep)
    return key_prefix + '/'.join(l)

def _upload_part(bucketname, aws_key, aws_secret, multipart_id, part_num,
                 source_path, offset, bytes, debug, cb, num_cb,
                 amount_of_retries=10):
    '''
    Uploads a part with retries.
    '''
    if debug == 1:
        print("_upload_part(%s, %s, %s)" % (source_path, offset, bytes))

    def _upload(retries_left=amount_of_retries):
        try:
            if debug == 1:
                print('Start uploading part #%d ...' % part_num)
            conn = S3Connection(aws_key, aws_secret)
            conn.debug = debug
            bucket = conn.get_bucket(bucketname)
            for mp in bucket.get_all_multipart_uploads():
                if mp.id == multipart_id:
                    with FileChunkIO(source_path, 'r', offset=offset,
                                     bytes=bytes) as fp:
                        mp.upload_part_from_file(fp=fp, part_num=part_num,
                                                 cb=cb, num_cb=num_cb)
                    break
        except Exception as exc:
            if retries_left:
                _upload(retries_left=retries_left - 1)
            else:
                print('Failed uploading part #%d' % part_num)
                raise exc
        else:
            if debug == 1:
                print('... Uploaded part #%d' % part_num)

    _upload()

def check_valid_region(conn, region):
    if conn is None:
        print('Invalid region (%s)' % region)
        sys.exit(1)

def multipart_upload(bucketname, aws_key, aws_secret, source_path, keyname,
                     reduced, debug, cb, num_cb, acl='private', headers={},
                     guess_mimetype=True, parallel_processes=4,
                     region=DEFAULT_REGION):
    """
    Parallel multipart upload.
    """
    conn = boto.s3.connect_to_region(region, aws_access_key_id=aws_key,
                                     aws_secret_access_key=aws_secret)
    check_valid_region(conn, region)
    conn.debug = debug
    bucket = conn.get_bucket(bucketname)

    if guess_mimetype:
        mtype = mimetypes.guess_type(keyname)[0] or 'application/octet-stream'
        headers.update({'Content-Type': mtype})

    mp = bucket.initiate_multipart_upload(keyname, headers=headers,
                                          reduced_redundancy=reduced)

    source_size = os.stat(source_path).st_size
    bytes_per_chunk = max(int(math.sqrt(5242880) * math.sqrt(source_size)),
                          5242880)
    chunk_amount = int(math.ceil(source_size / float(bytes_per_chunk)))

    pool = Pool(processes=parallel_processes)
    for i in range(chunk_amount):
        offset = i * bytes_per_chunk
        remaining_bytes = source_size - offset
        bytes = min([bytes_per_chunk, remaining_bytes])
        part_num = i + 1
        pool.apply_async(_upload_part, [bucketname, aws_key, aws_secret, mp.id,
                                        part_num, source_path, offset, bytes,
                                        debug, cb, num_cb])
    pool.close()
    pool.join()

    if len(mp.get_all_parts()) == chunk_amount:
        mp.complete_upload()
        key = bucket.get_key(keyname)
        key.set_acl(acl)
    else:
        mp.cancel_upload()


def singlepart_upload(bucket, key_name, fullpath, *kargs, **kwargs):
    """
    Single upload.
    """
    k = bucket.new_key(key_name)
    k.set_contents_from_filename(fullpath, *kargs, **kwargs)


def expand_path(path):
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    return os.path.abspath(path)


def main():

    # default values
    aws_access_key_id = None
    aws_secret_access_key = None
    bucket_name = ''
    ignore_dirs = []
    debug = 0
    cb = None
    num_cb = 0
    quiet = False
    no_op = False
    prefix = os.getcwd()
    key_prefix = ''
    grant = None
    no_overwrite = False
    reduced = False
    headers = {}
    host = None
    multipart_requested = False
    region = None

    try:
        opts, args = getopt.getopt(
            sys.argv[1:], 'a:b:c::d:g:hi:k:np:qs:wr',
            ['access_key=', 'bucket=', 'callback=', 'debug=', 'help', 'grant=',
             'ignore=', 'key_prefix=', 'no_op', 'prefix=', 'quiet',
             'secret_key=', 'no_overwrite', 'reduced', 'header=', 'multipart',
             'host=', 'region='])
    except:
        usage(1)

    # parse opts
    for o, a in opts:
        if o in ('-h', '--help'):
            usage(0)
        if o in ('-a', '--access_key'):
            aws_access_key_id = a
        if o in ('-b', '--bucket'):
            bucket_name = a
        if o in ('-c', '--callback'):
            num_cb = int(a)
            cb = submit_cb
        if o in ('-d', '--debug'):
            debug = int(a)
        if o in ('-g', '--grant'):
            grant = a
        if o in ('-i', '--ignore'):
            ignore_dirs = a.split(',')
        if o in ('-n', '--no_op'):
            no_op = True
        if o in ('-w', '--no_overwrite'):
            no_overwrite = True
        if o in ('-p', '--prefix'):
            prefix = a
            if prefix[-1] != os.sep:
                prefix = prefix + os.sep
            prefix = expand_path(prefix)
        if o in ('-k', '--key_prefix'):
            key_prefix = a
        if o in ('-q', '--quiet'):
            quiet = True
        if o in ('-s', '--secret_key'):
            aws_secret_access_key = a
        if o in ('-r', '--reduced'):
            reduced = True
        if o == '--header':
            (k, v) = a.split("=", 1)
            headers[k] = v
        if o == '--host':
            host = a
        if o == '--multipart':
            if multipart_capable:
                multipart_requested = True
            else:
                print("multipart upload requested but not capable")
                sys.exit(4)
        if o == '--region':
            regions = boto.s3.regions()
            for region_info in regions:
                if region_info.name == a:
                    region = a
                    break
            else:
                raise ValueError('Invalid region %s specified' % a)

    if len(args) < 1:
        usage(2)

    if not bucket_name:
        print("bucket name is required!")
        usage(3)

    connect_args = {
        'aws_access_key_id': aws_access_key_id,
        'aws_secret_access_key': aws_secret_access_key
    }

    if host:
        connect_args['host'] = host

    c = boto.s3.connect_to_region(region or DEFAULT_REGION, **connect_args)
    check_valid_region(c, region or DEFAULT_REGION)
    c.debug = debug
    b = c.get_bucket(bucket_name, validate=False)

    # Attempt to determine location and warn if no --host or --region
    # arguments were passed. Then try to automagically figure out
    # what should have been passed and fix it.
    if host is None and region is None:
        try:
            location = b.get_location()

            # Classic region will be '', any other will have a name
            if location:
                print('Bucket exists in %s but no host or region given!' % location)

                # Override for EU, which is really Ireland according to the docs
                if location == 'EU':
                    location = 'eu-west-1'

                print('Automatically setting region to %s' % location)

                # Here we create a new connection, and then take the existing
                # bucket and set it to use the new connection
                c = boto.s3.connect_to_region(location, **connect_args)
                c.debug = debug
                b.connection = c
        except Exception as e:
            if debug > 0:
                print(e)
            print('Could not get bucket region info, skipping...')

    existing_keys_to_check_against = []
    files_to_check_for_upload = []

    for path in args:
        path = expand_path(path)
        # upload a directory of files recursively
        if os.path.isdir(path):
            if no_overwrite:
                if not quiet:
                    print('Getting list of existing keys to check against')
                for key in b.list(get_key_name(path, prefix, key_prefix)):
                    existing_keys_to_check_against.append(key.name)
            for root, dirs, files in os.walk(path):
                for ignore in ignore_dirs:
                    if ignore in dirs:
                        dirs.remove(ignore)
                for path in files:
                    if path.startswith("."):
                        continue
                    files_to_check_for_upload.append(os.path.join(root, path))

        # upload a single file
        elif os.path.isfile(path):
            fullpath = os.path.abspath(path)
            key_name = get_key_name(fullpath, prefix, key_prefix)
            files_to_check_for_upload.append(fullpath)
            existing_keys_to_check_against.append(key_name)

        # we are trying to upload something unknown
        else:
            print("I don't know what %s is, so i can't upload it" % path)

    for fullpath in files_to_check_for_upload:
        key_name = get_key_name(fullpath, prefix, key_prefix)

        if no_overwrite and key_name in existing_keys_to_check_against:
            if b.get_key(key_name):
                if not quiet:
                    print('Skipping %s as it exists in s3' % fullpath)
                continue

        if not quiet:
            print('Copying %s to %s/%s' % (fullpath, bucket_name, key_name))

        if not no_op:
            # 0-byte files don't work and also don't need multipart upload
            if os.stat(fullpath).st_size != 0 and multipart_capable and \
                    multipart_requested:
                multipart_upload(bucket_name, aws_access_key_id,
                                 aws_secret_access_key, fullpath, key_name,
                                 reduced, debug, cb, num_cb,
                                 grant or 'private', headers,
                                 region=region or DEFAULT_REGION)
            else:
                singlepart_upload(b, key_name, fullpath, cb=cb, num_cb=num_cb,
                                  policy=grant, reduced_redundancy=reduced,
                                  headers=headers)

if __name__ == "__main__":
    main()
