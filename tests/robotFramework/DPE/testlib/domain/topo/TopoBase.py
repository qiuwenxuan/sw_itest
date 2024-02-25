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

class TopoBase(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        pass
        
    def __initlib(self):
        '''拓扑里面主要包含：路由交换设备、linux、测试仪设备
        '''
        self.topo = BuiltIn().get_library_instance('Topology')
        self.devlib = BuiltIn().get_library_instance('AppDevice')
        self.testerlib = BuiltIn().get_library_instance('Tester')
    
    def topoGetExistIPv4(self, dev, port):
        # '1.1.1.1/24'
        if self.topo.topoDevIsCha(dev):
            hostlist = self.testerlib.findHostByPort(port)
            if len(hostlist) <= 0:
                return None
            return self.testerlib.getHostIpv4Ex(hostlist[0])
        else:
            return self.devlib.getIpv4AndMaskByInterface(dev,port)
    
    def __getIntfConfig(self,intf,ip,mask='255.255.255.0',config=None):
        '''获取接口相关配置 若为测试仪 则设置测试仪地址 若为设备，则配置接口ip等信息
        '''
        ret = dict()
        ret.setdefault('int',dict())
        ret['int'][intf] = {
                'ipv4'   : ip,
                'maskv4' : mask,
            }
        if 'vrf' in config:
            ret['int'][intf]['vrf'] = config['vrf']
            ret['vrf'] = {
                    config['vrf'] : {
                        'rd' : '100:12',
                        'af': ['ipv4'],
                        'route-target-import' :['100:1'],
                        'route-target-export' :['100:1'],
                        },
                }   
        return ret
    
    def __getChaConfig(self, port,ipv4=None,ipv4Mask=None,ipv4sutAddr=None,config=None):
        '''根据地址构建测试仪port以及host信息
        
        | config = {
        |   'hostnum' : 1,   在端口上创建的host的个数 
        |}
        '''
        cfg = dict()
        if config == None : config = dict()
        hostnum =config.get('hostnum',1)
        chaport = "port%s"%port
        cfg.setdefault('port', {
            chaport:{'PortLocation':str(port), 'PortType':'ETHERNET'}
            })
        cfg.setdefault('traffic', {chaport+'Traffic':{'object': chaport}})
        cfg.setdefault('staEngine',{chaport+'Sta':{'engtype': 'Statistics','object': chaport},chaport+'Ana':{'engtype':'Analysis','object':chaport}})
        cfg.setdefault('host',{})

        if (ipv4 == None) or (ipv4Mask == None):
            return cfg
        prefixlen = _baselib.appIpPrefixLen(ipv4Mask)
        for i in range(1,hostnum+1):
            hostname = chaport+'host'+str(i)
            mac = self.topo.topoGetMac()
            if i == 1:
                ip =ipv4
            else:
                ip = self.topo.topoGetNetRandIP(config['net'])
            cfg['host'][hostname] = {
                'object' : chaport,
                'MacAddr'  : mac,
                'Ipv4Addr' : ip,            #@ip4.24@inprefix1.inipv42
                'Ipv4Mask' : str(prefixlen),
                'Ipv4sutAddr' :ipv4sutAddr, #@ip4.24@inprefix1.inipv41
                'Arpd' : 'enable',
                'FlagPing' :'enable',
                'Ipv6Addr' :'6000::2',
                'Ipv6Mask' :'64',
                'Ipv6sutAddr' : '6000::1'
            }
        logger.info("cha host {}, {}".format(ipv4Mask,prefixlen))
        return cfg

    def __getPortConfigNoHost(self, path):
        ''' 修改端口配置 - 用于创建配置字典
         用于创建端口时，构建接口相关配置(包含设备以及测试仪上的配置)
        '''
        ret = dict()
        (a,b,t,pa,pb) = self.topo.topGetRealPath(path)
        logger.info("TopoConfigCreatePort path(%s): %s %s %s %s %s"%(path,a,b,t,pa,pb))
        if '->' in t:
            ret.setdefault(a)
            if 'cha' in a:
                ret[a] = self.__getChaConfig(pa)  
        if '<-' in t:
            ret.setdefault(b)
            if 'cha' in b:
                ret[b] = self.__getChaConfig(pb)
        return ret

    def __getPortConfig(self, path,config=None):
        ''' 修改端口配置 - 用于创建配置字典
         用于创建端口时，构建接口相关配置(包含设备以及测试仪上的配置)
        '''
        ret = dict()
        if config == None:config = dict()
        (a,b,t,pa,pb) = self.topo.topGetRealPath(path)
        logger.info("TopoConfigCreatePort path(%s): %s %s %s %s %s"%(path,a,b,t,pa,pb))
        net = config.get('net',self.topo.topoGetNet())
        mask = _baselib.IP(net).strNetmask()
        ip1 = config.get('ip1',self.topo.topoGetNetRandIP(net))
        ip2 = config.get('ip2',self.topo.topoGetNetRandIP(net))
        config['net'] = net
        if '->' in t:
            ret.setdefault(a)
            if 'cha' in a:
                ret[a] = self.__getChaConfig(pa,ip1,mask,ip2,config)  
            else:
                ret[a] = self.__getIntfConfig(pa,ip1,mask,config)  
        if '<-' in t:
            ret.setdefault(b)
            if 'cha' in b:
                ret[b] = self.__getChaConfig(pb,ip2,mask,ip1,config)
            else:
                ret[b] = self.__getIntfConfig(pb,ip2,mask,config)
    
        return ret
    
    def topoVirtualPortCreate(self, path,virtualport,config=None,setip=True):
        #创建虚端口
        # setip = True 配置一个地址, 否则不配置地址
        self.__initlib()    
        (a,b,t,pa,pb) = self.topo.topGetRealPath(path)
        if 'smartgroup' in virtualport:
            tmppath=a+'.'+virtualport+t+b+'.'+virtualport
            self.topo.topoCreateVirtualPortLine(tmppath)
        if 'loopback' in virtualport:
            net = self.topo.topoGetNet('_TOPOBASE_loopback')
        else:
            net = self.topo.topoGetNet()
        ret = dict()
        ret.setdefault(a,dict())
        ret[a].setdefault('int',dict())
        ret[a]['int'][virtualport] = {}
        if setip :
            ret[a]['int'][virtualport] = {
                'ipv4'   : self.topo.topoGetNetRandIP(net),
                'maskv4' : '255.255.255.0',
                }
        if b and '<-' in t:
            ret.setdefault(b,dict())
            ret[b].setdefault('int',dict())
            ret[b]['int'][virtualport] = dict()
            if setip :
                ret[b]['int'][virtualport] = {
                    'ipv4'   : self.topo.topoGetNetRandIP(net),
                    'maskv4' : '255.255.255.0', #sg口的不能为全255
                    }
        self.topo.topoRunConfig(ret)
    
    def TopoVirtualGetPortLine(self, path):
        lineall = []
        #取smartgroup
        
        return lineall

    def TopoPortCreate(self,path):
         #创建测试仪端口，可以收发报文，不创建host
        self.__initlib()
        ret = self.__getPortConfigNoHost(path)
        self.topo.topoRunConfig(ret)

    def TopoPortSet(self, path,config=None):
        #配置端口(包含设备上接口信息的配置 以及 测试仪端口host等信息的配置)
        #默认： config['arpd'] = 'enable' , config['FlagPing'] = 'enable'
        self.__initlib()
        ret = self.__getPortConfig(path,config)
        self.topo.topoRunConfig(ret)
        
    def topoPortDel(self, path,config=None):
        #删除端口配置: 若是子接口，则删除子接口；若为物理口，则清除物理口的配置
        self.__initlib()
        (a,b,t,pa,pb) = self.topo.topGetRealPath(path)
        ret = {}
        if '->' in t:
            if 'cha' in a:
                __portName = self.testerlib.getPortNameByLocation(pa)
                ret[a] = {'port':{__portName:None}}
            else :
                ret[a] = {'int':{pa:{'ipv4':'','vrf':''}}}
        if '<-' in t:
            if 'cha' in b:
                __portName = self.testerlib.getPortNameByLocation(pb)
                ret.setdefault(b,dict())
                ret.setdefault(b['port'],dict())
                ret[b]['port'][__portName] =None
            else :
                ret[b] = {'int':{pb:{'ipv4':'','vrf':''}}}
        self.topo.topoClearConfig(ret)
        
    def topoPortShutdown(self, path):
        ''' shutdown path间的接口
        '''
        self.__initlib()
        (a,b,t,pa,pb) = self.topo.topGetRealPath(path)
        if '->' in t:
            if not self.topo.topoDevIsCha(a):
                self.devlib.appRun("interfaceShutdown",a,pa)
        if '<-' in t:
            if not self.topo.topoDevIsCha(a):
                self.devlib.appRun("interfaceShutdown",b,pb)
    
    def topoPortNoShutdown(self, path):
        ''' no shutdown path间的接口
        '''
        self.__initlib()
        (a,b,t,pa,pb) = self.topo.topGetRealPath(path)
        if '->' in t:
            if not self.topo.topoDevIsCha(a):
                self.devlib.appRun("interfaceNoShutdown",a,pa)
        if '<-' in t:
            if not self.topo.topoDevIsCha(b):
                self.devlib.appRun("interfaceNoShutdown",b,pb)
     
    def TopoPortGetIpv4(self, path):
        (a,b,t,pa,pb) = self.topo.topGetRealPath(path)
        ip = None
        if not self.topo.topoDevIsCha(a):
            ip = self.devlib.appRun("getIpv4ByInterface",a,pa)
        else:
            hostlist = self.testerlib.findHostByLocation(b)
            if len(hostlist) <= 0:
                ip = self.testerlib.getHostIpv4(hostlist[0])
        return ip
    
    def TopoPortGetVrf(self, path):
        #获取指定路径 a->b 路径上a设备的vrf信息 若未指定具体口，则取topo第一个
        (a,b,t,pa,pb) = self.topo.topGetRealPath(path)
        vrf = None
        if not self.topo.topoDevIsCha(a):
            vrf = self.devlib.appRun("getInterfaceVrf",a,pa)
        return vrf
    
    def topoGetVrfAndNextHop(self, path):
        #根据路径a->b获取设备的a上的vrf，以及a到设备b的下一跳信息
        (a,b,t,pa,pb) = self.topo.topGetRealPath(path)
        vrf = None
        #从a中获取vrf
        if not self.topo.topoDevIsCha(a):
            vrf = self.devlib.appRun("getInterfaceVrf",a,pa)
        #从b获取下一跳
        if not self.topo.topoDevIsCha(b):
            nh,_ = self.devlib.appRun("getIpv4AndMaskByInterface",b,pb)
        return vrf,nh
    
    def topPortGetNet(self,path):
        (a,b,t,pa,pb) = self.topo.topGetRealPath(path)
        net = None
        if not self.topo.topoDevIsCha(a):
            net = self.devlib.appRun("getInterfaceNet",a,pa)
        else:
            host = self.testerlib.getHostFirstByLocation(pa)
            net = self.testerlib.getHostIpv4(host)
        return net
    def topoPortGetNetlist(self, path):
        '''获取cha到设备的子网列表
        '''
        self.__initlib()
        ret = []
        hostlist = []
        location = self.topo.topoGetPort(path)
        hostlist = self.testerlib.findHostByLocation(location)
        for hostdst in hostlist:
            ip = self.testerlib.getHostIpv4(hostdst)
            mask = self.testerlib.getHostIpv4Mask(hostdst)
            net= _baselib.IP(ip).make_net(mask)
            ret.append(net)
        return ret
            