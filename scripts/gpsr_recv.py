#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String
from gpsr.msg import Ans
import re
import numpy as np
import math
import difflib
import sys
from time import sleep
import os

def callback(data):
    rate=rospy.Rate(10)
    if(data.place!=''):
        place=data.place
        thing=data.thing
        destination=data.destination
        follow=data.follow
        sentence_num=data.sentence_num
        print('___________getInformation___________')
        print('place:'+place)
        print('thing:'+thing)
        print('destination:'+destination)
        print('follow:'+follow)
        print('sentence_num:'+str(sentence_num))
        print('____________________________________')

        pub=rospy.Publisher('next_order', String, queue_size=100)
        if sentence_num>=1:
            rospy.sleep(5)
            pub.publish('one more order')
            print('I sent message')

            
        if sentence_num==0:
            pub.publish('all message were sent')
            print('all message were sent')
        

def gpsr_recv():
    rospy.init_node('gpsr_recv', anonymous=True)
    rospy.Subscriber('gpsr_deal', Ans, callback)
    rospy.spin()

if __name__=='__main__':
    gpsr_recv()
