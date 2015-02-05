#!/usr/bin/env python

import time
import boto.ec2
import os

conn=boto.ec2.connect_to_region("us-west-1")
instances=conn.get_only_instances(instance_ids=['i-f63a573c'])
instance=instances[0]
print "on demand instance:",instance,instance.state
images=conn.get_all_images(owners='self',image_ids=['ami-c4a0b981'])
image= images[0]

print "selected image: ",image.id
#instances[0].start() # start the on demand instance
price_list=conn.get_spot_price_history(product_description='Linux/UNIX',filters={'instance-type':'g2.2xlarge'})
prices=[x.price for x in price_list]
if prices:
    print "recent max spot price: ",max(prices)
else:
    print "Didn't find prices"
myprice=0.07
print "bidding now ",myprice
spot_req=conn.request_spot_instances(price=str(myprice),count=1,image_id=image.id,instance_type='g2.2xlarge',key_name='EC2Key2',ebs_optimized=True) # can send user_data also

#conn.run_instances(' ')
job_instance_id=None
SPIN_WAIT_TIME=60 # seconds
while job_instance_id==None:
    time.sleep(SPIN_WAIT_TIME)
    print "checking..."
    job_id=spot_req[0].id
    print job_id
    reqs=conn.get_all_spot_instance_requests(request_ids=[job_id])
    job_instance_id=reqs[0].instance_id
    print "job instance id: " + str(job_instance_id)

launched=conn.get_only_instances(instance_ids=[job_instance_id])
instance = launched[0]
print "spot launched: ",instance,instance.id,instance.state
time.sleep(SPIN_WAIT_TIME)


#keep on termination volume attached as /dev/sda1:
#instance.modify_attribute('blockDeviceMapping', { '/dev/sda1' : False }) 

# delete on termination volume attached as /dev/sda1:
#instance.modify_attribute('blockDeviceMapping', { '/dev/sda1' : True }) 




time.sleep(SPIN_WAIT_TIME)
print "ip address:",instance.ip_address
os.system("gnome-terminal -e 'bash -c \"ssh -X -i EC2Key2.pem ubuntu@"+instance.ip_address+"; exec bash\"'")

#time.sleep(SPIN_WAIT_TIME) 
#print "Terminating"
#conn.terminate_instances(instance_ids=[instance.id])

