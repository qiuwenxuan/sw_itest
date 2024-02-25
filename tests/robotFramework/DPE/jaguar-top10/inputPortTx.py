#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy , re, random, time, os, subprocess, sys
from pprint import pprint
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from pprint import pprint

class inputPortTx(object):
    def __init__(self):
        self.Data = {
    'input_port_tx':
        {
        "group": [
            {
                "tbl_name": "input_tx",
                "key": {
                    "INPUT_PORT_TX_SRC_PORT": 70
                },
                "table": {
                    "INPUT_PORT_TX_DEF_ACT_INDEX": 1000,
                    "INPUT_PORT_TX_OP_CODE": 3,
                    "INPUT_PORT_TX_RPE_OP_CODE": 4,
                    "INPUT_PORT_TX_MEP_DSTRIBUT_PROF": 1,
                    "INPUT_PORT_TX_MEP_DSPTCH_TYPE": 7,
                    "INPUT_PORT_TX_ACT_TYPE": 0,
                    "INPUT_PORT_TX_DEF_DST": 1234,
                    "INPUT_PORT_TX_GROUP_IDX": 100,
                    "INPUT_PORT_TX_RPE_GROUP_IDX": 110,
                    "INPUT_PORT_TX_MIRR_PRI": 0,
                    "INPUT_PORT_TX_MIRR_METER_IDX": 5678,
                    "INPUT_PORT_TX_MIRR_IDX": 567,
                    "INPUT_PORT_TX_METE_INFO0": 4321,
                    "INPUT_PORT_TX_ANTI_SPOOF": 3,
                    "INPUT_PORT_TX_ALLOWED_TP_ID": 5,
                    "INPUT_PORT_TX_DEF_TP_ID": 0,
                    "INPUT_PORT_TX_PRI_ANTI_SPOOF": 1,
                    "INPUT_PORT_TX_ALLOWED_PRI": 100,
                    "INPUT_PORT_TX_DEF_PRI": 0,
                    "INPUT_PORT_TX_SMAC_ANTI": 2,
                    "INPUT_PORT_TX_SMAC": 1108152157446,
                    "INPUT_PORT_TX_RPE_OVERLAY_FLAG": 1,
                    "INPUT_PORT_TX_RPE_QID": 1111
                }
            },
            {
                "tbl_name": "input_tx",
                "key": {
                    "INPUT_PORT_TX_SRC_PORT": 72
                },
                "table": {
                    "INPUT_PORT_TX_DEF_ACT_INDEX": 2000,
                    "INPUT_PORT_TX_OP_CODE": 3,
                    "INPUT_PORT_TX_RPE_OP_CODE": 4,
                    "INPUT_PORT_TX_MEP_DSTRIBUT_PROF": 1,
                    "INPUT_PORT_TX_MEP_DSPTCH_TYPE": 7,
                    "INPUT_PORT_TX_ACT_TYPE": 0,
                    "INPUT_PORT_TX_DEF_DST": 2345,
                    "INPUT_PORT_TX_GROUP_IDX": 100,
                    "INPUT_PORT_TX_RPE_GROUP_IDX": 110,
                    "INPUT_PORT_TX_MIRR_PRI": 0,
                    "INPUT_PORT_TX_MIRR_METER_IDX": 5678,
                    "INPUT_PORT_TX_MIRR_IDX": 567,
                    "INPUT_PORT_TX_METE_INFO0": 4321,
                    "INPUT_PORT_TX_ANTI_SPOOF": 3,
                    "INPUT_PORT_TX_ALLOWED_TP_ID": 5,
                    "INPUT_PORT_TX_DEF_TP_ID": 0,
                    "INPUT_PORT_TX_PRI_ANTI_SPOOF": 1,
                    "INPUT_PORT_TX_ALLOWED_PRI": 100,
                    "INPUT_PORT_TX_DEF_PRI": 0,
                    "INPUT_PORT_TX_SMAC_ANTI": 2,
                    "INPUT_PORT_TX_SMAC": 2211975595527,
                    "INPUT_PORT_TX_RPE_OVERLAY_FLAG": 1,
                    "INPUT_PORT_TX_RPE_QID": 1111
                }
            },
            {
                "tbl_name": "input_tx",
                "key": {
                    "INPUT_PORT_TX_SRC_PORT": 75
                },
                "table": {
                    "INPUT_PORT_TX_DEF_ACT_INDEX": 3000,
                    "INPUT_PORT_TX_OP_CODE": 3,
                    "INPUT_PORT_TX_RPE_OP_CODE": 4,
                    "INPUT_PORT_TX_MEP_DSTRIBUT_PROF": 1,
                    "INPUT_PORT_TX_MEP_DSPTCH_TYPE": 7,
                    "INPUT_PORT_TX_ACT_TYPE": 0,
                    "INPUT_PORT_TX_DEF_DST": 1234,
                    "INPUT_PORT_TX_GROUP_IDX": 100,
                    "INPUT_PORT_TX_RPE_GROUP_IDX": 110,
                    "INPUT_PORT_TX_MIRR_PRI": 0,
                    "INPUT_PORT_TX_MIRR_METER_IDX": 5678,
                    "INPUT_PORT_TX_MIRR_IDX": 567,
                    "INPUT_PORT_TX_METE_INFO0": 4321,
                    "INPUT_PORT_TX_ANTI_SPOOF": 3,
                    "INPUT_PORT_TX_ALLOWED_TP_ID": 5,
                    "INPUT_PORT_TX_DEF_TP_ID": 0,
                    "INPUT_PORT_TX_PRI_ANTI_SPOOF": 1,
                    "INPUT_PORT_TX_ALLOWED_PRI": 100,
                    "INPUT_PORT_TX_DEF_PRI": 0,
                    "INPUT_PORT_TX_SMAC_ANTI": 2,
                    "INPUT_PORT_TX_SMAC": 4419622471689,
                    "INPUT_PORT_TX_RPE_OVERLAY_FLAG": 1,
                    "INPUT_PORT_TX_RPE_QID": 1111
                }
            },
            {
                "tbl_name": "input_tx",
                "key": {
                    "INPUT_PORT_TX_SRC_PORT": 80
                },
                "table": {
                    "INPUT_PORT_TX_DEF_ACT_INDEX": 4000,
                    "INPUT_PORT_TX_OP_CODE": 3,
                    "INPUT_PORT_TX_RPE_OP_CODE": 4,
                    "INPUT_PORT_TX_MEP_DSTRIBUT_PROF": 1,
                    "INPUT_PORT_TX_MEP_DSPTCH_TYPE": 7,
                    "INPUT_PORT_TX_ACT_TYPE": 0,
                    "INPUT_PORT_TX_DEF_DST": 1234,
                    "INPUT_PORT_TX_GROUP_IDX": 100,
                    "INPUT_PORT_TX_RPE_GROUP_IDX": 110,
                    "INPUT_PORT_TX_MIRR_PRI": 0,
                    "INPUT_PORT_TX_MIRR_METER_IDX": 5678,
                    "INPUT_PORT_TX_MIRR_IDX": 567,
                    "INPUT_PORT_TX_METE_INFO0": 4321,
                    "INPUT_PORT_TX_ANTI_SPOOF": 3,
                    "INPUT_PORT_TX_ALLOWED_TP_ID": 5,
                    "INPUT_PORT_TX_DEF_TP_ID": 0,
                    "INPUT_PORT_TX_PRI_ANTI_SPOOF": 1,
                    "INPUT_PORT_TX_ALLOWED_PRI": 100,
                    "INPUT_PORT_TX_DEF_PRI": 0,
                    "INPUT_PORT_TX_SMAC_ANTI": 2,
                    "INPUT_PORT_TX_SMAC": 5523445909770,
                    "INPUT_PORT_TX_RPE_OVERLAY_FLAG": 1,
                    "INPUT_PORT_TX_RPE_QID": 1111
                }
            }
        ]
    }
}

    def getData(self):
        return self.Data



if __name__ == '__main__':
    c = inputPortTx()                     #实例化对象
    pprint(c.getData())



