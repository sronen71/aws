#!/usr/bin/env python

# Notifier example from tutorial
#
# See: http://github.com/seb-m/pyinotify/wiki/Tutorial
#
import pyinotify
import boto
from boto.s3.key import Key
import os

class EventHandler(pyinotify.ProcessEvent):
    def my_init(self):
        conn=boto.connect_s3()
        b=conn.get_bucket('emr71')
        k=Key(b)
        self.Key=k

    def _push_s3(self,pathname):
       k=self.Key
       k.key=os.path.basename(pathname)
       k.set_contents_from_filename(pathname)
       k.set_acl('public-read')

    def process_IN_CREATE(self, event):
        print "Creating:", event.pathname
        self._push_s3(event.pathname)

    def process_IN_MODIFY(self,event):
        print "Modify:",event.pathname
        self._push_s3(event.pathname)

def main():
    

    wm = pyinotify.WatchManager()  # Watch Manager
    #mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | \
    #        pyinotify.IN_MODIFY  # watched events
    mask = pyinotify.ALL_EVENTS

    handler = EventHandler()
    notifier = pyinotify.Notifier(wm, handler)
    path='/home/shai/caffe/examples/plankton/'
    dd = wm.add_watch(path, mask, rec=True,auto_add=True)
    notifier.loop()

if __name__ == '__main__':
    main()
