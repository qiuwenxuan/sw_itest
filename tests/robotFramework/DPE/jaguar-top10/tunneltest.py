#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy , re, random, time, os, subprocess, sys
from pprint import pprint
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from pprint import pprint

class tunneltest(object):
    def __init__(self):
        self.Data = {
            'cfg_tool_test': {
                "group": [
                    {
                        "tbl_name": "cfg_test",
                    }
                ]
            }
        }


    def getData(self):
        return self.Data



if __name__ == '__main__':
    c = tunneltest()                     #实例化对象
    pprint(c.getData())



