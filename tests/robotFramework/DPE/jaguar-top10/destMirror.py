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

class destMirror(object):
    def __init__(self):

        self.value1 = {                                 
            'dest_mirror' : {
                'key' : 
                    {'VNIC_INDEX' :  0}
                    ,
                'table' : 
                    {'DEST_MIRROR_INDEX' : 1,
                    'DEST_MIRROR_PRI' : 1,
                    'DEST_MIRROR_METER_ID' : 1     
                    }                           
                }              
        }

        self.value2 = {                                 
            'dest_mirror' : {
                'key' : 
                    {'VNIC_INDEX' :  2}
                    ,
                'table' : 
                    {'DEST_MIRROR_INDEX' : 1,
                    'DEST_MIRROR_PRI' : 1,
                    'DEST_MIRROR_METER_ID' : 1     
                    }                           
                }              
        }             
   
    def getDestMirrorValue1(self):
        return self.value1    

    def getDestMirrorValue2(self):
        return self.value2   




if __name__ == '__main__':
    c = destMirror()
    pprint(c.getPortConfig())



