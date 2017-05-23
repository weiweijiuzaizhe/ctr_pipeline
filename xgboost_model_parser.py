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
  model_file - 输入xgboost的模型文件,文件格式如下:
	1:1_44:9260
	2:1_45:8671
	feature_id:cls_value:cnt

Returns:
  dict  to_return_list[tree_id]=>{node_id=>node_content}
"""
def dict_from_model(model_file,max_feature_id):  
    file = open(model_file)
    oldLine = '0'
    count = 0
    
    to_return_list = []
    current_tree_id = -1
    current_feature_id = max_feature_id

    while 1:
        lines = file.readlines( cache_size ) 
        if not lines:
            break
        for line in lines:
            if line.strip():  
                newLine =  line
                if (newLine != oldLine):
                    if newLine.find("booster[") ==0: #该行以booster开头
                    	tree_id = newLine.replace("booster[","").replace("]:","")
                    	print "tree_id:" + tree_id
                    	current_tree_id = int(tree_id)
                    	current_tree = {}
                    	to_return_list.insert(current_tree_id,current_tree)
                    	continue


                    split_res = newLine.split(":")
                    node_id = int(split_res[ 0 ])
                    node_content = split_res[ 1 ]
                    if node_content.find("leaf=")>=0: #这是个leaf
                    	 node_content = node_content.replace("\n","") + ":new_feature=" + str(current_feature_id)
                    	 current_feature_id = current_feature_id + 1

                    to_return_list[ current_tree_id ][ node_id ] = node_content.replace("\n","")
                    oldLine = newLine


    file.close()
    return to_return_list





def list_from_dict(model_list_dict):
	to_return = []

	for tree_id in range(0, len(model_list_dict)):  #第tree_id棵树
		current_list = []
		for node_id in model_list_dict[tree_id]: # dict的key
			if(model_list_dict[tree_id][node_id].find("<") > 0): #是一个中间节点
				old_id = model_list_dict[tree_id][node_id].split("<")[0].split("[f")[1]
				current_list.insert(node_id, int(old_id))
			if(model_list_dict[tree_id][node_id].find("new_feature") > 0):
				feature_id = model_list_dict[tree_id][node_id].split("new_feature=")[1]
				current_list.insert(node_id, int(feature_id) * -1)
		to_return.insert(tree_id, current_list)
	return to_return










"""
Parameters:
feature_id_file - 输入feature_id_file的模型文件,文件格式如下:
feature_id:cls_value:cnt
1:1_44:9260
2:1_45:8671
3:1_46:8184
4:1_47:7614
5:1_40:11962
6:1_41:11068
7:1_42:10616
Returns:
  dict  max_feature_id
"""
def max_feature_id(feature_id_file):
    file = open(feature_id_file)
    oldLine = '0'
    count = 0
    to_return_id = 0
    
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
                    hash_id = int(split_res[ 0 ])
                    if to_return_id < hash_id:
                    	to_return_id = hash_id
    file.close()
    return to_return_id




feature_id_file = sys.argv[1];
model_file = sys.argv[2]; 


max_feature_id = max_feature_id(feature_id_file)
print max_feature_id
model_list_dict = dict_from_model(model_file,max_feature_id)
model_list = list_from_dict(model_list_dict)







for tree_id in range(1,1000):
	if tree_id == 900:
		for node_id in range(0,len(model_list[tree_id])):
			print node_id, model_list[tree_id][node_id]





#from_criteo_to_format(feature_id_dict,input_file)

