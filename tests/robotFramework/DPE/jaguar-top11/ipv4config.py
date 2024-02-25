#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket , struct , copy , time , random , json, itertools
from pprint import pprint

from robot.libraries.BuiltIn import BuiltIn

from scapy.all import *
from scapy_helper import mac2int,ip2int,int2ip
from scapy.contrib.geneve import GENEVE
from scapy.layers.vxlan import VXLAN

__path = os.path.realpath(os.path.join(__file__,'..','..','testlib')) 
if __path not in sys.path:sys.path.append(__path)

from domain.device.register import *
from base.nvgre import NVGRE
from domain.device.corsica import corsica_dpe

class ipv4config(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    def __init__(self):
        self.default_action = 10
        self.groupid = self.__getlocationPort()
        self.profileid = 100
        self.proflielist = list()
        
    def __getlocationPort(self):
        loc1 = 10000
        try:
            loc1 = int(BuiltIn().get_variable_value('${dut1port101}'))
        except:
            pass
        return loc1
    
    def __getlocationOutputPort(self):
        loc1 = 10001
        try:
            loc1 = int(BuiltIn().get_variable_value('${dut1port102}'))
        except:
            pass
        return loc1   
    
    def getClassifySuiteConfig(self):
        loc1 =self.__getlocationPort()
        value = {
            'input_port_rx':{
                "group":[
                    {
                         "tbl_name": "input_port_rx",
                         "key" : {
                            "INPUT_PORT_RX_SRC_PORT" :  loc1+8,  #8是0口
                            "INPUT_PORT_RX_TUNNEL_PKT_FLAG" : 0,
                        },
                        "table" : {
                            "INPUT_PORT_RX_OP_CODE": 2, # classify
                            "INPUT_PORT_RX_GROUP_IDX": loc1, 
                        }
                    },
                    {
                         "tbl_name": "input_port_rx",
                         "key" : {
                            "INPUT_PORT_RX_SRC_PORT" :  loc1+8,  #8是0口
                            "INPUT_PORT_RX_TUNNEL_PKT_FLAG" : 1,
                        },
                        "table" : {
                            "INPUT_PORT_RX_OP_CODE": 2, # classify
                            "INPUT_PORT_RX_GROUP_IDX": loc1, 
                        }
                    }
                ]
            },
            'default_action' : {
                "group":[
                    {
                        "index":self.default_action,
                        "table":{
                             "REPLACE_SMAC":1,
                             "DESTINATION_VALID":1,
                             "ACTION_TYPE":0,  #单播
                             "DESTINATION": loc1<<6 if loc1 else 0, # 0口
                             "data":[0x78563412,0x2113],
                        }
                    }
                ]
            }

        }
        value = corsica_dpe.corsica_config_check(value)
        return value

    def getNvgreRegConfig(self):
        value = {
            'register':{
                "tbl_pipe": 0,
                "key": {
                    "REG_TYPE": DPE_IPAE_GP0_CSR,
                    "REG_ID": PAE_CSR_GP0_GLOBAL_CTRL_REG
                },
                "table": {
                    "REG_VALUE": 0x28b78
                }
            }

        }
        return value 

    def getGreTencentRegConfig(self):
        value = {
            'register':{
                "tbl_pipe": 0,
                "key": {
                    "REG_TYPE": DPE_IPAE_GP0_CSR,
                    "REG_ID": PAE_CSR_GP0_GLOBAL_CTRL_REG
                },
                "table": {
                    "REG_VALUE": 0xa8b38
                }
            }

        }
        return value   

    def ClearSuiteConfig(self,config):
        return config         

    def __getClassifyValue(self,pkttype,layer,mode=5,ilist=None):
        loc1 = self.__getlocationOutputPort()
        pkttype = pkttype.lower()
        pkt = corsica_dpe.getPacket(pkttype)
        pktchk = pkt.copy()
        pktchk[Ether].src = "12:34:56:78:13:21"

        value = {
            'classify' :{
                "tbl_id": 0,
                "tbl_pipe": 0,
                "priority": 0,
                "key": {
                    "CLASSIFY1_GROUP_INDEX": loc1, #直接使用port 索引
                },
                "mask": {
                    "CLASSIFY1_GROUP_INDEX": 0xff, 
                },
                "table": {
                    "CLASSIFY1_OPRATE_CODE": 1,
                    "CLASSIFY1_DEFAULT_ACTION_INDEX":self.default_action
                }      
            },
            'register':{
                "group":[
                    {
                        "tbl_pipe": 0,
                        "key": {
                            "REG_TYPE": DPE_IPIPE_GRP0_CSR,
                            "REG_ID": PIPE_GRP_CSR_P0_CLASSIFY_ADDR_SEL_CFG_REG
                        },
                        "table": {
                            "REG_VALUE": int(mode) 
                        }
                    }                   
                ]
            }
        }

        #pkttunlnum = corsica_dpe.getTunlnumByPkttype(pkttype)
        info = corsica_dpe.paserPacket(pkt)
       
        value['classify'],ilist = corsica_dpe.setClassifyByPkt(value['classify'],info,layer,mode,ilist)
        value['register'] = corsica_dpe.setClassifyRegisterByConf(value['register'],info,layer,mode,ilist)
        #value['input_port_rx'] = corsica_dpe.setInputPortRxByTunnel(value['input_port_rx'],info)

        value = corsica_dpe.corsica_config_check(value)
        ret = {
            'corsica': value,
            'packet': {
                'custompkt' : pkt,
                'chkpkt'    : pktchk
            }
        }
        return copy.deepcopy(ret)
    
    def getClassifyValue(self,pktname,layer,mode=5,ilist=None):
        value = self.__getClassifyValue(pktname,layer,mode,ilist)
        return value

    def getProfileSuiteConfig(self):
        
        loc1 = self.__getlocationPort()
        value = {
            'input_port_rx':{
                "group":[
                    {
                         "tbl_name": "input_port_rx",
                         "key" : {
                            "INPUT_PORT_RX_SRC_PORT" :  loc1+8,  #8是0口
                            "INPUT_PORT_RX_TUNNEL_PKT_FLAG" : 0,
                        },
                        "table" : {
                            "INPUT_PORT_RX_OP_CODE": 2, # classify
                            "INPUT_PORT_RX_GROUP_IDX": loc1, 
                        }
                    },
                    {
                         "tbl_name": "input_port_rx",
                         "key" : {
                            "INPUT_PORT_RX_SRC_PORT" :  loc1+8,  #8是0口
                            "INPUT_PORT_RX_TUNNEL_PKT_FLAG" : 1,
                        },
                        "table" : {
                            "INPUT_PORT_RX_OP_CODE": 2, # classify
                            "INPUT_PORT_RX_GROUP_IDX": loc1, 
                        }
                    }
                ]
            },
            'profile' :{ "group":list()},
            'default_action' : {
                "group":[
                    {
                        "index":self.default_action,
                        "table":{
                             "REPLACE_SMAC":1,
                             "DESTINATION_VALID":1,
                             "ACTION_TYPE":0,  #单播
                             "DESTINATION": loc1<<6 if loc1 else 0, # 0口
                             "data":[0x78563412,0x2113],
                        }
                    }
                ]
            },
            'register':{
                "group":[
                    {
                        "tbl_pipe": 0,
                        "key": {
                            "REG_TYPE": DPE_IPIPE_GRP0_CSR,
                            "REG_ID": PIPE_GRP_CSR_PROFI_TUN_FLAGS_CFG_01_REG
                        },
                        "table": {
                            "REG_VALUE": 0x1  #vxlan
                        }
                    },
                    {
                        "tbl_pipe": 0,
                        "key": {
                            "REG_TYPE": DPE_IPIPE_GRP0_CSR,
                            "REG_ID": PIPE_GRP_CSR_PROFI_TUN_FLAGS_CFG_02_REG
                        },
                        "table": {
                            "REG_VALUE": 0x1  #geneve
                        }
                    },
                    {
                        "tbl_pipe": 0,
                        "key": {
                            "REG_TYPE": DPE_IPIPE_GRP0_CSR,
                            "REG_ID": PIPE_GRP_CSR_PROFI_TUN_FLAGS_CFG_04_REG
                        },
                        "table": {
                            "REG_VALUE": 0x1  #GRE
                        }
                    },
                    {
                    "tbl_pipe": 0,
                        "key": {
                            "REG_TYPE": DPE_IPIPE_GRP0_CSR,
                            "REG_ID": PIPE_GRP_CSR_PROFI_TUN_FLAGS_CFG_06_REG
                        },
                        "table": {
                            "REG_VALUE": 0x1  #vxlan-gpe
                        }
                    },
                    {
                        "tbl_pipe": 0,
                        "key": {
                            "REG_TYPE": DPE_IPIPE_GRP0_CSR,
                            "REG_ID": PIPE_GRP_CSR_PROFI_TUN_FLAGS_CFG_08_REG
                        },
                        "table": {
                            "REG_VALUE": 0x1  #vxlan-ali
                        }
                    },                    
                ]
            }

        }
        
        profileadd = []
        #self.proflielist = profileadd + corsica_dpe.getProfileDefaultTemplates('default')
        for t in self.proflielist:
            p = self.createProfile(t)
            value['profile']['group'].append(p)
        value = corsica_dpe.corsica_config_check(value)
        return value
    
    def getNvgreProfileSuiteConfig(self):
        value = self.getProfileSuiteConfig()
        value['register'] = {
            "tbl_pipe": 0,
            "key": {
                "REG_TYPE": DPE_IPAE_GP0_CSR,
                "REG_ID": PAE_CSR_GP0_GLOBAL_CTRL_REG
            },
            "table": {
                "REG_VALUE": 0x28b78
            }
        }
        return value   
    
    def getGreTencentProfileSuiteConfig(self):
        value = self.getProfileSuiteConfig()
        value['register'] = {
            "tbl_pipe": 0,
            "key": {
                "REG_TYPE": DPE_IPAE_GP0_CSR,
                "REG_ID": PAE_CSR_GP0_GLOBAL_CTRL_REG
            },
            "table": {
                "REG_VALUE": 0xa8b38
            }
        }
        return value 

    def getErrorPktProfileSuiteConfig(self):
        value = self.getProfileSuiteConfig()
        value['register'] = {
            "tbl_pipe": 0,
            "key": {
                "REG_TYPE": DPE_IPAE_GP0_CSR,
                "REG_ID": PAE_CSR_GP0_GLOBAL_ERR_REG
            },
            "table": {
                "REG_VALUE": 0       #默认值0x3ff
            }
        }
        return value         
    
    def createProfile(self,t):
        profile = {
            "key": {
                "PROFILE_GROUP_INDEX": self.groupid, 
                "PROFILE_KEY_BUILD_PROFILE_ID": self.profileid,
            },
            "mask": {
                "PROFILE_GROUP_INDEX": 255,
                "PROFILE_KEY_BUILD_PROFILE_ID": 255,
            },
            "table": {
                "PROFILE_KEY_BUILD_OP_CODE": 1,
                "PROFILE_DEF_ACT_IDX": self.default_action,
            }
        }
        corsica_dpe.setProfileTemplate(profile,t)
        return profile
    
    def getProfileValue(self,pktname):
        pktname = pktname.lower()
        pkt = corsica_dpe.getPacket(pktname)
        profile = None
        if pktname not in self.proflielist:
            #raise AssertionError("Can't find pktname in profile")
            profile = self.createProfile(pktname)
            #self.proflielist.append(pktname)           

        pktchk = pkt.copy()
        if Ether in pktchk:
            pktchk[Ether].src = "12:34:56:78:13:21"
        else:
            pkt = Ether()/pkt
            pktchk = Ether(src="12:34:56:78:13:21")/pktchk

        #IP分片不在不是first
        pktchk = corsica_dpe.parsePktIpFragment(pktchk)
        
        value = {
            'classify' :{
                "tbl_id": 0,
                "tbl_pipe": 0,
                "priority": 0,
                "key": {
                    "CLASSIFY1_GROUP_INDEX": self.groupid, #直接使用port 索引                    
                },
                "mask": {
                    "CLASSIFY1_GROUP_INDEX": 0xff, 
                },
                "table": {
                    "CLASSIFY1_KEY_BUILD_PROFILE_ID": self.profileid,
                    "CLASSIFY1_OPRATE_CODE": 2
                }      
            }
        }
        if profile :
            value['profile'] = profile
        value = corsica_dpe.corsica_config_check(value)
        ret = {
            'corsica': value,
            'packet': {
                'custompkt' : pkt,
                'chkpkt'    : pktchk
            }
        }
        return copy.deepcopy(ret)

    def getErrorPktProfileValue(self,pktname):
        value = self.getProfileValue(pktname)
        #错包只校验MAC
        pktchk = Ether(src="12:34:56:78:13:21")
        value['packet']['chkpkt'] = pktchk
        return value

    def getEmSuiteConfig(self):
        loc1 = self.__getlocationOutputPort()
        value = {
            'input_port_rx':{
                "group":[
                    {
                         "tbl_name": "input_port_rx",
                         "key" : {
                            "INPUT_PORT_RX_SRC_PORT" :  loc1+8,  #8是0口
                            "INPUT_PORT_RX_TUNNEL_PKT_FLAG" : 0,
                        },
                        "table" : {
                            "INPUT_PORT_RX_OP_CODE": 2, # classify
                            "INPUT_PORT_RX_GROUP_IDX": loc1, 
                        }
                    },
                    {
                         "tbl_name": "input_port_rx",
                         "key" : {
                            "INPUT_PORT_RX_SRC_PORT" :  loc1+8,  #8是0口
                            "INPUT_PORT_RX_TUNNEL_PKT_FLAG" : 1,
                        },
                        "table" : {
                            "INPUT_PORT_RX_OP_CODE": 2, # classify
                            "INPUT_PORT_RX_GROUP_IDX": loc1, 
                        }
                    }
                ]
            },
            'classify' :{
                "tbl_id": 0,
                "tbl_pipe": 0,
                "priority": 0,
                "key": {
                    "CLASSIFY1_GROUP_INDEX": self.groupid, #直接使用port 索引                    
                },
                "mask": {
                    "CLASSIFY1_GROUP_INDEX": 0xff, 
                },
                "table": {
                    "CLASSIFY1_KEY_BUILD_PROFILE_ID": self.profileid,
                    "CLASSIFY1_OPRATE_CODE": 2
                }      
            },
            'default_action' : {
                "group":[
                    {
                        "index":self.default_action,
                        "table":{
                             "REPLACE_SMAC":1,
                             "DESTINATION_VALID":1,
                             "ACTION_TYPE":0,  #单播
                             "DESTINATION": loc1<<6 if loc1 else 0, # 0口
                             "data":[0x78563412,0x2115],
                        }
                    }
                ]
            }

        }
        
        value = corsica_dpe.corsica_config_check(value)
        return value

    def getNvgreEmSuiteConfig(self):
        value = self.getEmSuiteConfig()
        value['register'] = {
            'group':[
                {
                    "tbl_pipe": 0,
                    "key": {
                        "REG_TYPE": DPE_IPAE_GP0_CSR,
                        "REG_ID": PAE_CSR_GP0_GLOBAL_CTRL_REG
                    },
                    "table": {
                        "REG_VALUE": 0x28b78
                    }
                }               
            ]
        }
        return value 

    def getGreTencentEmSuiteConfig(self):
        value = self.getEmSuiteConfig()
        value['register'] = {
            'group':[
                {
                    "tbl_pipe": 0,
                    "key": {
                        "REG_TYPE": DPE_IPAE_GP0_CSR,
                        "REG_ID": PAE_CSR_GP0_GLOBAL_CTRL_REG
                    },
                    "table": {
                        "REG_VALUE": 0xa8b38
                    }
                },
                {
                    "tbl_pipe": 0,
                    "key": {
                        "REG_TYPE": DPE_IPIPE_GRP0_CSR,
                        "REG_ID": PIPE_GRP_CSR_PROFI_TUN_FLAGS_CFG_07_REG
                    },
                    "table": {
                        "REG_VALUE": 0x1  #07表示gre-ten隧道，根据offset指定的bit位置 连续提取8bit作为TunnelFlags域段，offset=0
                    }
                },
                {
                    "tbl_pipe": 0,
                    "key": {
                        "REG_TYPE": DPE_IPIPE_GRP0_CSR,
                        "REG_ID": PIPE_GRP_CSR_SPECIAL_TUN_VNI_CFG_00_REG   #reg0 for gre-ten
                    },
                    "table": {
                        "REG_VALUE": 0x303F  #根据offset指定的bit位置 连续提取8bit作为TunnelFlags域段，offset=0
                    }
                },
                {
                    "tbl_pipe": 0,
                    "key": {
                        "REG_TYPE": DPE_IPIPE_GRP0_CSR,
                        "REG_ID": PIPE_GRP_CSR_WC_EM_KEY_TUN_VNI_OFFSET_MAP_03_REG   #03表示tunnel flag key,取k,s=1
                    },
                    "table": {
                        "REG_VALUE": 8  #tunnel offset映射表，tunnel type为gre_tencent,udf3和udf4时有效.offset 4bit为粒度.0xff是无效值，查到offset为0xff时，tunnel VNI字段填写0
                    }
                }                                               
            ]
        }
        return value 

    def getGreTencentSeqIdEmSuiteConfig(self):
        value = self.getEmSuiteConfig()
        value['register'] = {
            'group':[
                {
                    "tbl_pipe": 0,
                    "key": {
                        "REG_TYPE": DPE_IPAE_GP0_CSR,
                        "REG_ID": PAE_CSR_GP0_GLOBAL_CTRL_REG
                    },
                    "table": {
                        "REG_VALUE": 0xa8b38
                    }
                },
                {
                    "tbl_pipe": 0,
                    "key": {
                        "REG_TYPE": DPE_IPIPE_GRP0_CSR,
                        "REG_ID": PIPE_GRP_CSR_PROFI_TUN_FLAGS_CFG_07_REG
                    },
                    "table": {
                        "REG_VALUE": 0x1  #07表示gre-ten隧道，根据offset指定的bit位置 连续提取8bit作为TunnelFlags域段，offset=0
                    }
                },
                {
                    "tbl_pipe": 0,
                    "key": {
                        "REG_TYPE": DPE_IPIPE_GRP0_CSR,
                        "REG_ID": PIPE_GRP_CSR_SPECIAL_TUN_VNI_CFG_00_REG   #reg0 for gre-ten
                    },
                    "table": {
                        "REG_VALUE": 0x303F  #根据offset指定的bit位置 连续提取8bit作为TunnelFlags域段，offset=0
                    }
                },
                {
                    "tbl_pipe": 0,
                    "key": {
                        "REG_TYPE": DPE_IPIPE_GRP0_CSR,
                        "REG_ID": PIPE_GRP_CSR_WC_EM_KEY_TUN_VNI_OFFSET_MAP_03_REG   #03表示tunnel flag key,取k,s=1
                    },
                    "table": {
                        "REG_VALUE": 16  #tunnel offset映射表，tunnel type为gre_tencent,udf3和udf4时有效.offset 4bit为粒度.0xff是无效值，查到offset为0xff时，tunnel VNI字段填写0
                    }
                }                
            ]
        }
        return value         
    
    def getEmValue(self,pktname,keymask,keylen=None,action=None):
        loc1 = self.__getlocationOutputPort()
        pktname = pktname.lower()
        pkt = corsica_dpe.getPacket(pktname)
        
        pkt = pkt/(20*"x")
        
        pktchk = pkt.copy()
        pktchk[Ether].src = "12:34:56:78:13:21"
        pktchk = corsica_dpe.parsePktIpFragment(pktchk)
        specConf = dict()
        template0 = {
            "key": {"KEY_TEMPLATE_INDEX": 12},
            "table": {}
        }
        if keymask :
            template,specConf = corsica_dpe.setKeyTemplate(template0,keymask)
        else:
            template,_ = corsica_dpe.setKeyTemplate(template0,pkt)


        if keylen == None:
            iemkeypara = corsica_dpe.getEmKeyTpid('default','768bits')
        else:
            keylendict = corsica_dpe.tansStrToDict(keylen)
            for k,v in keylendict.items():
                iemkeypara = corsica_dpe.getEmKeyTpid(v['type'],k)
                           
        profileemkeylen = iemkeypara[0]
        tbl_id = iemkeypara[1]
        emkeylen = iemkeypara[2]
             
        #ikey,_ = corsica_dpe.getEmKey(pkt,template,keylen=keylen,config=dict())
        ikey,_ = corsica_dpe.getEmKey(pkt,template,iemkeypara,specConf)
        value = {
            'key_template' : template0,           
            'profile' :{             
                "key": {
                    "PROFILE_GROUP_INDEX": self.groupid, 
                    "PROFILE_KEY_BUILD_PROFILE_ID": self.profileid,
                    "PROFILE_OT_L2_HD_VALID": 1,
                },
                "mask": {
                    "PROFILE_GROUP_INDEX": 255,
                    "PROFILE_KEY_BUILD_PROFILE_ID": 255,
                    "PROFILE_OT_L2_HD_VALID": 1,
                },
                "table": {
                    "PROFILE_KEY_BUILD_OP_CODE": 2,
                    "PROFILE_EM_LK_ENABLE": 1,
                    #"PROFILE_EM_LK_PROF_ID": 0,
                    "PROFILE_EM_LK_KEY_ID": 12,
                    "PROFILE_EM_TBL_ID": tbl_id,
                    "PROFILE_EM_KEY_LEN": profileemkeylen,  #查EM表的KEY长度。字段值编码如下：0：128bit；1：256bit；2：512bit；3：768bit；            
                }
            },
            'key_mask' :{
                "tbl_pipe": 0,
                "key": {
                    "KEY_MASK_INDEX": 12
                },
                "table": corsica_dpe.getKeyMask(keymask)
            },
            'em_table': {
                    "tbl_id":tbl_id,                
                    "key_len":emkeylen,               
                    "key":ikey,          
                    "table":{            
                            "PRIORITY":  0, 
                            "REPLACE_SMAC": 1,
                            "DESTINATION_VALID":1,
                            "ACTION_TYPE":0,  #单播
                            "DESTINATION": loc1<<6 if loc1 else 0, # 0口
                            "data":[0x78563412,0x2113],
                    }
            },

        }
        value = corsica_dpe.corsica_config_check(value)
        ret = {
            'corsica': value,
            'packet': {
                'custompkt' : pkt,
                'chkpkt'    : pktchk
            }
        }
        return copy.deepcopy(ret)
    
    def getEmActionSuiteConfig(self):
        loc1 = self.__getlocationPort()
        value = {
            'input_port_rx':{
                "group":[
                    {
                         "tbl_name": "input_port_rx",
                         "key" : {
                            "INPUT_PORT_RX_SRC_PORT" :  loc1+8,  #8是0口
                            "INPUT_PORT_RX_TUNNEL_PKT_FLAG" : 0,
                        },
                        "table" : {
                            "INPUT_PORT_RX_OP_CODE": 2, # classify
                            "INPUT_PORT_RX_GROUP_IDX": loc1, 
                        }
                    },
                    {
                         "tbl_name": "input_port_rx",
                         "key" : {
                            "INPUT_PORT_RX_SRC_PORT" :  loc1+8,  #8是0口
                            "INPUT_PORT_RX_TUNNEL_PKT_FLAG" : 1,
                        },
                        "table" : {
                            "INPUT_PORT_RX_OP_CODE": 2, # classify
                            "INPUT_PORT_RX_GROUP_IDX": loc1, 
                        }
                    }
                ]
            },
            'classify' :{
                "tbl_id": 0,
                "tbl_pipe": 0,
                "priority": 0,
                "key": {
                    "CLASSIFY1_GROUP_INDEX": self.groupid, #直接使用port 索引                    
                },
                "mask": {
                    "CLASSIFY1_GROUP_INDEX": 0xff, 
                },
                "table": {
                    "CLASSIFY1_KEY_BUILD_PROFILE_ID": self.profileid,
                    "CLASSIFY1_OPRATE_CODE": 2
                }      
            },
            'default_action' : {
                "group":[
                    {
                        "index":self.default_action,
                        "table":{
                             "REPLACE_SMAC":1,
                             "SOURCE_TABLE":loc1,
                             "DESTINATION_VALID":1,
                             "ACTION_TYPE":0,  #单播
                             "DESTINATION": loc1<<6 if loc1 else 0, # 0口
                             "data":[0x78563412,0x2115],
                        }
                    }
                ]
            },
            'source_mode1' :
            {
                "tbl_name": "source_mode1",
                "key": {
                    "SOURCE_MODE1_INDEX":loc1+1
                },
                "table":{
                "SOURCE_MODE1_SRC_MAC":0x001223345678,
                "SOURCE_MODE1_IPV4_ADDR":0x10000001
                }
            },
            'source_mode2' :
            {
                "tbl_name": "source_mode2",
                "key": {
                    "SOURCE_MODE2_INDEX":loc1
                },
                "table":{
                "SOURCE_MODE2_SRC_MAC":0x001223345678,
                "SOURCE_MODE2_IPV6_ADDR1": 0x10000001,
                "SOURCE_MODE2_IPV6_ADDR2": 0x10000002,
                "SOURCE_MODE2_IPV6_ADDR3": 0x10000003,
                "SOURCE_MODE2_IPV6_ADDR4": 0x10000004
                }
            },
            'register':
            {
            'group':list()
            } 
        }
        value['register'] = corsica_dpe.setDscp2PriReg(value['register'])
        
        value = corsica_dpe.corsica_config_check(value)
        return value

    def getEmActionValue(self,pktname,keymask,keylen=None,atype=None,action=None):
        loc1 = self.__getlocationOutputPort()
        pktname = pktname.lower()
        pkt = corsica_dpe.getPacket(pktname)

        template0 = {
            "key": {"KEY_TEMPLATE_INDEX": 12},
            "table": {}
        }
        if keymask :
            template,_ = corsica_dpe.setKeyTemplate(template0,keymask)
        else:
            template,_ = corsica_dpe.setKeyTemplate(template0,pkt)

        if keylen == None:
            iemkeypara = corsica_dpe.getEmKeyTpid('default','768bits')
        else:
            keylendict = corsica_dpe.tansStrToDict(keylen)
            for k,v in keylendict.items():
                iemkeypara = corsica_dpe.getEmKeyTpid(v['type'],k)
                           
        profileemkeylen = iemkeypara[0]
        tbl_id = iemkeypara[1]
        emkeylen = iemkeypara[2] 

        #ikey,_ = corsica_dpe.getEmKey(pkt,template,keylen=keylen,config=dict())
        ikey,_ = corsica_dpe.getEmKey(pkt,template,iemkeypara,config=dict())
        value = {
            'key_template' : template0,           
            'profile' :{             
                "key": {
                    "PROFILE_GROUP_INDEX": self.groupid, 
                    "PROFILE_KEY_BUILD_PROFILE_ID": self.profileid,
                    "PROFILE_OT_L2_HD_VALID": 1,
                },
                "mask": {
                    "PROFILE_GROUP_INDEX": 255,
                    "PROFILE_KEY_BUILD_PROFILE_ID": 255,
                    "PROFILE_OT_L2_HD_VALID": 1,
                },
                "table": {
                    "PROFILE_KEY_BUILD_OP_CODE": 2,
                    "PROFILE_EM_LK_ENABLE": 1,
                    #"PROFILE_EM_LK_PROF_ID": 0,
                    "PROFILE_EM_LK_KEY_ID": 12,
                    "PROFILE_EM_TBL_ID": tbl_id,
                    "PROFILE_EM_KEY_LEN": profileemkeylen,                
                }
            },
            'key_mask' :{
                "tbl_pipe": 0,
                "key": {
                    "KEY_MASK_INDEX": 12
                },
                "table": corsica_dpe.getKeyMask(keymask)
            },
            'em_table': {
                    "tbl_id":tbl_id,                
                    "key_len":emkeylen,               
                    "key":ikey,          
                    "table":{            
                            "PRIORITY":  0, 
                            "REPLACE_SMAC": "12:34:56:78:13:21",
                            "DESTINATION_VALID":1,
                            "ACTION_TYPE":0,  #单播
                            "DESTINATION": loc1<<6 if loc1 else 0, # 0口
                    }
            },
            'tunnel_encap':
            {
                "tbl_name": "tunnel_encap",
                "tbl_pipe": 0,
                "key": {
                    "TUNNEL_ENCAP_INDEX":loc1
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
            } 
        }
        em = value['em_table']
        tunnel_encap = value['tunnel_encap']
        if atype == 'action':
            em['table'].pop("REPLACE_SMAC")
            corsica_dpe.setDefaultAction(em,action)
            corsica_dpe.setTunnelEncapCfgTable(tunnel_encap,action)
            pktchk = corsica_dpe.getDefaultActionPacket(pkt,em)
        elif atype == 'drop':
            em["table"]["ACTION_TYPE"] = 4 #??
            pktchk = None
        value = corsica_dpe.corsica_config_check(value)
        ret = {
            'corsica': value,
            'packet': {
                'custompkt' : pkt,
                'chkpkt'    : pktchk
            }
        }
        return copy.deepcopy(ret)

    def getInportActionSuiteConfig(self):
        loc1 =self.__getlocationPort()
        value = {
            'input_port_rx':{
                "group":[
                    {
                         "key" : {
                            "INPUT_PORT_RX_SRC_PORT" :  loc1+8  #8是0口
                        },
                        "table" : {
                            "INPUT_PORT_RX_DEF_ACT_INDEX": self.default_action,
                            "INPUT_PORT_RX_OP_CODE": 1,  # 2 to classify ,4 dorp
                        }
                    }
                ]
            }
        }
        value = corsica_dpe.corsica_config_check(value)
        return value     

    def getInportActionValue(self,pkttype,atype,action):
        loc1 =self.__getlocationOutputPort()
        pkt = corsica_dpe.getBasePkt(pkttype)
        #只修改最外层MAC
        value = {
            'default_action' : {

                        "index":self.default_action,
                        "table":{
                             "DESTINATION_VALID":1,
                             "ACTION_TYPE":0,  #单播
                             "DESTINATION": loc1<<6 if loc1 else 0 # 0口
                        }

            }
        }
        defaultaction = value['default_action']
        if atype == 'action':
            corsica_dpe.setDefaultAction(defaultaction,action)
            pktchk = corsica_dpe.getDefaultActionPacket(pkt,defaultaction)
        elif atype == 'drop':
            defaultaction["table"].pop("DESTINATION_VALID")
            defaultaction["table"].pop("DESTINATION")
            defaultaction["table"]["ACTION_TYPE"] = 2 #0: 单播， 1：组播，2：Drop
            pktchk = None
        value = corsica_dpe.corsica_config_check(value)
        ret = {
            'corsica': value,
            'packet': {
                'custompkt' : pkt,
                'chkpkt'    : pktchk
            }
        }
        return copy.deepcopy(ret)

if __name__ == '__main__':
    c = ipv4config()
    print("======SuiteConfig========")
    pprint(c.getClassifySuiteConfig())

    print("======getClassifyIpv4Value========")
    #pprint(c.getClassifyIpv4Value(0))
    print("======getClassifyIpv4Value========")
    #pprint(c.getClassifyIpv4Value(1))
    print("======getClassifyIpv4Value - Save========")
    print(corsica_dpe.saveJson(c.getClassifyIpv4Value(mode=-1,ilist=['ETH_TYPE'])['corsica'],"ClassifyIpv4_vlan_"))
    print(corsica_dpe.saveJson(c.getClassifyValue("ipv4_qq",mode=-1,ilist='OUT_VLAN_ID')['corsica'],"ClassifyIpv4_vlan_"))
    print(corsica_dpe.saveJson(c.getClassifyValue("ipv4_qq",mode=-1,ilist='OUT_VLAN_ID,OUT_VLAN_TPID')['corsica'],"ClassifyIpv4_vlan_"))
    for i in range(10):
        print(corsica_dpe.saveJson(c.getClassifyIpv4Value(i)['corsica'],"ClassifyIpv4_%d_"%i))
    
    print("======getClassifyIpv4Value - Save========")
    for i in range(10):
        print(corsica_dpe.saveJson(c.getClassifyIpv6Value(i)['corsica'],"ClassifyIpv6_%d_"%i))

    print("======getClassifyIpv4Value - Save========")
    for i in range(10):
        print(corsica_dpe.saveJson(c.getClassifyIpv4VxlanValue(i)['corsica'],"ClassifyIpv6_%d_"%i))

