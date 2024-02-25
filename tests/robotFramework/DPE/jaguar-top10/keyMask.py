#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy , re, random, time, os, subprocess, sys
from pprint import pprint
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from pprint import pprint

class keyMask(object):
    def __init__(self):
        self.Data = {
    'key_mask':{
        "group": [
            {
                "tbl_name": "key_mask",
                "tbl_pipe": 0,
                "tbl_id": 0,
                "key": {
                    "KEY_MASK_INDEX": 1
                },
                "table": {
                    "KEY_MASK1": 11111,
                    "KEY_MASK2": 12222,
                    "KEY_MASK3": 13333,
                    "KEY_MASK4": 14444,
                    "KEY_MASK5": 15555,
                    "KEY_MASK6": 16666,
                    "KEY_MASK7": 17777,
                    "KEY_MASK8": 18888,
                    "KEY_MASK9": 19999,
                    "KEY_MASK10": 12121,
                    "KEY_MASK11": 13131,
                    "KEY_MASK12": 14141
                }
            },
            {
                "tbl_name": "key_mask",
                "tbl_pipe": 0,
                "tbl_id": 0,
                "key": {
                    "KEY_MASK_INDEX": 3
                },
                "table": {
                    "KEY_MASK1": 21111,
                    "KEY_MASK2": 22222,
                    "KEY_MASK3": 23333,
                    "KEY_MASK4": 24444,
                    "KEY_MASK5": 25555,
                    "KEY_MASK6": 26666,
                    "KEY_MASK7": 27777,
                    "KEY_MASK8": 28888,
                    "KEY_MASK9": 29999,
                    "KEY_MASK10": 22121,
                    "KEY_MASK11": 23131,
                    "KEY_MASK12": 24141
                }
            },
            {
                "tbl_name": "key_mask",
                "tbl_pipe": 2,
                "tbl_id": 0,
                "key": {
                    "KEY_MASK_INDEX": 3
                },
                "table": {
                    "KEY_MASK1": 31111,
                    "KEY_MASK2": 32222,
                    "KEY_MASK3": 33333,
                    "KEY_MASK4": 34444,
                    "KEY_MASK5": 35555,
                    "KEY_MASK6": 36666,
                    "KEY_MASK7": 37777,
                    "KEY_MASK8": 38888,
                    "KEY_MASK9": 39999,
                    "KEY_MASK10": 32121,
                    "KEY_MASK11": 33131,
                    "KEY_MASK12": 34141
                }
            },
            {
                "tbl_name": "key_mask",
                "tbl_pipe": 4,
                "tbl_id": 0,
                "key": {
                    "KEY_MASK_INDEX": 3
                },
                "table": {
                    "KEY_MASK1": 41111,
                    "KEY_MASK2": 42222,
                    "KEY_MASK3": 43333,
                    "KEY_MASK4": 44444,
                    "KEY_MASK5": 45555,
                    "KEY_MASK6": 46666,
                    "KEY_MASK7": 47777,
                    "KEY_MASK8": 48888,
                    "KEY_MASK9": 49999,
                    "KEY_MASK10": 42121,
                    "KEY_MASK11": 43131,
                    "KEY_MASK12": 44141
                }
            }
        ]
    }
}

    def getData(self):
        return self.Data



if __name__ == '__main__':
    c = keyMask()                     #实例化对象
    pprint(c.getData())



