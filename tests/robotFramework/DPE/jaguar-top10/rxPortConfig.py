#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy , re, random, time, os, subprocess, sys
from pprint import pprint
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from pprint import pprint

from scapy.all import *  
from scapy.contrib.mpls import * # import from contrib folder of scapy 
from scapy.layers.inet6 import *
from scapy.contrib.geneve import GENEVE

class rxPortConfig(object):
    def __init__(self):
        #loc1 = str(BuiltIn().get_variable_value('${cha1port1}'))
        #loc2 = str(BuiltIn().get_variable_value('${cha1port2}'))
        #loc3 = str(BuiltIn().get_variable_value('${cha1port3}'))
        #loc4 = str(BuiltIn().get_variable_value('${cha1port4}'))
        loc1 = 1
        loc2 = 2
        loc3 = 3
        loc4 = 4
        in_port = 1
        out_port = 5
        
        mirrorIndex = 10
        meterIndex = 100
        meterModIndex = 255
        defActionIndex = 10
        emActionIndex = 20
        keyTemplateIndex  = 30

        self.value1 = {
            'reg_table':{
                  'reg':[
                  {"reg_type":'PIPE_GRP_0' , "reg_name":"PIPE_GRP_MEM_CTRL_BUS_00_REG" , "value":0x100},
                  {"reg_type":'PIPE_GRP_1' , "reg_name":"PIPE_GRP_MEM_CTRL_BUS_00_REG" , "value":0x01020304},
                  ] 
                  },                

            'input_rx' : {
                'key' : [
                {'SOURCE_PORT' :  in_port, 
                 'TUNNEL_PKT' : 0},
                ],
                'table' : [
                {'DEF_ACT_IDX' : 0, 
                'OP_CODE' : 0,
                'MEP_CODE' : 0,
                'MEP_TYPE' : 0,
                'ACT_TYPE' : 0,
                'DEF_DST' : out_port, 
                'MIRR_PRI' : 0,
                'MIRR_METER_IDX' : 0,
                'MIRR_IDX' : 0,
                'METE_INFO0' : 0,
                'GROUP_IDX' :   loc1}
                ]
                },
            'classify' : {
                'group':
                [
                    {
                        'tbl_name': "classify",
                        'tbl_id': 0,
                        'tbl_pipe': 0,
                        'priority': 0,
                        'key' : 
                        {
                            'CLASSIFY1_PKT_TYPE' :  0,
                            'CLASSIFY1_PKT_ERROR_FLAG' :  0,
                            'CLASSIFY1_PKT_ERROR_TYPE' :  0,
                            'CLASSIFY1_GROUP_INDEX' :  0,
                            'CLASSIFY1_OUT_TUNNEL_TYPE' :  0,
                            'CLASSIFY1_OUT_L5P5_HEAD_TYPE' :  0,
                            'CLASSIFY1_INNER_TUNNEL_TYPE' :  0,
                            'CLASSIFY1_INNER_L5P5_HEAD_TYPE' :  0,
                            'CLASSIFY1_TUNNEL_ID' :  0,
                            'CLASSIFY1_ADDRESS0' :  0,
                            'CLASSIFY1_ADDRESS1' :  0,
                            'CLASSIFY1_ADDRESS_EXTEND' :  0,
                            'CLASSIFY1_OUT_VLAN_VALID' :  0,
                            'CLASSIFY1_INNER_VLAN_VALID' :  0,
                            'CLASSIFY1_OUT_VLAN_ID' :  0,
                            'CLASSIFY1_OUT_VLAN_TPID' :  0,
                            'CLASSIFY1_INNER_VLAN_ID' :  0,
                            'CLASSIFY1_INNER_VLAN_TPID' : 0,                    
                            'CLASSIFY1_ETH_TYPE' : 2046,
                            'CLASSIFY1_RSV1': 0,
                            'CLASSIFY1_RSV2': 0,
                            'CLASSIFY1_PIPE_ID': 0
                        },          
                        'mask' : 
                        {
                            'CLASSIFY1_PKT_TYPE' :  0,
                            'CLASSIFY1_PKT_ERROR_FLAG' :  0,
                            'CLASSIFY1_PKT_ERROR_TYPE' :  0,
                            'CLASSIFY1_GROUP_INDEX' :  0,
                            'CLASSIFY1_OUT_TUNNEL_TYPE' :  0,
                            'CLASSIFY1_OUT_L5P5_HEAD_TYPE' :  0,
                            'CLASSIFY1_INNER_TUNNEL_TYPE' :  0,
                            'CLASSIFY1_INNER_L5P5_HEAD_TYPE' :  0,
                            'CLASSIFY1_TUNNEL_ID' :  0,
                            'CLASSIFY1_ADDRESS0' :  0,
                            'CLASSIFY1_ADDRESS1' :  0,
                            'CLASSIFY1_ADDRESS_EXTEND' :  0,
                            'CLASSIFY1_OUT_VLAN_VALID' :  0,
                            'CLASSIFY1_INNER_VLAN_VALID' :  0,
                            'CLASSIFY1_OUT_VLAN_ID' :  0,
                            'CLASSIFY1_OUT_VLAN_TPID' :  0,
                            'CLASSIFY1_INNER_VLAN_ID' :  0,
                            'CLASSIFY1_INNER_VLAN_TPID' : 0,                     
                            'CLASSIFY1_ETH_TYPE' : 65535,
                            'CLASSIFY1_RSV1': 0,
                            'CLASSIFY1_RSV2': 0,
                            'CLASSIFY1_PIPE_ID': 1
                        },               
                        'table' : 
                        {
                            'CLASSIFY1_OPRATE_CODE' : 2,
                            'CLASSIFY1_DEFAULT_ACTION_INDEX' : 0,
                            'CLASSIFY1_KEY_BUILD_PROFILE_ID' : 10,
                            'CLASSIFY1_DISTRIBUTE_MODE' : 0,
                            'CLASSIFY1_DISPATCH_TYPE' : 0,
                            'CLASSIFY1_DEFAULT_DEST_VALID' : 0,
                            'CLASSIFY1_DEFAULT_DEST_ACT_TYPE' : 0,
                            'CLASSIFY1_DEFAULT_DEST' : 0,
                            'CLASSIFY1_RESET_TC_FLAG' : 0,
                            'CLASSIFY1_TC_VALUE' : 0
                        }
                    }                   
                ]             
            },                    
            'profile' : {
                'key' : [
                {'GROUP_INDEX' :  0,
                'KEY_BUILD_PROFILE_ID' :  10,
                'L4_DST_PORT' :  0,
                'L4_IS_TCPDUP' :  0,
                'L4_HD_TYPE' :  0,
                'L4_HD_VALID' :  0,
                'L3P5_HD_TYPE' :  0,
                'L3P5_VALID' :  0,
                'L3_IS_IP' :  0,
                'L3_HD_TYPE' :  0,
                'L3_HD_VALID' :  0,
                'L2P5_SUBTYPE' :  0,
                'L2P5_HD_TYPE' :  0,
                'L2P5_HD_VALID' :  0,
                'INNER_VLAN_TAG' :  0,
                'OUT_VLAN_TAG' :  0,
                'INNER_VLAN_ID' :  0,
                'INNER_VLAN_TPID' :  0,    
                'MAC_TYPE' :  0,
                'L2_HD_VALID' :  0,
                'TL_L5P5_HD_TYPE' :  0,
                'TL_L5P5_HD_VALID' :  0,
                'TL_TUNNEL_FLAGS' :  0,
                'TL_TUNNEL_TYPE' :  0,
                'TL_TUNNEL_VALID' :  0,
                'TL_L4_IS_TCPUDP' :  0,
                'TL_L4_HD_TYPE' :  0,
                'TL_L4_HD_VALID' :  0,
                'TL_L3P5_HD_TYPE' :  0,
                'TL_L3P5_VALID' :  0,     
                'TL_L3_IS_IP' :  0,
                'TL_L3_HD_TYPE' :  0,
                'TL_L3_HD_VALID' :  0,
                'TL_L2P5_SUBTYPE' :  0,
                'TL_L2P5_HD_TYPE' :  0,
                'TL_L2P5_HD_VALID' :  0,
                'TL_INNER_VLAN_TAG' :  0,
                'TL_OUT_VLAN_TAG' :  0,
                'TL_MAC_TYPE' :  0,
                'TL_L2_HD_VALID' :  0,
                'OT_L5P5_HD_TYPE' :  0,    
                'OT_L5P5_HD_VALID' :  0,
                'OT_TUNNEL_FLAGS' :  0,
                'OT_TUNNEL_TYPE' :  0,
                'OT_TUNNEL_VALID' :  0,
                'OT_L4_IS_TCPUDP' :  0,
                'OT_L4_HD_TYPE' :  0,
                'OT_L4_HD_VALID' :  0,
                'OT_L3P5_HD_TYPE' :  0,
                'OT_L3P5_VALID' :  0,
                'OT_L3_IS_IP' :  0,
                'OT_L3_HD_TYPE' :  0,
                'OT_L3_HD_VALID' :  0,            
                'OT_L2P5_SUBTYPE' :  0,
                'OT_L2P5_HD_TYPE' :  0,
                'OT_L2P5_HD_VALID' :  0,
                'OT_INNER_VLAN_TAG' :  0,
                'OT_OUT_VLAN_TAG' :  0,
                'OT_MAC_TYPE' :  0,                      
                'OT_L2_HD_VALID' : 0}
                ],
                'mask' : [
                {'GROUP_INDEX' :  0,
                'KEY_BUILD_PROFILE_ID' :  0xff,
                'L4_DST_PORT' :  0,
                'L4_IS_TCPDUP' :  0,
                'L4_HD_TYPE' :  0,
                'L4_HD_VALID' :  0,
                'L3P5_HD_TYPE' :  0,
                'L3P5_VALID' :  0,
                'L3_IS_IP' :  0,
                'L3_HD_TYPE' :  0,
                'L3_HD_VALID' :  0,
                'L2P5_SUBTYPE' :  0,
                'L2P5_HD_TYPE' :  0,
                'L2P5_HD_VALID' :  0,
                'INNER_VLAN_TAG' :  0,
                'OUT_VLAN_TAG' :  0,
                'INNER_VLAN_ID' :  0,
                'INNER_VLAN_TPID' :  0,    
                'MAC_TYPE' :  0,
                'L2_HD_VALID' :  0,
                'TL_L5P5_HD_TYPE' :  0,
                'TL_L5P5_HD_VALID' :  0,
                'TL_TUNNEL_FLAGS' :  0,
                'TL_TUNNEL_TYPE' :  0,
                'TL_TUNNEL_VALID' :  0,
                'TL_L4_IS_TCPUDP' :  0,
                'TL_L4_HD_TYPE' :  0,
                'TL_L4_HD_VALID' :  0,
                'TL_L3P5_HD_TYPE' :  0,
                'TL_L3P5_VALID' :  0,     
                'TL_L3_IS_IP' :  0,
                'TL_L3_HD_TYPE' :  0,
                'TL_L3_HD_VALID' :  0,
                'TL_L2P5_SUBTYPE' :  0,
                'TL_L2P5_HD_TYPE' :  0,
                'TL_L2P5_HD_VALID' :  0,
                'TL_INNER_VLAN_TAG' :  0,
                'TL_OUT_VLAN_TAG' :  0,
                'TL_MAC_TYPE' :  0,
                'TL_L2_HD_VALID' :  0,
                'OT_L5P5_HD_TYPE' :  0,    
                'OT_L5P5_HD_VALID' :  0,
                'OT_TUNNEL_FLAGS' :  0,
                'OT_TUNNEL_TYPE' :  0,
                'OT_TUNNEL_VALID' :  0,
                'OT_L4_IS_TCPUDP' :  0,
                'OT_L4_HD_TYPE' :  0,
                'OT_L4_HD_VALID' :  0,
                'OT_L3P5_HD_TYPE' :  0,
                'OT_L3P5_VALID' :  0,
                'OT_L3_IS_IP' :  0,
                'OT_L3_HD_TYPE' :  0,
                'OT_L3_HD_VALID' :  0,            
                'OT_L2P5_SUBTYPE' :  0,
                'OT_L2P5_HD_TYPE' :  0,
                'OT_L2P5_HD_VALID' :  0,
                'OT_INNER_VLAN_TAG' :  0,
                'OT_OUT_VLAN_TAG' :  0,
                'OT_MAC_TYPE' :  0,                      
                'OT_L2_HD_VALID' : 0}
                ],                    
                'table' : [
                {'KEY_BUILD_OP_CODE' : 2,
                'DEF_ACT_IDX' : 0,
                'MEP_DSTR_PROF' : 0,
                'MEP_DSPATCH_TYPE' : 0,
                'DEFAULT_DEST_VALID' : 0,
                'ACT_TYPE' : 0,
                'DEFAULT_DEST' : 0,
                'EM_LK_ENABLE' : 1,
                'EM_LK_PROF_ID' : 0,
                'EM_LK_KEY_ID' : keyTemplateIndex,
                'EM_TBL_ID' : 0,
                'EM_KEY_LEN' : 0,
                'WC_LK_ENABLE' : 0,
                'WC_LK_PROF_ID' : 0,
                'WC_LK_KEY_ID' : loc2,
                'WC_KEY_LEN' : 0,
                'SET_TC_ENABLE' : 0,
                'SET_TC_VALUE' : 0}
                ]
                },  
            'key_template' : {
                'key' : [
                {'KEY_TEMPLATE_INDEX' :  keyTemplateIndex }
                ],
                'table' : [
                {'KEY_PROF_ID' : 0 ,
                'GROUP_IDX' : 0 ,
                'VNIC_ID' : 0 ,
                'META_DATA' : 0 ,
                'MAC_PORT_ENABLE' : 0 ,
                'OT_L2_DMAC' : 0 ,
                'OT_L2_SMAC' : 0 ,
                'OT_L2_OUT_VLAN_TPID' : 0 ,
                'OT_L2_OUT_VLAN_PRI' : 0 ,
                'OT_L2_OUT_VLAN_DE' : 0 ,
                'OT_L2_OUT_VLAN_VID' : 0 ,
                'OT_L2_INNER_VLAN_TPID' : 0 ,
                'OT_L2_INNER_VLAN_PRI' : 0 ,
                'OT_L2_INNER_VLAN_DE' : 0 ,
                'OT_L2_INNER_VLAN_VID' : 0 ,
                'OT_L3_TYPE' : 0 ,
                'OT_L3_SIP3' : 0 ,
                'OT_L3_SIP2' : 0 ,
                'OT_L3_SIP1' : 0 ,
                'OT_L3_SIP0' : 1 ,
                'OT_L3_DIP3' : 0 ,
                'OT_L3_DIP2' : 0 ,
                'OT_L3_DIP1' : 0 ,
                'OT_L3_DIP0' : 1 ,
                'OT_L3_PROT' : 0 ,
                'OT_L3_TTL' : 0 ,
                'OT_L3_TOS' : 0 ,
                'OT_L3_FLOW' : 0 ,
                'OT_L3_FRAG' : 0 ,
                'OT_L3_EXT_HD_VALID' : 0 ,
                'OT_L4_SPORT1' : 0 ,
                'OT_L4_SPORT2' : 0 ,
                'OT_L4_DPORT' : 0 ,
                'OT_L4_FLAGS' : 0 ,
                'OT_TUNNEL_TYPE' : 0 ,
                'OT_TUNNEL_ID' : 0 ,
                'OT_TUNNEL_FLAGS' : 0 ,
                'OT_L5P5_NSH_FLAGS' : 0 ,
                'OT_L5P5_NSH_TTL' : 0 ,
                'OT_L5P5_NSH_LEN' : 0 ,
                'OT_L5P5_NSH_MD_TYPE' : 0 ,
                'OT_L5P5_NSH_NEXT_PROTO' : 0 ,
                'OT_L5P5_NSH_SPI' : 0 ,
                'OT_L5P5_NSH_SI' : 0 ,
                'TL_L2_DMAC' : 0 ,
                'TL_L2_SMAC' : 0 ,
                'TL_L2_OUT_VLAN_TPID' : 0 ,
                'TL_L2_OUT_VLAN_PRI' : 0 ,
                'TL_L2_OUT_VLAN_DE' : 0 ,
                'TL_L2_OUT_VLAN_VID' : 0 ,
                'TL_L2_INNER_VLAN_TPID' : 0 ,
                'TL_L2_INNER_VLAN_PRI' : 0 ,
                'TL_L2_INNER_VLAN_DE' : 0 ,
                'TL_L2_INNER_VLAN_VID' : 0 ,
                'TL_L3_TYPE' : 0 ,
                'TL_L3_SIP3' : 0 ,
                'TL_L3_SIP2' : 0 ,
                'TL_L3_SIP1' : 0 ,
                'TL_L3_SIP0' : 0 ,
                'TL_L3_DIP3' : 0 ,
                'TL_L3_DIP2' : 0 ,
                'TL_L3_DIP1' : 0 ,
                'TL_L3_DIP0' : 0 ,
                'TL_L3_PRTL' : 0 ,
                'TL_L3_TTL' : 0 ,
                'TL_L3_TOS' : 0 ,
                'TL_L3_FLOW' : 0 ,
                'TL_L3_FRAG' : 0 ,
                'TL_L3_EXT_HD_VALID' : 0 ,
                'TL_L4_SPORT1' : 0 ,
                'TL_L4_SPORT2' : 0 ,
                'TL_L4_DPORT' : 0 ,
                'TL_L4_FLAGS' : 0 ,
                'TL_TUNNEL_TYPE' : 0 ,
                'TL_TUNNEL_ID' : 0 ,
                'TL_TUNNEL_FLAGS' : 0 ,
                'TL_L5P5_NSH_FLAGS' : 0 ,
                'TL_L5P5_NSH_TTL' : 0 ,
                'TL_L5P5_NSH_LEN' : 0 ,
                'TL_L5P5_NSH_MD_TYPE' : 0 ,
                'TL_L5P5_NSH_NEXT_PRTLO' : 0 ,
                'TL_L5P5_NSH_SPI' : 0 ,
                'TL_L5P5_NSH_SI' : 0 ,
                'L2_DMAC' : 0 ,
                'L2_SMAC' : 0 ,
                'L2_OUT_VLAN_TPID' : 0 ,
                'L2_OUT_VLAN_PRI' : 0 ,
                'L2_OUT_VLAN_DE' : 0 ,
                'L2_OUT_VLAN_VID' : 0 ,
                'L2_INNER_VLAN_TPID' : 0 ,
                'L2_INNER_VLAN_PRI' : 0 ,
                'L2_INNER_VLAN_DE' : 0 ,
                'L2_INNER_VLAN_VID' : 0 ,
                'L3_TYPE' : 0 ,
                'L3_SIP3' : 0 ,
                'L3_SIP2' : 0 ,
                'L3_SIP1' : 0 ,
                'L3_SIP0' : 0 ,
                'L3_DIP3' : 0 ,
                'L3_DIP2' : 0 ,
                'L3_DIP1' : 0 ,
                'L3_DIP0' : 0 ,
                'L3_PRTL' : 0 ,
                'L3_TTL' : 0 ,
                'L3_TOS' : 0 ,
                'L3_FLOW' : 0 ,
                'L3_FRAG' : 0 ,
                'L3_EXT_HD_VALID' : 0 ,
                'L4_SPORT1' : 0 ,
                'L4_SPORT2' : 0 ,
                'L4_DPORT' : 0 ,
                'L4_FLAGS' : 0 ,
                'UDF0_EN' : 0 ,
                'UDF0_SEL' : 0 ,
                'UDF1_EN' : 0 ,
                'UDF1_SEL' : 0 ,
                'UDF2_EN' : 0 ,
                'UDF2_SEL' : 0 ,
                'UDF3_EN' : 0 ,
                'UDF3_SEL' : 0 ,
                'UDF4_EN' : 0 ,
                'UDF4_SEL' : 0 ,
                'UDF5_EN' : 0 ,
                'UDF5_SEL' : 0 ,
                'UDF6_EN' : 0 ,
                'UDF6_SEL' : 0 ,
                'UDF7_EN' : 0 ,
                'UDF7_SEL' : 0 ,
                'RANGE_CHECK_TYPE0' : 0 ,
                'RANGE_CHECK_TYPE1' : 0 } 
                ]
                },  
            'key_mask' : {
                'key' : [
                {'KEY_TEMPLATE_INDEX' :  keyTemplateIndex }
                ],
                'table' : [
                {'data' : 0xffffffffffffffffffffffffffffffff}
                ]
                },
            'mirror' : {
                'key' : [
                {'MIRROR_INDEX' :  mirrorIndex }
                ],
                'table' : [
                {'MODE' : 2,
                'IGNORE_DROP' : 0,
                'TRUNC' : 0,
                'ENCAP_FLAG' : 0,
                'SAMPLE_FLAG' : 1,
                'SAMPLE_CONFIG' : 1,
                'TIME_MODEL' : 0,
                'LNS' : 0,
                'ENCAP_MODE' : 0,
                'DESTINATION' : loc3}
                ]
                },
            'em_table' : {
                "tbl_name":"em_table",
                "tbl_id":2,                 #目前约定 0:512_RX 1:512_TX 2:1024_RX 3:1024_TX
                "key_len":16,               #支持 16 、32 、64、96 四种长度key
                "key":[1,2,3,4],            #这里的 key 值是 uint32 ，四个元素长度正好是 key_ken = 16
                "kt_index":1,               #kt_index 从 0 开始，由用户维护
                "table":{                   #以下是table的表项取值，除了 EXT_RST_IDX 由 em表自动填写外，其他都有用户填写。
                    "PRIORITY":1,  
                    "VERSION0":0,
                    "VERSION1":1,
                    "VERSION2":2,
                    "VERSION3":1,
                    "VERSION_GROUP0":72,
                    "VERSION_GROUP1":1,
                    "VERSION_GROUP2":2,
                    "VERSION_GROUP3":2,
                    "RANGE_INDEX0":1,
                    "RANGE_INDEX1":1,
                    "STATISTIC_SAME_IDX":2,
                    "STATISTICS":2,
                    "CMD_QUEUE_ID":1,
                    "AGE_MODE":1,
                    "ECMP_ENABLE":2,
                    "ECMP_ENTRY_NUM":1,
                    "TSE_RSV":1,
                    "EXT_RST_IDX":1,
                    "TSE_EXT_RST_LEN":1,
                    "PIPE_EXT_RST_LEN":1,
                    "OP_CODE":1,
                    "KEY_BUILD_PROF_ID":1,
                    "STORAGE_READ":1,
                    "GROUP_STATS_IDX":2,
                    "MEP_DSTR_PROF":2,
                    "MEP_DSPATCH_TYPE":2,
                    "SRCE_TBL":2,
                    "SET_TC_ENABLE":2,
                    "SET_TC_VALUE":2,
                    "DEST_VALID":1,
                    "ACT_TYPE":1,
                    "DESTINATION":1,
                    "DECAPSULATION":0,
                    "MIRR_PRI":1,
                    "MIRR_METER_IDX":2,
                    "MIRRORING":1,
                    "EXT_BIT_MAP":72,
                    "METER_NUM":1,
                    "META_DATA_UPDATE":2,
                    "REMV_OUT_VLAN":2,
                    "REMV_INNER_VLAN":1,
                    "REPLACE_OUT_VLAN":1,
                    "REPLACE_INNER_VLAN":2,
                    "TTL_UPDATE":72,
                    "TOS_UPDATE":1,
                    "DEC_NSH_TTL":2,
                    "INT_TUNNEL_DELE":2,
                    "UPDATE_FIELD":1,
                    "REPLACE_DMAC":1,
                    "REPLACE_SMAC":2,
                    "REPLACE_SIPV6":2,
                    "REPLACE_DIPV6":1,
                    "REPLACE_SIPV4":1,
                    "REPLACE_DIPV4":2,
                    "REPLACE_L4_SPORT":1,
                    "REPLACE_L4_DPORT":1,
                    "TUNNEL_ENCAP_TYPE":1,
                    "TUNNEL_ENCAP_LEN":1,
                    "L4_ENCAP_TYPE":1,
                    "L3_ENCAP_TYPE":1,
                    "VTAG_TYPE":1,
                    "L2_FLAG":1,
                    "METER_INFO0":1,
                    "METER_INFO1":2,
                    "METER_INFO2":1,
                    "METER_INFO3":2,
                    "RSV":0,
                    "data":[100,200,300,400,500]
                }
            },
            'meter_model' : 
                {
                'key' : [
                    {'METER_MOD_INDEX' :  meterModIndex}
                    ],
                'table' : [
                    {'VALID' : 1,
                    'EIR' : 10,
                    'CIR' : 5,
                    'EBS' : 1000,
                    'CBS' : 500,
                    'EBND' : 0,
                    'CBND' : 0,
                    'EBSM' : 0,
                    'CBSM' : 0,
                    'RFC2698' : 1,
                    'PM' : 0,
                    'CF' : 0,
                    'GREEN_ACTION' : 0,                    
                    'YELLOW_ACTION' : 1,
                    'RED_ACTION' : 2,
                    'GREEN_DSCP' : 0,
                    'YELLOW_DSCP' : 20,
                    'RED_DSCP' : 0}
                    ]
                },                    
            'meter_table' : {
                'key' : [
                    {'METER_INDEX' :  meterIndex}
                    ],
                'table' : [
                    {'VALID' : 1,
                    'METER_MODEL' : meterModIndex,
                    'BKT_E' : 0,
                    'BKT_C' : 0,
                    'METER_PKT_CNT' : 0,
                    'METER_BYTE_CNT' : 0,
                    'LAST_TIMESTAMP' : 0}
                    ]                  
                }              
        }
    

    #RX 收到报文后， 直接发往目的地
    def getPortConfig(self):
        return self.value1    

    def getPortFlow(self):
        flow = dict()
        base_pkt = Ether(src='22:22:22:22:22:11',dst='08:00:27:bb:c0:3c')/IP(src='1.1.1.1',dst='2.2.2.2')/UDP(sport=5000,dport=5000)
        base_pkt_len = len(base_pkt)
        base_pkt /= 'x' * max(0, 128 - base_pkt_len)
        flow.setdefault('custompkt', base_pkt)
        return flow

    #RX 收到报文后， 直接发往目的地, 同时配置了mirror, 做入口镜像
    def getPortConfigMirror(self):
       __value = copy.deepcopy(self.value1)
       __value['tables']['input_rx'][0]['table']['MIRR_IDX'] = self.mirrorIndex
       return __value        
       
    #RX 收到报文后， 直接发往目的地, 同时配置了meter
    def getPortConfigMeter(self):
       __value = copy.deepcopy(self.value1)
       __value['tables']['input_rx'][0]['table']['METE_INFO0'] = self.meterIndex
       return __value        
       
    #RX 收到报文后， 直接发往目的地, 同时配置了meter和mirror
    def getPortConfigMeterAndMirror(self):
       __value = copy.deepcopy(self.value1)
       __value['tables']['input_rx'][0]['table']['METE_INFO0'] = self.meterIndex
       __value['tables']['input_rx'][0]['table']['MIRR_IDX'] = self.mirrorIndex
       return __value               
   
   
    #RX 收到报文后， 使用默认action转发
    def getPortDefaultActionConfig(self):
       __value = copy.deepcopy(self.value1)
       __value['tables']['input_rx'][0]['table']['OP_CODE'] = 1
       return __value        
        
    #RX 收到报文后， 使用默认action转发, 同时配置了mirror, 做入口镜像
    def getPortDefaultActionConfigMirror(self):
       __value = copy.deepcopy(self.value1)
       __value['tables']['input_rx'][0]['table']['OP_CODE'] = 1
       __value['tables']['input_rx'][0]['table']['MIRR_IDX'] = self.mirrorIndex
       return __value        
       
    #RX 收到报文后， 使用默认action转发, 同时配置了meter
    def getPortDefaultActionConfigMeter(self):
       __value = copy.deepcopy(self.value1)
       __value['tables']['input_rx'][0]['table']['OP_CODE'] = 1
       __value['tables']['input_rx'][0]['table']['METE_INFO0'] = self.meterIndex
       return __value        
       
    #RX 收到报文后， 使用默认action转发, 同时配置了meter和mirror
    def getPortDefaultActionConfigMeterAndMirror(self):
       __value = copy.deepcopy(self.value1)
       __value['tables']['input_rx'][0]['table']['OP_CODE'] = 1
       __value['tables']['input_rx'][0]['table']['METE_INFO0'] = self.meterIndex
       __value['tables']['input_rx'][0]['table']['MIRR_IDX'] = self.mirrorIndex
       return __value                  
       
       
    #RX 收到报文后， to MEP转发
    def getPortToMepActionConfig(self):
       __value = copy.deepcopy(self.value1)
       __value['tables']['input_rx'][0]['table']['OP_CODE'] = 3
       __value['tables']['input_rx'][0]['table']['MEP_CODE'] = 0
       __value['tables']['input_rx'][0]['table']['MEP_TYPE'] = 1
       return __value        
        
    #RX 收到报文后， to MEP转发, 同时配置了mirror, 做入口镜像
    def getPortToMepActionConfigMirror(self):
       __value = copy.deepcopy(self.value1)
       __value['tables']['input_rx'][0]['table']['OP_CODE'] = 3
       __value['tables']['input_rx'][0]['table']['MEP_CODE'] = 0
       __value['tables']['input_rx'][0]['table']['MEP_TYPE'] = 1       
       __value['tables']['input_rx'][0]['table']['MIRR_IDX'] = self.mirrorIndex
       return __value        
       
    #RX 收到报文后， to MEP转发, 同时配置了meter
    def getPortToMepActionConfigMeter(self):
       __value = copy.deepcopy(self.value1)
       __value['tables']['input_rx'][0]['table']['OP_CODE'] = 3
       __value['tables']['input_rx'][0]['table']['MEP_CODE'] = 0
       __value['tables']['input_rx'][0]['table']['MEP_TYPE'] = 1       
       __value['tables']['input_rx'][0]['table']['METE_INFO0'] = self.meterIndex
       return __value        
       
    #RX 收到报文后， to MEP转发, 同时配置了meter和mirror
    def getPortToMepActionConfigMeterAndMirror(self):
       __value = copy.deepcopy(self.value1)
       __value['tables']['input_rx'][0]['table']['OP_CODE'] = 3
       __value['tables']['input_rx'][0]['table']['MEP_CODE'] = 0
       __value['tables']['input_rx'][0]['table']['MEP_TYPE'] = 1       
       __value['tables']['input_rx'][0]['table']['METE_INFO0'] = self.meterIndex
       __value['tables']['input_rx'][0]['table']['MIRR_IDX'] = self.mirrorIndex
       return __value                         
       
       
       
    #RX 收到报文后， 丢弃
    def getPortDropActionConfig(self):
       __value = copy.deepcopy(self.value1)
       __value['tables']['input_rx'][0]['table']['OP_CODE'] = 4
       return __value        
        
    #RX 收到报文后， 丢弃, 同时配置了mirror, 做入口镜像
    def getPortDropActionConfigMirror(self):
       __value = copy.deepcopy(self.value1)
       __value['tables']['input_rx'][0]['table']['OP_CODE'] = 4
       __value['tables']['input_rx'][0]['table']['MIRR_IDX'] = self.mirrorIndex
       return __value        
       
    #RX 收到报文后， 丢弃, 同时配置了meter
    def getPortDropActionConfigMeter(self):
       __value = copy.deepcopy(self.value1)
       __value['tables']['input_rx'][0]['table']['OP_CODE'] = 4
       __value['tables']['input_rx'][0]['table']['METE_INFO0'] = self.meterIndex
       return __value        
       
    #RX 收到报文后， 丢弃, 同时配置了meter和mirror
    def getPortDropActionConfigMeterAndMirror(self):
       __value = copy.deepcopy(self.value1)
       __value['tables']['input_rx'][0]['table']['OP_CODE'] = 4
       __value['tables']['input_rx'][0]['table']['METE_INFO0'] = self.meterIndex
       __value['tables']['input_rx'][0]['table']['MIRR_IDX'] = self.mirrorIndex
       return __value                                
   
    def __createOutStream(self, dut, hostsrc,hostdst,config=None):
        #if config['direct'] not in ['out','both']: return
        if 'outprofile' in config : return True
        index = self.__getindex()
        pkttype     = self.__getProtocolByConfig(config)  #L4
        flowtype    = (config.get('flowtype','ipv4')).lower() #L3
        streamname  = config.get('outstream','outStream' + index)
        profilename = config.get('outprofile','port1ProfileOut' + index)
        FrameNum    = config.get('framenum',None)
        fps         = self.__getFpsByConfig(config)
        config['outstream']  = streamname
        config['outprofile'] = profilename
        config.setdefault('outprofile', profilename)
        firsthost = self.__getHostFirst(hostsrc)
        traffic = self.testerlib.getTrafficByHost(firsthost)
        
        #创建数据流
        conf = {
                profilename :{
                    'config' :{
                        'object' : traffic,
                        'Type' : 'Constant',
                        },
                    'stream' : {}
                    }
                }
        
        if fps != None:
            conf[profilename]['config']['TrafficLoad']     = fps
            conf[profilename]['config']['TrafficLoadUnit'] = 'fps'
            
        if FrameNum != None:
            conf[profilename]['config']['Type']      = 'Burst'
            conf[profilename]['config']['FrameNum']  = FrameNum

        streamNum = 1
        for hostname in self.__getHostList(hostsrc):
            stream = {
                      'hostsrc' : hostname,
                      'hostdst' : hostdst,
                      'flowType' : flowtype,
                      'L3': flowtype,
                      'L4': pkttype
                     }
            #处理config中的自定义信息
            if 'ipinc' in config:
                stream['IpSrcAddrMode'] = 'increment'
                stream['IpSrcAddrCount'] = config['ipinc']
                stream['IpSrcAddrStep'] = '0.0.0.1'
                
            if 'vlaninc' in config:
                stream['VlanIdMode'] = 'increment'
                stream['VlanIdCount'] = config['vlaninc']
                stream['VlanIdStep'] = 1
                
            if 'vlanid' in config:
                stream['VlanId'] = config['vlanid']
                
            if 'portinc' in config:
                if pkttype == 'tcp' :
                    stream['TcpSrcPortMode'] = 'increment'
                    stream['TcpSrcPortCount'] = config['portinc']
                    stream['TcpSrcPortStep'] = 1
                elif pkttype == 'udp' :
                    stream['UdpSrcPortMode'] = 'increment'
                    stream['UdpSrcPortCount'] = config['portinc']
                    stream['UdpSrcStep'] = 1
                else :
                    raise AssertionError("Known protocol %s"%pkttype)
                    
            if 'streamspecial' in config:
                stream.update(config['streamspecial'])

            if self.__isInputTun(config) :
                stream['tun_dl_src'] = self.testerlib.getHostMac(hostsrc)
                self.__setStreamTunnel(stream,config['tun_info'])

            for _flowconfig in config['flowRule']:
                '''根据流表规则创建一条流'''
                __stream = copy.deepcopy(stream)
                if _flowconfig['action']['output'] != config['outport']:
                    continue
                self.__setStreamByFlow(dut, __stream, _flowconfig)
                conf[profilename]['stream'][streamname+hostname+str(streamNum)] = __stream
                _flowconfig.setdefault('stream', streamname+hostname+str(streamNum))
                streamNum = streamNum + 1
            self.testerlib.createProfile(conf)
        return True
    
    #"input表：opcode:5   default destination: 直接发送的目的地"      待支持环回的用例开发后，再测试该功能
    #"叠加input表的mirror和meter
    #vm2vm:loopback为0时，支持mirror和meter
    #mirror:loopback为1时， 不支持mirror和meter
    #tx_miss:loopback为2时， 不做mirror， 支持meter
    #组播：loopback为3时， 不支持mirror和meter"



    
if __name__ == '__main__':
    c = rxPortConfig()
    pprint(c.getPortConfig())



