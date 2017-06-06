# -*- coding: utf-8 -*-  

import sys
import time
import subprocess
import os 

distance = 1000000
cls_num = 40
threshold = 1
cache_size = 10*10*1024


def dict_from_model(model_file):  
    file = open(model_file)
    oldLine = '0'
    count = 0
    to_return_dict = {}


    while 1:
        lines = file.readlines( cache_size ) 
        if not lines:
            break
        for line in lines:
            if line.strip():  
                newLine =  line
                if (newLine != oldLine):
                	newLine = newLine.strip()
                	feature_id = newLine.split("\t")[0]
                	to_return_dict[ feature_id ] = 1 

    file.close()
    return to_return_dict


def file_filter(train_file,feature_dict):
    oldLine = '0'
    file = open(train_file)
    while 1:
        lines = file.readlines( cache_size ) 
        if not lines:
            break
        for line in lines:
            if line.strip():  
                newLine =  line
                if (newLine != oldLine):
                	split_res = newLine.strip().split(" ")
                	label = split_res[0] # id
                	feature_res = split_res[1:]
                	key_dict = {}
                	for k in feature_res: # 这一行的feature
                		feature_id = k.split(":")[0]
                		if feature_dict.get(feature_id,-1) > 0: 
                			key_dict[ int(feature_id) ] = 1

                	sorted_dict = sorted(key_dict.items(), key=lambda d:d[0]) #根据key排序
                	str_to_print = ""
                	for v in sorted_dict:
                		str_to_print = str_to_print + str( v[0] ) +":1 "
                	str_to_print = str_to_print.strip()
                	print label + " " + str_to_print

model_file = sys.argv[1];
input_file = sys.argv[2]; 
feature_dict = dict_from_model(model_file)
file_filter(input_file,feature_dict)

