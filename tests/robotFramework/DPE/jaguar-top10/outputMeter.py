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

class outputMeter(object):
    def __init__(self):

        self.value1 = {                                 
            'output_meter' : {
                'key' : 
                    {'OUTPUT_METER_INDEX' :  0}
                    ,
                'table' : 
                    {'OUTPUT_METER_ID' : 1}                              
                }              
        }

        self.value2 = {                                 
            'output_meter' : {
                'key' : 
                    {'OUTPUT_METER_INDEX' :  1}
                    ,
                'table' : 
                    {'OUTPUT_METER_ID' : 2}                              
                }               
        }
   
    def getOutputMeterValue1(self):
        return self.value1    

    def getOutputMeterValue2(self):
        return self.value2   




if __name__ == '__main__':
    c = outputMeter()
    pprint(c.getPortConfig())



