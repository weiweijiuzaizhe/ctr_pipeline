# -*- coding: utf-8 -*-  

import sys
import time
import subprocess
import os 

distance = 1000000
cls_num = 40
threshold = 1

def dict_from_meta(input_file):  
    s1 = time.clock()
    file = open(input_file)
    oldLine = '0'
    count = 0
    
    to_return = dict()
    
    while 1:
        lines = file.readlines(10*10*1024)  
        #print len(lines)
        if not lines:
            break
        for line in lines:
            if line.strip():  
                newLine =  line
                if (newLine != oldLine):
                    split_res = newLine.split(":")
                    hash_id = split_res[1]
                    cls_v = split_res[0]
                    to_return[ cls_v ] = hash_id
                    oldLine = newLine
                    count += 1
                    if (count % distance == 0):
    					print  "now have read %s lines" %(count)

    print "deal %s lines" %(count)
    e1 = time.clock()
    print "spent time:" + str(e1-s1)
    return to_return



def from_criteo_to_format(meta_dict,input_file):
    s1 = time.clock()
    file = open(input_file)
    oldLine = '0'
    count = 0
    
    to_return = dict()
    
    while 1:
        lines = file.readlines(10*10*1024)  
        #print len(lines)
        if not lines:
            break
        for line in lines:
            if line.strip():  
                newLine =  line
                if (newLine != oldLine):
                    split_res = newLine.split("\t")
                    for i in range(0,cls_num   ):
                        print  "%d:%s" %(i,split_res[i] )
                        if(i != 0):
                            key = str(i) + "_" + split_res[i]
                            value = meta_dict.get(key , -1)
                            print key




                 
                    oldLine = newLine
                    count += 1
                    if (count % distance == 0):
                        print  "now have read %s lines" %(count)

    print "deal %s lines" %(count)
    e1 = time.clock()
    print "spent time:" + str(e1-s1)
    return to_return


    





input_file = sys.argv[1];
out_file = sys.argv[2]; 


feature_id_dict = dict_from_meta(input_file)
from_criteo_to_format(feature_id_dict,out_file)

