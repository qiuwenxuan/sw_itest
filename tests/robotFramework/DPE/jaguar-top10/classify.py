#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy , re, random, time, os, subprocess, sys
from pprint import pprint
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from pprint import pprint

class classify(object):
    def __init__(self):
        self.Data = {
    'classify': {
        "group": [
            {
                "tbl_name": "classify",
                "tbl_id": 0,
                "tbl_pipe": 0,
                "priority": 0,
                "key": {
                    "CLASSIFY1_PKT_TYPE": 1,
                    "CLASSIFY1_PKT_ERROR_FLAG": 0,
                    "CLASSIFY1_PKT_ERROR_TYPE": 3,
                    "CLASSIFY1_GROUP_INDEX": 2,
                    "CLASSIFY1_OUT_TUNNEL_TYPE": 4,
                    "CLASSIFY1_OUT_L5P5_HEAD_TYPE": 1,
                    "CLASSIFY1_INNER_TUNNEL_TYPE": 5,
                    "CLASSIFY1_INNER_L5P5_HEAD_TYPE": 7,
                    "CLASSIFY1_TUNNEL_ID": 2,
                    "CLASSIFY1_ADDRESS0": 1108152157446,
                    "CLASSIFY1_ADDRESS1": 16553022851850,
                    "CLASSIFY1_ADDRESS_EXTEND": 3,
                    "CLASSIFY1_OUT_VLAN_VALID": 1,
                    "CLASSIFY1_INNER_VLAN_VALID": 1,
                    "CLASSIFY1_OUT_VLAN_ID": 100,
                    "CLASSIFY1_OUT_VLAN_TPID": 2,
                    "CLASSIFY1_INNER_VLAN_ID": 200,
                    "CLASSIFY1_INNER_VLAN_TPID": 2,
                    "CLASSIFY1_ETH_TYPE": 2048,
                    "CLASSIFY1_RSV1": 0,
                    "CLASSIFY1_RSV2": 0,
                    "CLASSIFY1_PIPE_ID": 0
                },
                "mask": {
                    "CLASSIFY1_PKT_TYPE": 15,
                    "CLASSIFY1_PKT_ERROR_FLAG": 0,
                    "CLASSIFY1_PKT_ERROR_TYPE": 7,
                    "CLASSIFY1_GROUP_INDEX": 255,
                    "CLASSIFY1_OUT_TUNNEL_TYPE": 31,
                    "CLASSIFY1_OUT_L5P5_HEAD_TYPE": 7,
                    "CLASSIFY1_INNER_TUNNEL_TYPE": 31,
                    "CLASSIFY1_INNER_L5P5_HEAD_TYPE": 7,
                    "CLASSIFY1_TUNNEL_ID": 4294967295,
                    "CLASSIFY1_ADDRESS0": 281474976710655,
                    "CLASSIFY1_ADDRESS1": 281474976710655,
                    "CLASSIFY1_ADDRESS_EXTEND": 4294967295,
                    "CLASSIFY1_OUT_VLAN_VALID": 1,
                    "CLASSIFY1_INNER_VLAN_VALID": 1,
                    "CLASSIFY1_OUT_VLAN_ID": 4095,
                    "CLASSIFY1_OUT_VLAN_TPID": 7,
                    "CLASSIFY1_INNER_VLAN_ID": 4095,
                    "CLASSIFY1_INNER_VLAN_TPID": 7,
                    "CLASSIFY1_ETH_TYPE": 65535,
                    "CLASSIFY1_RSV1": 0,
                    "CLASSIFY1_RSV2": 0,
                    "CLASSIFY1_PIPE_ID": 1
                },
                "table": {
                    "CLASSIFY1_OPRATE_CODE": 2,
                    "CLASSIFY1_DEFAULT_ACTION_INDEX": 1234,
                    "CLASSIFY1_KEY_BUILD_PROFILE_ID": 170,
                    "CLASSIFY1_DISTRIBUTE_MODE": 2,
                    "CLASSIFY1_DISPATCH_TYPE": 7,
                    "CLASSIFY1_DEFAULT_DEST_VALID": 1,
                    "CLASSIFY1_DEFAULT_DEST_ACT_TYPE": 0,
                    "CLASSIFY1_DEFAULT_DEST": 5592405,
                    "CLASSIFY1_RESET_TC_FLAG": 1,
                    "CLASSIFY1_TC_VALUE": 5
                }
            }
        ]
    }
}

    def getData(self):
        return self.Data



if __name__ == '__main__':
    c = classify()                     #实例化对象
    pprint(c.getData())



