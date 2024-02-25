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

class meterProfile(object):
    def __init__(self):

        self.value1 = {                                 
            'meter_profile' : {
                'key' : 
                    {'METER_PROFILE_INDEX' :  0}
                    ,
                'table' : 
                    {'METER_PROFILE_VALID' : 1,
                    'METER_PROFILE_EIR' : 1,
                    'METER_PROFILE_CIR' : 1,
                    'METER_PROFILE_EBS' : 1,
                    'METER_PROFILE_CBS' : 1,
                    'METER_PROFILE_EBND' : 1,
                    'METER_PROFILE_CBND' : 0,
                    'METER_PROFILE_EBSM' : 1,
                    'METER_PROFILE_CBSM' : 1,
                    'METER_PROFILE_RFC' : 1,
                    'METER_PROFILE_PM' : 1,
                    'METER_PROFILE_CF' : 0,
                    'METER_PROFILE_G_ACT' : 1,                    
                    'METER_PROFILE_Y_ACT' : 1,
                    'METER_PROFILE_R_ACT' : 1,
                    'METER_PROFILE_G_DSCP' : 0,
                    'METER_PROFILE_Y_DSCP' : 1,                       
                    'METER_PROFILE_R_DSCP' : 1                 
                    }
                                  
                }              
        }

        self.value2 = {                                 
            'meter_profile' : {
                'key' : 
                    {'METER_PROFILE_INDEX' :  2}
                    ,
                'table' : 
                    {'METER_PROFILE_VALID' : 1,
                    'METER_PROFILE_EIR' : 1,
                    'METER_PROFILE_CIR' : 1,
                    'METER_PROFILE_EBS' : 1,
                    'METER_PROFILE_CBS' : 1,
                    'METER_PROFILE_EBND' : 1,
                    'METER_PROFILE_CBND' : 0,
                    'METER_PROFILE_EBSM' : 1,
                    'METER_PROFILE_CBSM' : 1,
                    'METER_PROFILE_RFC' : 1,
                    'METER_PROFILE_PM' : 1,
                    'METER_PROFILE_CF' : 0,
                    'METER_PROFILE_G_ACT' : 1,                    
                    'METER_PROFILE_Y_ACT' : 1,
                    'METER_PROFILE_R_ACT' : 1,
                    'METER_PROFILE_G_DSCP' : 0,
                    'METER_PROFILE_Y_DSCP' : 1,                       
                    'METER_PROFILE_R_DSCP' : 1                 
                    }
                                  
                }              
        }
   
    def getMeterProfileValue1(self):
        return self.value1    

    def getMeterProfileValue2(self):
        return self.value2   




if __name__ == '__main__':
    c = meterProfile()
    pprint(c.getPortConfig())



