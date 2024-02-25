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

class meter(object):
    def __init__(self):

        self.value1 = {                               
            'meter_table' : {
                'key' : 
                    {'METER_TABLE_INDEX' :  0}
                    ,
                'table' : 
                    {'METER_TABLE_VALID' : 1,
                    'METER_PROFILE_ID' : 1,
                    'METER_TABLE_BKT_E' : 1,
                    'METER_TABLE_BKT_C' : 1,
                    'METER_TABLE_PKT_CNT' : 1,
                    'METER_TABLE_BYTE_CNT' : 1,
                    'METER_TABLE_LAST_TS' : 0,
                    'METER_TABLE_LAST_RSV' : 1}
                                  
                }              
        }

        self.value2 = {                                 
            'meter_table' : {
                'key' : 
                    {'METER_TABLE_INDEX' :  2}
                    ,
                'table' : 
                    {'METER_TABLE_VALID' : 1,
                    'METER_PROFILE_ID' : 2,
                    'METER_TABLE_BKT_E' : 2,
                    'METER_TABLE_BKT_C' : 2,
                    'METER_TABLE_PKT_CNT' : 2,
                    'METER_TABLE_BYTE_CNT' : 2,
                    'METER_TABLE_LAST_TS' : 0,
                    'METER_TABLE_LAST_RSV' : 1}
                                  
                }              
        }
   
    def getMeterValue1(self):
        return self.value1    

    def getMeterValue2(self):
        return self.value2   




if __name__ == '__main__':
    c = meter()
    pprint(c.getMeterValue1())



