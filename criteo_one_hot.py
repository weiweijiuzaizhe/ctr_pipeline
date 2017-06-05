# -*- coding: utf-8 -*-  

import sys
import time
import subprocess
import os 

distance = 1000000
cls_num = 40
threshold = 1
cache_size = 10*10*1024

"""
Parameters:
  input_file - 输入特征编码文件,文件格式如下:
	1:1_44:9260
	2:1_45:8671
	feature_id:cls_value:cnt

Returns:
  dict  cls_value->hash_id
"""
def dict_from_meta(dict_file):  
    s1 = time.clock()
    file = open(dict_file)
    oldLine = '0'
    count = 0
    
    to_return = dict()
    
    while 1:
        lines = file.readlines( cache_size ) 
        if not lines:
            break
        for line in lines:
            if line.strip():  
                newLine =  line
                if (newLine != oldLine):
                    split_res = newLine.split(":")
                    hash_id = split_res[ 0 ]
                    cls_v = split_res[ 1 ]
                    to_return[ cls_v ] = hash_id
                    oldLine = newLine
                    count += 1

    return to_return





"""
Parameters:
  meta_dict - 输入的数组cls_value->hash_id
  input_file - criteo训练文件,tag以及39列数据

Returns:
  print one_hot 编码后的数据,调用方法类似于root@91fbbd3742ac:/github/ctr_pipeline# nohup python criteo_one_hot.py feature_id.txt /github/temp_data/train.txt >  /github/temp_data/train_one_hot.txt &
"""
def from_criteo_to_format(meta_dict,input_file):
    s1 = time.clock()
    file = open(input_file)
    oldLine = '0'
    count = 0
    
    to_return = dict()
    
    while 1:
        lines = file.readlines( cache_size ) 
        if not lines:
            break
        for line in lines:
            str_to_print = ""
            if line.strip():  
                newLine =  line
                if (newLine != oldLine):
                    split_res = newLine.split("\t") #将输入的一行分解为数组
                    key_dict = {}
                    for i in range(0,cls_num   ):
                        if(i != 0):
                            key = str(i) + "_" + split_res[ i ]
                            value = meta_dict.get(key , -1)
                            if(value > 0): #找到了这个对应的下标
                            	#str_to_print = str_to_print + value +":1 "
                            	key_dict[ int(value) ] = 1


                        if(i == 0):
                        	tag = split_res[ 0 ]
                        	str_to_print = str_to_print + tag + " "


                count += 1
                sorted_dict = sorted(key_dict.items(), key=lambda d:d[0]) #根据key排序 
                for v in sorted_dict:
                	str_to_print = str_to_print + str(v[0]) +":1 "
                str_to_print = str_to_print.strip()
                print str_to_print

                oldLine = newLine
    return to_return



dict_file = sys.argv[1];
input_file = sys.argv[2]; 


feature_id_dict = dict_from_meta(dict_file) 
from_criteo_to_format(feature_id_dict,input_file)

