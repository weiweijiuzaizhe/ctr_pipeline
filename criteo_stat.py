# -*- coding: utf-8 -*-  

import sys
import time
import subprocess
import os 



distance = 1000000
cls_num = 40
threshold = 1

def read_from_data(input_file,cls):  # input_file 输入的文件路径,cls 对应的列号
    s1 = time.clock()
    file = open(input_file)
    oldLine = '0'
    count = 0
    cl_dist = dict()
    to_return = dict()
    
    while 1:
        lines = file.readlines(10*10*1024)  #用缓存提高速度
        #print len(lines)
        if not lines:
            break
        for line in lines:
            if line.strip():  #去掉首末的不可见字符
                newLine =  line
                if (newLine != oldLine):
                    split_res = newLine.split("\t")
                    #tag = int( split_res[ 0 ] )
                    cls_v  =  split_res[ cls ]  #得到指定列的值
                    
                    if (cl_dist.has_key( cls_v ) ): 
                      cl_dist[ cls_v ] = cl_dist[ cls_v ] + 1
                    else:
                      cl_dist[ cls_v ] = 1


                    oldLine = newLine
                    count += 1
                    if (count % distance == 0):
    					print  "now have read %s lines,tag:%s" %(count,tag)

                        #print  "tag:%d" %(tag)


    for k in cl_dist:
        if cl_dist[ k ] > threshold : #出现了threshold次以上
            to_return[ str(cls) + "_" + str(k) ] =  cl_dist[ k ]


    print "deal %s lines" %(count)
    e1 = time.clock()
    print "spent time:" + str(e1-s1)
    return to_return



def write_dict_to_file(output_file,input_dict):
    f = open(output_file, 'w')
    for k in input_dict:
        f.write( str(k) + ":" + str(input_dict[k]) + "\n" )

    f.close() 


def get_featue_id_file(out_file,input_file,max_cls): #最好在这里将中间文件产生与消除
    for i in range(1,cls_num ):
        print i
        stat_dict = read_from_data(input_file,i)
        write_dict_to_file(out_file + "_" + str(i),stat_dict) #会产生 cls_num - 1 个中间文件

    command_str="ls|grep \""+out_file+"\"|xargs cat |awk '{printf(\"%d:%s\\n\",NR,$0)}'> "+out_file+".txt" 
    print command_str
    os.system(command_str)
    rm_command = "ls|grep \""+out_file+"\"|grep -v \".txt\"|xargs rm"
    print rm_command
    os.system(rm_command) #删除中间文件







input_file = sys.argv[1];
out_file = sys.argv[2]; 
#stat_dict = read_from_data( input_file,2 )
#write_dict_to_file(out_file,stat_dict)

get_featue_id_file(out_file,input_file,cls_num)



