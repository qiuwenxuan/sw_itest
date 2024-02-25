#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy , re, random, time, os, subprocess, sys
from pprint import pprint
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from pprint import pprint

class mcGroupTx(object):
    def __init__(self):
        self.Data = {
    'mc_group_tx':{
        "group": [
            {
                "tbl_name": "mc_group_tx",
                "key": {
                    "MC_GROUP_TX_INDEX": 1
                },
                "table": {
                    "MC_GROUP_TX_SRC_FILTER": 1,
                    "MC_GROUP_TX_NEXT_LEAF_INDEX": 123
                }
            },
            {
                "tbl_name": "mc_group_tx",
                "key": {
                    "MC_GROUP_TX_INDEX": 2
                },
                "table": {
                    "MC_GROUP_TX_SRC_FILTER": 1,
                    "MC_GROUP_TX_NEXT_LEAF_INDEX": 456
                }
            },
            {
                "tbl_name": "mc_group_tx",
                "key": {
                    "MC_GROUP_TX_INDEX": 5
                },
                "table": {
                    "MC_GROUP_TX_SRC_FILTER": 1,
                    "MC_GROUP_TX_NEXT_LEAF_INDEX": 789
                }
            }
        ]
    }
}

    def getData(self):
        return self.Data



if __name__ == '__main__':
    c = mcGroupTx()                     #实例化对象
    pprint(c.getData())



