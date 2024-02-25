#!/usr/bin/python
# -*- coding: utf-8 -*-
from natconfig import *
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger

''' 流配置接口，以OVS的配置为基准进行配置：
        https://www.man7.org/linux/man-pages/man7/ovs-fields.7.html
'''

class chaipv4config(chaconfig):
    def __init__(self):
        #使用chaconfig来配置 
        self.value = {
            'cha' :{
                'port' : {
                    'port1' : {
                        'PortLocation' :  "101/4",
                        'PortType'     : 'ETHERNET',
                        }
                    },
                'subint' : {
                    'cha1Vlan' : {
                        'object'  : 'port1',
                        'config'  : {
                                'VlanTag' : '0x8100' ,
                                'VlanId'  : '10'
                            }
                        }
                    },
                'host' : {
                    'host1': {
                        'object' : 'port1',
                        'MacAddr'  : '00:01:00:00:00:01',
                        'Ipv4Addr' : '177.0.0.2', #@ip4.24@inprefix1.inipv42
                        'Ipv4Mask' : '24',
                        'Ipv4sutAddr' :'177.0.0.1',#@ip4.24@inprefix1.inipv41
                        'Arpd' : 'enable',
                        'FlagPing' :'enable',
                        'Ipv6Addr' :'6000::2',
                        'Ipv6Mask' :'64',
                        'Ipv6sutAddr' : '6000::1'
                        },
                    'hostvlan': {
                        'object' : 'cha1Vlan',
                        'MacAddr'  : '00:02:00:00:00:03',
                        'Ipv4Addr' : '178.0.0.2', 
                        'Ipv4Mask' : '24',
                        'Ipv4sutAddr' :'178.0.0.1',
                        'Arpd' : 'enable',
                        'FlagPing' :'enable',
                        },
                    },
                'traffic' : {
                    'port1Traffic' : {
                        'object' : 'port1',
                        }
                    },
                'profile' : {       
                    'profile1' : {       # createProfile
                        'config' : {
                            'object' : 'port1Traffic',  # getTrafficByHost
                            'TrafficLoad' : 'faster',   # faster 
                            'TrafficLoadUnit' : 'fps',  #
                            'Type' : 'Constant',    #Constant / Burst
                            'FrameNum' : '2',
                            'port' : 'port1',    #自动找object
                        },
                        'stream' : {  
                            'stream1' :{ # createStream
                                'hostsrc' : 'host1',  # 从host1取默认值
                                'hostdst' : 'host2',  # 从host2取默认值
                                'flowType' : 'ipv4',  #4in6 / ipv4 / ipv6
                                'framelen': '128',
                                'EthSrc' : '00:01:00:00:00:01',
                                'EthDst' : '00:01:00:00:00:02',
                                'ethtype' : '0x0800',
                                'vlanid' : '100',
                                'VlanIdMode' : 'increment',
                                'VlanIdCount' : '10',
                                'VlanIdStep'  : '1',
                                'IpSrcAddr' : '10.1.1.1',
                                'IpSrcAddrMode' : 'increment',
                                'IpSrcAddrCount' : '100',
                                'IpSrcAddrStep' : '0.0.0.1',
                                'IpDstAddr' : '10.1.1.1',
                                'IpDstAddrMode' : 'increment',
                                'IpDstAddrCount' : '100',
                                'IpDstAddrStep' : '0.0.0.1',
                                'Ipv6SrcAddress' : '800::1',
                                'Ipv6SrcAddressMode' : 'increment',
                                'Ipv6SrcAddressCount' : '1',
                                'Ipv6SrcAddressStep' : '::1',
                                'Ipv6DstAddress' : '800::2',
                                'UdpSrcPort' : '1000',
                                'UdpDstPort' : '1000',
                                'UdpSrcPortMode' : 'increment',
                                'UdpSrcPortStep' : '1',
                                'UdpSrcPortCount' : '10',
                                'TcpDstPort' : '1000',
                                'TcpSrcPort' : '1000',
                                'TcpSrcPortMode' : 'increment',
                                'TcpSrcPortStep' : '1',
                                'TcpSrcPortCount' : '10',
                                'TcpFlagSyc' : 'true',
                                'TcpFlagAck' : 'true',
                                'IcmpType' : 'echo_request',     #echo_request echo_reply 或数值
                                'IcmpId' : '100',
                                'CustomHeader' : '',
                                'HexString' : '',
                            }
                        }
                    }
                },
                'staEngine' : {
                    'port1Sta' : {
                        'engtype': 'Statistics',  #Statistics , Analysis
                        'object' : 'port1',
                        },
                    'port1Ana' : {
                        'engtype': 'Analysis', #
                        'object' : 'port1',
                        },
                    },
                }
            }
    
    def get(self):
        pass
    




