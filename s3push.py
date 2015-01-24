#!/usr/bin/env python

import boto
from boto.s3.key import Key

conn=boto.connect_s3()
b=conn.get_bucket('emr71')
b.set_acl('public-read')
k=Key(b)

PATH='/home/shai/caffe/examples/plankton/'
files=['inet_train_test.prototxt','inet_solver.prototxt']

for f in files:
    k.key=f
    k.set_contents_from_filename(PATH+f)
    k.set_acl('public-read')

