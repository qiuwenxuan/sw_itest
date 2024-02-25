#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy , re, random, time, os, subprocess, sys
from pprint import pprint
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from pprint import pprint

class mcLeafTx(object):
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
            }
        ]
    },
    'mc_leaf_tx':{
        "group": [
            {
                "tbl_name": "mc_leaf_tx",
                "key": {
                    "MC_LEAF_INDEX": 1,
                    "MC_LEAF_GROUP_INDEX": 1
                },
                "table": {
                    "MC_LEAF_DEST": 1234,
                    "MC_LEAF_ACTION_INDEX": 123,
                    "MC_LEAF_NEXT_INDEX": 10,
                    "MC_LEAF_ENCAP_LEN": 11
                }
            },
            {
                "tbl_name": "mc_leaf_tx",
                "key": {
                    "MC_LEAF_INDEX": 10,
                    "MC_LEAF_GROUP_INDEX": 1
                },
                "table": {
                    "MC_LEAF_DEST": 2345,
                    "MC_LEAF_ACTION_INDEX": 234,
                    "MC_LEAF_NEXT_INDEX": 15,
                    "MC_LEAF_ENCAP_LEN": 12
                }
            },
            {
                "tbl_name": "mc_leaf_tx",
                "key": {
                    "MC_LEAF_INDEX": 21,
                    "MC_LEAF_GROUP_INDEX": 1
                },
                "table": {
                    "MC_LEAF_DEST": 6789,
                    "MC_LEAF_ACTION_INDEX": 678,
                    "MC_LEAF_NEXT_INDEX": 0,
                    "MC_LEAF_ENCAP_LEN": 13
                }
            }
        ]
    }
}

    def getData(self):
        return self.Data



if __name__ == '__main__':
    c = mcLeafTx()                     #实例化对象
    pprint(c.getData())



