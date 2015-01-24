#!/usr/bin/env python

import boto
from boto.s3.key import Key

conn=boto.connect_s3()
b=conn.get_bucket('emr71')
lk=b.list()
PATH='downloads/'

for key in lk:
    if 'iter' in key.key:
        print key.key
        key.get_contents_to_filename(PATH+key.key)

