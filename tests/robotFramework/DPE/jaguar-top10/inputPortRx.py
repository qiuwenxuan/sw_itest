#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy , re, random, time, os, subprocess, sys
from pprint import pprint
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from pprint import pprint

class inputPortRx(object):
    def __init__(self):
        self.Data = {
    'input_port_rx':{
        "group": [
            {
                "tbl_name": "input_rx",
                "key": {
                    "INPUT_PORT_RX_TUNNEL_PKT_FLAG": 1,
                    "INPUT_PORT_RX_SRC_PORT": 5
                },
                "table": {
                    "INPUT_PORT_RX_DEF_ACT_INDEX": 1234,
                    "INPUT_PORT_RX_OP_CODE": 3,
                    "INPUT_PORT_RX_MEP_DSTRIBUT_PROF": 2,
                    "INPUT_PORT_RX_MEP_DSPTCH_TYPE": 7,
                    "INPUT_PORT_RX_RSV": 0,
                    "INPUT_PORT_RX_ACT_TYPE": 0,
                    "INPUT_PORT_RX_DEF_DST": 5678,
                    "INPUT_PORT_RX_MIRR_PRI": 1,
                    "INPUT_PORT_RX_MIRR_METER_IDX": 1000,
                    "INPUT_PORT_RX_MIRR_IDX": 100,
                    "INPUT_PORT_RX_METE_INFO0": 10,
                    "INPUT_PORT_RX_GROUP_IDX": 57
                }
            },
            {
                "tbl_name": "input_rx",
                "key": {
                    "INPUT_PORT_RX_TUNNEL_PKT_FLAG": 1,
                    "INPUT_PORT_RX_SRC_PORT": 11
                },
                "table": {
                    "INPUT_PORT_RX_DEF_ACT_INDEX": 1234,
                    "INPUT_PORT_RX_OP_CODE": 3,
                    "INPUT_PORT_RX_MEP_DSTRIBUT_PROF": 2,
                    "INPUT_PORT_RX_MEP_DSPTCH_TYPE": 7,
                    "INPUT_PORT_RX_RSV": 0,
                    "INPUT_PORT_RX_ACT_TYPE": 0,
                    "INPUT_PORT_RX_DEF_DST": 5678,
                    "INPUT_PORT_RX_MIRR_PRI": 1,
                    "INPUT_PORT_RX_MIRR_METER_IDX": 2000,
                    "INPUT_PORT_RX_MIRR_IDX": 200,
                    "INPUT_PORT_RX_METE_INFO0": 20,
                    "INPUT_PORT_RX_GROUP_IDX": 57
                }
            },
            {
                "tbl_name": "input_rx",
                "key": {
                    "INPUT_PORT_RX_TUNNEL_PKT_FLAG": 1,
                    "INPUT_PORT_RX_SRC_PORT": 8
                },
                "table": {
                    "INPUT_PORT_RX_DEF_ACT_INDEX": 1234,
                    "INPUT_PORT_RX_OP_CODE": 3,
                    "INPUT_PORT_RX_MEP_DSTRIBUT_PROF": 2,
                    "INPUT_PORT_RX_MEP_DSPTCH_TYPE": 7,
                    "INPUT_PORT_RX_RSV": 0,
                    "INPUT_PORT_RX_ACT_TYPE": 0,
                    "INPUT_PORT_RX_DEF_DST": 5678,
                    "INPUT_PORT_RX_MIRR_PRI": 1,
                    "INPUT_PORT_RX_MIRR_METER_IDX": 3000,
                    "INPUT_PORT_RX_MIRR_IDX": 300,
                    "INPUT_PORT_RX_METE_INFO0": 30,
                    "INPUT_PORT_RX_GROUP_IDX": 57
                }
            },
            {
                "tbl_name": "input_rx",
                "key": {
                    "INPUT_PORT_RX_TUNNEL_PKT_FLAG": 1,
                    "INPUT_PORT_RX_SRC_PORT": 13
                },
                "table": {
                    "INPUT_PORT_RX_DEF_ACT_INDEX": 1234,
                    "INPUT_PORT_RX_OP_CODE": 3,
                    "INPUT_PORT_RX_MEP_DSTRIBUT_PROF": 2,
                    "INPUT_PORT_RX_MEP_DSPTCH_TYPE": 7,
                    "INPUT_PORT_RX_RSV": 0,
                    "INPUT_PORT_RX_ACT_TYPE": 0,
                    "INPUT_PORT_RX_DEF_DST": 5678,
                    "INPUT_PORT_RX_MIRR_PRI": 1,
                    "INPUT_PORT_RX_MIRR_METER_IDX": 4000,
                    "INPUT_PORT_RX_MIRR_IDX": 400,
                    "INPUT_PORT_RX_METE_INFO0": 40,
                    "INPUT_PORT_RX_GROUP_IDX": 57
                }
            }
        ]
    }
}

    def getData(self):
        return self.Data



if __name__ == '__main__':
    c = inputPortRx()                     #实例化对象
    pprint(c.getData())



