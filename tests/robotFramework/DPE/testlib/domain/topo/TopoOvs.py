#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, copy, os, sys
import collections
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Collections import Collections

__path = os.path.realpath(os.path.join(__file__,'..','..','..')) 
if __path not in sys.path:sys.path.append(__path)

import base.AppBaseLib as _baselib

class TopoOvs(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        pass
        
    def __initlib(self):
        '''拓扑里面主要包含：路由交换设备、linux、测试仪设备
        '''
        self.topo = BuiltIn().get_library_instance('Topology')
        self.baselib = BuiltIn().get_library_instance('TopoBase')
        self.linuxlib = BuiltIn().get_library_instance('Linux')
        self.ovslib = BuiltIn().get_library_instance('Ovs')
        self.devlib = BuiltIn().get_library_instance('AppDevice')
        self.testerlib = BuiltIn().get_library_instance('Tester')

    def topoOvsCreateTunnel(self,A,br1,br2,config):
        '''配置隧道

         网桥br1中配置隧道， 网桥br2作为出口
                
        '''
        self.__initlib()
        if 'tun_type' not in config:
            return

        #创建隧道
        ovsconfig = {
            "port" : dict()
        }

        tunport = self.ovs.getNewPortName()
        net = config.get('tun_net',self.topo.topoGetNet())
        mask = _baselib.IP(net).strNetmask()
        ip1 = config.get('tun_remote',self.topo.topoGetNetRandIP(net))
        ip2 = config.get('tun_local',self.topo.topoGetNetRandIP(net))
        ovsconfig['port'][tunport] = {
            'type' : config['tun_type'],
            'options':{'remote_ip':ip1,'local_ip':ip2,
                            'in_key':100,'out_key':100}}
            
        self.ovs.setBridge(A,br1,ovsconfig)

        self.linux.addInterfaceConfig(A,{br2:{
                'ipv4' : ip2,
                'maskv4' : mask,
            }})
        self.linux.interfaceNoShutdown(A,br2)

