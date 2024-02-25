#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy , re, random, time, os, subprocess, sys
from pprint import pprint
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from pprint import pprint

class mcGroupRx(object):
    def __init__(self):
        self.Data = {
    'mc_group_rx':{
        "group": [
            {
                "tbl_name": "mc_group_rx",
                "key": {
                    "MC_GROUP_RX_INDEX": 1
                },
                "table": {
                    "MC_GROUP_RX_SRC_FILTER": 1,
                    "MC_GROUP_RX_NEXT_LEAF_INDEX": 1234
                }
            },
            {
                "tbl_name": "mc_group_rx",
                "key": {
                    "MC_GROUP_RX_INDEX": 2
                },
                "table": {
                    "MC_GROUP_RX_SRC_FILTER": 1,
                    "MC_GROUP_RX_NEXT_LEAF_INDEX": 1567
                }
            },
            {
                "tbl_name": "mc_group_rx",
                "key": {
                    "MC_GROUP_RX_INDEX": 5
                },
                "table": {
                    "MC_GROUP_RX_SRC_FILTER": 1,
                    "MC_GROUP_RX_NEXT_LEAF_INDEX": 1111
                }
            }
        ]
    }
}

    def getData(self):
        return self.Data



if __name__ == '__main__':
    c = mcGroupRx()                     #实例化对象
    pprint(c.getData())



