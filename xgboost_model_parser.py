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
解析xgboost模型,将node_id和node_content放入一个dict中,不同tree的dict放入一个list,liist的下表了是tree_id
Parameters:
  model_file		- 输入xgboost的模型文件,文件格式如下:
	feature_id:cls_value:cnt 例子
	1:1_44:9260
	2:1_45:8671	
  max_feature_id	- 当前已经分配的最大的维度id
Returns:
  dict  			- to_return_list[tree_id]=>{node_id=>node_content}
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
                    if newLine.find("booster[") ==0: # 该行以booster开头,说明行是一个tree的开头
                    	current_tree_id = int(newLine.replace("booster[","").replace("]:",""))
                    	current_tree = {}
                    	to_return_list.insert(current_tree_id,current_tree)
                    	continue
                    split_res = newLine.split(":")
                    node_id = int(split_res[ 0 ])
                    node_content = split_res[ 1 ]
                    if node_content.find("leaf=") >= 0: # 这是个leaf
                    	 node_content = node_content.replace("\n","") + \
                    	 ":new_feature=" + str(current_feature_id) # 将这个leaf申请一个新feature
                    	 current_feature_id = current_feature_id + 1
                    to_return_list[ current_tree_id ][ node_id ] = node_content.replace("\n","")
                    oldLine = newLine

    file.close()
    return to_return_list

"""
class:
  存放一个Node的信息,
left_node_id	- 左Node的id,往往是<和missing进入这个分支
right_node_id	- 右Node的id
feature_id 		- 特征id > 0说明是原有的维度,feature_id < 0 表示是gbdt新增加出来的维度
"""
class Node:
	left_node_id = 0
	right_node_id = 0
	feature_id = 0



"""
输入之前从dict_from_model得到的dict,得到一个数组,下标[tree_id]{node_id},对应的内容是Node
Parameters:
  model_list_dict - 输入的一个list,其中下标值是tree_id,每个value是一个dict,key是node_id,value是node_content
Returns:
  list			  -  [tree_id]{node_id} => value>0 表示的是feature_id,value<0表示的是一个从根节点到叶节点的新feature_id
"""
def list_from_dict(model_list_dict):
	to_return = []

	for tree_id in range(0, len(model_list_dict)):  # 第tree_id棵树
		current_list = {}
		for node_id in model_list_dict[ tree_id ]: # dict的key
			
			if(model_list_dict[ tree_id ][ node_id ].find("<") > 0): # 是一个中间节点
				currnet_node = Node();
				feature_id = model_list_dict[ tree_id ][ node_id ].split("<")[0].split("[f")[1]
				currnet_node.feature_id = int(feature_id)
				left_node_id	= model_list_dict[ tree_id ][ node_id ].split("yes=")[1].split(",")[0]
				right_node_id	= model_list_dict[ tree_id ][ node_id ].split("no=")[1].split(",")[0] 
				currnet_node.left_node_id = int(left_node_id)
				currnet_node.right_node_id= int(right_node_id)
			
			elif(model_list_dict[ tree_id ][ node_id ].find("new_feature") > 0): # 是一个叶子节点
				currnet_node = Node();
				currnet_node.left_node_id = 0
				currnet_node.right_node_id = 0
				feature_id = int(model_list_dict[ tree_id ][ node_id ].split("new_feature=")[1]) * -1
				currnet_node.feature_id = feature_id
			current_list[node_id] = currnet_node

		to_return.insert(tree_id, current_list)

	return to_return



"""
Parameters:
	model_list[][]	- model_list[tree_id][node_id]
	tree_num 		- number of tress in model
	sampled_tree_id	- the tree will be printed in the model
Returns:
	none
"""
def list_from_dict_test(model_list,tree_num,sampled_tree_id):
	for tree_id in model_list:
		if tree_id == sampled_tree_id:
			for node_id in range(0,len(model_list[ tree_id ])):
				print str(tree_id),node_id, \
				str(model_list[ tree_id ][ node_id ].left_node_id),	\
				str(model_list[ tree_id ][ node_id ].right_node_id), \
				str(model_list[ tree_id ][ node_id ].feature_id)


"""
读取feature_id_file,找到里面feature_id最大的值
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



"""
Parameters:
	line_feature_dict	- feature_id为key,1为value 
	tree_list			- tree_list是list_from_dict返回的一个元素,是用list表示的某一课树
Returns:
	to_return_id		- 这棵树要添加上的新维度,没有新维度返回0
"""
def find_feature_id(line_feature_dict,tree_list):
	suffix = 0
	to_return_id = tree_list[ suffix ].feature_id
	all_missing_flag = 0
	while( 1):		
		if to_return_id < 0:
			break
		elif  line_feature_dict.get(tree_list[ suffix ].feature_id) > 0 :  # 这个节点的维度不是0
			suffix = tree_list[ suffix ].right_node_id # found,turn right
			all_missing_flag = all_missing_flag + 1
		else:
			suffix = tree_list[ suffix ].left_node_id # not found,turn left
		to_return_id = tree_list[ suffix ].feature_id
	
	if all_missing_flag == 0 : #如果一次都没有命中,都走missing的维度没有意义
		to_return_id = 0 

	return to_return_id * -1


"""
Parameters:
	one_hot_libsvm_file	- 输入的libsvm格式文件,一般进行了one_hot编码\
	list_from_dict 		- 保存所有树的二维数组
Returns:
	需要添加在输入数据尾部的新字符串 
	
"""
def add_gdbt_feature(one_hot_libsvm_file,list_from_dict):
    file = open(one_hot_libsvm_file)
    oldLine = '0'
    while 1:
        lines = file.readlines( cache_size ) 
        if not lines:
            break
        for line in lines:
            if line.strip():  
                newLine =  line
                if (newLine != oldLine):
                    split_res = newLine.strip().split(" ")
                    feature_res = split_res[1:]
                    line_feature_dict = {}
                    for k in feature_res: # 这一行的feature
                    	feature_id = int(k.split(":")[0])
                    	line_feature_dict[ feature_id ] = 1 # 把目前已经有的feature放入dict中作为key
                    str_to_add = " "

                    for tree_id in range(0, len(list_from_dict) - 1 ):
                    	new_feature_id = find_feature_id(line_feature_dict,list_from_dict[ tree_id ])
                    	if new_feature_id > 0:                  	
                    		str_to_add = str(new_feature_id ) + ":1 " + str_to_add
                    if str_to_add != " ":
	                    print newLine.replace("\n","") + str_to_add

    file.close()
    

feature_id_file = sys.argv[1]
model_file 		= sys.argv[2]
libsvm_file_path= sys.argv[3]

max_feature_id = max_feature_id(feature_id_file)

model_list_dict = dict_from_model(model_file,max_feature_id)


model_list = list_from_dict(model_list_dict)


add_gdbt_feature(libsvm_file_path,model_list)
#list_from_dict_test(model_list,100,93)


#from_criteo_to_format(feature_id_dict,input_file)

