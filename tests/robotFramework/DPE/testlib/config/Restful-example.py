#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy , re, random, time, os, subprocess, sys
from pprint import pprint
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from pprint import pprint

from scapy.all import *  
from scapy.contrib.mpls import * # import from contrib folder of scapy 
from scapy.layers.inet6 import *
from scapy.contrib.geneve import GENEVE

class Restful(object):
    def __init__(self):
        self.lib = BuiltIn().get_library_instance('CorsicaDefault')
        in_port = str(BuiltIn().get_variable_value('${cha1port1}'))
        out_port = str(BuiltIn().get_variable_value('${cha1port2}'))
        
        #获取流量模板
        self.value1 = self.lib.getFlowType1(in_port,out_port)

        #保留关联信息
        groupidx = self.value1["input_rx"]['table'][0]['GROUP_IDX']

        #修改流量模板参数
        self.value1["reg_table"] = {
                  'reg':[
                        {"reg_type":'PIPE_GRP_0' , "reg_name":"PIPE_GRP_MEM_CTRL_BUS_00_REG" , "value":0x100},
                        {"reg_type":'PIPE_GRP_1' , "reg_name":"PIPE_GRP_MEM_CTRL_BUS_00_REG" , "value":0x01020304},
                    ] 
                  }
        self.value1["input_rx"] = {
                'key' : [
                {'SOURCE_PORT' :  in_port, 
                 'TUNNEL_PKT' : 0},
                ],
                'table' : [
                {'DEF_ACT_IDX' : 0, 
                'OP_CODE' : 0,
                'MEP_CODE' : 0,
                'MEP_TYPE' : 0,
                'ACT_TYPE' : 0,
                'DEF_DST' : out_port, 
                'MIRR_PRI' : 0,
                'MIRR_METER_IDX' : 0,
                'MIRR_IDX' : 0,
                'METE_INFO0' : 0,
                'GROUP_IDX' :   groupidx}
                ]
            }

    #返回配置信息
    def getConfig(self):
        return self.lib.checkTable(self.value1)    

    
if __name__ == '__main__':
    c = Restful()
    pprint(c.getPortConfig())



