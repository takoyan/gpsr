#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nltk
import numpy as np
import os
import glob
import rospy
from pocketsphinx import LiveSpeech, get_model_path
from std_msgs.msg import String
from gpsr.msg import Ans
import os
import sys


speak=['answer', 'tell', 'say', 'speak', 'talk', 'explain', 'teach', 'express', 'mouth', 'mention', 'utter']
go=['go', 'come', 'move', 'run', 'transfer', 'shift', 'travel', 'follow']
carry=['carry', 'accompany', 'escort', 'deliver', 'bring', 'place', 'navigate', 'locate', 'send', 'bear', 'channel', 'transport', 'transmit', 'submit']
find=['find', 'look', 'meet', 'get', 'pick', 'search', 'seek', 'hunt', 'watch']





"""
get_Index_of_nextNoun関数
入力された文章内における,指定された単語の次に来る名詞のindex番号を返す.
"""
def get_Index_of_nextNoun(sentence, word):
    global result
    index_of_word=sentence.index(word)
    for k in range(index_of_word+1, len(sentence)):
        if (result[k][1]=='NN' or
        result[k][1]=='NNS' or
        result[k][1]=='NNP' or
        result[k][1]=='NNPS' or
        result[k][1]=='PRP' or
        result[k][1]=='PRP$'):
            return k
    


"""
check_And関数
入力された文章内に'and'があるかどうかをチェックする.
'and'がない場合は要素数1の配列で返還.
'and'がある場合は要素数('and'の個数-1)の配列で返還.
いずれも各要素は'and'で区切られた文章である.
"""
def check_And(sentence):
    checked_sentence=sentence.split('and')
    return checked_sentence   #配列での返還




"""
check_Verb関数
文章が命令文の場合,1ワード目の動詞を動詞として判定するための関数
命令文の先頭に主語となるHeを加えて再度構文解析を行い解析結果を返す.
"""
def check_Verb(sentence):
    return [(word, tag[:2]) if tag.startswith('VB') else(word, tag) for word, tag in nltk.pos_tag(['He']+sentence)[1:]]



"""
check_properNoun関数
文中に存在する固有名詞を判別する.
単語の頭が大文字のものを固有名詞と判定している(改良の必要があるかも...)
元の文章と構文解析結果を引数としている.
"""
def check_properNoun(sentence, result):
    if result[[0][0]][0].isupper() and result[0][1].startswith('VB'):#命令文の場合の処置
        return result
    
    new_result={}
    for word in sentence:
        top=word[0]
        if top.isupper():
            new_result.update(result)
            new_result[word]='NN'
            new_result=new_result.items()
            return new_result

    return result
    

"""
separate_Verb関数
入力された文章内の動詞を分類する.
返り値として動詞の単語が返還される.
"""
def separate_Verb(sentence):
    for verbs in (speak, go, carry, find):
        for verb in verbs:
            if verb in sentence:
                return verb   #動詞の返還


            
def look_func(sentence, verb):
    ans=[]
    if 'from' in sentence: #fromが文中にある場合
        index_of_from=get_Index_of_nextNoun(sentence, 'from')
        index_of_verb=get_Index_of_nextNoun(sentence, verb)
        place=result[index_of_from][0] #場所を示す名詞を格納
        destination=result[index_of_verb][0] #目的地を示す名詞を格納
        index_of_dest=get_Index_of_nextNoun(sentence, destination)
        thing=result[index_of_dest][0]
        ans.append(place)
        ans.append(thing)
        ans.append(destination)
        return ans

    if 'for' in sentence:
        index_of_for=get_Index_of_nextNoun(sentence, 'for')
        thing=result[index_of_for][0]
        index_of_verb=get_Index_of_nextNoun(sentence, thing)
        place=result[index_of_verb][0]
        ans.append(place)
        ans.append(thing)
        return ans

    place=result[get_Index_of_nextNoun(sentence, verb)][0]
    ans.append(place)
    ans.append('empty')
    return ans



def carry_func(sentence, verb):
    ans=[]
    if 'from' in sentence:
        return look_func(sentence, verb)
        

    if 'to' in sentence:
        index_of_to=get_Index_of_nextNoun(sentence, 'to')
        index_of_verb=get_Index_of_nextNoun(sentence, verb)
        place=result[index_of_to][0]
        thing=result[index_of_verb][0]
        ans.append(place)
        ans.append(thing)
        return ans
    else:
        index_of_verb=get_Index_of_nextNoun(sentence, verb)
        place=result[index_of_verb][0]
        ans.append(place)
        
        index_of_next=get_Index_of_nextNoun(sentence, place)
        if index_of_next!=True:
            return ans
        thing=result[index_of_next][0]
        ans.append(thing)
        return ans


def go_func(sentence, verb):
    ans=[]
    if 'to' in sentence:
        index_of_to=get_Index_of_nextNoun(sentence, 'to')
        place=result[index_of_to][0]
        ans.append(place)
        return ans

    if ('after' in sentence):
        index_of_after=get_Index_of_nextNoun(sentence, 'after')
        follow=result[index_of_after][0]
        if len(ans)<=0:
            ans=['empty']*4
            ans[3]=follow
        return ans
    else:
        index_of_noun=get_Index_of_nextNoun(sentence, verb)
        follow=result[index_of_noun][0]
        if len(ans)<=0:
            ans=['empty']*4
            ans[3]=follow
        return ans
        

def start_speech(data):
    global start_flag
    start_flag=True
    return 

def restart_speech(data):
    global flag
    flag=True
    return


def next_order(data):
    global next_flag
    global continue_flag
    next_flag=True
    if(data.data=='all message were sent'):
        print('co')
        continue_flag=True
    return


    

def gpsr_deal():
    #sentence='bring me this apple'
    #sentence='bring me this apple from the kitchen'
    #sentence='bring this apple to him'
    #sentence='look for the fruit in the corridor'
    #sentence='go to the kitchen'
    #sentence='go after him'
    sentence='go to the sofa, meet Emily, and follow her'
    #sentence='meet Emily'
    #sentence=sentence.lower()
    sent_li=[]
    sent_li=sentence.split(',')
    
    
    global start_flag
    global result
    global sentence_num
    global next_flag
    global continue_flag

    sentence_num=len(sent_li)
    start_flag=False
    next_flag=False
    continue_flag=True

    
    rospy.init_node('gpsr_deal', anonymous=True)
    
    while(1):
        while(1):
            rospy.Subscriber('gpsr_ctrl', String, start_speech)

            if(start_flag==True):
                """音声認識を使う場合は要改良
                while(sent_li<=0):
                speech=LiveSpeech(dic='/home/takoyan/catkin_ws/src/spr/ziso.dict')
                for i in speech:
                sentence=i
                break
                break
                """
                break
                
        if(continue_flag==False):#次の命令までの待機
            print('continue_flag')
            continue
    

        while(sentence_num>=1):
            sentence=sent_li.pop(0)
            sentence_num=len(sent_li)
    
            #sentence=check_And(sentence) #文中のandの有無を確認
            sentence=sentence.split()#単語で区切る
            
            result={}#構文解析結果 [('Please', 'VB')]のような形
            result=check_Verb(sentence)
            result=check_properNoun(sentence, result)

            verb=separate_Verb(sentence) #文中の動詞を獲得


            answer=[]

            if verb in carry:
                answer=carry_func(sentence, verb)
            elif verb in find:
                answer=look_func(sentence, verb) #[place, thing]の順
            elif verb in go:
                answer=go_func(sentence, verb)


            place='empty'
            thing='empty'
            destination='empty'
            follow='empty'

            if len(answer)>=4:
                follow=answer[3]
            if len(answer)>=3:
                destination=answer[2]
            if len(answer)>=2:
                thing=answer[1]
            if len(answer)>=1:
                place=answer[0]



            pub=rospy.Publisher('gpsr_deal', Ans, queue_size=100)
            box=Ans()
            box.place=place
            box.thing=thing
            box.destination=destination
            box.follow=follow
            box.sentence_num=sentence_num
            print('----------infomation----------')
            print(box)
            print('------------------------------')
            rospy.sleep(5)
            pub.publish(box)
            if sentence_num==0:
                print('change flag')
                start_flag=False
                continue_flag=False

            while(next_flag==False):
                rospy.Subscriber('next_order', String, next_order)
        
        
        

        
if __name__=='__main__':
    try:
        gpsr_deal()
    except rospy.ROSInterruptException:
        pass
