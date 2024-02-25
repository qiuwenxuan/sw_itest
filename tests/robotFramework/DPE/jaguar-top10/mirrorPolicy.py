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

class mirrorPolicy(object):
    def __init__(self):

        self.value1 = {                                 
            'mirror_policy' : {
                'key' : 
                    {'MIRROR_POLICY_INDEX' :  0}
                    ,
                'table' : 
                    {'MIRROR_POLICY_MODE' : 1,
                    'MIRROR_POLICY_IGNORE_DROP' : 1,
                    'MIRROR_POLICY_TRUNC' : 1,
                    'MIRROR_POLICY_ENCAP_FLAG' : 1,
                    'MIRROR_POLICY_SAMPLE' : 1,
                    'MIRROR_POLICY_SAMPLE_CONF' : 1,
                    'MIRROR_POLICY_TIME_MODEL' : 0,
                    'MIRROR_POLICY_LNS' : 1,
                    'MIRROR_POLICY_ENCAP_MODE' : 1,
                    'MIRROR_POLICY_DEST' : 1                  
                    }
                                  
                }              
        }

        self.value2 = {                                 
            'mirror_policy' : {
                'key' : 
                    {'MIRROR_POLICY_INDEX' :  1}
                    ,
                'table' : 
                    {'MIRROR_POLICY_MODE' : 1,
                    'MIRROR_POLICY_IGNORE_DROP' : 1,
                    'MIRROR_POLICY_TRUNC' : 1,
                    'MIRROR_POLICY_ENCAP_FLAG' : 1,
                    'MIRROR_POLICY_SAMPLE' : 1,
                    'MIRROR_POLICY_SAMPLE_CONF' : 1,
                    'MIRROR_POLICY_TIME_MODEL' : 0,
                    'MIRROR_POLICY_LNS' : 1,
                    'MIRROR_POLICY_ENCAP_MODE' : 1,
                    'MIRROR_POLICY_DEST' : 1                  
                    }
                                  
                }               
        }
   
    def getMirrorPolicyValue1(self):
        return self.value1    

    def getMirrorPolicyValue2(self):
        return self.value2   




if __name__ == '__main__':
    c = mirrorPolicy()
    pprint(c.getPortConfig())



