#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String, Bool

def callback(data):
    rate=rospy.Rate(10)
    result=[]
    if(data.data!=''):
        print(data.data)
        result.append(data.data)
    if(data.data==False):
        print('aa')
        print(result)
    
def test_sub():
    rospy.Subscriber('sound_system/recognition/result', String, callback)
    rospy.Subscriber('sound_system/module/recognition/active', Bool, callback)
    rospy.spin()

def test_pub():
    rospy.init_node('sound_system', anonymous=True)
    start_record=rospy.Publisher('sound_system/recognition', String, queue_size=10)
    rospy.sleep(1)
    start_record.publish('')
    test_sub()
    

if __name__=='__main__':
    test_pub()
    
