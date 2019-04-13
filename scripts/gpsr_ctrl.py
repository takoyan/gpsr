#!/usr/bin/env python
#encoding: utf-8

import rospy
from std_msgs.msg import String
from pocketsphinx import LiveSpeech, get_model_path
import os
import sys

model_path=get_model_path() #pocketのモデル参照場所
gpsr_path=os.path.dirname(os.path.abspath(__file__))

rospy.init_node('controler', anonymous=True)
pub=rospy.Publisher('gpsr_ctrl', String, queue_size=10)
rate=rospy.Rate(10)

#while(1):
"""今回は割愛(コメントアウト版は音声認識が正しく認識したと仮定する)
    speech=LiveSpeech(dic=os.path.join(model_path, 'ziso.dict'))
    for i in speech:
        print(i)
        if i =='let start gpsr':
            rospy.loginfo(i)
            pub.publish('start_gpsr')
            print('I sent message')
"""

rospy.sleep(1)
gpsr_c=String()
gpsr_c.data='start_gpsr'
pub.publish(gpsr_c)
print('I sent message')
