#!/usr/bin/python
# -*- coding: utf-8 -*-

from ast import Bytes
import sys,os,re,time , random , math , binascii
import socket , struct , copy , json, itertools
from pprint import pprint

import requests
import scapy
from robot.api import logger
from scapy.all import *
from scapy_helper import mac2int,ip2int,int2ip, int2mac
from scapy.contrib.geneve import GENEVE
from scapy.contrib.mpls import MPLS
from scapy.layers.vxlan import VXLAN
from scapy.contrib.nsh import NSH
from scapy.contrib.igmp import *
from scapy.contrib.igmpv3 import *

__path = os.path.realpath(os.path.join(__file__,'..','..','..','base'))
if __path not in sys.path:sys.path.append(__path)
__path = os.path.realpath(os.path.join(__file__,'..'))  #当前路径
if __path not in sys.path:sys.path.append(__path)

from register import *

class JaguarConfig(object):
    headers = {'Content-Type': 'application/json'}
    
    def __init__(self,ip):
        if ':' in ip :
            self.ip,self.port = ip.split(':')
        else:
            self.ip = ip
            self.port = 3000

    def __urlSleep(self):
        pass

    def __getJsonNew(self):
        now = time.strftime("%m%d%H%M%S")
        filename = "jaguar_json_"+now+str(random.randint(100,999))
        file = os.path.join(os.getenv('TEMP'),filename+".json")
        return filename+".json",file

    def __getBaseUrl(self):
        ip = self.ip
        port = self.port
        return "http://%s:%s/jmndapi/v2/ovsconfig"%(ip,port)

    def __createUrl(self,table,params=dict()):
        '''获取url
        '''
        url = self.__getBaseUrl()
        if table != None:
            url += '/' + table + '?token=jmnd_001'
        return url

    def postTable(self,table,name,config):
        url = self.__createUrl(table,name)
        data = config
        r = requests.post(url=url,
                          headers=self.headers,
                          data=json.dumps(data))
        if not r.ok :
            raise AssertionError("Post error!")
        retdata = r.json()
        ret = retdata.get('data',"")
        retSucNum = ret.count('success!')
        return retSucNum

    def getTable(self,table=None,name=None, data=None, params=None):

        url = self.__createUrl(table,name)
        if data != None:
            data=json.dumps(data)
        if params != None:
            params=json.dumps(params)
        r = requests.get(url=url, headers=self.headers, data=data, params=params)
        if not r.ok :
            raise AssertionError("Get error!")
        return r.json()

    def putTable(self,table,name=None):
        url = self.__createUrl(table,name)
        if self.__isCurl():
            raise AssertionError("Not support")
            return
        r = requests.put(url=url, headers=self.headers)
        if not r.ok :
            raise AssertionError("Put error!")
        return r.json()

    def deleteTable(self,table=None,name=None):
        url = self.__createUrl(table,name)
        r = requests.delete(url=url, headers=self.headers)
        if not r.ok :
            raise AssertionError("Delete error!")
        ret = r.json().get('data')
        if ret != 'success!':
            pass
        return

    def jaguarRunConfig(self, config):
        for k in config.keys():
            retSucNum = self.postTable(k, None, config[k])         
        return True

    def jaguarClearConfig(self,config=None):
        '''删除jaguar已经配置的基本配置
        '''
        if config == None:
            return True

        for k,v in config.items():
            if k == 'register':
                if 'group' in v:
                    for j in v['group']:
                        j['table']['REG_VALUE'] = 0
                        retSucNum = self.postTable(k,None, j)
                else:
                    v['table']['REG_VALUE'] = 0
                    retSucNum = self.postTable(k,None, v)          
            else:
                retSucNum = self.deleteTable(k, v)
        return True
    
    def jaguarClearConfigAll(self):
        '''删除jaguar已经配置的基本配置
        '''
        '''
        先在这里定义，后面看支不支持从设备获取
        '''
        '''
        configlist = ['source_mode1', 'source_mode2', 'input_port_rx', 'input_port_tx', 'classify', 'profile',
                      'key_template', 'key_mask', 'mc_group_rx', 'mc_group_tx', 'mc_leaf_rx', 'mc_leaf_tx', 'mc_leaf_action_rx',
                      'mc_leaf_action_tx', 'em_table', 'register', 'meter_table', 'meter_profile', 'output_meter', 'dest_mirror', 
                      'mirror_policy']
        '''
        configlist = ['source_mode1', 'source_mode2', 'input_port_rx', 'input_port_tx', 'classify', 'profile',
                'key_template', 'key_mask', 'mc_group_rx', 'mc_group_tx', 'mc_leaf_rx', 'mc_leaf_tx', 'mirror_policy']
              
        for table in configlist:
            self.deleteTable(table, None)
            self.__urlSleep()

        return True

class corsica_dpe (object):
    default_json = {
        "input_port_rx" : {
            "tbl_name": "input_port_rx",
            "key" :  {
                "INPUT_PORT_RX_TUNNEL_PKT_FLAG" : 0,
                "INPUT_PORT_RX_SRC_PORT" :  0
            },
            "table" : {
                "INPUT_PORT_RX_DEF_ACT_INDEX": 0,#默认到0口
                "INPUT_PORT_RX_OP_CODE": 4,  # 2 to classify ,4 dorp
                "INPUT_PORT_RX_MEP_DSTRIBUT_PROF": 0,
                "INPUT_PORT_RX_MEP_DSPTCH_TYPE": 0,
                "INPUT_PORT_RX_RSV": 0,
                "INPUT_PORT_RX_ACT_TYPE": 0,
                "INPUT_PORT_RX_DEF_DST": 0,
                "INPUT_PORT_RX_MIRR_PRI": 0,
                "INPUT_PORT_RX_MIRR_METER_IDX": 0,
                "INPUT_PORT_RX_MIRR_IDX": 0,
                "INPUT_PORT_RX_METE_INFO0": 0,
                "INPUT_PORT_RX_GROUP_IDX": 0
            }
        },
        "default_action" :{
            "index":0,
            "tbl_name": "default_action",
            "table":{
                "PRIORITY":0,
                "VERSION0":0,
                "VERSION1":0,
                "VERSION2":0,
                "VERSION3":0,
                "VER_GROUP0":0,
                "VER_GROUP1":0,
                "VER_GROUP2":0,
                "VER_GROUP3":0,
                "RANG_INDEX0":0,
                "RANG_INDEX1":0,
                "STATS_SAME_IDX":0,
                "STATISTICS":0,
                "CMD_QUEUE_ID":0,
                "AGE_MOD":0,
                "ECMP_ENABLE":0,
                "ECMP_ENTRY_NUM":0,
                "TSE_RSV":0,
                "EX_RESULT_INDEX":0,
                "TSE_EXT_RESULT_LEN":0,
                "PIPE_EXT_RESULT_LEN":0,
                "OPCODE":0,
                "KEYBUILD_PROFILE_ID":0,
                "STORAGE_READ":0,
                "GROUP_STATS_INDEX":0,
                "MEP_DISTRI_PROF":0,
                "MEP_DISPATCH_TYPE":0,
                "SOURCE_TABLE":0,
                "SET_TC_ENABLE":0,
                "SET_TC_VALUE":0,
                "DESTINATION_VALID":1,
                "ACTION_TYPE":0,
                "DESTINATION":128,
                "DECAPSULATION":0,
                "MIRROR_PRI":0,
                "MIRROR_METER_INDEX":0,
                "MIRRORING":0,
                "EXT_BIT_MAP":0,
                "METER_NUM":0,
                "METADATA_UPDATE":0,
                "REPLACE_L4_DPORT":0,
                "REPLACE_L4_SPORT":0,
                "REPLACE_DIPV4":0,
                "REPLACE_SIPV4":0,
                "REPLACE_DIPV6":0,
                "REPLACE_SIPV6":0,
                "TTL_UPDATE":0,
                "TOS_UPDATE":0,
                "REMOVE_OUTER_VLAN":0,
                "REMOVE_INNER_VLAN":0,
                "REPLACE_INNER_VLAN":0,
                "REPLACE_OUTER_VLAN":0,
                "REPLACE_SMAC":0,
                "REPLACE_DMAC":0,
                "DEC_NSH_TTL":0,
                "INT_TUNNEL_DELETE":0,
                "UPDATE_FIELD":0,
                "TUNNEL_ENCAP_TYPE":0,
                "TUNNEL_ENCAP_LEN":0,
                "L4_ENCAP_TYPE":0,
                "L3_ENCAP_TYPE":0,
                "VTAG_TYPE":0,
                "L2_FLAG":0,
                "ECN_INHERIT_TO_INNER":0,
                "ECN_INHERIT_TO_OUTER":0,
                "data":[]
            }
        },
        "classify" : {
            "tbl_name": "classify",
            "tbl_id": 0,
            "tbl_pipe": 0,
            "priority": 0,
            "key": {
                "CLASSIFY1_PKT_TYPE": 0,
                "CLASSIFY1_PKT_ERROR_FLAG": 0,
                "CLASSIFY1_PKT_ERROR_TYPE": 0,
                "CLASSIFY1_GROUP_INDEX": 0,
                "CLASSIFY1_OUT_TUNNEL_TYPE": 0,
                "CLASSIFY1_OUT_L5P5_HEAD_TYPE": 0,
                "CLASSIFY1_INNER_TUNNEL_TYPE": 0,
                "CLASSIFY1_INNER_L5P5_HEAD_TYPE": 0,
                "CLASSIFY1_TUNNEL_ID": 0,
                "CLASSIFY1_ADDRESS0": 0,
                "CLASSIFY1_ADDRESS1": 0,
                "CLASSIFY1_ADDRESS_EXTEND": 0,
                "CLASSIFY1_OUT_VLAN_VALID": 0,
                "CLASSIFY1_INNER_VLAN_VALID": 0,
                "CLASSIFY1_OUT_VLAN_ID": 0,
                "CLASSIFY1_OUT_VLAN_TPID": 0,
                "CLASSIFY1_INNER_VLAN_ID": 0,
                "CLASSIFY1_INNER_VLAN_TPID": 0,
                "CLASSIFY1_ETH_TYPE": 0,
                "CLASSIFY1_RSV1": 0,
                "CLASSIFY1_RSV2": 0,
                "CLASSIFY1_PIPE_ID": 0
            },
            "mask": {
                "CLASSIFY1_PKT_TYPE": 0,
                "CLASSIFY1_PKT_ERROR_FLAG": 0,
                "CLASSIFY1_PKT_ERROR_TYPE": 0,
                "CLASSIFY1_GROUP_INDEX": 0,
                "CLASSIFY1_OUT_TUNNEL_TYPE": 0,
                "CLASSIFY1_OUT_L5P5_HEAD_TYPE": 0,
                "CLASSIFY1_INNER_TUNNEL_TYPE": 0,
                "CLASSIFY1_INNER_L5P5_HEAD_TYPE": 0,
                "CLASSIFY1_TUNNEL_ID": 0,
                "CLASSIFY1_ADDRESS0": 0,
                "CLASSIFY1_ADDRESS1": 0,
                "CLASSIFY1_ADDRESS_EXTEND": 0,
                "CLASSIFY1_OUT_VLAN_VALID": 0,
                "CLASSIFY1_INNER_VLAN_VALID": 0,
                "CLASSIFY1_OUT_VLAN_ID": 0,
                "CLASSIFY1_OUT_VLAN_TPID": 0,
                "CLASSIFY1_INNER_VLAN_ID": 0,
                "CLASSIFY1_INNER_VLAN_TPID": 0,
                "CLASSIFY1_ETH_TYPE": 0,
                "CLASSIFY1_RSV1": 0,
                "CLASSIFY1_RSV2": 0,
                "CLASSIFY1_PIPE_ID": 0
            }, "table":
            {
                "CLASSIFY1_OPRATE_CODE": 0,
                "CLASSIFY1_DEFAULT_ACTION_INDEX": 0,
                "CLASSIFY1_KEY_BUILD_PROFILE_ID": 0,
                "CLASSIFY1_DISTRIBUTE_MODE": 0,
                "CLASSIFY1_DISPATCH_TYPE": 0,
                "CLASSIFY1_DEFAULT_DEST_VALID": 0,
                "CLASSIFY1_DEFAULT_DEST_ACT_TYPE": 0,
                "CLASSIFY1_DEFAULT_DEST": 0,
                "CLASSIFY1_RESET_TC_FLAG": 0,
                "CLASSIFY1_TC_VALUE": 0
            }
        },
        "profile" : {
            "tbl_name": "profile",
            "tbl_id": 0,
            "tbl_pipe": 0,
            "priority": 0,
            "key": {
                "PROFILE_GROUP_INDEX": 0,
                "PROFILE_KEY_BUILD_PROFILE_ID": 0,
                "PROFILE_L4_DST_PORT": 0,
                "PROFILE_L4_IS_TCPUDP": 0,
                "PROFILE_L4_HD_TYPE": 0,
                "PROFILE_L4_HD_VALID": 0,
                "PROFILE_L3P5_HD_TYPE": 0,
                "PROFILE_L3P5_VALID": 0,
                "PROFILE_L3_IS_IP": 0,
                "PROFILE_L3_HD_TYPE": 0,
                "PROFILE_L3_HD_VALID": 0,
                "PROFILE_L2P5_SUBTYPE": 0,
                "PROFILE_L2P5_HD_TYPE": 0,
                "PROFILE_L2P5_HD_VALID": 0,
                "PROFILE_INNER_VLAN_TAG": 0,
                "PROFILE_OUT_VLAN_TAG": 0,
                "PROFILE_MAC_TYPE": 0,
                "PROFILE_L2_HD_VALID": 0,
                "PROFILE_TL_L5P5_HD_TYPE": 0,
                "PROFILE_TL_L5P5_HD_VALID": 0,
                "PROFILE_TL_TUNNEL_FLAGS": 0,
                "PROFILE_TL_TUNNEL_TYPE": 0,
                "PROFILE_TL_TUNNEL_VALID": 0,
                "PROFILE_TL_L4_IS_TCPUDP": 0,
                "PROFILE_TL_L4_HD_TYPE": 0,
                "PROFILE_TL_L4_HD_VALID": 0,
                "PROFILE_TL_L3P5_HD_TYPE": 0,
                "PROFILE_TL_L3P5_VALID": 0,
                "PROFILE_TL_L3_IS_IP": 0,
                "PROFILE_TL_L3_HD_TYPE": 0,
                "PROFILE_TL_L3_HD_VALID": 0,
                "PROFILE_TL_L2P5_SUBTYPE": 0,
                "PROFILE_TL_L2P5_HD_TYPE": 0,
                "PROFILE_TL_L2P5_HD_VALID": 0,
                "PROFILE_TL_INNER_VLAN_TAG": 0,
                "PROFILE_TL_OUT_VLAN_TAG": 0,
                "PROFILE_TL_MAC_TYPE": 0,
                "PROFILE_TL_L2_HD_VALID": 0,
                "PROFILE_OT_L5P5_HD_TYPE": 0,
                "PROFILE_OT_L5P5_HD_VALID": 0,
                "PROFILE_OT_TUNNEL_FLAGS": 0,
                "PROFILE_OT_TUNNEL_TYPE": 0,
                "PROFILE_OT_TUNNEL_VALID": 0,
                "PROFILE_OT_L4_IS_TCPUDP": 0,
                "PROFILE_OT_L4_HD_TYPE": 0,
                "PROFILE_OT_L4_HD_VALID": 0,
                "PROFILE_OT_L3P5_HD_TYPE": 0,
                "PROFILE_OT_L3P5_VALID": 0,
                "PROFILE_OT_L3_IS_IP": 0,
                "PROFILE_OT_L3_HD_TYPE": 0,
                "PROFILE_OT_L3_HD_VALID": 0,
                "PROFILE_OT_L2P5_SUBTYPE": 0,
                "PROFILE_OT_L2P5_HD_TYPE": 0,
                "PROFILE_OT_L2P5_HD_VALID": 0,
                "PROFILE_OT_INNER_VLAN_TAG": 0,
                "PROFILE_OT_OUT_VLAN_TAG": 0,
                "PROFILE_OT_MAC_TYPE": 0,
                "PROFILE_OT_L2_HD_VALID": 0,
                "PROFILE_RSV": 0,
                "PROFILE_PIPE_ID": 0
            },
            "mask": {
                "PROFILE_GROUP_INDEX": 0,
                "PROFILE_KEY_BUILD_PROFILE_ID": 0,
                "PROFILE_L4_DST_PORT": 0,
                "PROFILE_L4_IS_TCPUDP": 0,
                "PROFILE_L4_HD_TYPE": 0,
                "PROFILE_L4_HD_VALID": 0,
                "PROFILE_L3P5_HD_TYPE": 0,
                "PROFILE_L3P5_VALID": 0,
                "PROFILE_L3_IS_IP": 0,
                "PROFILE_L3_HD_TYPE": 0,
                "PROFILE_L3_HD_VALID": 0,
                "PROFILE_L2P5_SUBTYPE": 0,
                "PROFILE_L2P5_HD_TYPE": 0,
                "PROFILE_L2P5_HD_VALID": 0,
                "PROFILE_INNER_VLAN_TAG": 0,
                "PROFILE_OUT_VLAN_TAG": 0,
                "PROFILE_MAC_TYPE": 0,
                "PROFILE_L2_HD_VALID": 0,
                "PROFILE_TL_L5P5_HD_TYPE": 0,
                "PROFILE_TL_L5P5_HD_VALID": 0,
                "PROFILE_TL_TUNNEL_FLAGS": 0,
                "PROFILE_TL_TUNNEL_TYPE": 0,
                "PROFILE_TL_TUNNEL_VALID": 0,
                "PROFILE_TL_L4_IS_TCPUDP": 0,
                "PROFILE_TL_L4_HD_TYPE": 0,
                "PROFILE_TL_L4_HD_VALID": 0,
                "PROFILE_TL_L3P5_HD_TYPE": 0,
                "PROFILE_TL_L3P5_VALID": 0,
                "PROFILE_TL_L3_IS_IP": 0,
                "PROFILE_TL_L3_HD_TYPE": 0,
                "PROFILE_TL_L3_HD_VALID": 0,
                "PROFILE_TL_L2P5_SUBTYPE": 0,
                "PROFILE_TL_L2P5_HD_TYPE": 0,
                "PROFILE_TL_L2P5_HD_VALID": 0,
                "PROFILE_TL_INNER_VLAN_TAG": 0,
                "PROFILE_TL_OUT_VLAN_TAG": 0,
                "PROFILE_TL_MAC_TYPE": 0,
                "PROFILE_TL_L2_HD_VALID": 0,
                "PROFILE_OT_L5P5_HD_TYPE": 0,
                "PROFILE_OT_L5P5_HD_VALID": 0,
                "PROFILE_OT_TUNNEL_FLAGS": 0,
                "PROFILE_OT_TUNNEL_TYPE": 0,
                "PROFILE_OT_TUNNEL_VALID": 0,
                "PROFILE_OT_L4_IS_TCPUDP": 0,
                "PROFILE_OT_L4_HD_TYPE": 0,
                "PROFILE_OT_L4_HD_VALID": 0,
                "PROFILE_OT_L3P5_HD_TYPE": 0,
                "PROFILE_OT_L3P5_VALID": 0,
                "PROFILE_OT_L3_IS_IP": 0,
                "PROFILE_OT_L3_HD_TYPE": 0,
                "PROFILE_OT_L3_HD_VALID": 0,
                "PROFILE_OT_L2P5_SUBTYPE": 0,
                "PROFILE_OT_L2P5_HD_TYPE": 0,
                "PROFILE_OT_L2P5_HD_VALID": 0,
                "PROFILE_OT_INNER_VLAN_TAG": 0,
                "PROFILE_OT_OUT_VLAN_TAG": 0,
                "PROFILE_OT_MAC_TYPE": 0,
                "PROFILE_OT_L2_HD_VALID": 0,
                "PROFILE_RSV": 0,
                "PROFILE_PIPE_ID": 0
            },
            "table": {
                "PROFILE_KEY_BUILD_OP_CODE": 4,
                "PROFILE_DEF_ACT_IDX": 0,
                "PROFILE_MEP_DSTR_PROF": 0,
                "PROFILE_MEP_DSPATCH_TYPE": 0,
                "PROFILE_DEFAULT_DEST_VALID": 0,
                "PROFILE_ACT_TYPE": 0,
                "PROFILE_DEFAULT_DEST": 0,
                "PROFILE_EM_LK_ENABLE": 0,
                "PROFILE_EM_LK_PROF_ID": 0,
                "PROFILE_EM_LK_KEY_ID": 0,
                "PROFILE_EM_TBL_ID": 0,
                "PROFILE_EM_KEY_LEN": 0,
                "PROFILE_WC_LK_ENABLE": 0,
                "PROFILE_WC_LK_PROF_ID": 0,
                "PROFILE_WC_LK_KEY_ID": 0,
                "PROFILE_WC_KEY_LEN": 0,
                "PROFILE_SET_TC_ENABLE": 0,
                "PROFILE_SET_TC_VALUE": 0,
                "PROFILE_EM_TCP_FLAG_POLICY": 0
            }
        },
        "register" : {
            "tbl_name": "register",
            "tbl_pipe": 0,
            "key": {
                "REG_TYPE": 0,
                "REG_ID": 0
            },
            "table": {
                "REG_VALUE": 0
            }
        },
        "key_mask" : {
            "tbl_name": "key_mask",
            "tbl_pipe": 0,
            "key": {
                "KEY_MASK_INDEX": 1
            },
            "table": {
                "KEY_MASK1_L": 0,
                "KEY_MASK1_H": 0,
                "KEY_MASK2_L": 0,
                "KEY_MASK2_H": 0,
                "KEY_MASK3_L": 0,
                "KEY_MASK3_H": 0,
                "KEY_MASK4_L": 0,
                "KEY_MASK4_H": 0,
                "KEY_MASK5_L": 0,
                "KEY_MASK5_H": 0,
                "KEY_MASK6_L": 0,
                "KEY_MASK6_H": 0,
                "KEY_MASK7_L": 0,
                "KEY_MASK7_H": 0,
                "KEY_MASK8_L": 0,
                "KEY_MASK8_H": 0,
                "KEY_MASK9_L": 0,
                "KEY_MASK9_H": 0,
                "KEY_MASK10_L": 0,
                "KEY_MASK10_H": 0,
                "KEY_MASK11_L": 0,
                "KEY_MASK11_H": 0,
                "KEY_MASK12_L": 0,
                "KEY_MASK12_H": 0
            }
        },
        "key_template" : {
            "tbl_name": "key_template",
            "tbl_id": 0,
            "tbl_pipe": 0,
            "key": {
                "KEY_TEMPLATE_INDEX": 12
            },
            "table": {
                "KEY_TEMPLATE_KEY_PROF_ID": 0,
                "KEY_TEMPLATE_GROUP_IDX": 0,
                "KEY_TEMPLATE_VNIC_ID": 0,
                "KEY_TEMPLATE_META_DATA": 0,
                "KEY_TEMPLATE_MAC_PORT_ENABLE": 0,
                "KEY_TEMPLATE_OT_L2_DMAC": 0,
                "KEY_TEMPLATE_OT_L2_SMAC": 0,
                "KEY_TEMPLATE_OT_L2_OUT_VLAN_TPID": 0,
                "KEY_TEMPLATE_OT_L2_OUT_VLAN_PRI": 0,
                "KEY_TEMPLATE_OT_L2_OUT_VLAN_DE": 0,
                "KEY_TEMPLATE_OT_L2_OUT_VLAN_VID": 0,
                "KEY_TEMPLATE_OT_L2_INNER_VLAN_TPID": 0,
                "KEY_TEMPLATE_OT_L2_INNER_VLAN_PRI": 0,
                "KEY_TEMPLATE_OT_L2_INNER_VLAN_DE": 0,
                "KEY_TEMPLATE_OT_L2_INNER_VLAN_VID": 0,
                "KEY_TEMPLATE_OT_L3_TYPE": 0,
                "KEY_TEMPLATE_OT_L3_SIP": 0,
                "KEY_TEMPLATE_OT_L3_DIP": 0,
                "KEY_TEMPLATE_OT_L3_PROT": 0,
                "KEY_TEMPLATE_OT_L3_TTL": 0,
                "KEY_TEMPLATE_OT_L3_TOS": 0,
                "KEY_TEMPLATE_OT_L3_FLOW": 0,
                "KEY_TEMPLATE_OT_L3_FRAG": 0,
                "KEY_TEMPLATE_OT_L3_EXT_HD_VALID": 0,
                "KEY_TEMPLATE_OT_L4_SPORT1": 0,
                "KEY_TEMPLATE_OT_L4_SPORT2": 0,
                "KEY_TEMPLATE_OT_L4_DPORT": 0,
                "KEY_TEMPLATE_OT_L4_FLAGS": 0,
                "KEY_TEMPLATE_OT_TUNNEL_TYPE": 0,
                "KEY_TEMPLATE_OT_TUNNEL_ID": 0,
                "KEY_TEMPLATE_OT_TUNNEL_FLAGS": 0,
                "KEY_TEMPLATE_OT_L5P5_NSH_FLAGS": 0,
                "KEY_TEMPLATE_OT_L5P5_NSH_TTL": 0,
                "KEY_TEMPLATE_OT_L5P5_NSH_LEN": 0,
                "KEY_TEMPLATE_OT_L5P5_NSH_MD_TYPE": 0,
                "KEY_TEMPLATE_OT_L5P5_NSH_NEXT_PROT": 0,
                "KEY_TEMPLATE_OT_L5P5_NSH_SPI": 0,
                "KEY_TEMPLATE_OT_L5P5_NSH_SI": 0,
                "KEY_TEMPLATE_TL_L2_DMAC": 0,
                "KEY_TEMPLATE_TL_L2_SMAC": 0,
                "KEY_TEMPLATE_TL_L2_OUT_VLAN_TPID": 0,
                "KEY_TEMPLATE_TL_L2_OUT_VLAN_PRI": 0,
                "KEY_TEMPLATE_TL_L2_OUT_VLAN_DE": 0,
                "KEY_TEMPLATE_TL_L2_OUT_VLAN_VID": 0,
                "KEY_TEMPLATE_TL_L2_INNER_VLAN_TPID": 0,
                "KEY_TEMPLATE_TL_L2_INNER_VLAN_PRI": 0,
                "KEY_TEMPLATE_TL_L2_INNER_VLAN_DE": 0,
                "KEY_TEMPLATE_TL_L2_INNER_VLAN_VID": 0,
                "KEY_TEMPLATE_TL_L3_TYPE": 0,
                "KEY_TEMPLATE_TL_L3_SIP": 0,
                "KEY_TEMPLATE_TL_L3_DIP": 0,
                "KEY_TEMPLATE_TL_L3_PROT": 0,
                "KEY_TEMPLATE_TL_L3_TTL": 0,
                "KEY_TEMPLATE_TL_L3_TOS": 0,
                "KEY_TEMPLATE_TL_L3_FLOW": 0,
                "KEY_TEMPLATE_TL_L3_FRAG": 0,
                "KEY_TEMPLATE_TL_L3_EXT_HD_VALID": 0,
                "KEY_TEMPLATE_TL_L4_SPORT1": 0,
                "KEY_TEMPLATE_TL_L4_SPORT2": 0,
                "KEY_TEMPLATE_TL_L4_DPORT": 0,
                "KEY_TEMPLATE_TL_L4_FLAGS": 0,
                "KEY_TEMPLATE_TL_TUNNEL_TYPE": 0,
                "KEY_TEMPLATE_TL_TUNNEL_ID": 0,
                "KEY_TEMPLATE_TL_TUNNEL_FLAGS": 0,
                "KEY_TEMPLATE_TL_L5P5_NSH_FLAGS": 0,
                "KEY_TEMPLATE_TL_L5P5_NSH_TTL": 0,
                "KEY_TEMPLATE_TL_L5P5_NSH_LEN": 0,
                "KEY_TEMPLATE_TL_L5P5_NSH_MD_TYPE": 0,
                "KEY_TEMPLATE_TL_L5P5_NSH_NEXT_PROT": 0,
                "KEY_TEMPLATE_TL_L5P5_NSH_SPI": 0,
                "KEY_TEMPLATE_TL_L5P5_NSH_SI": 0,
                "KEY_TEMPLATE_L2_DMAC": 0,
                "KEY_TEMPLATE_L2_SMAC": 0,
                "KEY_TEMPLATE_L2_OUT_VLAN_TPID": 0,
                "KEY_TEMPLATE_L2_OUT_VLAN_PRI": 0,
                "KEY_TEMPLATE_L2_OUT_VLAN_DE": 0,
                "KEY_TEMPLATE_L2_OUT_VLAN_VID": 0,
                "KEY_TEMPLATE_L2_INNER_VLAN_TPID": 0,
                "KEY_TEMPLATE_L2_INNER_VLAN_PRI": 0,
                "KEY_TEMPLATE_L2_INNER_VLAN_DE": 0,
                "KEY_TEMPLATE_L2_INNER_VLAN_VID": 0,
                "KEY_TEMPLATE_L3_TYPE": 0,
                "KEY_TEMPLATE_L3_SIP": 0,
                "KEY_TEMPLATE_L3_DIP": 0,
                "KEY_TEMPLATE_L3_PROT": 0,
                "KEY_TEMPLATE_L3_TTL": 0,
                "KEY_TEMPLATE_L3_TOS": 0,
                "KEY_TEMPLATE_L3_FLOW": 0,
                "KEY_TEMPLATE_L3_FRAG": 0,
                "KEY_TEMPLATE_L3_EXT_HD_VALID": 0,
                "KEY_TEMPLATE_L4_SPORT1": 0,
                "KEY_TEMPLATE_L4_SPORT2": 0,
                "KEY_TEMPLATE_L4_DPORT": 0,
                "KEY_TEMPLATE_L4_FLAGS": 0,
                "KEY_TEMPLATE_UDF0_EN": 0,
                "KEY_TEMPLATE_UDF0_SEL": 0,
                "KEY_TEMPLATE_UDF1_EN": 0,
                "KEY_TEMPLATE_UDF1_SEL": 0,
                "KEY_TEMPLATE_UDF2_EN": 0,
                "KEY_TEMPLATE_UDF2_SEL": 0,
                "KEY_TEMPLATE_UDF3_EN": 0,
                "KEY_TEMPLATE_UDF3_SEL": 0,
                "KEY_TEMPLATE_UDF4_EN": 0,
                "KEY_TEMPLATE_UDF4_SEL": 0,
                "KEY_TEMPLATE_UDF5_EN": 0,
                "KEY_TEMPLATE_UDF5_SEL": 0,
                "KEY_TEMPLATE_UDF6_EN": 0,
                "KEY_TEMPLATE_UDF6_SEL": 0,
                "KEY_TEMPLATE_UDF7_EN": 0,
                "KEY_TEMPLATE_UDF7_SEL": 0,
                "KEY_TEMPLATE_RANGE_CHECK_TYPE0": 0,
                "KEY_TEMPLATE_RANGE_CHECK_TYPE1": 0
            }
        },
        "em_table" : {
            "tbl_name":"em_table",
            "tbl_id": 0,
            "key_len": 0,
            "key": None,
            "table":{
                "PRIORITY":  0,
                "VERSION0":  0,
                "VERSION1":  0,
                "VERSION2":  0,
                "VERSION3":  0,
                "VER_GROUP0":  0,
                "VER_GROUP1":  0,
                "VER_GROUP2":  0,
                "VER_GROUP3":  0,
                "RANG_INDEX0":  0,
                "RANG_INDEX1":  0,
                "STATS_SAME_IDX":  0,
                "STATISTICS":  0,
                "CMD_QUEUE_ID":  0,
                "AGE_MOD":  0,
                "ECMP_ENABLE":  0,
                "ECMP_ENTRY_NUM":  0,
                "TSE_RSV":  0,
                "EX_RESULT_INDEX":  0,
                "TSE_EXT_RESULT_LEN":  0,
                "PIPE_EXT_RESULT_LEN":  0,
                "OPCODE":  0,
                "KEYBUILD_PROFILE_ID":  0,
                "STORAGE_READ":  0,
                "GROUP_STATS_INDEX":  0,
                "MEP_DISTRI_PROF":  0,
                "MEP_DISPATCH_TYPE":  0,
                "SOURCE_TABLE":  4,
                "SET_TC_ENABLE":  0,
                "SET_TC_VALUE":  0,
                "DESTINATION_VALID":  0,
                "ACTION_TYPE":  0,
                "DESTINATION":  0,
                "DECAPSULATION":  0,
                "MIRROR_PRI":  0,
                "MIRROR_METER_INDEX":  0,
                "MIRRORING":  0,
                "EXT_BIT_MAP":  0,
                "METER_NUM":  0,
                "METADATA_UPDATE":  0,
                "REPLACE_L4_DPORT":  0,
                "REPLACE_L4_SPORT":  0,
                "REPLACE_DIPV4":  0,
                "REPLACE_SIPV4":  0,
                "REPLACE_DIPV6":  0,
                "REPLACE_SIPV6":  0,
                "TTL_UPDATE":  0,
                "TOS_UPDATE":  0,
                "REMOVE_OUTER_VLAN":  0,
                "REMOVE_INNER_VLAN":  0,
                "REPLACE_INNER_VLAN":  0,
                "REPLACE_OUTER_VLAN":  0,
                "REPLACE_SMAC":  0,
                "REPLACE_DMAC":  0,
                "DEC_NSH_TTL":  0,
                "INT_TUNNEL_DELETE":  0,
                "UPDATE_FIELD":  0,
                "TUNNEL_ENCAP_TYPE":  0,
                "TUNNEL_ENCAP_LEN":  0,
                "L4_ENCAP_TYPE":  0,
                "L3_ENCAP_TYPE":  0,
                "VTAG_TYPE":  0,
                "L2_FLAG":  0,
                "ECN_INHERIT_TO_INNER":  0,
                "ECN_INHERIT_TO_OUTER":  0,
                "RSV":  0,
                "data":[]
            }
        },
        'tunnel_encap':
        {
            "tbl_name": "tunnel_encap",
            "key": {
                "TUNNEL_ENCAP_INDEX":0
            },
                "table":{
                        "TUNNEL_ENCAP_V4_ID":0,
                        "TUNNEL_ENCAP_SRC_MAC":0,
                        "TUNNEL_ENCAP_VLAN":0,
                        "TUNNEL_ENCAP_DST_MAC":0,
                        "TUNNEL_ENCAP_V6_TC":0,
                        "TUNNEL_ENCAP_V6_HL":0,
                        "TUNNEL_ENCAP_V4_TOS":0,
                        "TUNNEL_ENCAP_V4_TTL":0
                }
        },
        'source_mode1' :
        {
            "tbl_name": "source_mode1",
            "key": {
                "SOURCE_MODE1_INDEX":0
            },
            "table":{
            "SOURCE_MODE1_SRC_MAC":0,
            "SOURCE_MODE1_IPV4_ADDR":0
            }
        },
        'source_mode2' :
        {
            "tbl_name": "source_mode2",
            "key": {
                "SOURCE_MODE2_INDEX":0
            },
            "table":{
            "SOURCE_MODE2_SRC_MAC":0,
            "SOURCE_MODE2_IPV6_ADDR1": 0,
            "SOURCE_MODE2_IPV6_ADDR2": 0,
            "SOURCE_MODE2_IPV6_ADDR3": 0,
            "SOURCE_MODE2_IPV6_ADDR4": 0
            }
        }        
    }
    
    mask_template_id = 0
    
    def __init__(self):
        pass

    def ipv62int2(ip):
        ''' Convert ipv6 to 2 numbers, 8 bytes each'''
        ip = inet_pton(socket.AF_INET6, ip)
        a, b,c,d =  struct.unpack("!IIII", ip)
        #return a<<16 | b, c<<16 | d
        #return a<<16 | (b & 0xffff0000), (b & 0x0000ffff)<<32 | c, d
        return a, b << 16 | ((c>>16) & 0xffff), (c & 0x0000ffff)<<32 | d

    def int2ipv62(a):
        ''' Convert the two 8bytes numbers to IPv6 human readable string '''
        #return socket.inet_ntop(socket.AF_INET6, int.to_bytes(a,16,'big'))
        #a = a[::-1]
        return socket.inet_ntop(socket.AF_INET6, a)

    def getvlantpid(vlantype):
        if vlantype == 0:
            return 0
        tpid = {
            '0x88a8'     : 0,
            '0x8100'     : 1,
            '0x9100'     : 2,
            '0x9200'     : 3,
            '0x9300'     : 4,
        }
        if str(hex(vlantype)) not in tpid:
            return 0
        return tpid[str(hex(vlantype))]

    @staticmethod	
    def parsePktIpFragment(pkt):
        #IP分片不在不是first
        layername = pkt.name
        chkhead = pkt
        while layername != 'NoPayload':
            if layername == 'IP' and chkhead[IP].frag != 0:            
                chkhead[IP].remove_payload()
            chkhead =  chkhead.payload
            layername = chkhead.name  
        return pkt 

    @staticmethod
    def value_check(k,v,default=1):
        if 'ip' in k.lower() and type(v) == str:
            if '.' in v: return ip2int(v)
            if ':' in v: return inet_pton(socket.AF_INET6, v)
        if 'mac' in k.lower() and type(v) == str:
            if ':' in v: return mac2int(v)
        if type(default) == int:
            if type(v) == str:
                if '0x' in v : return int(v,16)
                if '0b' in v : return int(v,2)
            return int(v)
        return v

    @staticmethod
    def table_check(config,default_json,simplify=False):
        if 'group' in config:
            for i in config['group']:
                corsica_dpe.table_check(i,default_json,simplify)
            return config

        if simplify:
            for k,v in default_json.items():
                if isinstance(v,dict):
                    config.setdefault(k,dict())
                    for k1,v1 in v.items():
                        if k1 in config[k] and config[k][k1] != 0 :
                            config[k].pop(k1)
            config.pop('tbl_name',None)
        else :
            config['tbl_name'] = default_json['tbl_name']
            for k,v in default_json.items():
                config.setdefault(k,v)
                config[k] = corsica_dpe.value_check(k,config[k],v)
                if isinstance(v,dict):
                    config.setdefault(k,dict())
                    for k1,v1 in v.items():
                        config[k].setdefault(k1,v1)
                        config[k][k1] = corsica_dpe.value_check(k1,config[k][k1],v1)
        return config

    @staticmethod
    def corsica_config_check(config,simplify=False):
        if 'tbl_name' in config:
            k = config['tbl_name']
            v = config
            if k == "input_port_rx":
                config = corsica_dpe.input_port_rx_check(v,simplify)
            elif k == "default_action":
                config = corsica_dpe.default_action_check(v,simplify)
            elif k == "classify":
                config = corsica_dpe.classify_check(v,simplify)
            elif k == 'register':
                config = corsica_dpe.register_check(v,simplify)
            elif k == 'profile':
                config = corsica_dpe.profile_check(v,simplify)
            elif k == 'key_mask':
                config = corsica_dpe.key_mask_check(v,simplify)
            elif k == 'key_template':
                config = corsica_dpe.key_template_check(v,simplify)
            elif k == 'em_table':
                config = corsica_dpe.em_check(v,simplify)
            elif k == 'source_mode1':
                config = corsica_dpe.source_mode1_check(v,simplify)
            elif k == 'source_mode2':
                config = corsica_dpe.source_mode2_check(v,simplify)
            elif k == 'tunnel_encap':
                config = corsica_dpe.tunnel_encap_check(v,simplify)
            else :
                config = corsica_dpe.table_common_check(v,k,simplify)
            return config

        for k,v in config.items():
            if k == "input_port_rx":
                config[k] = corsica_dpe.input_port_rx_check(v,simplify)
            elif k == "default_action":
                config[k] = corsica_dpe.default_action_check(v,simplify)
            elif k == "classify":
                config[k] = corsica_dpe.classify_check(v,simplify)
            elif k == 'register':
                config[k] = corsica_dpe.register_check(v,simplify)
            elif k == 'profile':
                config[k] = corsica_dpe.profile_check(v,simplify)
            elif k == 'key_mask':
                config[k] = corsica_dpe.key_mask_check(v,simplify)
            elif k == 'key_template':
                config[k] = corsica_dpe.key_template_check(v,simplify)
            elif k == 'em_table':
                config[k] = corsica_dpe.em_check(v,simplify)
            elif k == 'source_mode1':
                config[k] = corsica_dpe.source_mode1_check(v,simplify)
            elif k == 'source_mode2':
                config[k] = corsica_dpe.source_mode2_check(v,simplify)
            elif k == 'tunnel_encap':
                config[k] = corsica_dpe.tunnel_encap_check(v,simplify)
            else :
                config[k] = corsica_dpe.table_common_check(k,v,simplify)
        return config

    @staticmethod
    def table_template_get(tablename=None):
        if tablename == None:
            default_json = copy.deepcopy(corsica_dpe.default_json)
        else:
            if tablename not in corsica_dpe.default_json:
                return None
            default_json = copy.deepcopy(corsica_dpe.default_json[tablename])
        return default_json

    @staticmethod
    def table_common_check(tablename,config,simplify=False):
        if tablename not in corsica_dpe.default_json:
            return config
        default_json = corsica_dpe.default_json[tablename]
        config = corsica_dpe.table_check(config,default_json,simplify)
        return config

    @staticmethod
    def input_port_rx_check(config,simplify=False):
        default_json = corsica_dpe.default_json["input_port_rx"]
        config = corsica_dpe.table_check(config,default_json,simplify)
        return config

    @staticmethod
    def default_action_check(config,simplify=False):
        default_json = corsica_dpe.default_json["default_action"]
        if 'table' in config:
            config["table"] = corsica_dpe.createData(config["table"])
        config = corsica_dpe.table_check(config,default_json,simplify)
        return config

    @staticmethod
    def classify_check(config,simplify=False):
        default_json = corsica_dpe.default_json["classify"]
        config = corsica_dpe.table_check(config,default_json,simplify)
        return config
    
    @staticmethod
    def profile_check(config,simplify=False):
        default_json = corsica_dpe.default_json["profile"]
        config = corsica_dpe.table_check(config,default_json,simplify)
        return config

    @staticmethod
    def register_check(config,simplify=False):
        default_json = corsica_dpe.default_json["register"]
        config = corsica_dpe.table_check(config,default_json,simplify)
        return config

    @staticmethod
    def key_mask_check(config,simplify=False):
        default_json = corsica_dpe.default_json["key_mask"]
        keys = default_json['table'].keys()
        if "KEY_MASK" in config['table']:
            k = config['table']["KEY_MASK"]
            for i in range(0,int(len(k)/4)):
                value = int("0x"+k[i*4:(i+1)*4])
                config['table'][keys[i]] = value
        config = corsica_dpe.table_check(config,default_json,simplify)
        return config
		
    @staticmethod
    def key_template_check(config,simplify=False):
        default_json = corsica_dpe.default_json["key_template"]
        config = corsica_dpe.table_check(config,default_json,simplify)
        return config
		
    @staticmethod
    def em_check(config,simplify=False):
        default_json = corsica_dpe.default_json["em_table"]
        if isinstance(config['key'],dict):
            info = config['key']
            keytemp = copy.deepcopy(info)
            for k in keytemp.keys():
                keytemp[k] = 1
            keylen = info.get('keylen',None)
            for k in info:
                info[k] = corsica_dpe.value_check(k,info[k])
            config['key'] = corsica_dpe.getEmKey(None,keytemp,keylen,info)[0]
        if 'table' in config:
            config["table"] = corsica_dpe.createData(config["table"])
        config = corsica_dpe.table_check(config,default_json,simplify)
        return config

    @staticmethod
    def source_mode1_check(config,simplify=False):
        default_json = corsica_dpe.default_json["source_mode1"]
        config = corsica_dpe.table_check(config,default_json,simplify)
        return config
    
    @staticmethod
    def source_mode2_check(config,simplify=False):
        default_json = corsica_dpe.default_json["source_mode2"]
        config = corsica_dpe.table_check(config,default_json,simplify)
        return config
 
    @staticmethod
    def tunnel_encap_check(config,simplify=False):
        default_json = corsica_dpe.default_json["tunnel_encap"]
        config = corsica_dpe.table_check(config,default_json,simplify)
        return config   
    
    @staticmethod
    def saveJson(ijson,filebase='jaguar_json_'):
        now = time.strftime("%m%d%H%M%S")
        filename = filebase+now+str(random.randint(100,999))
        #file = os.path.join(os.getenv('TEMP'),filename+".json")
        file = os.path.join("d:\\json_tmp",filename+".json")
        with open(file,"w") as f:
            json.dump(ijson,f)
        return file
    
    @staticmethod
    def createEncapData(info):
        val = None
        itype = ['notunnel','common','vxlan','geneve','nvgre','gre','v4inv4','v4inv6','vxlan-gpe+nsh','gre+nsh','vxlan-gpe',
                  'l2+nsh','v6inv4','v6inv6','gre-ten']
        type = itype[info[0]]
        #通用隧道头信息
        if type == 'common':
            pass
        #vxlan信息 
        elif type == 'vxlan':
            val = bytes(8)
            val = struct.pack(">II", info[1].flags<<24, info[1].vni<<8)
        elif type == 'geneve':
            if info[1].optionlen == None or info[1].optionlen == 0:
                data0 = info[1].proto
            else:
                data0 = (info[1].optionlen << 24) + info[1].proto

            val = struct.pack(">II", data0, info[1].vni<<8)
            if info[1].optionlen != 0:
               val = val + info[1].options
        elif type == 'gre' or type == 'nvgre': 
            chksum_present = info[1].getfieldval('chksum_present') 
            routing_present = info[1].getfieldval('routing_present') 
            key_present = info[1].getfieldval('key_present') 
            seqnum_present = info[1].getfieldval('seqnum_present')
            data = (chksum_present << 31) + (routing_present << 30) + (key_present << 29) + (seqnum_present << 28) + info[1].proto
            val = data.to_bytes(4,'big',signed=False) 
            if chksum_present:
                data = (info[1].chksum << 16) + info[1].offset
                val += data.to_bytes(4,'big',signed=False) 
            if key_present: 
                data = info[1].key
                val += data.to_bytes(4,'big',signed=False) 
            if seqnum_present:     
                data = info[1].seqence_number
                val += data.to_bytes(4,'big',signed=False) 
        elif type == 'vxlan-gpe':
            val = bytes(8)
            val = struct.pack(">II", (info[1].flags<<24) | info[1].NextProtocol, info[1].vni<<8)

            
        return val 
    
    def createVtagVlanData(info):
        '''
        bitmap_tpid_88a8 = 1
        bitmap_tpid_8100 = 2
        bitmap_tpid_9100 = 4
        bitmap_tpid_9200 = 8
        bitmap_tpid_9300 = 16
        bitmap_tpid_9500 = 32
        '''
        if type(info) == Dot1Q:
            tpid = 2
        pri = info.prio
        cfi = info.id
        vid = info.vlan
        val = struct.pack(">BH", tpid, (pri << 13) + (cfi << 12) +vid) 
        return val       

    @staticmethod
    def createData(config):
        if "data" in config:
            return config
        keylist = [
            ("METADATA_UPDATE",40,''),
            ("REPLACE_L4_DPORT",16,''),
            ("REPLACE_L4_SPORT",16,''),
            ("REPLACE_DIPV4",32,'ip'),
            ("REPLACE_SIPV4",32,'ip'),
            ("REPLACE_DIPV6",128,'ip'),
            ("REPLACE_SIPV6",128,'ip'),
            ("TTL_UPDATE",24,""),
            ("TOS_UPDATE",16,""),
            ("REPLACE_INNER_VLAN",24,''),
            ("REPLACE_OUTER_VLAN",24,''),
            ("REPLACE_SMAC",48,'mac'),
            ("REPLACE_DMAC",48,'mac'),
            ("DEC_NSH_TTL",24,'nt'),
            ("UPDATE_FIELD",32,''),
            ("TUNNEL_ENCAP_TYPE",128,''),
            ("L4_ENCAP_TYPE",32,''),
            ("L3_ENCAP_TYPE",176,''),
            ("VTAG_TYPE",48,''),
            ("L2_FLAG",48,'mac'),
            ("DECAPSULATION",0,''),
        ]
        valuelist = []
        isin = lambda k: int(k in info)
        for k,l,t in keylist:
            if None == config.get(k,None):
                continue
            info = config[k]
            if k not in ['DECAPSULATION','TUNNEL_ENCAP_TYPE', 'L3_ENCAP_TYPE', 'VTAG_TYPE','L2_FLAG']:
                config[k] = 1 #重新设置信息
            val = info
            if type(info) == dict:
                if 'value' in info: config[k] = info
            if "TOS_UPDATE" == k:
                if type(info) == dict:
                    mask = info.get('mask',0)
                    tos = info.get('tos',0)
                    val = struct.pack("BB",mask,tos) #大端
            elif "TTL_UPDATE" == k:
                if type(info) == dict:
                    opcode = info.get('opcode',0)
                    rss = info.get('rss',0)
                    spd = info.get('spd',0)
                    lag = info.get('lag',0)
                    vnic = info.get('vnic',0)
                    queueid=info.get('queueid',0)
                    ttl = info.get('ttl',0)
                    if opcode == 1:
                        val = struct.pack(">BH", opcode<<6, 0)
                    elif opcode == 2:
                        val = struct.pack(">BH", opcode<<6, ttl)                       
                    elif opcode == 0:
                        val = struct.pack(">BH", opcode<<6 + rss <<5 + lag<<4 + vnic>>10, (vnic & 0x3FF) + queueid) #大端
            elif "METADATA_UPDATE" == k: val = info
            elif k in ["REPLACE_OUTER_VLAN","REPLACE_INNER_VLAN"]:
                if type(info) == dict:
                    tpid = corsica_dpe.getvlantpid(info.get('tpid',0))
                    inherit = info.get('inherit',0)
                    pri = info.get('pri',0)
                    cfi = info.get('cfi',0)
                    vid = info.get('vid',0)
                    mask = info.get('mask',(isin('tpid')<<2)+(isin('cfi')<<1)+isin('vid'))
                    val = struct.pack(">BH", (tpid<<5) + (inherit <<3) + mask,
                                     (pri << 13) + (cfi << 12) +vid)
            elif "TUNNEL_ENCAP_TYPE" == k:
                #val = struct.pack("")
                config[k] = info[0]
                #组装封装表
                val = corsica_dpe.createEncapData(info)
                if val != None:
                    config['TUNNEL_ENCAP_LEN'] = len(val)
                    l = len(val) * 8
                else:
                    continue
            elif str(t) == 'ip' and type(info) == str:
                val = corsica_dpe.value_check(k,info)     #小序
            elif str(t) == 'mac' and type(info) == str:
                val = int(re.sub('[^\dabcdefABCDEF]','',info),16)
            elif "L4_ENCAP_TYPE" == k:
                config[k] = info[0]
                val = info[1]
            elif "L3_ENCAP_TYPE" == k:
                if type(info) == list:
                    config[k] = info[0] 
                    #tmp = bytes_encode(raw(info[1]))
                    #tmp = linehexdump(info[1],onlyhex=1,dump=1)             #报文转成bytes  
                    #if info[1].type == IP:

                    if type(info[1]) == IP:
                        #val = bytes(12)
                        #val = tmp[0:8] + tmp[16:20]                             #取96bit，前8+后4,
                        val = bytes(12)
                        data0 = (info[1].version<<28 | 5<<24 | info[1].tos<<16 | info[1].id)  #info[1].len不做检查，这里随机赋值
                        data1 = (info[1].flags<<29 | info[1].frag<<16 | info[1].ttl<<8 | info[1].proto)
                        dip = corsica_dpe.value_check('ip',info[1].dst)
                        val = data0.to_bytes(4,'big',signed=False) + data1.to_bytes(4,'big',signed=False) + dip.to_bytes(4,'big',signed=False)
                        l = 96                           
                    elif type(info[1]) == IPv6:
                        val = bytes(22)
                        tmp = bytes_encode(raw(info[1]))                       
                        val = tmp[0:4] + tmp[6:8] + tmp[24:40]       #取176bit，前8+后4
            elif "VTAG_TYPE" == k:
                config[k] = info[0]
                vlan = info[1]
                val = corsica_dpe.createVtagVlanData(vlan)
                l = 24
        
                if vlan.type == 0x8100:
                    vlan1 = info[1].payload 
                    val += corsica_dpe.createVtagVlanData(vlan1) 
                    l += 24  
            elif "L2_FLAG" == k:  
                if type(info) == list:
                    config[k] = info[0]
                    dmac = info[1].dst
                    val = int(re.sub('[^\dabcdefABCDEF]','',dmac),16)   
            elif "DECAPSULATION" == k:
                  config[k] = info
                  continue
            elif "UPDATE_FIELD" == k:
                #val = struct.pack("")
                config[k] = info[0]
                val = info[1]
            valuelist.append((k,val,l))

        ikeylist =[]
        ilen = 0 ; ikeyb = b""
        #需要在这里处理字符拼接
        for _,x,y in valuelist:
            if type(x) == bytes:   #进来的统一是大字节序
                #x = x[::-1]
                x=x
            else:
                x = x.to_bytes(int(y/8),'big',signed=False)
            ikeyb += x
            ilen += int(y/8)
        ikeyb += bytes(3)
        ikeylist = []
        for i in range(0,ilen,4):
            v = int.from_bytes(ikeyb[i:i+4],'little')   #转换成小字节序
            ikeylist.append(v)
        config['data'] = ikeylist
        return config

    @staticmethod
    def getTypeid(layer=None,itype=None):
        length = {
            'l2' :3,
            'l2p5' : 3,
            'l3':4,
            'l3p5':3,
            'l4':4,
            'tunnel':5,
            'l5p5':3
        }
        typeid = {
            'l2' :{'eth0':0,'eth1':1,'eth2':2},
            'l2p5' : {'mpls':0,'pppoe-discovery':1,'pppoe-session':2},
            'l3':{'ipv4-frag':0,'ipv4-option':1,'ipv4':2,'ipv6-ext':3,'ipv6':4,'arp':5,'rocev1':6},
            'l3p5':{'ifa':0,'ifa2':0},
            'l4':{'icmp':0,'igmp':1,'tcp':2,'udp':3,'icmp6':4,'sctp':5},
            'tunnel':{'notunnel':0,'vxlan':1,'geneve':2,'nvgre':3,'gre':4,'ipinip':5,'vxlan-gpe':6,'gre-tencent':7,'vxlan-ali':8},
            'l5p5':{'nol5.5':0,'nsh':1}
        }
        if layer != None:
            return typeid[layer][itype],length[layer]
        for k,v in typeid.items():
            if itype in v:
                return v[itype],length[k]
        return None,0

    @staticmethod
    def getPktType(itypes=None):
        typeid = {
            'l2' :['eth','eth1','eth2'],
            'l2_vlan' :['vlan','2vlan'],
            'l2p5' : ['mpls','pppoe-discovery','pppoe-session'],
            'l3_ipv4':['ipv4','ipv4-option','ipv4-frag'],
            'l3_ipv6':['ipv6','ipv6-ext'],
            'l3_other':['arp','rocev1'],
            'l3p5':['ifa2'],
            'l4_ipv4':['icmp','igmp','tcp','udp','sctp'],
            'l4_ipv6':['tcp','udp','icmp6','sctp'],
            'tunnel':['notunnel','vxlan','geneve','nvgre','gre','ipinip','vxlan-gpe','gre-tencent','vxlan-ali'],
            'l5p5':['nol5.5','nsh']
            }
        typeid['l3'] = typeid['l3_ipv4'] + typeid['l3_ipv6']
        typeid['l4'] = typeid['l4_ipv4'] + typeid['l4_ipv6']
        if itypes == None:
            return typeid
        return typeid[itypes]

    @staticmethod
    def checkPacket(pkt):
        '''转换报文或短名称标准格式， 转换Scapy描述为报文
        '''
        if isinstance(pkt, Packet):
            return pkt
        if '/' in pkt:  #转换为报文
            its = pkt.split('/')
            pktstr = ""
            for i in its:
                if '(' not in i: i = i+'()'
                pktstr += '/'+i
            pktstr = pktstr.strip('/')
            pkt = eval(pktstr)
            return pkt
        name = pkt
        name = '.' + name.lower() + '.'
        name = name.replace("qinq",'2vlan')
        name = name.replace(".v4",'.ipv4')
        name = name.replace(".v4(",'.ipv4(')
        name = name.replace(".v6",'.ipv6')
        name = name.replace(".v6(",'.ipv6(')
        name = name.replace(".ip.",'.ipv4.')
        name = name.replace(".ip(",'.ipv4(')
        name = name.replace(".mac0.",'.mac.')
        name = name.replace(".mac0(",'.mac(')
        name = name.strip('.')
        return name

    @staticmethod
    def getPacketLong(pkt):
        '''转换报文或短名称为 字符串长名称, 字符已经符合标准
        '''
        pkt = corsica_dpe.checkPacket(pkt)
        if isinstance(pkt, Packet):  #如果是报文，转换为名称
            itype = ""

            for i in pkt.iterpayloads():
                ikey,iarg = None,""
                istr = i.command().split('/')[0]
                t = re.search("(.+)(\(.*\))",istr)
                if t :
                    ikey = t.group(1)
                    iarg = t.group(2)
                if type(i) == Ether:ikey = "eth"
                elif type(i) == IP :
                    ikey = 'ipv4'
                    tmp = IP(raw(i))
                    if tmp.ihl > 5 : ikey = 'ipv4-option'
                    if i.flags & 0x1 : ikey = 'ipv4-frag'
                elif type(i) == Dot1Q : ikey = 'vlan'
                itype += "/"+ikey+iarg
            itype = itype.replace('()','')
            itype = itype.replace("vlan.vlan",'2vlan')
            itype = itype.replace('/','.')
            itype = itype.strip(".").lower()
            return itype

        name = corsica_dpe.checkPacket(pkt)
        name = '.' + name.lower() + '.'
        #不能调用paserPacket
        tun_patten = r'(?:gre|vxlan|geneve|nvgre|gre|vxlan-gpe|gre-tencent|vxlan-ali)(?:\([^()]*\))*\.'
        tuns = re.split(tun_patten,name)
        tuntypes = re.findall(tun_patten,name)
        ret = ""
        for i, v in enumerate(tuntypes):
            if tuns[i].startswith('.ip') :
                tuns[i] = 'eth' + tuns[i]
            elif tuns[i] in ['','.']:
                head = 'eth.ipv4.' if 'gre' in v else 'eth.ipv4.udp.'
                tuns[i] = head
            
            ret += tuns[i]+v
        if tuns[-1] in ['','.'] : tuns[-1] = 'eth.ipv4.udp'
        ret = ret+tuns[-1]
        return ret.strip(".")

    @staticmethod
    def paserPacket(pkt):
        '''分解字符串或Packet类型为 ot tl inner
        Packet 类型分解为Packet类型
        字符串分解为字符串类型
        '''
        ret = dict()
        if pkt == None : return ret
        ret['ot'] = pkt
        ret['tl'] = None
        ret['in'] = None
        ret['ottype'] = None
        ret['tltype'] = None
        ret['tunnel_number'] = 0
        ot    = corsica_dpe.paserPacketFirstLayer(pkt)
        for k,v in ot.items():
            ret['ot_'+k] = v
        ret['ottype'] = ot.get('tuntype',None)
        if ret['ottype'] == None:
            return ret
        ret['tunnel_number'] = 1
        ret['tl'] = ot['last']
        tl    = corsica_dpe.paserPacketFirstLayer(ot['last'])
        for k,v in tl.items():
            ret['tl_'+k] = v
        ret['tltype'] = tl.get('tuntype',None)
        if ret['tltype'] == None:
            return ret
        ret['tunnel_number'] = 2
        ret['in'] = tl['last']
        inner = corsica_dpe.paserPacketFirstLayer(tl['last'])
        for k,v in inner.items():
            ret[k] = v
        return ret

    @staticmethod
    def paserPacketFirstLayer(pkt):
        '''解析首层的协议头
        '''
        ret = dict()
        pkt  = corsica_dpe.checkPacket(pkt)
        pTypeFunc = lambda x: p.command()[:p.command().find('(')]
        if isinstance(pkt,Packet):
            p = pkt
            if type(p) == Ether : 
                ret['l2proto'] = p.type
                ret['l2'] = ret['eth'] = p ; p = p.payload
            if type(p) == Dot1Q :
                ret['l2proto'] = p.type
                ret['vlan'] = p ; p = p.payload
                if type(p) == Dot1Q :
                    ret['l2proto'] = p.type
                    ret['vlan1'] = p ; p = p.payload
            if type(p) == MPLS:
                ret['l2proto'] = p.type #???
                ret['l2p5'] = ret['mpls'] = p ; p = p.payload
            if type(p) == PPPoE:
                ret['l2proto'] = p.type #???
                if 'l2p5' not in ret : ret['l2p5'] = p
                ret['pppoe'] = p ; p = p.payload
            if type(p) in [IP,IPv6,ARP]:
                ret[p.name.lower()] = p
                ret['l3type'] = pTypeFunc(p).lower()
                if type(p) == IP : 
                    ret['ipv4'] = p ; ret['l3type'] = 'ipv4' ; 
                    ret['l3proto'] = p.proto
                    ret['l3ttl'] = p.ttl
                    ret['l3tos'] = p.tos
                    ret['l3flow'] = p.id
                    ret['ipv4fragment'] = p.flags & 0x1
                    ret['ipv4option'] = (IP(raw(p)).ihl > 5)
                elif type(p) == IPv6 : 
                    ret['ipv6'] = p ; ret['l3type']= 'ipv6' ; 
                    ret['l3proto'] = p.nh  #确认是直接取nh
                    ret['l3ttl'] = p.hlim
                    ret['l3tos'] = p.tc
                    ret['l3flow'] = p.fl
                    ret['ipv6ext'] = p.payload.command().startswith("IPv6ExtHdr")
                ret['l3'] = p ; p = p.payload
            if type(p) in [ICMP,TCP,UDP,SCTP] or p.command().startswith("ICMP"):
                ptype = pTypeFunc(p)
                ret[ptype] = p
                if ptype.startswith("ICMPv6"): ret['icmp6'] = p
                if type(p) in [TCP,UDP,SCTP]:
                    if p.sport != None:     #SCTP没有默认端口
                        ret['l4sport1'] = p.sport & 0xff
                        ret['l4sport2'] = p.sport >> 8
                        ret['l4sport'] = p.sport
                    if p.dport != None:
                        ret['l4dport'] = p.dport
                    if type(p) in [TCP]:
                        ret['l4flag'] = p.flags
                else:
                    ret['icmp'] = p
                    ret['l4sport'] = (p.type << 8) | p.code
                    ret['l4sport1'] = p.code
                    ret['l4sport2'] = p.type
                    ret['l4dport'] = 0
                    if p.type in [0,8,13,14,15,16,128,129]:
                        ret['l4dport'] = p.id

                ret['l4type'] = ptype.lower()
                ret['l4'] = p ; p = p.payload
            if type(p) in [VXLAN,GENEVE,GRE]:
                ret['tuntype'] = pTypeFunc(p).lower()
                if type(p) in [VXLAN,GENEVE] :
                    ret['tunid'] = p.vni     
                    if 'l4dport' in ret and ret['l4dport'] ==4790:             
                        ret['tuntype'] = 'vxlan-gpe'
                    if 'l4dport' in ret and ret['l4dport'] == 4799:
                        ret['tuntype'] = 'vxlan-ali'                   
                #GRE固定取0，NVGRE取VSID,GRE-TEN特殊计算
                if type(p) in [GRE] :
                    ret['tunid'] = 0
                    #NVGRE
                    if p.key == 0x7FFFF200:
                        ret['tuntype'] = 'nvgre'
                        ret['tunid'] = p.key >> 8  #取24bit vsid
                    if p.key == 0x2132980A:
                        ret['tuntype'] = 'gre-tencent'
                        ret['tunid'] = p.key                
                    if p.seqence_number == 0x12345678:   #测试seq id使用
                        ret['tunid'] = p.seqence_number
                #ret[ret['tuntype']] = p
                ret['tunnel'] = p ; p = p.payload
            elif (type(p.underlayer) in [IPv6,IP]) and (type(p) in [IPv6,IP]):
                ret['tuntype'] = 'ipinip'
                ret['tunnel'] = p ; p = p.payload
            if isinstance(p,NSH):
                ret['l5p5type'] = 'nsh'
                ret['l5p5'] = ret['nsh'] = p ; p = p.payload
            ret['last'] = p
        else:
            ilist = corsica_dpe.splitName(pkt)
            p = 0
            if ilist[p].startswith('eth'): 
                ret['l2'] = ret['mac'] = ilist[p] ; p += 1
            if len(ilist) > p and ilist[p].startswith('2vlan') :
                ret['vlan1'] = ret['vlan'] = ilist[p] ; p += 1
            if len(ilist) > p and ilist[p].startswith('vlan') :
                ret['vlan'] = ilist[p] ; p += 1
                if len(ilist) > p and ilist[p].startswith('vlan') :
                    ret['vlan1'] = p ; p += 1
            if len(ilist) > p and ilist[p].startswith('mpls'):
                ret['l2p5'] = ret['mpls'] = ilist[p] ; p += 1
            if len(ilist) > p and ilist[p].startswith('pppoe'):
                if 'l2p5' not in ret : ret['l2p5'] = p
                ret['pppoe'] = ilist[p] ; p += 1
            if len(ilist) > p and ilist[p].startswith('ip'):
                if 'ipv6' in ilist[p]: 
                    ret['ipv6'] = ilist[p]
                    ret['l3type'] = 'ipv6'
                else:
                    ret['l3type'] = 'ipv4'
                    ret['ipv4'] = ilist[p]
                ret['l3'] = ilist[p] ; p += 1
            if len(ilist) >p :
                tun = re.search(r'^(tcp|udp|sctp|igmp|icmp6|icmp)',ilist[p])
                if tun:
                    ret[tun.group(1)] = ilist[p]
                    ret['l4type'] = tun.group(1)
                    ret['l4'] = ilist[p] ; p += 1
            if len(ilist) >p :
                tun = re.search(r'^(gre|vxlan|geneve|nvgre|gre|vxlan-gpe|gre-tencent|vxlan-ali|ipinip)',ilist[p])
                if tun:
                    ret['tuntype'] = ilist[p]
                    ret['tunnel'] = ilist[p] ; p += 1
            elif len(ilist) > p and  p > 0 and ilist[p-1].startswith('ip'):
                ret['tuntype'] = 'ipinip'
                ret['tunnel'] = ilist[p] ; p += 1
            if len(ilist) > p and ilist[p].startswith('nsh'):
                ret['l5p5type'] = 'nsh'
                ret['l5p5'] = ret['nsh'] = ilist[p] ; p += 1
            ret['last'] = None
            if len(ilist) > p:
                ret['last'] = '.'.join(ilist[p:])
        return ret

    @staticmethod
    def getPacketHeader(itype,pktlen=0,padlen=0):
        '''转换报文类型（非长名称）为 Packet , 默认不填充
           包含2种类型：
           1、Ether/IP/UDP/GENEVE/IPv6/UDP(dport=4791)/Raw(10*"a")
           2、Eth.IP.UDP
        '''
        itype = corsica_dpe.checkPacket(itype)
        if isinstance(itype,Packet):
            return itype
        
        its = corsica_dpe.splitName(itype)
        pkt = None
        for i,v in enumerate(its):
            args = dict()
            if '(' in v:  #分析参数
                v,args=v.split('(',maxsplit=1)
                args = args.strip(')')
                args = eval(f"dict({args})")  #转换为字典
            if v == 'geneve' : 
                if pkt.lastlayer().name == 'UDP':
                    pkt.lastlayer().sport=random.randint(10000,15000)
                    pkt.lastlayer().dport=6081
                pkt1 =  GENEVE(vni=0x7FFFFD)
            elif v == 'vxlan' : pkt1 = VXLAN(flags=0x8,vni=0x7FFFF1)
            elif v == 'vxlan-gpe' : 
                if pkt.lastlayer().name == 'UDP':
                    pkt.lastlayer().dport=4790                
                pkt1 = VXLAN(flags=0xc,vni=0x7FFFFE) #ipv4 1, ipv6 2 , eth 3 ,nsh 4
            elif v == 'vxlan-ali' : 
                if pkt.lastlayer().name == 'UDP':
                    pkt.lastlayer().dport=4799 
                pkt1 = VXLAN(flags=0x8,vni=0x7FFFF3)
            elif v == 'ipinip' : continue
            elif v == 'gre' :
                pkt1 = GRE(key_present=1,seqnum_present=1,key=0x21329809,seqence_number=0x98765321)
                if 'c' in args:
                    if args['c'] == 0:
                        pkt1.chksum = None  
                    pkt1.chksum_present = args.pop('c')
                     
                if 'k' in args:
                    if args['k'] == 0:
                         pkt1.key = None
                    pkt1.key_present    = args.pop('k')

                if 's' in args:
                    if args['s'] == 0:
                        pkt1.seqence_number = None                    
                    pkt1.seqnum_present = args.pop('s')

                if 'vni' in args: pkt1.key = args.pop('vni')
            elif v == 'nvgre' : pkt1 = GRE(key_present=1,key=0x7FFFF200)
            elif v == 'gre-tencent' : pkt1 = GRE(key_present=1,seqnum_present=1,key=0x2132980A)
            elif v.upper() in scapy.all.__dict__:
                pkt1 = scapy.all.__dict__[v.upper()]()
            elif v == 'noeth' :pkt1 = Raw(load='01234567801234567801234567')
            elif v in ['eth','eth0'] : pkt1 = Ether()
            elif v in ['eth1'] : pkt1 = Ether(dst='ff:ff:ff:ff:ff:ff')
            elif v in ['eth2'] : pkt1 = Ether(dst='01:11:11:11:11:11')
            elif v == 'vlan' : pkt1 = Dot1Q()
            elif v in ['2vlan','qinq'] : pkt1 = Dot1Q()/Dot1Q()
            #elif v in ['ipv4-option']: pkt1 = IP()/IPOption(b'\x01\x01\x01\x00')
            elif v in ['ipv4-option']: pkt1 = IP(dst="48.0.0.1",options=IPOption(b'\x01\x01\x01\x00'))
            elif v in ['ip','ipv4','ipv4-frag'] : pkt1 = IP()
            #elif v in ['ipv4-option']: pkt1 = IP(flags=0x02,options={"vtype": "EXPRESSION", "expr": "[IPOption_SSRR(copy_flag=0, routers=['1.2.3.4', '5.6.7.8'])]"})
            elif v in ['ipv6'] : pkt1 = IPv6()
            elif v in ['ipv6-ext'] : pkt1 = IPv6()/IPv6ExtHdrHopByHop()
            elif v in ['icmp6']: pkt1 = ICMPv6ND_NS(type=135)
            elif v in ['igmp']: pkt1 = IGMP()
            elif v == 'raw' :
                pkt1 = Raw(load=10*'a')
                if 'load' in args: pkt1.load = args.pop('load')
            else:
                raise AssertionError(f"Uknow pkt type : {v}")
            for k1,v1 in args.items():
                if k1 in pkt1.default_fields:
                    pkt1.fields[k1] = v1
                else:
                    raise AssertionError(f"[getPacketHeader]Unknow argument {v}({k1}={v1})")
            pkt = pkt/pkt1 if pkt else pkt1
        if type(pkt.lastlayer()) in [UDP,TCP,IP,IPv6]:
            if padlen > 0:
                pkt = pkt/(int(padlen)*'x')
            elif pktlen > 0 and pktlen-len(pkt) > 0:
                pad = (pktlen-len(pkt))*"x" 
                pkt = pkt/pad
        return pkt
    
    @staticmethod
    def getPacket(itype,pktlen=0,padlen=0):
        '''转换为随机报文，如果已经设置则跳过
        '''
        if itype == None:
            return None
        _dmac   = '00:10:00:00:%02x:%02x'%(random.randint(0,254),random.randint(1,254))
        _smac   = '00:11:27:01:%02x:%02x'%(random.randint(0,254),random.randint(1,254))
        _dmacin = '00:12:94:01:%02x:%02x'%(random.randint(0,254),random.randint(1,254))
        _smacin = '00:13:94:02:%02x:%02x'%(random.randint(0,254),random.randint(1,254))
        _dmac2  = '00:14:94:03:%02x:%02x'%(random.randint(0,254),random.randint(1,254))
        _smac2  = '00:15:94:04:%02x:%02x'%(random.randint(0,254),random.randint(1,254))
        itype = corsica_dpe.checkPacket(itype)
        longname = corsica_dpe.getPacketLong(itype)
        if isinstance(itype,Packet):
            pkt = corsica_dpe.getPacketHeader(itype,pktlen,padlen)
        else:
            pkt = corsica_dpe.getPacketHeader(longname,pktlen,padlen)   
        info = corsica_dpe.paserPacket(pkt)
        ot,tl,inner = info['ot'],info['tl'],info['in']
        isdefault = lambda x,y : x.getfieldval(y) == x.default_fields[y]
        if  ot:
            k = "ot_"
            if isinstance(ot[0],Ether):
                ot[Ether].fields.setdefault('src',_smac)
                ot[Ether].fields.setdefault('dst',_dmac)
            if k+'vlan' in info:
                #ot[Dot1Q].vlan = random.randint(0,4094)
                ot[Dot1Q].fields.setdefault('vlan',random.randint(0,4094))
            if k+'vlan1' in info:
                #ot[Dot1Q].payload[Dot1Q].vlan = random.randint(0,4094)
                ot[Dot1Q].payload[Dot1Q].fields.setdefault('vlan',random.randint(0,4094))
            if k+'ipv4' in info:
                ot[IP].fields.setdefault('src','192.188.%d.%d'%(random.randint(0,250),random.randint(1,250)))
                ot[IP].fields.setdefault('dst','192.188.%d.%d'%(random.randint(0,250),random.randint(1,250)))
            if k+'ipv6' in info:
                ot[IPv6].fields.setdefault('src','192:1::%x:%x'%(random.randint(1,250),random.randint(1,250)))
                ot[IPv6].fields.setdefault('dst','192:2::%x:%x'%(random.randint(1,250),random.randint(1,250)))
            if k+'udp' in info:
                if isdefault(ot[UDP],'sport'):
                    ot[UDP].fields.setdefault('sport',2089)
                if isdefault(ot[UDP],'dport'):
                    ot[UDP].fields.setdefault('dport',10356)
            if k+'tcp' in info:
                if isdefault(ot[TCP],'sport'):
                    ot[TCP].fields.setdefault('sport',2089)
                if isdefault(ot[TCP],'dport'):
                    ot[TCP].fields.setdefault('dport',10356)
        if tl :
            k = "tl_"
            if k+'eth' in info:
                tl[Ether].fields.setdefault('src',_smac2)
                tl[Ether].fields.setdefault('dst',_dmac2)
            if k+'vlan' in info:
                tl[Dot1Q].fields.setdefault('vlan',random.randint(0,4094))
            if k+'vlan1' in info:
                tl[Dot1Q].payload[Dot1Q].fields.setdefault('vlan',random.randint(0,4094))
            if k+'ipv4' in info:
                tl[IP].fields.setdefault('src','100.22.%d.%d'%(random.randint(0,250),random.randint(1,250)))
                tl[IP].fields.setdefault('dst','100.22.%d.%d'%(random.randint(0,250),random.randint(1,250)))
            if k+'ipv6' in info:
                tl[IPv6].fields.setdefault('src','102:1::%x:%x'%(random.randint(1,250),random.randint(1,250)))
                tl[IPv6].fields.setdefault('dst','102:2::%x:%x'%(random.randint(1,250),random.randint(1,250)))
        if inner :
            if isinstance(inner[0],Ether):
                inner[Ether].fields.setdefault('src',_smacin)
                inner[Ether].fields.setdefault('dst',_dmacin)
            if 'vlan' in info:
                inner[Dot1Q].fields.setdefault('vlan',random.randint(0,4094))
            if 'vlan1' in info:
                inner[Dot1Q].payload[Dot1Q].fields.setdefault('vlan',random.randint(0,4094))
            if 'ipv4' in info:
                inner[IP].fields.setdefault('src','200.22.%d.%d'%(random.randint(0,250),random.randint(1,250)))
                inner[IP].fields.setdefault('dst','200.22.%d.%d'%(random.randint(0,250),random.randint(1,250)))
            if 'ipv6' in info:
                inner[IPv6].fields.setdefault('src','103:50::%x:%x'%(random.randint(1,250),random.randint(1,250)))
                inner[IPv6].fields.setdefault('dst','103:50::%x:%x'%(random.randint(1,250),random.randint(1,250)))
        if Ether not in pkt:
            pkt = Ether()/pkt
        return pkt
        
    @staticmethod    
    def getBasePkt(itype,pktlen=0):
        pktmap = {
            'vxlan_ipv4'      : 'eth.vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.tcp',
            'geneve_ipv4'     : 'eth.vlan.ipv4.udp.geneve.eth.2vlan.ipv4.udp',
            'nvgre_ipv4'      : 'eth.vlan.ipv4.nvgre.eth.2vlan.ipv4.udp',
            'ipinip_ipv6'     : 'eth.vlan.ipv4.ipv6.udp',
            'gre_ipv6'         : 'eth.vlan.ip.gre.eth.2vlan.ipv6',
            'gre_ten_ipv6'    : 'eth.vlan.ip.gre-tencent.eth.2vlan.ipv6.udp',
            'vxlan_gpe_ipv6'  : 'eth.vlan.ip.udp.vxlan-gpe.eth.2vlan.ipv6.udp',
            'vxlanali_ipv6'   : 'eth.vlan.ip.udp.vxlan-ali.eth.2vlan.ipv6.udp',
            'vxlan_vxlan'     : 'eth.vlan.ip.udp.vxlan.eth.ip.udp.vxlan.eth.2vlan.ipv6.tcp',
            'vxlan_geneve'    : 'eth.vlan.ip.udp.vxlan.eth.ip.udp.geneve.eth.2vlan.ipv6.udp',
            'vxlan_nvgre'     : 'eth.vlan.ip.udp.vxlan.eth.ip.nvgre.eth.2vlan.ipv6.udp',
            'vxlan_ipinip'    : 'eth.vlan.ip.udp.vxlan.eth.ip.ipv6.udp',
            'vxlan_gre'       : 'eth.vlan.ip.udp.vxlan.eth.ip.gre.eth.2vlan.ipv6.udp',
            'vxlan_vxlan_gpe' : 'eth.vlan.ip.udp.vxlan.eth.ip.udp.vxlan-gpe.eth.2vlan.ipv6.udp',
            'vxlan_gre_ten'   : 'eth.vlan.ip.udp.vxlan.eth.ip.gre-tencent.eth.2vlan.ipv6.udp',
            'vxlan_vxlan_ali' : 'eth.vlan.ip.udp.vxlan.eth.ip.udp.vxlan-ali.eth.2vlan.ipv6.udp'
            }
        itype = pktmap.get(itype,itype)
        _dmac   = '52:54:00:00:%02x:%02x'%(random.randint(0,254),random.randint(1,254))
        _smac   = '0A:00:27:01:%02x:%02x'%(random.randint(0,254),random.randint(1,254))
        _dmacin = '00:10:94:01:%02x:%02x'%(random.randint(0,254),random.randint(1,254))
        _smacin = '00:10:94:02:%02x:%02x'%(random.randint(0,254),random.randint(1,254))
        _dmac2  = '00:10:94:03:%02x:%02x'%(random.randint(0,254),random.randint(1,254))
        _smac2  = '00:10:94:04:%02x:%02x'%(random.randint(0,254),random.randint(1,254))
        _eth = Ether(dst=_dmac,src=_smac)
        _ip  = IP(src='192.188.1.222',dst='192.188.1.210')
        _ipv6 = IPv6(src='100::1',dst='100::2')
        _udp = UDP(sport=2089,dport=10356)
        _arp = ARP()
        _q1 = Dot1Q(vlan=101)
        _vxlan = VXLAN(flags=0x8,vni=0x7FFFF1)
        _vxlan_gpe = VXLAN(flags=0xc,vni=0x7FFFFE,NextProtocol=3) #ipv4 1, ipv6 2 , eth 3 ,nsh 4
        _vxlan_ali = VXLAN(flags=0x8,vni=0x7FFFF3)
        _vxlan_gpe_udp = UDP(dport=4790)
        _gre = GRE(seqnum_present=1,seqence_number=0x12345678)
        _gre_ten = GRE(key_present=1,seqnum_present=1,key=0x21329809,seqence_number=0x98765321)
        _nvgre = GRE(key_present=1,key=0x7FFFF2)
        _geneve_udp = UDP(sport=12345, dport=6081)
        _geneve = GENEVE(proto=0x6558,vni=0x7FFFFD) #eth
        _geneve_ip = GENEVE(proto=0x0800,vni=0x7FFFFD)
        _geneve_ipv6 = GENEVE(proto=0x86DD,vni=0x7FFFFD)
        _eth_in = Ether(dst=_dmacin,src=_smacin)
        _eth2 = Ether(dst=_dmac2,src=_smac2)
        pktdict = {
            'eth.ipv4'  : _eth/_ip/(10*'a'),
            'eth.ipv4.udp' : _eth/_ip/_udp/(10*'a'),
            'eth.ipv6' : _eth/_ipv6/_udp/(10*'a'),
            'eth.arp'  : _eth/_ip/_arp,
            'eth.vlan.ipv4' : _eth/_q1/_ip/(10*'a'),
            'eth.2vlan.ipv4' : _eth/_q1/_q1/_ip/(10*'a'),
            'eth.vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.tcp'  : _eth/Dot1Q()/IP()/UDP()/_vxlan/_eth_in/Dot1Q()/Dot1Q()/IP()/TCP(),
            'eth.vlan.ipv4.udp.geneve.eth.2vlan.ipv4.udp' : _eth/Dot1Q()/IP()/_geneve_udp/_geneve/_eth_in/Dot1Q()/Dot1Q()/IP()/UDP(),
            'eth.vlan.ipv4.nvgre.eth.2vlan.ipv4.udp'      : _eth/Dot1Q()/IP()/_nvgre/_eth_in/Dot1Q()/Dot1Q()/IPv6()/UDP(),
            'eth.vlan.ipv4.ipv6.udp'     : _eth/Dot1Q()/IP()/IPv6()/UDP(),
            'eth.vlan.ip.gre.eth.2vlan.ipv6'         : _eth/Dot1Q()/IP()/_gre/_eth_in/Dot1Q()/Dot1Q()/IPv6()/UDP(),
            'eth.vlan.ip.gre-tencent.eth.2vlan.ipv6.udp'    : _eth/Dot1Q()/IP()/_gre_ten/_eth_in/Dot1Q()/Dot1Q()/IPv6()/UDP(),
            'eth.vlan.ip.udp.vxlan-gpe.eth.2vlan.ipv6.udp'  : _eth/Dot1Q()/IP()/_vxlan_gpe_udp/_vxlan_gpe/_eth_in/Dot1Q()/Dot1Q()/IPv6()/UDP(),
            'eth.vlan.ip.udp.vxlan-ali.eth.2vlan.ipv6.udp'   : _eth/Dot1Q()/IP()/UDP()/_vxlan_ali/_eth_in/Dot1Q()/Dot1Q()/IPv6()/UDP(),
            'eth.vlan.ip.udp.vxlan.eth.ip.udp.vxlan.eth.2vlan.ipv6.tcp'     : _eth/Dot1Q()/IP()/UDP()/_vxlan/_eth2/Dot1Q()/IP()/UDP()/_vxlan/_eth_in/Dot1Q()/Dot1Q()/IPv6()/TCP(),
            'eth.vlan.ip.udp.vxlan.eth.ip.udp.geneve.eth.2vlan.ipv6.udp'    : _eth/Dot1Q()/IP()/UDP()/_vxlan/_eth2/Dot1Q()/IP()/_geneve_udp/_geneve/_eth_in/Dot1Q()/Dot1Q()/IPv6()/UDP(),
            'eth.vlan.ip.udp.vxlan.eth.ip.nvgre.eth.2vlan.ipv6.udp'     : _eth/Dot1Q()/IP()/UDP()/_vxlan/_eth2/Dot1Q()/IP()/_nvgre/_eth_in/Dot1Q()/Dot1Q()/IPv6()/UDP(),
            'eth.vlan.ip.udp.vxlan.eth.ip.ipv6.udp'    : _eth/Dot1Q()/IP()/UDP()/_vxlan/_eth2/Dot1Q()/IP()/IPv6()/UDP(),
            'eth.vlan.ip.udp.vxlan.eth.ip.gre.eth.2vlan.ipv6.udp'       : _eth/Dot1Q()/IP()/UDP()/_vxlan/_eth2/Dot1Q()/IP()/_gre/_eth_in/Dot1Q()/Dot1Q()/IPv6()/UDP(),
            'eth.vlan.ip.udp.vxlan.eth.ip.udp.vxlan-gpe.eth.2vlan.ipv6.udp' : _eth/Dot1Q()/IP()/UDP()/_vxlan/_eth2/Dot1Q()/IP()/_vxlan_gpe_udp/_vxlan_gpe/_eth_in/Dot1Q()/Dot1Q()/IPv6()/UDP(),
            'eth.vlan.ip.udp.vxlan.eth.ip.gre-tencent.eth.2vlan.ipv6.udp'   : _eth/Dot1Q()/IP()/UDP()/_vxlan/_eth2/Dot1Q()/IP()/_gre_ten/_eth_in/Dot1Q()/Dot1Q()/IPv6()/UDP(),
            'eth.vlan.ip.udp.vxlan.eth.ip.udp.vxlan-ali.eth.2vlan.ipv6.udp' : _eth/Dot1Q()/IP()/UDP()/_vxlan/_eth2/Dot1Q()/IP()/UDP()/_vxlan_ali/_eth_in/Dot1Q()/Dot1Q()/IPv6()/UDP(),
            }
        if itype not in pktdict:
            return corsica_dpe.getPacket(itype,pktlen=128)
        return pktdict[itype]

    @staticmethod
    def setClassifyByRuleList(info,ilist=list()):
        ottype=0
        tltype=0
        if 'ottype' in info and info['ottype'] != None:
            ottype,l = corsica_dpe.getTypeid('tunnel',info['ottype'])
            
        if 'tltype' in info and info['tltype'] != None:
            tltype,l = corsica_dpe.getTypeid('tunnel',info['tltype'])

        pktvalue = {"key": {
                "CLASSIFY1_PKT_TYPE": 0,
                "CLASSIFY1_OUT_TUNNEL_TYPE": ottype if ottype != 0 else 0,
                "CLASSIFY1_OUT_L5P5_HEAD_TYPE": 0,
                "CLASSIFY1_INNER_TUNNEL_TYPE": tltype if tltype != 0 else 0,
                "CLASSIFY1_INNER_L5P5_HEAD_TYPE": 0,
                "CLASSIFY1_TUNNEL_ID": 0,
                "CLASSIFY1_OUT_VLAN_VALID": 0,
                "CLASSIFY1_INNER_VLAN_VALID": 0,
                "CLASSIFY1_OUT_VLAN_ID":  0,
                "CLASSIFY1_OUT_VLAN_TPID": 0,
                "CLASSIFY1_INNER_VLAN_ID": 0,
                "CLASSIFY1_INNER_VLAN_TPID": 0,
                "CLASSIFY1_ETH_TYPE": 0,
            },
            "mask": {
                "CLASSIFY1_PKT_TYPE": 0xff,
                "CLASSIFY1_OUT_TUNNEL_TYPE": (1<<5)-1 if ottype != 0 else 0,
                "CLASSIFY1_OUT_L5P5_HEAD_TYPE": (1<<3)-1,
                "CLASSIFY1_INNER_TUNNEL_TYPE": (1<<5)-1 if tltype != 0 else 0,
                "CLASSIFY1_INNER_L5P5_HEAD_TYPE": (1<<3)-1,
                "CLASSIFY1_TUNNEL_ID": (1<<32)-1,
                "CLASSIFY1_OUT_VLAN_VALID": 1,
                "CLASSIFY1_INNER_VLAN_VALID": 1,
                "CLASSIFY1_OUT_VLAN_ID": (1<<12)-1,
                "CLASSIFY1_OUT_VLAN_TPID": 0x7,
                "CLASSIFY1_INNER_VLAN_ID": (1<<12)-1,
                "CLASSIFY1_INNER_VLAN_TPID": 0x7,
                "CLASSIFY1_ETH_TYPE": 0xffff
            }
        }
                  
        iinfo = corsica_dpe.getClassifyIpktInfo(info)
        #根据配置设置表项
        for i in ilist:
            if i in iinfo:
                field = re.sub('OT_', '', i)
                field = re.sub('TL_', '', field)
                field = 'CLASSIFY1_'+field
                v = iinfo[i]
                pktvalue['key'][field] = v

        return pktvalue  
    
    @staticmethod
    def getClassifyIpktInfo(info):
        '''根据报文设置classify的key
        '''
        
        idict = {
                "OT_OUT_VLAN_VALID": 1 if 'ot_vlan' in info else 0,
                "OT_INNER_VLAN_VALID": 1 if 'ot_vlan1' in info else 0,
                "OT_OUT_VLAN_TPID": corsica_dpe.getvlantpid(info['ot'][0].type) if 'ot_vlan' in info else 0,
                "OT_OUT_VLAN_ID": info['ot_vlan'].vlan if 'ot_vlan' in info else 0,
                "OT_INNER_VLAN_TPID": corsica_dpe.getvlantpid(info['ot'][1].type) if 'ot_vlan1' in info else 0,
                "OT_INNER_VLAN_ID": info['ot_vlan1'].vlan if 'ot_vlan1' in info else 0,
                "OT_ETH_TYPE": info['ot_l2proto'] if 'ot_l2proto' in info else 0,
                "OT_TUNNEL_ID": info['ot_tunid'] if 'ot_tunid' in info else 0,
                "TL_OUT_VLAN_VALID": 1 if 'tl_vlan' in info else 0,
                "TL_INNER_VLAN_VALID": 1 if 'tl_vlan1' in info else 0,
                "TL_OUT_VLAN_TPID": corsica_dpe.getvlantpid(info['tl'][0].type) if 'tl_vlan' in info else 0,
                "TL_OUT_VLAN_ID": info['tl_vlan'].vlan if 'tl_vlan' in info else 0,
                "TL_INNER_VLAN_TPID": corsica_dpe.getvlantpid(info['tl'][1].type) if 'tl_vlan1' in info else 0,
                "TL_INNER_VLAN_ID": info['tl_vlan1'].vlan if 'tl_vlan1' in info else 0,
                "TL_ETH_TYPE": info['tl_l2proto'] if 'tl_l2proto' in info else 0,
                "TL_TUNNEL_ID": info['tl_tunid'] if 'tl_tunid' in info else 0, 
                "OUT_VLAN_VALID": 1 if 'vlan' in info else 0,
                "INNER_VLAN_VALID": 1 if 'vlan1' in info else 0,
                "OUT_VLAN_TPID": corsica_dpe.getvlantpid(info['in'][0].type) if 'vlan' in info else 0,
                "OUT_VLAN_ID":info['vlan'].vlan if 'vlan' in info else 0,
                "INNER_VLAN_TPID": corsica_dpe.getvlantpid(info['in'][1].type) if 'vlan1' in info else 0,
                "INNER_VLAN_ID": info['vlan1'].vlan if 'vlan1' in info else 0,
                "ETH_TYPE": info['l2proto'] if 'l2proto' in info else 0,             
        }
        
        return idict     
    
    @staticmethod 
    def setClassifyByPkt(config,info,layer,mode=-1,ilist=None):
        #设置Classify匹配的pkt条件              
        pkttmp = info[layer]
        if IP in pkttmp and mode == 0: #dip , dmac
            config["key"]["CLASSIFY1_ADDRESS0"] = ip2int(pkttmp[IP].dst)
            config["key"]["CLASSIFY1_ADDRESS1"] = mac2int(pkttmp[Ether].dst)
            config["mask"]["CLASSIFY1_ADDRESS0"] = 0xffffffff
            config["mask"]["CLASSIFY1_ADDRESS1"] = mac2int("FF:FF:FF:FF:FF:FF")
        elif IP in pkttmp and mode == 1: #dip , smac
            config["key"]["CLASSIFY1_ADDRESS0"] = ip2int(pkttmp[IP].dst)
            config["key"]["CLASSIFY1_ADDRESS1"] = mac2int(pkttmp[Ether].src)
            config["mask"]["CLASSIFY1_ADDRESS0"] = 0xffffffff
            config["mask"]["CLASSIFY1_ADDRESS1"] = mac2int("FF:FF:FF:FF:FF:FF")
        elif IP in pkttmp and mode == 2: #dip,sip
            config["key"]["CLASSIFY1_ADDRESS0"] = ip2int(pkttmp[IP].dst)
            config["key"]["CLASSIFY1_ADDRESS1"] = ip2int(pkttmp[IP].src)
            config["mask"]["CLASSIFY1_ADDRESS0"] = 0xffffffff
            config["mask"]["CLASSIFY1_ADDRESS1"] = 0xffffffff
        elif IP in pkttmp and mode == 3: #sip,dmac
            config["key"]["CLASSIFY1_ADDRESS0"] = ip2int(pkttmp[IP].src)
            config["key"]["CLASSIFY1_ADDRESS1"] = mac2int(pkttmp[Ether].dst)
            config["mask"]["CLASSIFY1_ADDRESS0"] = 0xffffffff
            config["mask"]["CLASSIFY1_ADDRESS1"] = mac2int("FF:FF:FF:FF:FF:FF")
        elif IP in pkttmp and mode == 4: #sip,smac
            config["key"]["CLASSIFY1_ADDRESS0"] = ip2int(pkttmp[IP].src)
            config["key"]["CLASSIFY1_ADDRESS1"] = mac2int(pkttmp[Ether].src)
            config["mask"]["CLASSIFY1_ADDRESS0"] = 0xffffffff
            config["mask"]["CLASSIFY1_ADDRESS1"] = mac2int("FF:FF:FF:FF:FF:FF")
        elif mode == 5: #dmac,smac
            config["key"]["CLASSIFY1_ADDRESS0"] = mac2int(pkttmp[Ether].dst)
            config["key"]["CLASSIFY1_ADDRESS1"] = mac2int(pkttmp[Ether].src)
            config["mask"]["CLASSIFY1_ADDRESS0"] = mac2int("FF:FF:FF:FF:FF:FF")
            config["mask"]["CLASSIFY1_ADDRESS1"] = mac2int("FF:FF:FF:FF:FF:FF")
        elif IP in pkttmp and mode == 6: #dip,0
            config["key"]["CLASSIFY1_ADDRESS0"] = ip2int(pkttmp[IP].dst)
            config["mask"]["CLASSIFY1_ADDRESS0"] = 0xffffffff
        elif IP in pkttmp and mode == 7: #sip,0
            config["key"]["CLASSIFY1_ADDRESS0"] = ip2int(pkttmp[IP].src)
            config["mask"]["CLASSIFY1_ADDRESS0"] = 0xffffffff
        elif mode == 8: #dmac,0
            config["key"]["CLASSIFY1_ADDRESS0"] = mac2int(pkttmp[Ether].dst)
            config["mask"]["CLASSIFY1_ADDRESS0"] = mac2int("FF:FF:FF:FF:FF:FF")
        elif mode == 9: #smac,0
            config["key"]["CLASSIFY1_ADDRESS0"] = mac2int(pkttmp[Ether].src)
            config["mask"]["CLASSIFY1_ADDRESS0"] = mac2int("FF:FF:FF:FF:FF:FF")
        elif IPv6 in pkttmp and mode in [0,1,2,6]: #dip
            a,b,c = corsica_dpe.ipv62int2(pkttmp[IPv6].dst)
            config["key"]["CLASSIFY1_ADDRESS0"] = c
            config["key"]["CLASSIFY1_ADDRESS1"] = b
            config["key"]["CLASSIFY1_ADDRESS_EXTEND"] = a            
            config["mask"]["CLASSIFY1_ADDRESS0"] = (1<<48) -1
            config["mask"]["CLASSIFY1_ADDRESS1"] = (1<<48) -1
            config["mask"]["CLASSIFY1_ADDRESS_EXTEND"] = (1<<32) -1
        elif IPv6 in pkttmp and mode in [3,4,7]: #sip
            a,b,c = corsica_dpe.ipv62int2(pkttmp[IPv6].src)
            config["key"]["CLASSIFY1_ADDRESS0"] = c
            config["key"]["CLASSIFY1_ADDRESS1"] = b
            config["key"]["CLASSIFY1_ADDRESS_EXTEND"] = a
            config["mask"]["CLASSIFY1_ADDRESS0"] = (1<<48) -1
            config["mask"]["CLASSIFY1_ADDRESS1"] = (1<<48) -1
            config["mask"]["CLASSIFY1_ADDRESS_EXTEND"] = (1<<32) -1
        elif mode in [0,3]: #0,dmac
            config["key"]["CLASSIFY1_ADDRESS1"] = mac2int(pkttmp[Ether].dst)
            config["mask"]["CLASSIFY1_ADDRESS1"] = mac2int("FF:FF:FF:FF:FF:FF")
        elif mode in [1,4]: #0 , smac
            config["key"]["CLASSIFY1_ADDRESS1"] = mac2int(pkttmp[Ether].src)
            config["mask"]["CLASSIFY1_ADDRESS1"] = mac2int("FF:FF:FF:FF:FF:FF")
        elif mode in [2,6,7]: #dmac,smac
            config["key"]["CLASSIFY1_ADDRESS0"] = mac2int(pkttmp[Ether].dst)
            config["key"]["CLASSIFY1_ADDRESS1"] = mac2int(pkttmp[Ether].src),
            config["mask"]["CLASSIFY1_ADDRESS0"] = mac2int("FF:FF:FF:FF:FF:FF")
            config["mask"]["CLASSIFY1_ADDRESS1"] = mac2int("FF:FF:FF:FF:FF:FF")
        
        #IP和MAC取的层，不关心关注IP还是MAC，都设置
        if mode != -1:
            ikeyLayer = layer.upper()  
            ikey = ikeyLayer + '_KEY_IP' + ',' + ikeyLayer + '_KEY_MAC'
            if ilist != None:
                ilist = ilist + ',' + ikey
            else:
                ilist = ikey
                return config,ilist             
        
        if not isinstance(ilist,list):
            ilist = ilist.split(',')
                     
        #根据列表重新设置匹配项
        pktvalue = corsica_dpe.setClassifyByRuleList(info,ilist)

        for i in ilist:
            field = re.sub('OT_', '', i)
            field = re.sub('TL_', '', field)
            if 'CLASSIFY1_'+field in pktvalue["key"]:
                i = 'CLASSIFY1_'+field
                config["key"][i] = pktvalue['key'][i]
                config["mask"][i] = pktvalue['mask'][i]
        return config,ilist
    
    @staticmethod
    def setClassifyRegisterByConf(config,info,layer,mode=-1,ilist=None):
        '''
        PIPE0收到的带1层tunnel的报文classfy tcam的查找key中vid/mac/ip/ethertype的选取方式:
        0:选择outer tunnel的信息组key;
        1: 选择内层报文的信息组组key

        PIPE0收到的带2层tunnel的报文classfy tcam的查找key中vid/mac/ip/ethertype的选取方式:
        0：选择outer tunnel的信息组key;
        1: 选择inner tunnel的信息组key;
        2: 选择内层报文的信息组组key;
        3:reserved
        '''
        classifykeyselreg = {
                "tbl_pipe": 0,
                "key": {
                    "REG_TYPE": DPE_IPIPE_GRP0_CSR,
                    "REG_ID": PIPE_GRP_CSR_P0_CLASSIFY_KEY_SEL_CFG_REG
                },
                "table": {
                    "REG_VALUE": 0
                }
        }
        
        specrule = False
        if not isinstance(ilist,list):
            ilist = ilist.split(',')

        if len(ilist) > 0:
            specrule = True        
          
        #最外层匹配
        if layer == 'ot' and specrule == False:
            return config 

        #key sel寄存器bit位定义
        #oneTunnelIpSel: 0, oneTunnelMacSel: 1,oneTunnelVlanSel: 2,oneTunnelEthTypeSel: 3
        #twoTunnelIpSel: 4, twoTunnelMacSel: 6,twoTunnelVlanSel: 8,twoTunnelEthTypeSel: 10
    
        fieldmap = {
            'KEY_IP': 'IP_SEL',
            'KEY_MAC': 'MAC_SEL',
            'ETH_TYPE': 'ETH_TYPE_SEL',
            'VLAN_ID':  'VLAN_SEL',
            'VLAN_TPID': 'VLAN_SEL',
            'VLAN_VALID': 'VLAN_SEL',
        } 
        
        kset = {
            'TL_IP_SEL':       0,
            'TL_MAC_SEL':      0,
            'TL_VLAN_SEL':     0,
            'TL_ETH_TYPE_SEL': 0,
            'IN_IP_SEL':       0,
            'IN_MAC_SEL':      0,
            'IN_VLAN_SEL':     0,
            'IN_ETH_TYPE_SEL': 0,                        
        }       

        #待添加适配任意规则
        if specrule == True:
            for i in ilist:
                if i.count('TL'):
                    #field = re.sub('OT_', '', i)
                    field = re.sub('TL_', '', i)
                    field = re.sub('OUT_', '', field)
                    field = re.sub('INNER_', '', field)
                    if field in fieldmap:
                        kset['TL_' + fieldmap[field]] = 1
                elif i.count('IN'):
                    field = re.sub('IN_', '', i)
                    field = re.sub('OUT_', '', field)
                    field = re.sub('INNER_', '', field)
                    if field in fieldmap:
                        kset['IN_' + fieldmap[field]] = 2
 
        keySelValue = 0
        #一层隧道
        if info['tunnel_number'] == 1:
            keySelValue= kset['TL_ETH_TYPE_SEL']<<3 | kset['TL_VLAN_SEL']<<2 | kset['TL_MAC_SEL']<<1 | kset['TL_IP_SEL']
        elif info['tunnel_number'] == 2:
            keySelValue= kset['IN_ETH_TYPE_SEL']<<10 | kset['IN_VLAN_SEL']<<8 | kset['IN_MAC_SEL']<<6 | kset['IN_IP_SEL'] << 4| \
            kset['TL_ETH_TYPE_SEL']<<10 | kset['TL_VLAN_SEL']<<8 | kset['TL_MAC_SEL']<<6 | kset['TL_IP_SEL'] << 4

        classifykeyselreg['table']['REG_VALUE'] = keySelValue
        #classifykeyselreg['table']['REG_VALUE'] |= 15
        config['group'].append(classifykeyselreg)
        return config

    @staticmethod
    def setInputPortRxByTunnel(config,pktTunlnum):
        if pktTunlnum >= 1:
            config['key']['INPUT_PORT_RX_TUNNEL_PKT_FLAG'] = 1
        return config

    @staticmethod
    def splitName(itype=None,spt='.'):
        '''eth.ipv4(src=1.1.1.1).udp(dport=0x1234) ==> [eth,ipv4(src=1.1.1.1),udp(dport=0x1234)]
        '''
        ts = itype.split(spt)
        result = []
        start = 0
        for i in ts:
            if start and ')' not in i:
                result[-1] = result[-1]+spt+i
            elif start and ')' in i:
                result[-1] = result[-1]+spt+i
                start = 0
            elif '(' in i and ')' in i:
                result.append(i)
            elif '(' not in i and ')' not in i:
                result.append(i)
            elif '(' in i:
                start = 1 ; result.append(i)
        return result
    
    @staticmethod
    def tansStrToDict(itype):
        '''TYPE1,TYPE2(son=xx),TYPE3(dport=0x1234)
        '''
        result = dict()
        its = corsica_dpe.splitName(itype,',')
        for v in its:
            args = dict()
            if '(' in v:  #分析参数
                v,args=v.split('(',maxsplit=1)
                args = args.strip(')')
                args = eval(f"dict({args})")  #转换为字典
            elif '=' in v:
                v,args=v.split('=',maxsplit=1)
            else:
                args = None
            result[v] = args
        return result
    
    @staticmethod
    def setProfileTemplate(profile=None,itype=None):
        '''
        没有表示不关心
        Eth.2VLAN.L2p5.L3.L3p5.L4.Tunnel.L5p5.Eth.2VLAN.L2p5.L3.L3p5.L4.Tunnel.L5p5.Eth.2VLAN.L2p5.L3.L3p5.L4
        Eth.2VLAN.IP.UDP.Tunnel.Eth.2Vlan.IPv6.UDP.Tunnel.Eth.2Vlan.IP.UDP
        L2p5 : MPLS/PPPoE-Discovery/PPPoE-Session/User1...User5 L2.5Header1
        L3 : frag / no_frag&option / Ip_normal /Ipv6_ext / Ipv6 normal/ arp / rocev1 / user1 ... user8  L3Header1
        L3.5 : IFA2.0 / user1 ... user7 L3.5Header1
        L4 : ICMP/IGMP/TCP/UDP/ICMP6/SCTP/user1 ... user8 L4Header1
        Tunnel : NoTunnel/Vxlan/geneve/nvgre/gre/ipinip/vxlan-gpe/Gre-Tencent/vxlan-ali/user3 ... user8 TunnelHeader3
        L5.5 : NoL5.5/NSH/user1 ... user6 L5.5Header1
        '''
        itype = corsica_dpe.getPacketLong(itype)
        itype = re.sub(r"\([^()]*\)","",itype) #删除参数配置
        typeid = {
            'l2' :{'eth0':0,'eth1':1,'eth2':2},
            'l2p5' : {'mpls':0,'pppoe-discovery':1,'pppoe-session':2},
            'l3':{'ipv4-frag':0,'ipv4-option':1,'ipv4':2,'ipv6-ext':3,'ipv6':4,'arp':5,'rocev1':6},
            'l3p5':{'ifa':0,'ifa2':0},
            'l4':{'icmp':0,'igmp':1,'tcp':2,'udp':3,'icmp6':4,'sctp':5},
            'tunnel':{'notunnel':0,'vxlan':1,'geneve':2,'nvgre':3,'gre':4,'ipinip':5,'vxlan-gpe':6,'gre-tencent':7,'vxlan-ali':8},
            'l5p5':{'nol5.5':0,'nsh':1}
        }
        default_json = {
            "key": {
                "PROFILE_GROUP_INDEX": 0,
                "PROFILE_KEY_BUILD_PROFILE_ID": 0,
            },
            "mask": {
                "PROFILE_GROUP_INDEX": 255,
                "PROFILE_KEY_BUILD_PROFILE_ID": 255,
            }
        }
        default_mask = {
                "PROFILE_GROUP_INDEX": 0xff,
                "PROFILE_KEY_BUILD_PROFILE_ID": 0xff,
                "PROFILE_L4_DST_PORT": 0xffff,
                "PROFILE_L4_IS_TCPUDP": 1,
                "PROFILE_L4_HD_TYPE": 0xf,
                "PROFILE_L4_HD_VALID": 1,
                "PROFILE_L3P5_HD_TYPE": 0x7,
                "PROFILE_L3P5_VALID": 1,
                "PROFILE_L3_IS_IP": 1,
                "PROFILE_L3_HD_TYPE": 0xf,
                "PROFILE_L3_HD_VALID": 1,
                "PROFILE_L2P5_SUBTYPE": 0x7,
                "PROFILE_L2P5_HD_TYPE": 0x7,
                "PROFILE_L2P5_HD_VALID": 1,
                "PROFILE_INNER_VLAN_TAG": 1,
                "PROFILE_OUT_VLAN_TAG": 1,
                "PROFILE_MAC_TYPE": 3,  #单播，广播，组播
                "PROFILE_L2_HD_VALID": 1,
                "PROFILE_TL_L5P5_HD_TYPE": 7,
                "PROFILE_TL_L5P5_HD_VALID": 1,
                "PROFILE_TL_TUNNEL_FLAGS": 0xff,
                "PROFILE_TL_TUNNEL_TYPE": 0x1f,
                "PROFILE_TL_TUNNEL_VALID": 1,
                "PROFILE_TL_L4_IS_TCPUDP": 1,
                "PROFILE_TL_L4_HD_TYPE": 0xf,
                "PROFILE_TL_L4_HD_VALID": 1,
                "PROFILE_TL_L3P5_HD_TYPE": 0x7,
                "PROFILE_TL_L3P5_VALID": 1,
                "PROFILE_TL_L3_IS_IP": 1,
                "PROFILE_TL_L3_HD_TYPE": 0xf,
                "PROFILE_TL_L3_HD_VALID": 1,
                "PROFILE_TL_L2P5_SUBTYPE": 7,
                "PROFILE_TL_L2P5_HD_TYPE": 7,
                "PROFILE_TL_L2P5_HD_VALID": 1,
                "PROFILE_TL_INNER_VLAN_TAG": 1,
                "PROFILE_TL_OUT_VLAN_TAG": 1,
                "PROFILE_TL_MAC_TYPE": 3,
                "PROFILE_TL_L2_HD_VALID": 1,
                "PROFILE_OT_L5P5_HD_TYPE": 7,
                "PROFILE_OT_L5P5_HD_VALID": 1,
                "PROFILE_OT_TUNNEL_FLAGS": 0xff,
                "PROFILE_OT_TUNNEL_TYPE": 0x1f,
                "PROFILE_OT_TUNNEL_VALID": 1,
                "PROFILE_OT_L4_IS_TCPUDP": 1,
                "PROFILE_OT_L4_HD_TYPE": 0xf,
                "PROFILE_OT_L4_HD_VALID": 1,
                "PROFILE_OT_L3P5_HD_TYPE": 7,
                "PROFILE_OT_L3P5_VALID": 1,
                "PROFILE_OT_L3_IS_IP": 1,
                "PROFILE_OT_L3_HD_TYPE": 0xf,
                "PROFILE_OT_L3_HD_VALID": 1,
                "PROFILE_OT_L2P5_SUBTYPE": 7,
                "PROFILE_OT_L2P5_HD_TYPE": 7,
                "PROFILE_OT_L2P5_HD_VALID": 1,
                "PROFILE_OT_INNER_VLAN_TAG": 1,
                "PROFILE_OT_OUT_VLAN_TAG": 1,
                "PROFILE_OT_MAC_TYPE": 3,
                "PROFILE_OT_L2_HD_VALID": 1,
                "PROFILE_RSV": 1,
                "PROFILE_PIPE_ID": 1
            }
        if profile == None: profile = default_json
        key = profile['key']
        mask = profile['mask']

        info = corsica_dpe.paserPacket(itype)
        ot,tl,inner,ottype,tltype = info['ot'],info['tl'],info['in'],info['ottype'],info['tltype']
        isin = lambda x,y: [k for k in y if k in x]
        if ot != None:
            #隧道外层信息
            if ottype and 'ot_last' in info:
                otlastlen = len(info['ot_last'])
                ot = ot[:-otlastlen]
            ilist = ot.split('.')
            if ottype:
                key["PROFILE_OT_TUNNEL_VALID"] = 1
                #需要设置寄存器，后面修改
                
                key["PROFILE_OT_TUNNEL_TYPE"] = typeid['tunnel'][ottype]
                if ottype == 'vxlan' or ottype == 'vxlan-ali':
                    key["PROFILE_OT_TUNNEL_FLAGS"] = 0x08 
                elif ottype == 'vxlan-gpe':
                    key["PROFILE_OT_TUNNEL_FLAGS"] = 0x0c
                elif ottype == 'geneve':
                    key["PROFILE_OT_TUNNEL_FLAGS"] = 0x0
                #elif ottype == 'gre':
                    #key["PROFILE_OT_TUNNEL_FLAGS"] = 0x30 ---需要看具体FLAG
                    #key["PROFILE_OT_TUNNEL_FLAGS"] = 0
                #else:
                    #key["PROFILE_OT_TUNNEL_FLAGS"] = 0                
            t = isin(ilist,typeid["l5p5"].keys())
            if 'l5p5' in ilist or t:
                if t : key["PROFILE_OT_L5P5_HD_TYPE"] = typeid["l4"][t[0]]
                key["PROFILE_OT_L5P5_HD_VALID"] = 1
            t = isin(ilist,typeid["l4"].keys())
            if 'l4' in ilist or t:
                if t[0] in ['tcp','udp']:key["PROFILE_OT_L4_IS_TCPUDP"] = 1
                if t :key["PROFILE_OT_L4_HD_TYPE"] = typeid["l4"][t[0]]
                key["PROFILE_OT_L4_HD_VALID"] = 1
            t = isin(ilist,typeid["l3p5"].keys())
            if 'l3p5' in ilist:
                if t : key["PROFILE_OT_L3P5_HD_TYPE"] = typeid["l3p5"][t[0]]
                key["PROFILE_OT_L3P5_VALID"] = 1
            t = isin(ilist,typeid["l3"].keys())
            if 'l3' in ilist or t:
                if t :
                    if 'ipv4' in t[0] or 'ipv6' in t[0] : key["PROFILE_OT_L3_IS_IP"] = 1
                    key["PROFILE_OT_L3_HD_TYPE"] = typeid["l3"][t[0]]
                key["PROFILE_OT_L3_HD_VALID"] = 1
            t = isin(ilist,typeid["l2p5"].keys())
            if 'l2p5' in ilist or t:
                if 'mpls' in ilist : key["PROFILE_OT_L2P5_SUBTYPE"] = 0  #标签层数
                if 'mpls' in ilist :
                    key["PROFILE_OT_L2P5_HD_TYPE"] = typeid["l2p5"][t[0]]
                key["PROFILE_OT_L2P5_HD_VALID"] = 1
            if '2vlan' in ilist:
                key["PROFILE_OT_INNER_VLAN_TAG"] = 1
                key["PROFILE_OT_OUT_VLAN_TAG"] = 1
            if 'vlan' in ilist:
                key["PROFILE_OT_OUT_VLAN_TAG"] = 1
            if 'eth0' in ilist:
                key["PROFILE_OT_L2_HD_VALID"] = 1
                key["PROFILE_OT_MAC_TYPE"] = 0
            elif 'eth1' in ilist:
                key["PROFILE_OT_L2_HD_VALID"] = 1
                key["PROFILE_OT_MAC_TYPE"] = 0
            if 'eth' in ilist:
                key["PROFILE_OT_L2_HD_VALID"] = 1
            if 'noeth' in ilist:
                key["PROFILE_OT_L2_HD_VALID"] = 0
        if tl != None:
            ilist = tl.split('.')
            if tltype and 'tl_last' in info:
                tllastlen = len(info['tl_last'])
                tl = tl[:-tllastlen]
            ilist = tl.split('.')
            if tltype:
                key["PROFILE_TL_TUNNEL_VALID"] = 1
                #需要设置寄存器，后面修改
                if tltype == 'vxlan' or tltype == 'vxlan-ali':
                    key["PROFILE_TL_TUNNEL_FLAGS"] = 0x08 
                elif tltype == 'vxlan-gpe':
                    key["PROFILE_TL_TUNNEL_FLAGS"] = 0x0c
                elif tltype == 'geneve':
                    key["PROFILE_TL_TUNNEL_FLAGS"] = 0x0
                #elif tltype == 'gre':
                    #key["PROFILE_TL_TUNNEL_FLAGS"] = 0x30
                    #key["PROFILE_TL_TUNNEL_FLAGS"] = 0x0
                #else:
                    #key["PROFILE_TL_TUNNEL_FLAGS"] = 0
                key["PROFILE_TL_TUNNEL_TYPE"] = typeid['tunnel'][tltype]
            t = isin(ilist,typeid["l5p5"].keys())
            if 'l5p5' in ilist or t:
                if t : key["PROFILE_TL_L5P5_HD_TYPE"] = typeid["l4"][t[0]]
                key["PROFILE_TL_L5P5_HD_VALID"] = 1
            t = isin(ilist,typeid["l4"].keys())
            if 'l4' in ilist or t:
                if t and (t[0] in ['tcp','udp']):key["PROFILE_TL_L4_IS_TCPUDP"] = 1
                if t :key["PROFILE_TL_L4_HD_TYPE"] = typeid["l4"][t[0]]
                key["PROFILE_TL_L4_HD_VALID"] = 1
            t = isin(ilist,typeid["l3p5"].keys())
            if 'l3p5' in ilist:
                if t : key["PROFILE_TL_L3P5_HD_TYPE"] = typeid["l3p5"][t[0]]
                key["PROFILE_TL_L3P5_VALID"] = 1
            t = isin(ilist,typeid["l3"].keys())
            if 'l3' in ilist or t:
                if 'ip' in t : key["PROFILE_TL_L3_IS_IP"] = 1
                if t :
                    key["PROFILE_TL_L3_HD_TYPE"] = typeid["l3"][t[0]]
                key["PROFILE_TL_L3_HD_VALID"] = 1
            t = isin(ilist,typeid["l2p5"].keys())
            if 'l2p5' in ilist or t:
                if 'mpls' in ilist : key["PROFILE_TL_L2P5_SUBTYPE"] = 0  #标签层数
                if 'mpls' in ilist :
                    key["PROFILE_TL_L2P5_HD_TYPE"] = typeid["l2p5"][t[0]]
                key["PROFILE_TL_L2P5_HD_VALID"] = 1
            if '2vlan' in ilist:
                key["PROFILE_TL_INNER_VLAN_TAG"] = 1
                key["PROFILE_TL_OUT_VLAN_TAG"] = 1
            if 'vlan' in ilist:
                key["PROFILE_TL_OUT_VLAN_TAG"] = 1

            if 'eth' in ilist:
                key["PROFILE_TL_MAC_TYPE"] = 0 # 单播、广播、组播
            if 'noeth' in ilist:
                key["PROFILE_TL_L2_HD_VALID"] = 0
        if inner != None:
            ilist = inner.split('.')
            t = isin(ilist,typeid["l4"].keys())
            if 'l4' in ilist or t:
                if t and (t[0] in ['tcp','udp']):key["PROFILE_L4_IS_TCPUDP"] = 1
                if t :key["PROFILE_L4_HD_TYPE"] = typeid["l4"][t[0]]
                key["PROFILE_L4_HD_VALID"] = 1
            t = isin(ilist,typeid["l3p5"].keys())
            if 'l3p5' in ilist:
                if t : key["PROFILE_L3P5_HD_TYPE"] = typeid["l3p5"][t[0]]
                key["PROFILE_L3P5_VALID"] = 1
            t = isin(ilist,typeid["l3"].keys())
            if 'l3' in ilist or t:
                if 'ip' in t : key["PROFILE_L3_IS_IP"] = 1
                if t :
                    key["PROFILE_L3_HD_TYPE"] = typeid["l3"][t[0]]
                key["PROFILE_L3_HD_VALID"] = 1
            t = isin(ilist,typeid["l2p5"].keys())
            if 'l2p5' in ilist or t:
                if 'mpls' in ilist : key["PROFILE_L2P5_SUBTYPE"] = 0  #标签层数
                if t :
                    key["PROFILE_L2P5_HD_TYPE"] = typeid["l2p5"][t[0]]
                key["PROFILE_L2P5_HD_VALID"] = 1
            if '2vlan' in ilist:
                key["PROFILE_INNER_VLAN_TAG"] = 1
                key["PROFILE_OUT_VLAN_TAG"] = 1
            if 'vlan' in ilist:
                key["PROFILE_OUT_VLAN_TAG"] = 1
            t = isin(ilist,typeid["l2"].keys())
            if 'eth'in ilist or t:
                if t :
                    key["PROFILE_MAC_TYPE"] = typeid["l2"][t[0]]
                key["PROFILE_L2_HD_VALID"] = 1
            if 'noeth' in ilist:
                key["PROFILE_L2_HD_VALID"] = 0
        for i in key.keys():
            if i in mask : continue
            mask[i] = default_mask[i]
        logger.debug("profile: %s !"%profile)
        return profile
		
    @staticmethod
    def getKeyTemplateInfo():
        '''根据template获取pkt的key
        '''
        idict = {'list': list(),'value':dict()}
        def setkey(x,y,k,ilen):
            idict['list'].append(k)
            idict['value'][k] = {
                'key' : x, 'field' : y, # paser报文名称和域
                'len' : ilen,
            }

        setkey(None,None,"KEY_TEMPLATE_KEY_PROF_ID",11)
        setkey(None,None,"KEY_TEMPLATE_GROUP_IDX",8)
        setkey(None,None,"KEY_TEMPLATE_VNIC_ID",14)
        setkey(None,None,"KEY_TEMPLATE_META_DATA",32)
        setkey(None,None,"KEY_TEMPLATE_MAC_PORT_ENABLE",4)
        setkey('ot_eth','dst',"KEY_TEMPLATE_OT_L2_DMAC",48)
        setkey('ot_eth','src',"KEY_TEMPLATE_OT_L2_SMAC",48)
        setkey('ot_eth','type',"KEY_TEMPLATE_OT_L2_OUT_VLAN_TPID",3)
        setkey('ot_vlan','prio',"KEY_TEMPLATE_OT_L2_OUT_VLAN_PRI",3)
        setkey('ot_vlan','id',"KEY_TEMPLATE_OT_L2_OUT_VLAN_DE",1)
        setkey('ot_vlan','vlan',"KEY_TEMPLATE_OT_L2_OUT_VLAN_VID",12)
        setkey('ot_vlan','type',"KEY_TEMPLATE_OT_L2_INNER_VLAN_TPID",3)
        setkey('ot_vlan1','prio',"KEY_TEMPLATE_OT_L2_INNER_VLAN_PRI",3)
        setkey('ot_vlan1','id',"KEY_TEMPLATE_OT_L2_INNER_VLAN_DE",1)
        setkey('ot_vlan1','vlan',"KEY_TEMPLATE_OT_L2_INNER_VLAN_VID",12)
        setkey('ot_l2proto',None,"KEY_TEMPLATE_OT_L3_TYPE",16)
        setkey('ot_l3','src',"KEY_TEMPLATE_OT_L3_SIP",32)
        setkey('ot_l3','dst',"KEY_TEMPLATE_OT_L3_DIP",32)
        setkey('ot_l3proto',None,"KEY_TEMPLATE_OT_L3_PROT",8)
        setkey('ot_l3ttl',None,"KEY_TEMPLATE_OT_L3_TTL",8)
        setkey('ot_l3tos',None,"KEY_TEMPLATE_OT_L3_TOS",8)
        setkey('ot_l3flow',None,"KEY_TEMPLATE_OT_L3_FLOW",20)
        setkey('ot_ipv4','flags',"KEY_TEMPLATE_OT_L3_FRAG",1)
        setkey('ot_ipv6ext','xxx',"KEY_TEMPLATE_OT_L3_EXT_HD_VALID",1)
        setkey('ot_l4sport1',None,"KEY_TEMPLATE_OT_L4_SPORT1",8)
        setkey('ot_l4sport2',None,"KEY_TEMPLATE_OT_L4_SPORT2",8)
        setkey('ot_l4dport',None,"KEY_TEMPLATE_OT_L4_DPORT",16)
        setkey('ot_l4flag',None,"KEY_TEMPLATE_OT_L4_FLAGS",9)
        setkey('ot_tuntype',None,"KEY_TEMPLATE_OT_TUNNEL_TYPE",5)
        setkey('ot_tunid',None,"KEY_TEMPLATE_OT_TUNNEL_ID",32)
        setkey('ot_x','xxx',"KEY_TEMPLATE_OT_TUNNEL_FLAGS",8)
        setkey('ot_xxx','xxx',"KEY_TEMPLATE_OT_L5P5_NSH_FLAGS",2)
        setkey('ot_xxx','xxx',"KEY_TEMPLATE_OT_L5P5_NSH_TTL",6)
        setkey('ot_nsh','Len',"KEY_TEMPLATE_OT_L5P5_NSH_LEN",6)
        setkey('ot_nsh','MDType',"KEY_TEMPLATE_OT_L5P5_NSH_MD_TYPE",4)
        setkey('ot_nsh','NextProto',"KEY_TEMPLATE_OT_L5P5_NSH_NEXT_PROT",8)
        setkey('ot_nsh','NSP',"KEY_TEMPLATE_OT_L5P5_NSH_SPI",24)
        setkey('ot_nsh','NSI',"KEY_TEMPLATE_OT_L5P5_NSH_SI",8)
        setkey('tl_eth','dst',"KEY_TEMPLATE_TL_L2_DMAC",48)
        setkey('tl_eth','src',"KEY_TEMPLATE_TL_L2_SMAC",48)
        setkey('tl_eth','type',"KEY_TEMPLATE_TL_L2_OUT_VLAN_TPID",3)
        setkey('tl_vlan','prio',"KEY_TEMPLATE_TL_L2_OUT_VLAN_PRI",3)
        setkey('tl_vlan','id',"KEY_TEMPLATE_TL_L2_OUT_VLAN_DE",1)
        setkey('tl_vlan','vlan',"KEY_TEMPLATE_TL_L2_OUT_VLAN_VID",12)
        setkey('tl_vlan','type',"KEY_TEMPLATE_TL_L2_INNER_VLAN_TPID",3)
        setkey('tl_vlan1','prio',"KEY_TEMPLATE_TL_L2_INNER_VLAN_PRI",3)
        setkey('tl_vlan1','id',"KEY_TEMPLATE_TL_L2_INNER_VLAN_DE",1)
        setkey('tl_vlan1','vlan',"KEY_TEMPLATE_TL_L2_INNER_VLAN_VID",12)
        setkey('tl_l2proto',None,"KEY_TEMPLATE_TL_L3_TYPE",16)
        setkey('tl_l3','src',"KEY_TEMPLATE_TL_L3_SIP",32)
        setkey('tl_l3','dst',"KEY_TEMPLATE_TL_L3_DIP",32)
        setkey('tl_l3proto',None,"KEY_TEMPLATE_TL_L3_PROT",8)
        setkey('tl_l3ttl',None,"KEY_TEMPLATE_TL_L3_TTL",8)
        setkey('tl_l3tos',None,"KEY_TEMPLATE_TL_L3_TOS",8)
        setkey('tl_l3flow',None,"KEY_TEMPLATE_TL_L3_FLOW",20)
        setkey('tl_ipv4','flags',"KEY_TEMPLATE_TL_L3_FRAG",1)
        setkey('tl_ipv6ext',None,"KEY_TEMPLATE_TL_L3_EXT_HD_VALID",1)
        setkey('tl_l4sport1',None,"KEY_TEMPLATE_TL_L4_SPORT1",8)
        setkey('tl_l4sport2',None,"KEY_TEMPLATE_TL_L4_SPORT2",8)
        setkey('tl_l4dport',None,"KEY_TEMPLATE_TL_L4_DPORT",16)
        setkey('tl_l4flag',None,"KEY_TEMPLATE_TL_L4_FLAGS",9)
        setkey('tl_tuntype',None,"KEY_TEMPLATE_TL_TUNNEL_TYPE",5)
        setkey('tl_tunid',None,"KEY_TEMPLATE_TL_TUNNEL_ID",32)
        setkey('tl_x','xxx',"KEY_TEMPLATE_TL_TUNNEL_FLAGS",8)
        setkey('tl_xxx','xxx',"KEY_TEMPLATE_TL_L5P5_NSH_FLAGS",2)
        setkey('tl_xxx','xxx',"KEY_TEMPLATE_TL_L5P5_NSH_TTL",6)
        setkey('tl_nsh','Len',"KEY_TEMPLATE_TL_L5P5_NSH_LEN",6)
        setkey('tl_nsh','MDType',"KEY_TEMPLATE_TL_L5P5_NSH_MD_TYPE",4)
        setkey('tl_nsh','NextProto',"KEY_TEMPLATE_TL_L5P5_NSH_NEXT_PROT",8)
        setkey('tl_nsh','NSP',"KEY_TEMPLATE_TL_L5P5_NSH_SPI",24)
        setkey('tl_nsh','NSI',"KEY_TEMPLATE_TL_L5P5_NSH_SI",8)
        setkey('eth','dst',"KEY_TEMPLATE_L2_DMAC",48)
        setkey('eth','src',"KEY_TEMPLATE_L2_SMAC",48)
        setkey('eth','type',"KEY_TEMPLATE_L2_OUT_VLAN_TPID",3)
        setkey('vlan','prio',"KEY_TEMPLATE_L2_OUT_VLAN_PRI",3)
        setkey('vlan','id',"KEY_TEMPLATE_L2_OUT_VLAN_DE",1)
        setkey('vlan','vlan',"KEY_TEMPLATE_L2_OUT_VLAN_VID",12)
        setkey('vlan','type',"KEY_TEMPLATE_L2_INNER_VLAN_TPID",3)
        setkey('vlan1','prio',"KEY_TEMPLATE_L2_INNER_VLAN_PRI",3)
        setkey('vlan1','id',"KEY_TEMPLATE_L2_INNER_VLAN_DE",1)
        setkey('vlan1','vlan',"KEY_TEMPLATE_L2_INNER_VLAN_VID",12)
        setkey('l2proto',None,"KEY_TEMPLATE_L3_TYPE",16)
        setkey('l3','src',"KEY_TEMPLATE_L3_SIP",32)
        setkey('l3','dst',"KEY_TEMPLATE_L3_DIP",32)
        setkey('l3proto',None,"KEY_TEMPLATE_L3_PROT",8)
        setkey('l3ttl',None,"KEY_TEMPLATE_L3_TTL",8)
        setkey('l3tos',None,"KEY_TEMPLATE_L3_TOS",8)
        setkey('l3flow',None,"KEY_TEMPLATE_L3_FLOW",20)
        setkey('ipv4',"flags","KEY_TEMPLATE_L3_FRAG",1)
        setkey('ipv6ext',None,"KEY_TEMPLATE_L3_EXT_HD_VALID",1)
        setkey('l4sport1',None,"KEY_TEMPLATE_L4_SPORT1",8)
        setkey('l4sport2',None,"KEY_TEMPLATE_L4_SPORT2",8)
        setkey('l4dport',None,"KEY_TEMPLATE_L4_DPORT",16)
        setkey('l4flag',None,"KEY_TEMPLATE_L4_FLAGS",9)
        setkey('xxxx','xxx',"KEY_TEMPLATE_UDF0_EN",1)
        setkey('xxxx','xxx',"KEY_TEMPLATE_UDF0_SEL",17)
        setkey('xxxx','xxx',"KEY_TEMPLATE_UDF1_EN",1)
        setkey('xxxx','xxx',"KEY_TEMPLATE_UDF1_SEL",17)
        setkey('xxxx','xxx',"KEY_TEMPLATE_UDF2_EN",1)
        setkey('xxxx','xxx',"KEY_TEMPLATE_UDF2_SEL",17)
        setkey('xxxx','xxx',"KEY_TEMPLATE_UDF3_EN",1)
        setkey('xxxx','xxx',"KEY_TEMPLATE_UDF3_SEL",17)
        setkey('xxxx','xxx',"KEY_TEMPLATE_UDF4_EN",1)
        setkey('xxxx','xxx',"KEY_TEMPLATE_UDF4_SEL",17)
        setkey('xxxx','xxx',"KEY_TEMPLATE_UDF5_EN",1)
        setkey('xxxx','xxx',"KEY_TEMPLATE_UDF5_SEL",17)
        setkey('xxxx','xxx',"KEY_TEMPLATE_UDF6_EN",1)
        setkey('xxxx','xxx',"KEY_TEMPLATE_UDF6_SEL",17)
        setkey('xxxx','xxx',"KEY_TEMPLATE_UDF7_EN",1)
        setkey('xxxx','xxx',"KEY_TEMPLATE_UDF7_SEL",17)
        setkey('xxxx','xxx',"KEY_TEMPLATE_RANGE_CHECK_TYPE0",4)
        setkey('xxxx','xxx',"KEY_TEMPLATE_RANGE_CHECK_TYPE1",4)

        return idict

    @staticmethod
    def getEmKeyTpid(itype = None, keylen = None):
        #列表分别表示对应的PROFILE_EM_KEY_LEN，em tbl_id em key_len
        #tbl_id=0,表示边长，1，2，3，4表示定长
        val = {
            'default':
            {'768bits':[3,0,96]},
            'fix': 
            {'128bits':[0,4,16],
             '256bits':[1,3,32],
             '512bits':[2,2,64],
             '768bits':[3,1,96],
            },
            'change':
            {'128bits':[0,0,16],
             '256bits':[1,0,32],
             '512bits':[2,0,64],
             '768bits':[3,0,96],
            }
        }
        return val[itype][keylen]

    @staticmethod
    def getEmKey(pkt,template,iemkeypara=None,config=dict()):
        '''根据template获取pkt的key
        '''
        pkt = corsica_dpe.getPacket(pkt)
        info = corsica_dpe.paserPacket(pkt)
        keytemplate = template
        if 'table' in template:
            keytemplate = template['table']
        emkey = []

        def setkey(x,y,k,ilen):
            if not keytemplate.get(k,0): return
            if 'L3_SIP' in k or 'L3_SIP' in k or 'L3_DIP' in k or 'L3_DIP' in k:
                if x in info and type(info[x]) == IPv6 : ilen = 128
            #如果被设置了 ，使用设置的
            if k in config:
                emkey.append((config[k],ilen,k))
                return
            elif x not in info:
                emkey.append((0,ilen,k))
                return
            val = info[x]
            #判断是否 为报文类型
            if isinstance(info[x],Packet):
                t,v = val.getfield_and_val(y)
                if isinstance(t,Emph):
                    t= t.fld
                ibyte = t.i2m(val,v)
                try:
                    l= t.size
                except :
                    l = t.sz * 8
                if 'L3_FRAG' in k   : ibyte = ibyte&1 ; l = 1
                if 'VLAN_TPID' in k : ibyte = corsica_dpe.getvlantpid(val.type)
            else:
                ibyte = val
                if 'TUNNEL_TYPE' in k: ibyte,l = corsica_dpe.getTypeid('tunnel',val)
                
            if ilen > 0 : l = ilen
            emkey.append((ibyte,l,k))

        templateinfo = corsica_dpe.getKeyTemplateInfo()
        kinfo = templateinfo['value']
        for k in templateinfo['list']:
            setkey(kinfo[k]['key'], kinfo[k]['field'],k,kinfo[k]['len'])

        ilen = 0 ; inum64 = 0; ibits = 0; ikey64 = []
        #需要在这里处理字符拼接
        for x,y,_ in emkey:
            x1,x2 = x,None
            y1,y2 = y,None
            if y > 64 : y1 = 64 ; y2 = y - 64
            if y > 128 : raise AssertionError(f"Can't support {y} > 128")
            if y < 8 and type(x) == bytes : raise AssertionError(f"Error")
            if type(x) == bytes:
                if y > 64:
                    x1 = int.from_bytes(x[8:],'big')
                    x2 = int.from_bytes(x[:8],'big')                    
                else:
                    x1 = int.from_bytes(x,'big')
            inum64 += x1 << ibits ; ibits += y1
            if ibits >= 64 :
                ikey64.append(inum64 & 0xffffffffffffffff) ; ilen+=64
                inum64 = inum64 >> 64 ; ibits -= 64
            if y > 64:
                inum64 += x2 << ibits ; ibits += y2
                if ibits >= 64 :
                    ikey64.append(inum64 & 0xffffffffffffffff) ; ilen+=64
                inum64 = inum64 >> 64 ; ibits -= 64
        if ibits > 0 :
            ikey64.append(inum64); ilen+=ibits

        
        ikeylist = [0]*(int(iemkeypara[2]/4))
        #ikeylist = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for i,v in enumerate(ikey64):
            ikeylist[i*2]   = v & 0xffffffff
            ikeylist[i*2+1] = v >> 32
        
        #table id =0 表示变长，定长不用设置
        if iemkeypara[1] == 0:
            if iemkeypara[2] == 96   : ikeylist[-1] |= (0x3 << 30)
            elif iemkeypara[2] == 64: ikeylist[-1] |= (0x2 << 30)
            elif iemkeypara[2] == 32: ikeylist[-1] |= (0x1 << 30)
            elif iemkeypara[2] == 16: pass
            
        return ikeylist,ilen

    @staticmethod
    def getKeyMask(itype=None,pkt=None):
        '''设置keymask
        如果为None返回全ff
        1、OT_TUNNEL_TYPE(24),TL_TUNNEL_TYPE(0x1011)
        pkt 从packet中获取IP、IPv6长度信息
        '''
        ikeydict = {}
        keyinfo =  ["KEY_MASK1_L", "KEY_MASK1_H","KEY_MASK2_L","KEY_MASK2_H",
                    "KEY_MASK3_L","KEY_MASK3_H","KEY_MASK4_L","KEY_MASK4_H",
                    "KEY_MASK5_L","KEY_MASK5_H","KEY_MASK6_L","KEY_MASK6_H",
                    "KEY_MASK7_L","KEY_MASK7_H","KEY_MASK8_L","KEY_MASK8_H",
                    "KEY_MASK9_L","KEY_MASK9_H","KEY_MASK10_L","KEY_MASK10_H",
                    "KEY_MASK11_L","KEY_MASK11_H","KEY_MASK12_L","KEY_MASK12_H"]
        ikeylist = [0xffffffff]*len(keyinfo)

        '''
        specmask = False
        if '(' in itype :
            idict = corsica_dpe.tansStrToDict(itype)
            for k,v in idict.items():
                if v != None and 'mask' in v:
                    specmask = True
        '''

        if itype == None or '(' not in itype :
        #if itype == None or specmask == False :
            for i in range(0,len(keyinfo)):
                ikeydict[keyinfo[i]] = ikeylist[i]
            return ikeydict
           
        ilist = itype.split(',')
        idict = dict()
        for i in ilist:
            k = i ; v = None ; l = 0
            if '(' in i:
                tmp = re.search(r"(.*)\((.*)\)",i)
                if tmp:
                    k = 'KEY_TEMPLATE_'+tmp.group(1)
                    v = tmp.group(2)
                    if len(i) == 0 : v = None
                    elif '0x' in v: l = (len(v)-2)*4; v = int(v,16)
                    elif '0b' in v: l = len(v)-2; v = int(v,2)
                    else: v = (1<<int(v)) -1
            if 'L3_SIP' in k or 'L3_DIP' in k:
                if l >32 : idict[k+'len'] = 128
            if k.endswith("SPORT"):
                idict[k+'1'] = v & 0xFF
                idict[k+'2'] = v >> 8
            else:
                idict[k] = v

        if pkt!= None:
            pkt = corsica_dpe.getPacket(pkt)
            info = corsica_dpe.paserPacket(pkt)
        emkey = {"value":[],'len':[],'type':[]}
        def setkey(x,k,ilen):
            if k not in idict: return
            if 'L3_SIP' in k or 'L3_DIP' in k:
                ilen = idict.get(k+'len',ilen)
                if pkt and type(info[x]) == IPv6 :
                    ilen = 128
            emkey['type'].append(k)
            # 如果没有设置就使用默认长度全掩
            emkey['len'].append(ilen)
            if emkey['value'] == None:
                emkey['value'].append((1<<int(emkey['len'])) -1)
            else:
                emkey['value'].append(idict[k])
        
        templateinfo = corsica_dpe.getKeyTemplateInfo()
        kinfo = templateinfo['value']
        for k in templateinfo['list']:
            setkey(kinfo[k]['key'],k,kinfo[k]['len'])

        ilen = 0 ; inum64 = 0; ibits = 0; ikey64 = []
        #需要在这里处理字符拼接
        for x,y in zip(emkey['value'],emkey['len']):
            x1,x2 = x,None
            y1,y2 = y,None
            if y > 64 : y1 = 64 ; y2 = y - 64
            if y > 128 : raise AssertionError(f"Can't support {y} > 128")
            if y < 8 and type(x) == bytes : raise AssertionError(f"Error")
            if type(x) == bytes:
                if y > 64:
                    x1 = int.from_bytes(x[:8],'big')
                    x2 = int.from_bytes(x[8:],'big')
                else:
                    x1 = int.from_bytes(x,'big')
            inum64 += x1 << ibits ; ibits += y1
            if ibits >= 64 :
                ikey64.append(inum64 & 0xffffffffffffffff) ; ilen+=64
                inum64 = inum64 >> 64 ; ibits -= 64
            if y > 64:
                inum64 += x2 << y2 ; ibits += y2
                if ibits >= 64 :
                    ikey64.append(inum64 & 0xffffffffffffffff) ; ilen+=64
                inum64 = inum64 >> 64 ; ibits -= 64
        if ibits > 0 :
            #高位补1
            inum64 = (0xffffffffffffffff << ibits) & 0xffffffffffffffff | inum64
            ikey64.append(inum64); ilen+=ibits
            
        for i,v in enumerate(ikey64):
            ikeylist[i*2]   = v & 0xffffffff
            ikeylist[i*2+1] = v >> 32
        
        for i in range(0,len(keyinfo)):
            ikeydict[keyinfo[i]] = ikeylist[i]
        return ikeydict
    
    @staticmethod
    def transKeyTemplateStrToV(type,v):
        ivalue = {'range_check':
            {'ot_outer_vlan':0,'ot_inner_vlan':1,'tl_outer_vlan':2,'tl_inner_vlan':3,
             'outer_vlan':4,'inner_vlan':5,'ot_l4_sport':6,'ot_l4_dport':7,
             'tl_l4_sport':8,'tl_l4_dport':9,'l4_sport':10,'l4_dport':11,
             'ot_nsh_len':12,'tl_nsh_len':13,'udf0_low_16bits':14,'udf1_low_16bits':15}}
        return ivalue[type][v]
    
    @staticmethod
    def setKeyTemplate(config=None,itype=None):
        ''' 设置key
        1、OT_TUNNEL_TYPE,TL_TUNNEL_TYPE
        2、Packet类型 根据报文设置来进行set
        '''
        typeid = corsica_dpe.getPktType()
        key = config["table"]
        
        specConf = dict() 
        
        if not isinstance(itype,Packet):
            #处理类型1
            
            idict = corsica_dpe.tansStrToDict(itype)
            for k,v in idict.items():
                if v != None:
                    if 'mask' not in v:
                        if 'KEY_TEMPLATE_'+k in ['KEY_TEMPLATE_RANGE_CHECK_TYPE0','KEY_TEMPLATE_RANGE_CHECK_TYPE1']:
                            specConf['KEY_TEMPLATE_'+k] = \
                            corsica_dpe.transKeyTemplateStrToV('range_check',v['type'])
                if k.endswith("SPORT"):
                    key['KEY_TEMPLATE_'+k+'1'] = 1
                    key['KEY_TEMPLATE_'+k+'2'] = 1
                else:
                    key['KEY_TEMPLATE_'+k] = 1
                    
            return config,specConf
            
            '''
            tmp = re.sub(r'\(.*\)','',itype)
            if '_' in tmp:
                ilist = itype.split(',')
                
                for i in ilist:
                    if '(' in i:
                        tmp1 = re.search(r"(.*)\((.*)\)",i)
                        if tmp1:
                            k = 'KEY_TEMPLATE_'+tmp1.group(1)
                            v = tmp1.group(2)
                            specConf[k] = v
                            key[k] = 1 
                    else:                                           
                        if i.endswith("SPORT"):
                            key['KEY_TEMPLATE_'+i+'1'] = 1
                            key['KEY_TEMPLATE_'+i+'2'] = 1
                        else:
                            key['KEY_TEMPLATE_'+i] = 1
                return config,specConf
            '''
        #处理报文格式
        pkt    = corsica_dpe.getPacketHeader(itype)
        info = corsica_dpe.paserPacket(pkt)
        def setkey(x1,y1,z1):
            if 'L3_TYPE' in z1 : return
            if x1 in info and y1 == None:
                key[z1] = 1
            elif x1 in info and type(info[x1]) == Packet and y1 in info[x1].fields :
                key[z1]=1
        
        templateinfo = corsica_dpe.getKeyTemplateInfo()
        kinfo = templateinfo['value']
        for k in templateinfo['list']:
            setkey(kinfo[k]['key'], kinfo[k]['field'],k)
       
        return config,specConf

    @staticmethod
    def getProfileDefaultTemplates(name):
        '''
        没有表示不关心
        Eth.2VLAN.L2p5.L3.L3p5.L4.Tunnel.L5p5.Eth.2VLAN.L2p5.L3.L3p5.L4.Tunnel.L5p5.Eth.2VLAN.L2p5.L3.L3p5.L4
        Eth.2VLAN.IP.UDP.Tunnel.Eth.2Vlan.IPv6.UDP.Tunnel.Eth.2Vlan.IP.UDP
        L2.5 : MPLS/PPPoE-Discovery/PPPoE-Session/User1...User5 L2.5Header1
        L3 : frag / no_frag&option / Ip_normal /Ipv6_ext / Ipv6 normal/ arp / rocev1 / user1 ... user8  L3Header1
        L3.5 : IFA2.0 / user1 ... user7 L3.5Header1
        L4 : ICMP/IGMP/TCP/UDP/ICMP6/SCTP/user1 ... user8 L4Header1
        Tunnel : NoTunnel/Vxlan/geneve/nvgre/gre/ipinip/vxlan-gpe/Gre-Tencent/vxlan-ali/user3 ... user8 TunnelHeader3
        L5.5 : NoL5.5/NSH/user1 ... user6 L5.5Header1
        '''
        typeid = corsica_dpe.getPktType()
        linkall = lambda x,y : [f"{a}.{b}" for a,b in itertools.product(x,y)]
        link = lambda x,y : [f"{a}.{b}" for a,b in set.union(set(itertools.product(x[0:1],y)),set(itertools.product(x,y[0:1])))]
        link0 = lambda x,y : [f"{x[0]}.{b}" for b in y] #取x第一个进行组合

        l2   = link0(typeid['l2'],typeid['l2_vlan']) #['eth','eth1','eth2', 'eth.vlan', 'eth.2vlan']
        ipv4 = link0(typeid['l3_ipv4'],typeid['l4_ipv4'])#['ipv4.icmp', 'ipv4.igmp', 'ipv4.tcp', 'ipv4.udp', 'ipv4.sctp']
        ipv6 = link0(typeid['l3_ipv6'],typeid['l4_ipv6'])#['ipv6', 'ipv6-ext', 'ipv6.tcp', 'ipv6.udp', 'ipv6.icmp6', 'ipv6.sctp']
        
        tunnel_type = ['L3.tunnel','L3.L4.notunnel','L3.L4.tunnel',
                   'ipv4.udp.vxlan','ipv4.udp.geneve','ipv4.nvgre',
                   'ipv4.gre','ipv4','ipv4.udp.vxlan-gpe','ipv4.gre-tencent','ipv4.udp.vxlan-ali']
        tunnel_head_2vlan = link0(['eth.2vlan'],tunnel_type)
        one_tunnel = [f"{a}.eth.2vlan.ipv4.udp" for a in tunnel_head_2vlan]
        two_tunnel = [f"eth.2vlan.ipv4.upd.vxlan.{a}" for a in one_tunnel]

        packet = {
            'noeth':['noeth'],
            'l2' :['eth','eth1','eth2'],
            'l2_vlan' :['eth.vlan', 'eth.2vlan'],
            'l2p5' : ['eth.mpls','eth.pppoe-discovery','eth.pppoe-session'],
            'l3_ipv4':['eth.ipv4','eth.ipv4-frag', 'eth.ipv4-option'],
            'l3_ipv6':['eth.ipv6', 'eth.ipv6-ext',],
            'l3_other':['eth.arp','eth.rocev1'],
            'l3p5':['ifa2'],
            'l4_ipv4'      : link0(['eth'],ipv4),
            'l4_2vlan_ipv4': link0(['eth.2vlan'],ipv4),
            'l4_ipv6':['eth.ipv6.tcp', 'eth.ipv6.udp', 'eth.ipv6.icmp6', 'eth.ipv6.sctp',
                       'eth.vlan.ipv6.udp','eth.2vlan.ipv6.udp'],
            'notunnel' :['eth.2vlan.L3.notunnel','eth.2vlan.ipv4.L4.notunnel'],
            'tunnel' : one_tunnel,
            '2tunnel':two_tunnel,
            'nol5p5':['nol5.5'],
            'long':[
                'Eth.2VLAN.Mpls.ipv4.Udp.vxlan.Eth.2VLAN.ipv4.udp.vxlan.Eth.2VLAN.ipv4.tcp'
            ],
            'l5p5' :[
                'Eth.2VLAN.Mpls.ipv4.ifa2.Udp.vxlan.nsh.Eth.2VLAN.Mpls.ipv4.ifa2.udp.vxlan.nsh.Eth.2VLAN.mpls.ipv4.ifa2.udp',
                'Eth.2VLAN.Mpls.L3.L4.Tunnel.L5p5.Eth.2VLAN.L2p5.L3.L3p5.L4.Tunnel.L5p5.Eth.2VLAN.L2p5.L3.L3p5.L4']
            }
        list1 =['noeth','l2', 'l2_vlan','l3_ipv4','l3_other']
        ret = []
        for i in list1:
            ret += packet[i]
        return ret

    @staticmethod
    def createProfileTemplate(groupid,profileid,itype):
        profile = {
            "key": {
                "PROFILE_GROUP_INDEX": groupid,
                "PROFILE_KEY_BUILD_PROFILE_ID": profileid,
            },
            "mask": {
                "PROFILE_GROUP_INDEX": 255,
                "PROFILE_KEY_BUILD_PROFILE_ID": 255,
            }
        }
        return corsica_dpe.setProfileTemplate(profile,itype)
    
    @staticmethod
    def getEmActionTypeid(layer=None,itype=None,idata = None):
        typeid = {
            'l2encap' :{'None':0,'encap':1},
            'l3encap':{'None':0,'ipv4':2,'ipv6':3},
            'l3proto':{'ipv4':4,'ipv6':41,'udp':17},
            'l4encap':{'ipv4-frag':0,'ipv4-option':1,'ipv4':2,'ipv6-ext':3,'ipv6':4,'arp':5,'rocev1':6},
            'tunlencap':{ 'None': [0] , 'common': [1,128], 'vxlan':[2,8], 'geneve':[3,128], 'nvgre':[4,8], 'gre':[5,16], 
                        'v4inv4':[6,0], 'v4inv6':[7,0], 'vxlan-gpe+nsh':[8], 'gre+nsh':[9], 'vxlan-gpe':[10,8],
                        'l2+nsh':[11], 'v6inv4':[12,0], 'v6inv6':[13,0], 'gre-ten':[14,16]},
            'tunldecap':{ 'None': 0 , 'ot_l2': 1, 'ot_l3':2, 'ot_l4':3, 'ot_tun':4, 'ot_l5.5':5, 'tl_l2':6, 
                      'tl_l3':7, 'tl_l4':8, 'tl_tun':9, 'tl_l5.5':10, 'l2':11, 'l3':12, 'l4':13},
            'updfield_layer':{ 'ot_l2.5': 0 , 'ot_l3': 1, 'ot_l3.5':2, 'ot_l4':3, 'ot_tun':4, 'ot_l5.5':5, 'tl_l2.5':6, 
                      'tl_l3':7, 'tl_l3.5':8, 'tl_l4':9, 'tl_tun':10, 'tl_l5.5':11, 'l2.5':12, 'l3':13, 'l3.5':14,'l4':15},
            'updfield_offset':{
                'l3': {'version':0,'tos':16,'dscp':8,'ecn':14,'totallen':16,'identify':32,'flag':48,'ttl':64,'src':96,'dst':128},
                'tun_vxlan': {'vni': 0},
                'tun': {'seqence_number': 96},
                'l4': {'sport': 0, 'dport':16}
            },                
            'updfield_opcode':{ 'set': 0 , 'add': 1, 'sub':2},
        }
        
        if itype == 'tunlencap':
            return typeid[layer][itype][idata]
        return typeid[layer][itype]
    
    @staticmethod
    def setEmActionUpdateFieldReg(config=None,val=0,register=0):
        value = {
                    "tbl_pipe": 0,
                    "key": {
                        "REG_TYPE": DPE_IPIPE_GRP0_CSR,
                        "REG_ID": register
                    },
                    "table": {
                        "REG_VALUE": val
                    }
        }

        config['group'].append(value)
            
        return config

    @staticmethod
    def getMaskByOffset(offset=0):
        for i in range(offset):
            mask =+ offset<<1
        return mask  

    @staticmethod
    def getEmActionUpdateField(config=None,info=None, type='dst',regconf=None,mask_template_id=15):       
        #src_mode必须携带
        #立即数,使用立即数的时候，是从目标位置起始取32bit，去set/add/sub 立即数的，不使用长度；这32bit中要改写的bit通过mask控制
        if type == 'src' and config['src'] and config['src']['src_mode'] == 'data':
            data = config['src'].get('data',random.randint(0,0xffffffff))
            data = 0x01020304
            mask = config['src'].get('mask','0xffffffff')
            mask = int(mask,16)
            #mask_template_id = mask_template_id + 1   #全局16个
            corsica_dpe.setEmActionUpdateFieldReg(regconf,mask,\
                PIPE_GRP_CSR_UPDATE_FIELD_MASK_CFG_00_REG+mask_template_id) #PIPE_GRP_CSR_UPDATE_FIELD_MASK_CFG_15_REG
            data = (data & mask)
            config.setdefault('modsrc', data)  
            config.setdefault('mask_template_id', mask_template_id)
        #域段
        else:
            #重新计算校验报文
            #newfieldvalue = info[layer].getfieldval(field)
            layer = config[type].get('layer','ot_l3')
            layer_sel = corsica_dpe.getEmActionTypeid('updfield_layer', layer)

            layeroffset = layer
            ret =re.search(r"(.+)\_(.+)", layeroffset)
            if ret:
                layeroffset = ret.group(2)
            field = config[type].get('field','dst')
            #fieldvalue = info[layer].getfieldval(field) #保存就值
            fieldvalue = 0

            if type == 'dst':
                config.setdefault('moddst', fieldvalue)
            else:
                config.setdefault('modsrc', fieldvalue)  
            #选取的层上取的域段相对于header起始位置的偏移
            fieldoffset = corsica_dpe.getEmActionTypeid('updfield_offset', layeroffset)
            fieldoffset = fieldoffset[field]
            
            #用户配置的相对于字段的便宜
            valoffset = int(config[type].get('offset','0'))
            if valoffset != 0: #还有偏移，掩掉该bit位
                modmask = corsica_dpe.getMaskByOffset(valoffset)
                if type == 'src':
                    config['modsrc'] = config['modsrc'] & modmask          

            offset = fieldoffset + valoffset
            offset = int(offset/4) #必须是4的整数倍
           
            width = int(config[type].get('width','32'))
            #模板定义 
            # bit[3:0]:域段，bit[8:4]:长度，bit[16:9]:offset，bit[20:17]:mask模板号，
            # bit[21:21]:use_mask,bit[23:22]:op_code, bit[24:24]:source_data_mode, 共26bits      
                       
            if width % 4 !=0 :
                #设置长度掩码寄存器
                length = width % 4
                fieldlenmask = 1 << width
                #config['dst']['fieldlenmask'] = fieldlenmask
                use_mask = 1
                corsica_dpe.setEmActionUpdateFieldReg(regconf,fieldlenmask,\
                    PIPE_GRP_CSR_UPDATE_FIELD_MASK_CFG_00_REG+mask_template_id)
            else:
                length = int(width/4)-1
                use_mask = 0
        
            #offset = int(offset/4) #必须是4的整数倍

            op_code = corsica_dpe.getEmActionTypeid('updfield_opcode',config.get('opcode','set'))
            
            if config['src']['src_mode'] == 'data':
                source_data_mode = 0
                use_mask = 1
                mask_template_id = config['mask_template_id']
            else: 
                source_data_mode = 1

            if use_mask == 0:
                mask_template_id = 0
        
            data = (source_data_mode << 24) + (op_code << 22) + (use_mask << 21) + (mask_template_id << 17) + (offset << 9) + (length << 4) + layer_sel                       
            
            if type == 'dst':
                #取出待修改字段的长度，分为修改长度大于字段长度，修改长度小于等于字段长度,待修改
                #if width > fieldlen:
                #    remainlen = width - fieldlen                

                if valoffset == 0:
                    if op_code == 0: #set
                        newfieldvalue = config['modsrc']
                    elif op_code == 1: #add
                        newfieldvalue = config['moddst'] + config['modsrc']
                    else:#sub
                        newfieldvalue = config['moddst'] - config['modsrc']
                else:
                    modmask = corsica_dpe.getMaskByOffset(valoffset)
                    modval = config['moddst'] & modmask
                    if op_code == 0: #set
                        modval = config['modsrc']
                    elif op_code == 0: #add
                        modval = modval + config['modsrc']
                    else:#sub
                        modval = modval - config['modsrc']
                    
                    newfieldvalue = (config['moddst'] & (~modmask) + modval) >> (32-width)
        
                #info[layer].setfieldval(field, newfieldvalue)

        return data
    
    @staticmethod
    def getEmActionTunlEncapValue(config=None):
        type = config['type']
        #tunnel = corsica_dpe.getPacket(type)
        tunnel = None
        if type =='vxlan':
            tunnel= VXLAN(flags=0xc,vni=random.randint(0x700001,0xfffffe))
        elif type =='geneve':
            tunnel = GENEVE(vni=random.randint(0x700001,0xfffffe))
            #nextproto = config.get('nextproto','eth')
            #proto = corsica_dpe.getEmActionTypeid('tunlproto', nextproto)
            #tunnel.proto= proto
            optlen = config.get('optlen',0)
            if optlen != 0:
                optstart = random.randint(0x11223344,0x22334455)
                opt = bytes()
                for i in range(optlen):
                    data = optstart+i
                    opt += data.to_bytes(4,'big', signed=False)
                tunnel.optionlen= optlen
                tunnel.options = opt
        elif type =='gre':
            tunnel = GRE(key_present=1,seqnum_present=1,key=0x21329809,seqence_number=0x98765321)
            #nextproto = config.get('nextproto','eth')
            #proto = corsica_dpe.getEmActionTypeid('tunlproto', nextproto)
            #tunnel.proto= proto           
        elif type =='nvgre':
            tunnel = GRE(key_present=1,key=0x7FFFF200,proto=0x6558)
        elif type =='gre-tencent':
            tunnel =  GRE(key_present=1,seqnum_present=1,key=0x2132980A)
        elif type =='vxlan-gpe':
            tunnel =  VXLAN(flags=0xc,vni=0x7FFFFE)
        return tunnel 
    
    def getEmActionVlan(config): 
        value = {
            'pri': random.randint(0,7),
            'tpid': 0x8100,
            'inherit': 0,
            'cfi': random.randint(0,1),
            'vid': random.randint(0,4094)
        }
        
        for k,v in value.items():
            if k in config:
                  continue
            else :
               config[k] = v 
        
        return config
    
    def getEmActionVlanPrio(k = None, config=None,layer=None,info=None):
        inherit = config.get('inherit',0)
        
        #设置默认值            
        corsica_dpe.getEmActionVlan(config)
           
        pri = config['pri']
        
        isinherit = False
        
        #add vlan:
        #if inherit == 0:
            #add vlan: 从封装表中获取pri
            #if layer+'vlan' not in info:
                #pri = config.get('pri',random.randint(0,7))
            #replace vlan: 不修改pri
            #else:
                #pri = config.get('pri',random.randint(0,7))
        #表示从封装表中获取PRI
        #elif inherit == 1:   
            #pri = config.get('pri',random.randint(0,7)) 
        #从内层vlan继承，如果本身已经是内层vlan则从内层ipv4/ipv6 dscp继承，如果没有内层dscp，则从封装表中获取pri
        if inherit == 2: 
            #两层vlan,从内层继承
            if layer + 'vlan1'in info:
                pri =  info[layer + 'vlan1'].prio
                isinherit = True
            #一层vlan,从内层ipv4/ipv6 dscp继承，如果没有内层dscp，则从封装表中获取pri
            else:
                if k == 'REPLACE_INNER_VLAN' or (k == 'REPLACE_OUTER_VLAN' and layer + 'vlan' not in info):
                    if layer+'l3' in info  and type(info[layer+'l3']) in [IP,IPv6]:
                        pri = (info[layer+'l3'].tos >> 2)%8
                        isinherit = True
                    else:
                        pri = pri
                elif k == 'REPLACE_OUTER_VLAN':
                    pri = info[layer+'vlan'].prio
                
        #从内层dscp映射，如果内层没有dscp，则从封装表获取PRI
        elif inherit == 3:
            if layer+'l3' in info  and type(info[layer+'l3']) in [IP,IPv6]:
                pri = (info[layer+'l3'].tos >> 2)%8
                isinherit = True
            else:
                pri = pri
                
        if isinherit:
            config['pri'] = pri + 1   #修改封装表中的值和继承的值不一致                                
        return pri 
    
    def getEmActionVtagType(config=None,layer=None,info=None):
        #设置默认值            
        vtype = config.get('type', 0)
        value = [
            {'copy': 1, 'inherit': 0},
            {'add': 1, 'inherit': 0},
            {'add': 1, 'inherit': 1},
            {'add': 1, 'inherit': 2},
            {'add': 2, 'inherit': 0},
            {'add': 2, 'inherit': 2},
        ]
        
        #根据类型匹配动作,补充随机值
        conf1 = None
        conf2 = None
        conf = value[vtype]
        if 'add' in conf and conf['add'] == 1:
            conf1 = corsica_dpe.getEmActionVlan(conf)
        elif 'add' in conf and conf['add'] == 2:
            conf1 = corsica_dpe.getEmActionVlan(conf)
            conf2 = corsica_dpe.getEmActionVlan(conf)
        elif 'copy' in conf and conf['copy'] == 1:
            if info['tunnel_number'] == 0:
                if 'ot_vlan' in info:
                    config['type'] = 1
                    info['ot_vlan'].remove_payload()
                    return info['ot_vlan']

            if info['tunnel_number'] >= 1 :
                if 'tl_vlan1' in info:
                    config['type'] = 4
                    info['tl_vlan'].remove_payload()
                    info['tl_vlan1'].remove_payload()
                    return info['tl_vlan']/info['tl_vlan1']
                else:
                    config['type'] = 1
                    info['tl_vlan'].remove_payload() 
                    return info['tl_vlan']

        newvlan1 = Dot1Q(prio=conf1['pri'],id=conf1['cfi'],vlan=conf1['vid']) 

        #PRI继承内层VLAN
        #PRI继承内层VLAN ID， 但是没有内层vlan， 或者总共只有一层vlan。 PRI使用默认值（默认值是单独使用寄存器设置）
        if conf['inherit'] == 1:
            if layer + 'vlan1'not in info and layer + 'vlan' in info:
                newvlan1.prio = info[layer + 'vlan'].prio
            else:
                newvlan1.prio = 0    #寄存器默认为0，后面补充
        if conf['inherit'] == 2:
            if layer+'l3' in info  and type(info[layer+'l3']) in [IP,IPv6]:
                newvlan1.prio = (info[layer+'l3'].tos >> 2)%8

        if conf2 != None:
            newvlan2 = Dot1Q(prio=conf1['pri'],id=conf1['cfi'],vlan=conf1['vid']) 
            if conf['inherit'] == 2:
                if layer+'l3' in info  and type(info[layer+'l3']) in [IP,IPv6]:
                    newvlan2.prio = (info[layer+'l3'].tos >> 2)%8
            return newvlan1/newvlan2
        
        if conf['add'] == 1:
            return newvlan1
        
    @staticmethod
    def getDefaultActionPacket(pkt,config,regconf=None,layer="ot"):
        '''根据default action 修改报文
        '''
        if "table" in config:
            config = config["table"]
        if layer.lower() == "ot": layer = "ot_"
        elif layer.lower() == "tl": layer = "tl_"
        else: layer= ""

        if 'data' in config:
            raise AssertionError("Not SUPPORT")

        ttl = random.randint(0,255)  
        tos = random.randint(0,255) 
        
        #检查是否是继承
        isinherit = lambda x : \
            True if 'inherit' in x and x['inherit'] == 1 else False
                   
        #defaultInfo = corsica_dpe.getDefaultEmActionInfo()
        p = pkt.copy()
        info = corsica_dpe.paserPacket(p)
        for k,v in config.items():
            if type(v) != dict:
                v = corsica_dpe.value_check(k,v)
            if layer+'l2' in info:
                p2 = info[layer+'l2']
            if layer+'l3' in info:
                p3 = info[layer+'l3']
            if layer+'l4' in info:
                p4 = info[layer+'l4']
            if v == 0 :continue
            if "REPLACE_L4_DPORT" == k and type(p4) in [UDP,TCP,SCTP]:
                p4.dport = v
            elif "REPLACE_L4_SPORT" == k and type(p4) in [UDP,TCP,SCTP]:
                p4.sport = v
            elif "REPLACE_DIPV4" == k and type(p3) in [IP]:
                p3.dst = int2ip(v)
            elif "REPLACE_SIPV4" == k and type(p3) in [IP]:
                p3.src = int2ip(v)
            elif "REPLACE_DIPV6" == k and type(p3) in [IPv6]:
                p3.dst = corsica_dpe.int2ipv62(v)
            elif "REPLACE_SIPV6" == k and type(p3) in [IPv6]:
                p3.src = corsica_dpe.int2ipv62(v)
            elif "TTL_UPDATE" == k and type(p3) in [IP]:
                opcode = v.get('opcode',0) 
                if 'ttl' in v : newttl = v.get('ttl',0) 
                else: newttl =ttl              
                #opcode = 0 如果TTL<=1， 则重定向接口(用TTL UPDATE 的field中的重定向目的替换原destination)，
                # 此时action type固定填写单播；如果TTL>1,则当前外层L3 TTL/Hop limit减1，需要更新ipv4头Checksum
                if opcode == 0:
                    if type(p3)  == IP:
                        if p3.ttl > 1:
                            p3.ttl = p3.ttl - 1
                        else: #重定向
                            v['redirect'] = config['DESTINATION']
                    elif type(p3)  == IPv6:
                        if p3.hlim > 1:
                            p3.hlim = p3.hlim - 1
                elif opcode == 1:  #sub
                    if type(p3)  == IP:
                        if p3.ttl > 1:
                            p3.ttl = p3.ttl - 1 
                    elif type(p3)  == IPv6:
                        if p3.hlim > 1:
                            p3.hlim = p3.hlim - 1 
                elif opcode == 2:   #set
                    if type(p3)  == IP:   p3.ttl =   newttl
                    elif type(p3)  == IPv6: p3.hlim = newttl            
            elif "TOS_UPDATE" == k and type(p3) in [IP]: 
                mask = v.get('mask',0)    
                tos = v.get('tos',0)           
                if type(p3)  == IP:
                    p3.tos =  (p3.tos & (mask^0xFF))| (tos & mask)
                elif type(p3)  == IPv6:
                    p3.tc =  (p3.tc & (mask^0xFF))| (tos & mask)    
            elif "REMOVE_OUTER_VLAN" == k and type(p2) in [Ether]:
                #两层vlan
                if layer+'vlan1' in info:
                    p2[Ether].remove_payload()
                    p2[Ether].add_payload(info[layer + 'vlan1'])
                    info[layer + 'vlan1'] == None     #变成一层vlan
                #一层vlan
                elif layer+'vlan' in info:
                    p2[Ether].remove_payload()
                    p2[Ether].add_payload(p3)  
                    info[layer + 'vlan'] == None     #变成无vlan      
            elif "REMOVE_INNER_VLAN" == k and type(p2) in [Ether]: #如果Remove Outer VLAN有效，当前操作是基于在Remove Outer VLAN动作之后的vlan层数再做判断
                #两层vlan
                if layer+'vlan1' in info:
                    p2[Ether].remove_payload()
                    info[layer + 'vlan'].remove_payload()   #删除内层vlan
                    #info.setdefault(layer + 'vlan', info[layer + 'vlan1'].add_paylaod(p3))
                    #info[layer + 'vlan'] = info[layer + 'vlan1']  #变成单层vlan  
                    info[layer + 'vlan'].add_payload(p3)   #删除内层vlan
                    p2[Ether].add_payload(info[layer + 'vlan'])
                    info[layer + 'vlan1'] == None            #变成无vlan
                elif layer+'vlan' in info:
                    p2[Ether].remove_payload()
                    p2[Ether].add_payload(p3)
                    info[layer + 'vlan'] == None
            elif "REPLACE_INNER_VLAN" == k and type(p2) in [Ether]:                
                if type(v) == dict:
                    chkpri = corsica_dpe.getEmActionVlanPrio(k,v,layer,info) #替换后的pri
                    #tpid = corsica_dpe.getvlantpid(v['tpid'])
                    inherit = v.get('inherit',0)
                    pri = v.get('pri',0) #封装表中填的pri
                    cfi = v.get('cfi',0)
                    vid = v.get('vid',0)
                    if 'mask' in v: mask = v['mask']
                    else: mask = 0x07
                    #一层/两层vlan，替换内层vlan
                    if layer+'vlan1' in info :
                        if inherit != 0: #0不修改pri
                            info[layer+'vlan1'].prio = chkpri
                        if mask & 0x04:
                            info[layer+'vlan'].type = v['tpid']
                        if mask & 0x02:    
                            info[layer+'vlan1'].id = cfi
                        if mask & 0x01:
                            info[layer+'vlan1'].vlan = vid  

                    elif layer+'vlan' in info:
                        if inherit != 0: #0不修改pri
                            info[layer+'vlan'].prio = chkpri
                        if mask & 0x04:
                            p2[Ether].type = v['tpid']
                        if mask & 0x02:    
                            info[layer+'vlan'].id = cfi
                        if mask & 0x01:
                            info[layer+'vlan'].vlan = vid
                    else:
                        #添加的vlan信息，其它vlan类型待添加
                        if v['tpid'] == 0x8100:   #scapy支持
                            newvlan = Dot1Q(prio=chkpri,id=cfi,vlan=vid)
                            
                        info[layer+'vlan'] = newvlan
                        p2[Ether].remove_payload()
                        p = p2/info[layer+'vlan']
                        if layer+'l3' in info:
                            p = p/p3  

            elif "REPLACE_OUTER_VLAN" == k and type(p2) in [Ether]:
                if type(v) == dict:
                    chkpri = corsica_dpe.getEmActionVlanPrio(k,v,layer,info) #替换后的pri
                    #tpid = corsica_dpe.getvlantpid(v['tpid'])
                    inherit = v.get('inherit',0)
                    pri = v.get('pri',0) #封装表中填的pri
                    cfi = v.get('cfi',0)
                    vid = v.get('vid',0)
                
                    if 'mask' in v: mask = v['mask'] 
                    else: mask = 0x07
                    #两层vlan，替换外层vlan
                    if layer+'vlan1' in info:
                        if inherit != 0: #0不修改pri
                            info[layer+'vlan'].prio = chkpri
                        if mask & 0x04:
                            p2[Ether].type = v['tpid']    
                        if mask & 0x02:
                            info[layer+'vlan'].id = cfi 
                        if mask & 0x01:
                            info[layer+'vlan'].vlan = vid
                    #0/1层vlan，添加一层valn(添加的vlan做外层vlan，原vlan做内层vlan)
                    else:
                        #添加的vlan信息
                        if v['tpid'] == 0x8100:   #scapy支持
                            newvlan = Dot1Q(prio=chkpri,id=cfi,vlan=vid)
                        
                        #0层vlan，添加一层vlan
                        if layer+'vlan' not in info:
                            info[layer+'vlan'] = newvlan
                            p2[Ether].remove_payload()
                            p = p2/info[layer+'vlan']
                            if layer+'l3' in info:
                                p = p/p3
                        else:
                            info[layer+'vlan1'] = info[layer+'vlan']   #原来的vlan做內层vlan
                            info[layer+'vlan'] = newvlan
                            p2[Ether].remove_payload()
                            p = p2/info[layer+'vlan']/info[layer+'vlan1']
                            #if layer+'l3' in info:
                            #    p = p/p3                      
            elif "REPLACE_SMAC" == k and type(p2) in [Ether]:
                p2.src = int2mac(v)
            elif "REPLACE_DMAC" == k and type(p2) in [Ether]:
                p2.dst = int2mac(v)
            elif "DEC_NSH_TTL" == k:
                pass
            elif "INT_TUNNEL_DELETE" == k:
                pass
            elif "UPDATE_FIELD" == k:
                config[k] = list()
                
                upd_field_mask_num = 15
                config[k].append(0x10 + 1)
                data = corsica_dpe.getEmActionUpdateField(v, info,'src',regconf,upd_field_mask_num)
                config[k].append(data)
                #upd_field_mask_num = upd_field_mask_num - 1
                data = corsica_dpe.getEmActionUpdateField(v, info,'dst',regconf,upd_field_mask_num)
                corsica_dpe.setEmActionUpdateFieldReg(regconf, data, PIPE_GRP_CSR_UPDATE_FIELD_CFG_01_REG)
                
            elif "TUNNEL_ENCAP_TYPE" == k:
                t = v.get('type','None')
                typev = corsica_dpe.getEmActionTypeid('tunlencap',t,0)
                tunnel = corsica_dpe.getEmActionTunlEncapValue(v)           
                config[k] = list()
                config[k].append(typev[0])

                if tunnel != None:
                    p = tunnel/p
                    if t in ['vxlan','vxlan-gpe','vxlan-ali']:
                        tunnel.NextProtocol = p.NextProtocol
                    else:
                        tunnel.proto = p.proto
                    config[k].append(tunnel)
                    
            elif "TUNNEL_ENCAP_LEN" == k:
                pass
            elif "L4_ENCAP_TYPE" == k:
                itypev = v.get('type',0) 
                sport = v.get('sport',random.randint(0,0xffff))
                dport = v.get('dport',0)
                value = sport<<16 | dport                   
                config[k] = list()
                config[k].append(itypev)
                config[k].append(value)
                if itypev == 6 or itypev == 7:
                    ot_l4 = UDP(dport=dport)   #sport由硬件计算
                else:
                    ot_l4 = UDP(sport =sport,dport=dport)
                p = ot_l4/p
            elif "L3_ENCAP_TYPE" == k:
                t = v.get('type','ipv4')
                itype = corsica_dpe.getEmActionTypeid('l3encap',t)
                  
                if isinherit(v) and type(p3) in [IP, IPv6]:
                    if type(p3) == IP:
                        ttl = p3.ttl
                        tos = p3.tos   
                    if type(p3) == IPv6:
                        ttl = p3.hlim
                        tos = p3.tc         
                #封装IPv4
                if itype == 2:
                    dst = '100.51.%d.%d'%(random.randint(0,250),random.randint(1,250))  
                    ot_l3 = IP(dst=dst,ttl=ttl,tos=tos)
                elif itype == 3:
                    dst = '100:51::%x:%x'%(random.randint(0,250),random.randint(1,250))
                    ot_l3 = IPv6(dst=dst,hlim=ttl,tc=tos)  
                config[k] = list()
                config[k].append(itype)
                
                #重新计算prio
                p = ot_l3/p
                tmp = copy.deepcopy(p)
                tmpinfo =  corsica_dpe.paserPacket(tmp)
                if type(tmpinfo[layer + 'l3']) in [IP]:
                    ot_l3.proto =  tmpinfo[layer + 'l3'].proto
                if type(tmpinfo[layer + 'l3']) in [IPv6]:
                    ot_l3.nh =  tmpinfo[layer + 'l3'].nh
                config[k].append(ot_l3)
            elif "VTAG_TYPE" == k:
                config[k] = list()
                
                vtag = corsica_dpe.getEmActionVtagType(v, layer, info)
                config[k].append(v['type'])
                config[k].append(vtag)
                p = vtag/p
            elif "L2_FLAG" == k:
                #封装表
                dst = '22:24:26:28:%02x:%02x'%(random.randint(0,254),random.randint(1,254))
                #封装配置表
                if isinherit(v):
                    dst = p2[Ether].dst
                    src = p2[Ether].src 
                #if v==1:   #封装L2头
                ot_l2 = Ether(dst=dst)
                p = ot_l2/p
                config[k] = list()
                config[k].append(1)
                config[k].append(ot_l2)
            elif "DECAPSULATION" == k:
                ilayer = v.get('layer','')
                v = corsica_dpe.getEmActionTypeid('tunldecap',ilayer)
                config[k] = v
                p = info[ilayer]
            #重新解析报文
            info = corsica_dpe.paserPacket(p)
        return p

    @staticmethod
    def setDefaultAction(config,action):
        '''根据default action 修改报文
        '''
        conf = config
        if "table" in config:
            conf = config["table"]
        actiondict = corsica_dpe.tansStrToDict(action)

        if 'data' in conf: #不支持data混配
            raise AssertionError("Not SUPPORT")
        
        for k,v in actiondict.items():
            if "UPDATE_FIELD" == k:
                v['src'] = corsica_dpe.tansStrToDict(v['src'])
                v['dst'] = corsica_dpe.tansStrToDict(v['dst'])
            if v != None :
                conf[k] = v
                continue
            if "REPLACE_L4_DPORT" == k:
                v = random.randint(10000,20000)
            elif "REPLACE_L4_SPORT" == k:
                v = random.randint(10000,20000)
            elif "REPLACE_DIPV4" == k:
                v = '100.50.%d.%d'%(random.randint(0,250),random.randint(1,250))
            elif "REPLACE_SIPV4" == k:
                v = '100.50.%d.%d'%(random.randint(0,250),random.randint(1,250))
            elif "REPLACE_DIPV6" == k:
                v = '100:50::%x:%x'%(random.randint(0,250),random.randint(1,250))
            elif "REPLACE_SIPV6" == k:
                v = '100:50::%x:%x'%(random.randint(0,250),random.randint(1,250))
            elif "TTL_UPDATE" == k:
                v= {'ttl': random.randint(0,255)}
            elif "TOS_UPDATE" == k:
                v= {'tos': random.randint(0,255), 'mask': random.randint(0,255)}
            elif "REPLACE_SMAC" == k:
                v = '12:14:16:18:%02x:%02x'%(random.randint(0,254),random.randint(1,254))
            elif "REPLACE_DMAC" == k:
                v = '22:24:26:28:%02x:%02x'%(random.randint(0,254),random.randint(1,254))
            elif "DEC_NSH_TTL"== k:
                v=1
            elif "INT_TUNNEL_DELETE"== k:
                pass
            elif "TUNNEL_ENCAP_TYPE"== k:
                pass
            elif "TUNNEL_ENCAP_LEN" == k:
                v=0
            elif "L4_ENCAP_TYPE" == k:   #只支持UDP,不支持TCP
                v = {'type':4,
                     'sport':random.randint(0,0xffff),
                     'dport':random.randint(0,0xffff)}
            elif "L3_ENCAP_TYPE" == k:                      
                v = {'type':'ipv4'}  
            elif "VTAG_TYPE" == k:
                v = {'type': 1}  
            elif "L2_FLAG" == k:  
                v = {'inherit': 0}                        
            elif "REMOVE_OUTER_VLAN" == k or "REMOVE_INNER_VLAN" == k :
                v = 1     #置位
            elif "REPLACE_OUTER_VLAN"== k or "REPLACE_INNER_VLAN"== k:
                v = {'tpid' : 0x8100, 'inherit': 0, 'vid': random.randint(0,4094)}    #默认 
            elif "ACTION_TYPE" == k:  
                v=0            
            conf[k] = v
        return config
    
    @staticmethod
    def setDscp2PriReg(config):
        value = {
                    "tbl_pipe": 0,
                    "key": {
                        "REG_TYPE": DPE_IPIPE_GRP0_CSR,
                        "REG_ID": PIPE_GRP_CSR_DSCP2PRI_MAP_CFG_00_REG
                    },
                    "table": {
                        "REG_VALUE": 0x00
                    }
        }
        for i in range(0,63):
            tmp = None
            tmp = copy.deepcopy(value)
            tmp['key']['REG_ID']= PIPE_GRP_CSR_DSCP2PRI_MAP_CFG_00_REG + i
            tmp['table']['REG_VALUE'] = i%8
            config['group'].append(tmp)
            
        return config
    
    @staticmethod
    def setTunnelEncapCfgTable(tunnel_encap = None,action = None):
        actiondict = corsica_dpe.tansStrToDict(action)
        #检查是否是继承
        isinherit = lambda x : \
            True if 'inherit' in x and x['inherit'] == 1 else False
        for k,v in actiondict.items():
            if "TUNNEL_ENCAP_TYPE"== k:
                typev = corsica_dpe.getEmActionTypeid('tunlencap',v['type'],0)
                tunnel_encap['key']['TUNNEL_ENCAP_INDEX'] = typev[0]
            if v == None or (not isinherit(v)):
                continue
            if "L3_ENCAP_TYPE"== k:
                #从内层继承
                tunnel_encap['table']['TUNNEL_ENCAP_V4_ID'] =1
                tunnel_encap['table']['TUNNEL_ENCAP_V6_TC'] =1
                tunnel_encap['table']['TUNNEL_ENCAP_V6_HL'] =1
                tunnel_encap['table']['TUNNEL_ENCAP_V4_TOS'] =1
                tunnel_encap['table']['TUNNEL_ENCAP_V4_TTL'] =1
                    #v.pop('inherit')
            elif "VTAG_TYPE"== k:
                #从内层拷贝
                tunnel_encap['table']['TUNNEL_ENCAP_VLAN'] =1
            elif "L2_FLAG"== k:
                #从内层拷贝
                tunnel_encap['table']['TUNNEL_ENCAP_SRC_MAC'] =1
                tunnel_encap['table']['TUNNEL_ENCAP_DST_MAC'] =1
            else:
                continue
            
        return tunnel_encap

if __name__ == '__main__':
    config = {
                "index": 10,
                "table":{
                        "REPLACE_SMAC":"31:32:33:34:35:36",
                }
            }
    pkt = Ether(src='11:12:13:14:15:16',dst='21:22:23:24:25:26')/IP(src='1.2.3.4',dst="5.6.7.8",flags=1)/UDP()
    c = corsica_dpe.getDefaultActionPacket(pkt,config)
    c = corsica_dpe.createData({
        'REPLACE_SMAC' : '11:12:13:14:15:16',
        'REPLACE_DMAC' : 0x212223242526
        })
    if c['data'] != [0x14131211,0x22211615,0x26252423] :raise AssertionError("Error")
    c = corsica_dpe.getPacketLong(Ether(src='11:12:13:14:15:16',dst='21:22:23:24:25:26')/IP(src='1.2.3.4',dst="5.6.7.8",flags=1)/UDP())
    if c != "eth(dst='21:22:23:24:25:26', src='11:12:13:14:15:16').ipv4-frag(flags=1, src='1.2.3.4', dst='5.6.7.8').udp" :
        raise AssertionError("Error")
    template0 = {
        "key": {"KEY_TEMPLATE_INDEX": 12},
        "table": {}
        }
    template = copy.deepcopy(template0)
    pkt = Ether(src='11:12:13:14:15:16',dst='21:22:23:24:25:26')/IP(src='1.2.3.4',dst="5.6.7.8",flags=1)/UDP()
    #template = corsica_dpe.setKeyTemplate(template,pkt)
    template = corsica_dpe.setKeyTemplate(template,"OT_L2_SMAC,OT_L2_DMAC,OT_L3_SIP,OT_L3_DIP,OT_L3_FRAG")
    ikey,ilen  = corsica_dpe.getEmKey(pkt,template)
    if ikey[5] != 0x1 or ilen != 161 :raise AssertionError("Error")

    imask = corsica_dpe.getKeyMask("OT_L2_SMAC(0xFFFF00000000),OT_L2_DMAC(0b1111),OT_L3_SIP(8),OT_L3_DIP,OT_L3_FRAG",pkt)
    if imask['KEY_MASK1_L'] != 0xf or ilen != 161 :raise AssertionError("Error")
    
    template = copy.deepcopy(template0)
    pkt = Ether(src='11:12:13:14:15:16')/IP(src="5.6.7.8",flags=0x1fff)/UDP()/VXLAN(vni=0xfff)/Ether()/IP()
    #template = corsica_dpe.setKeyTemplate(template,pkt)
    template = corsica_dpe.setKeyTemplate(template,"OT_L2_SMAC,OT_L3_SIP,OT_L3_FRAG,OT_TUNNEL_ID,OT_TUNNEL_TYPE")
    ikey,ilen  = corsica_dpe.getEmKey(pkt,template)
    if ikey[0:4] != [0x13141516,0x07081112,0xffc30506,0x3] or ilen != 118 :raise AssertionError("Error")

    c = corsica_dpe.getPacket("eth.ipv4(chksum=1).udp.raw(load=10*'a')")
    if c[IP].chksum != 1 :raise AssertionError("Error")
    ret = corsica_dpe.paserPacket('eth.ipv4.udp.vxlan.eth.ipv4.udp.vxlan.eth.ipv4.udp')
    if ret['in'] != 'eth.ipv4.udp':raise AssertionError("Error")
    ret = corsica_dpe.paserPacket('eth.ipv4.udp.vxlan.eth.ipv4.udp')
    if ret['tl'] != 'eth.ipv4.udp':raise AssertionError("Error")
    ret = corsica_dpe.paserPacket('eth.ipv4.udp')
    if ret['ot'] != 'eth.ipv4.udp':raise AssertionError("Error")
    ret = corsica_dpe.paserPacket(Ether()/IP()/UDP())
    c = corsica_dpe.getPacket("Ether/IP/UDP/(10*'a')")
    if type(c.lastlayer()) != Raw :raise AssertionError("Error")
    c = corsica_dpe.getPacketLong(Ether()/IP()/UDP())
    if c != 'eth.ipv4.udp':raise AssertionError("Error")
    c = corsica_dpe.getPacketLong('ipv4.udp.vxlan.vxlan.eth.ipv4.udp')
    if c != 'eth.ipv4.udp.vxlan.eth.ipv4.udp.vxlan.eth.ipv4.udp':raise AssertionError("Error")
    c = corsica_dpe.getPacketLong('vxlan.vxlan.eth.ipv4.udp')
    if c != 'eth.ipv4.udp.vxlan.eth.ipv4.udp.vxlan.eth.ipv4.udp':raise AssertionError("Error")
    c = corsica_dpe.getPacketLong('vxlan.vxlan.')
    if c != 'eth.ipv4.udp.vxlan.eth.ipv4.udp.vxlan.eth.ipv4.udp':raise AssertionError("Error")
    pktlist = {
            'eth.ipv4'        : 'eth.ipv4',
            'eth.ipv4.udp'    : 'eth.ipv4.udp',
            'eth.ipv6'        : 'eth.ipv6',
            'eth.arp'         : 'eth.ipv4.arp',
            'eth.vlan.ipv4'   : 'eth.vlan.ipv4',
            'eth.2vlan.ipv4'  : 'eth.2vlan.ipv4',
            'vxlan_ipv4'      : 'eth.vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.tcp',
            'geneve_ipv4'     : 'eth.vlan.ipv4.udp.geneve.eth.2vlan.ipv4.udp',
            'nvgre_ipv4'      : 'eth.vlan.ipv4.nvgre.eth.2vlan.ipv4.udp',
            'ipinip_ipv6'     : 'eth.vlan.ipv4.ipv6.udp',
            'gre_ipv6'        : 'eth.vlan.ip.gre.eth.2vlan.ipv6',
            'gre_ten_ipv6'    : 'eth.vlan.ip.gre-tencent.eth.2vlan.ipv6.udp',
            'vxlan_gpe_ipv6'  : 'eth.vlan.ip.udp.vxlan-gpe.eth.2vlan.ipv6.udp',
            'vxlanali_ipv6'   : 'eth.vlan.ip.udp.vxlan-ali.eth.2vlan.ipv6.udp',
            'vxlan_vxlan'     : 'eth.vlan.ip.udp.vxlan.eth.ip.udp.vxlan.eth.2vlan.ipv6.tcp',
            'vxlan_geneve'    : 'eth.vlan.ip.udp.vxlan.eth.ip.udp.geneve.eth.2vlan.ipv6.udp',
            'vxlan_nvgre'     : 'eth.vlan.ip.udp.vxlan.eth.ip.nvgre.eth.2vlan.ipv6.udp',
            'vxlan_ipinip'    : 'eth.vlan.ip.udp.vxlan.eth.ip.ipv6.udp',
            'vxlan_gre'       : 'eth.vlan.ip.udp.vxlan.eth.ip.gre.eth.2vlan.ipv6.udp',
            'vxlan_vxlan_gpe' : 'eth.vlan.ip.udp.vxlan.eth.ip.udp.vxlan-gpe.eth.2vlan.ipv6.udp',
            'vxlan_gre_ten'   : 'eth.vlan.ip.udp.vxlan.eth.ip.gre-tencent.eth.2vlan.ipv6.udp',
            'vxlan_vxlan_ali' : 'eth.vlan.ip.udp.vxlan.eth.ip.udp.vxlan-ali.eth.2vlan.ipv6.udp'
    }
    c = corsica_dpe.getPacketHeader('noeth')
    wrpcap("d:\\a.pcap",c)
    for k,v in pktlist.items():
        pkt = corsica_dpe.getPacket(v,padlen=10)
        print("%s:%s"%(v,pkt.summary()))
        wrpcap("d:\\a.pcap",pkt,append=True)
        pkt1 = corsica_dpe.getBasePkt(k)
        print("%s:%s"%(k,pkt1.summary()))
        wrpcap("d:\\a.pcap",pkt1,append=True)
        
