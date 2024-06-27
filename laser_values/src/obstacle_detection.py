#! /usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String

safe_limit=1 #length in m below which an obstacle is detected
data="False"

def callback(msg):
    length=len(msg.ranges)-1
    count=0
    
    # values at 0 degree
    #print ("0 degree value: ", msg.ranges[0])
    # values at 90 degree
    #print ("90 degree value: ", msg.ranges[int(length/4)])
    # values at 180 degree
    #print ("180 degree value: ", msg.ranges[int(length/2)], "\n")
    # values at 270 degree
    #print ("270 degree value: ", msg.ranges[int(length*3/4)])
    # values at 360 degree
    #print ("360 degree value: ", msg.ranges[length])

    for i in range(int(length/4), int(length*3/4)):
        if msg.ranges[i] < safe_limit:
            for j in range(i, i+6): #obstacle is detected only if the value of msg.ranges[i] is less than the safe limit for 6 or more consecutive values
                if msg.ranges[j] < safe_limit:
                    count=count+1
                else:
                    count=0
                    break            
        if count > 5:
            data="True"
            break
        else:
            data="False"

    #print(data)
    pub.publish(data)

rospy.init_node('scan_values')
sub = rospy.Subscriber('/scan', LaserScan, callback)
pub = rospy.Publisher('obstacle_detection', String, queue_size=1)
rospy.spin()

