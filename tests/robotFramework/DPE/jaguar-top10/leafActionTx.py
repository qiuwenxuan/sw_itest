#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy , re, random, time, os, subprocess, sys
from pprint import pprint
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from pprint import pprint

class leafActionTx(object):
    def __init__(self):
        self.Data = {
    'mc_leaf_action_tx':{
        "group": [
            {
                "tbl_name": "mc_leaf_action_tx",
                "key": {
                    "LEAF_ACTION_INDEX": 10
                },
                "table": {
                    "LEAF_ACTION_IN_SRC_TBL": 12,
                    "LEAF_ACTION_IN_TUNNEL_ENCAP_TYPE": 5,
                    "LEAF_ACTION_IN_TUNNEL_ENCAP_LEN": 90,
                    "LEAF_ACTION_IN_L4_ENCAP_TYPE": 7,
                    "LEAF_ACTION_IN_L3_ENCAP_TYPE": 2,
                    "LEAF_ACTION_IN_VTAG_TYPE": 3,
                    "LEAF_ACTION_IN_L2_FLAG": 1,
                    "LEAF_ACTION_OUT_SRC_TBL": 84,
                    "LEAF_ACTION_OUT_TUNNEL_ENCAP_TYPE": 5,
                    "LEAF_ACTION_OUT_TUNNEL_ENCAP_LEN": 90,
                    "LEAF_ACTION_OUT_L4_ENCAP_TYPE": 7,
                    "LEAF_ACTION_OUT_L3_ENCAP_TYPE": 2,
                    "LEAF_ACTION_OUT_VTAG_TYPE": 3,
                    "LEAF_ACTION_OUT_L2_FLAG": 1
                }
            },
            {
                "tbl_name": "mc_leaf_action_tx",
                "key": {
                    "LEAF_ACTION_INDEX": 20
                },
                "table": {
                    "LEAF_ACTION_IN_SRC_TBL": 22,
                    "LEAF_ACTION_IN_TUNNEL_ENCAP_TYPE": 5,
                    "LEAF_ACTION_IN_TUNNEL_ENCAP_LEN": 90,
                    "LEAF_ACTION_IN_L4_ENCAP_TYPE": 7,
                    "LEAF_ACTION_IN_L3_ENCAP_TYPE": 2,
                    "LEAF_ACTION_IN_VTAG_TYPE": 3,
                    "LEAF_ACTION_IN_L2_FLAG": 1,
                    "LEAF_ACTION_OUT_SRC_TBL": 94,
                    "LEAF_ACTION_OUT_TUNNEL_ENCAP_TYPE": 5,
                    "LEAF_ACTION_OUT_TUNNEL_ENCAP_LEN": 90,
                    "LEAF_ACTION_OUT_L4_ENCAP_TYPE": 7,
                    "LEAF_ACTION_OUT_L3_ENCAP_TYPE": 2,
                    "LEAF_ACTION_OUT_VTAG_TYPE": 3,
                    "LEAF_ACTION_OUT_L2_FLAG": 1
                }
            },
            {
                "tbl_name": "mc_leaf_action_tx",
                "key": {
                    "LEAF_ACTION_INDEX": 30
                },
                "table": {
                    "LEAF_ACTION_IN_SRC_TBL": 32,
                    "LEAF_ACTION_IN_TUNNEL_ENCAP_TYPE": 5,
                    "LEAF_ACTION_IN_TUNNEL_ENCAP_LEN": 90,
                    "LEAF_ACTION_IN_L4_ENCAP_TYPE": 7,
                    "LEAF_ACTION_IN_L3_ENCAP_TYPE": 2,
                    "LEAF_ACTION_IN_VTAG_TYPE": 3,
                    "LEAF_ACTION_IN_L2_FLAG": 1,
                    "LEAF_ACTION_OUT_SRC_TBL": 104,
                    "LEAF_ACTION_OUT_TUNNEL_ENCAP_TYPE": 5,
                    "LEAF_ACTION_OUT_TUNNEL_ENCAP_LEN": 90,
                    "LEAF_ACTION_OUT_L4_ENCAP_TYPE": 7,
                    "LEAF_ACTION_OUT_L3_ENCAP_TYPE": 2,
                    "LEAF_ACTION_OUT_VTAG_TYPE": 3,
                    "LEAF_ACTION_OUT_L2_FLAG": 1
                }
            }
        ]
    }
}

    def getData(self):
        return self.Data



if __name__ == '__main__':
    c = leafActionTx()                     #实例化对象
    pprint(c.getData())



