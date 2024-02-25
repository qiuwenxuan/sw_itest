#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, copy, os, sys
import collections
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Collections import Collections
#from scapy.arch.windows.structures import TUNNEL_TYPE

__path = os.path.realpath(os.path.join(__file__,'../..')) 
if __path not in sys.path:sys.path.append(__path)

import base.AppBaseLib as _baselib

class TopoScene(object):
    '''场景初始化类
       
    topology中的顶层类， 不应被topo中的其他类引用
    '''
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    def __init__(self):
        self.topo = None
        pass
        
    def __initlib(self):
        if self.topo :
            return
        self.topo = BuiltIn().get_library_instance('Topology')
        self.topobase = BuiltIn().get_library_instance('TopoBase')
        self.linux = BuiltIn().get_library_instance('Linux')
        self.ovs = BuiltIn().get_library_instance('Ovs')
        self.testerlib = BuiltIn().get_library_instance('Tester')

    def isCheckHwOffload(self):
        info  = BuiltIn().get_variable_value('${hwoffload}',None)
        return info

    def __setOvsGlobal(self,dut,config):
        if 'hw-offload' in config:
            self.ovs.setOvsConfig(dut,{'hw-offload':config['hw-offload']})

    def sceneRouteInit(self, A,B,line=1):
        '''路由环境初始化 A与B设备直连线通过入参传入
         路由环境的初始化不包含配置路由，路由在各个案例中配置        
         cha ---->A<-------->B----->cha
                   <-------->
                
        '''
        self.__initlib()
        for i in range(1,int(line)+1):
           self.topobase.topoPortNoShutdown(A+'.'+str(i)+"<->"+B+'.'+str(i))
           self.topobase.TopoPortSet(A+'.'+str(i)+"<->"+B+'.'+str(i))
        self.topobase.topoPortNoShutdown(A+'<->cha')
        self.topobase.topoPortNoShutdown(B+'<->cha')
        self.topobase.TopoPortSet(A+'<->cha')
        self.topobase.TopoPortSet(B+'<->cha')
    
    def sceneOvsSigleBridgeInit(self,A,*args):
        '''单桥ovs环境        
         cha <---->A<----->cha
                
        '''
        self.__initlib()

        config = _baselib.appTransformToDict(*args)
        self.__setOvsGlobal(A,config)
        info = self.ovs.getOvsVersion(A)
        logger.info("Version : %s"%str(info))
        #查找端口，可能端口是jmnd已经创建的端口
        #self.topobase.TopoPortSet('cha.1->'+A+'.1')
        #self.topobase.TopoPortSet('cha.2->'+A+'.2')
        port1 = self.topo.topoGetPort(A+'.1<->cha')
        port2 = self.topo.topoGetPort(A+'.2<->cha')
        BuiltIn().should_be_true(self.ovs.isPci(port1) or self.ovs.isPci(port2), 
                                    "No pci port set(%s,%s)!"%(port1,port2))
        #释放PCI端口
        self.ovs.ovsPortsRelease(A,[port1,port2])

        #找到jmd端口创建的网桥，或者创建网桥
        ovsport1 = self.ovs.getRealPort(A,port1)
        ovsport2 = self.ovs.getRealPort(A,port2)
        br = self.ovs.getNewBridgeName()
        if ovsport1 != None:
            br = self.ovs.getBridgeByPort(A,ovsport1)
        if ovsport2 != None:
            br = self.ovs.getBridgeByPort(A,ovsport2)

        #初始化配置
        ovsconf = {
            "bridge" : {
                br:{
                    'port' : dict()
                }
            },
        }
        val_port = ovsconf['bridge'][br]['port']
        if self.ovs.isPci(port1):
            ovsport1 = self.ovs.getNewPortName()
            val_port[ovsport1] = {'options':{'dpdk-devargs':port1}}
        if self.ovs.isPci(port2):
            ovsport2 = self.ovs.getNewPortName()
            val_port[ovsport2] = {'options':{'dpdk-devargs':port2}}
        self.ovs.ovsRunConfig(A,ovsconf)
        
        #清除桥上的流表
        self.ovs.clearFlow(A,br) 
        #创建测试仪端口
        self.sceneOvsInlineInit(A,*args) 

    def sceneOvsDoubleBridgeInit(self,A,*args):
        '''为每个端口创建不同网桥
         cha <---->A<----->cha
                
        '''
        self.__initlib()
        config = _baselib.appTransformToDict(*args)
        self.__setOvsGlobal(A,config)

        logger.info("[sceneOvsDoubleBridgeInit] Create Ovs scene")
        #查找端口，可能端口是jmnd已经创建的端口
        port1 = self.topo.topoGetPort(A+'.1<->cha')
        port2 = self.topo.topoGetPort(A+'.2<->cha')
        BuiltIn().should_be_true(self.ovs.isPci(port1) or self.ovs.isPci(port2), 
                                    "No pci port set(%s,%s)!"%(port1,port2))
        #释放PCI端口
        self.ovs.ovsPortsRelease(A,[port1,port2])
        logger.info("[sceneOvsDoubleBridgeInit] Work at port [%s] [%s]"%(port1,port2))
        #初始化配置
        ovsconf = {
            "bridge" : {
            },
        }
        
        if self.ovs.isPci(port1):
            br1 = self.ovs.getNewBridgeName()
            ovsport1 = self.ovs.getNewPortName()
            ovsconf['bridge'][br1] = dict()
            ovsconf['bridge'][br1] = {
                        'port': {ovsport1 : {'options':{'dpdk-devargs':port1}}
                            }
                        }
        if self.ovs.isPci(port2):
            br2 = self.ovs.getNewBridgeName()
            ovsport2 = self.ovs.getNewPortName()
            ovsconf['bridge'][br2] = {
                        'port': {ovsport2 : {'options':{'dpdk-devargs':port2}}
                            }
                        }
        tun_br,ip_br  = br1,br2
        if 'reverse' in config:
            tun_br,ip_br  = br2,br1

        #创建隧道
        if 'tun_type' in config:
            tunport = self.ovs.getNewPortName()
            net = config.get('tun_net',self.topo.topoGetNet())
            mask = _baselib.IP(net).strNetmask()
            ip1 = config.get('tun_remote',self.topo.topoGetNetRandIP(net))
            ip2 = config.get('tun_local',self.topo.topoGetNetRandIP(net))
            ovsconf['bridge'][tun_br]['port'][tunport] = {
                'type' : config['tun_type'],
                'options':{'remote_ip':ip1,'local_ip':ip2,
                                'in_key':100,'out_key':100}}
            
        self.ovs.ovsRunConfig(A,ovsconf)
        self.ovs.clearFlow(A,tun_br) #清除桥上的流表
        if 'tun_type' in config:
            self.linux.addInterfaceConfig(A,{ip_br:{
                    'ipv4' : ip2,
                    'maskv4' : mask,
                }})
            self.linux.interfaceNoShutdown(A,ip_br)
        #创建测试仪端口
        self.sceneOvsInlineInit(A,*args) 

    def sceneOvsThreeBridgeInit(self,A,*args):
        '''为每个端口创建不同网桥，额外创建一个空的网桥
         cha <---->A<----->cha
         
                
        '''
        self.__initlib()
        config = _baselib.appTransformToDict(*args)
        self.__setOvsGlobal(A,config)

        logger.info("[sceneOvsDoubleBridgeInit] Create Ovs scene")
        #查找端口，可能端口是jmnd已经创建的端口
        port1 = self.topo.topoGetPort(A+'.1<->cha')
        port2 = self.topo.topoGetPort(A+'.2<->cha')
        BuiltIn().should_be_true(self.ovs.isPci(port1) or self.ovs.isPci(port2), 
                                    "No pci port set(%s,%s)!"%(port1,port2))
        #释放PCI端口
        self.ovs.ovsPortsRelease(A,[port1,port2])
        logger.info("[sceneOvsDoubleBridgeInit] Work at port [%s] [%s]"%(port1,port2))
        #初始化配置
        ovsconf = {
            "bridge" : {
            },
        }
        
        if self.ovs.isPci(port1):
            br1 = self.ovs.getNewBridgeName()
            
            ovsport11 = self.ovs.getNewPortName()
            ovsport12 = self.ovs.getNewPortName()
            ovsport32 = self.ovs.getNewPortName()
            ovsconf['bridge'][br1] = dict()
            ovsconf['bridge'][br1] = {
                        'port': {ovsport11 : {'options':{'dpdk-devargs':port1}},
                                 ovsport12 : {'type':'patch','options':{'peer':ovsport32}}
                            }
                        }
            br3 = self.ovs.getNewBridgeName()
            
            ovsconf['bridge'][br3] = dict()
            ovsconf['bridge'][br3] = {
                        'port': {ovsport32 : {'type':'patch','options':{'peer':ovsport12}}
                            }
                        }
        if self.ovs.isPci(port2):
            br2 = self.ovs.getNewBridgeName()
            ovsport2 = self.ovs.getNewPortName()
            ovsconf['bridge'][br2] = {
                        'port': {ovsport2 : {'options':{'dpdk-devargs':port2}}
                            }
                        }

        tun_br,ip_br  = br3,br2
        if 'reverse' in config:
            tun_br,ip_br  = br3,br2

        #创建隧道
        if 'tun_type' in config:
            tunport = self.ovs.getNewPortName()
            net = config.get('tun_net',self.topo.topoGetNet())
            mask = _baselib.IP(net).strNetmask()
            ip1 = config.get('tun_remote',self.topo.topoGetNetRandIP(net))
            ip2 = config.get('tun_local',self.topo.topoGetNetRandIP(net))
            ovsconf['bridge'][tun_br]['port'][tunport] = {
                'type' : config['tun_type'],
                'options':{'remote_ip':ip1,'local_ip':ip2,
                                'in_key':100,'out_key':100}}
            
            
        self.ovs.ovsRunConfig(A,ovsconf)
        self.ovs.clearFlow(A,br1) #清除桥上的流表

        #把tun桥的2个口打通
        self.ovs.clearFlow(A,tun_br) #清除桥上的流表
        _flowconfig={'match':{'in_port':ovsport32},
                    'action':{'output':tunport,'type':'fwd'}}
        self.ovs.setFlow(A, tun_br, _flowconfig)
        _flowconfig={'match':{'in_port':tunport},
                    'action':{'output':ovsport32,'type':'fwd'}}
        self.ovs.setFlow(A, tun_br, _flowconfig)

        #配置出接口网桥ip地址
        if 'tun_type' in config:
            self.linux.addInterfaceConfig(A,{ip_br:{
                    'ipv4' : ip2,
                    'maskv4' : mask,
                }})
            self.linux.interfaceNoShutdown(A,ip_br)
        #创建测试仪端口
        self.sceneOvsInlineInit(A,*args) 

    def sceneOvsInlineInit(self,A,*args):
        '''ovs已经配置好隧道 ,仅创建Cha端口      
         cha <---->A<----->cha
                
        '''
        self.__initlib()
        config = _baselib.appTransformToDict(*args)

        if 'tun_port' in config:
            tunnel_port = config['tun_port']
        else:
            tunnel_port = self.ovs.findInterfaceFirstTunnel(A)
        

        port1  = self.topo.topoGetPort(A+".1->cha")
        port2 = self.topo.topoGetPort(A+".2->cha")
        #找到实际的端口
        port1 = self.ovs.getRealPort(A,port1)
        port2 = self.ovs.getRealPort(A,port2)
        port1_br = self.ovs.getBridgeByPort(A,port1)
        port2_br = self.ovs.getBridgeByPort(A,port2)
        
        #如果出和入在一个网桥，那么按单网桥处理
        if tunnel_port == None or port1_br == port2_br:
            self.topobase.TopoPortSet('cha.1->%s'%A)
            self.topobase.TopoPortSet('cha.2->%s'%A)
            return

        info = self.ovs.ovsGetTunnelInfo(A,tunnel_port)
        if info == None or info.get('knl_intf',None) == None :
            self.topobase.TopoPortSet('cha.1->%s'%A)
            self.topobase.TopoPortSet('cha.2->%s'%A)
            return
        
        BuiltIn().should_be_true(info['knl_intf'] != None,"[TopoScene]Can't find local ip(%s) in kernel!"%info['local_ip'])
        config['ip1'] = info['remote_ip']
        config['ip2'] = info['local_ip']
        config['net'] = _baselib.appIpExGetNet(info['knl_ipex'])
        #V6暂不关注ARP
        if _baselib.appIsIpv6(config['net']):
            self.topobase.TopoPortSet('cha.1->%s'%A)
            self.topobase.TopoPortSet('cha.2->%s'%A)
        elif port1_br == info['knl_intf']:
            self.topobase.TopoPortSet('cha.1->%s'%A,config)
            self.topobase.TopoPortSet('cha.2->%s'%A)
        elif port2_br == info['knl_intf']:
            self.topobase.TopoPortSet('cha.1->%s'%A)
            self.topobase.TopoPortSet('cha.2->%s'%A,config)
        else:
            BuiltIn().should_be_true(0,"[TopoScene]Tunnel outport is not ")
        return

    def sceneOvsDeinit(self,A,*args):
        '''单桥ovs环境 清除环境           
        '''
        #删除所以自动化中配置的网桥和配置
        self.ovs.ovsClearConfig(A)  
        self.ovs.ovsCleanAuto(A)

    def sceneTestpmdInlineInit(self,A,*args):
        '''仅创建Cha端口      
         cha <---->A<----->cha
                
        '''
        self.__initlib()
        config = _baselib.appTransformToDict(*args)

        self.topobase.TopoPortSet('cha.1->%s'%A)
        self.topobase.TopoPortSet('cha.2->%s'%A)

        return

    def sceneTestpmdDeinit(self,A,*args):
        '''单桥ovs环境 清除环境           
        '''
        pass

    def Topo11Init(self,A,args):
        '''Ovs 环境初始化 包含ip地址配置
                
         cha ---->A----->cha
           
        '''
        self.__initlib()
        config = {}
        config = _baselib.appTransformToDict(*args)
        #self.topobase.TopoPortSet('cha.1->cha.2')


    def Topo20Init(self,A,B,*args):
        '''路由环境初始化 包含ip地址配置 以及路由配置
                
         cha ---->A<-------->B----->cha
                   <-------->
        
        arg参数列表:
        -line=1 | -route=True
        解析为
        | 参数名    | 默认值 | 说明 |
        | line      |  1      | A<->B间配置几对ip |
        | route     |  True   | 场景初始化时是否配置A到host2的路由 True添加 False不添加 |        
        '''
        self.__initlib()
        config = {}
        config = _baselib.appTransformToDict(*args)
        line = int(config.get('line',1))
        addroute = config.get('route','True')
        self.topobase.TopoPortSet(A+'<->cha')
        self.topobase.TopoPortSet(B+'<->cha')
        if addroute=='True':
            netlist = self.topobase.topoPortGetNetlist("{}->{}".format('cha',B))
            for i in range(1,int(line)+1):
                path = "{}.{}<->{}.{}".format(A,i,B,i)
                self.topobase.TopoPortSet(path)
                for net in netlist:
                    self.toporoute.TopoRouteStaSet(path,net)
    
    def Top20VlanInit(self,A,B,*args):
        '''创建vlan测试环境  cha ---->A<----port子接口---->B----->cha   
        
        arg参数列表:
        -line=1 | -route=True
        解析为
        | 参数名    | 默认值 | 说明 |
        | line      |  1      | A<->B间配置几对ip |
        | route     |  True   | 场景初始化时是否配置A到host2的路由 True添加 False不添加 |
        | sub       |  1      | 每个物理口子接口的个数 |
        | vlan      |  True   | 在子接口上配置vlan |
        | type      |  dot1q  | 配置的vlan类型:dot1q  dot1q-range  qinq qinq-range |
        '''
        self.__initlib()
        config = {}
        config = _baselib.appTransformToDict(*args)
        line = int(config.get('line',1))
        subnum = int(config.get('sub',1))
        addroute = config.get('route','True')
        addvlan =  config.get('vlan','True')
        
        self.topobase.TopoPortSet(A+'<->cha')
        self.topobase.TopoPortSet(B+'<->cha')
        if addroute=='True':
            netlist = self.topobase.topoPortGetNetlist("{}->{}".format('cha',B))
        for i in range(1,line+1):
            path = "{}.{}<->{}.{}".format(A,i,B,i)
            (a,b,t,pa,pb) = self.topo.topGetRealPath(path)
            for m in range(1,subnum+1):
                subpa = pa + '.' + str(m)
                subpb = pb + '.' +  str(m)
                subpath = A+'.'+subpa+'<->'+B+'.'+ subpb
                self.topo.topoCreateVirtualPortLine(subpath)
                self.topobase.TopoPortSet(subpath)
                if addroute=='True':
                    for net in netlist:
                        self.toporoute.TopoRouteStaSet(subpath,net)
                if addvlan =='True':
                    self.topobase.TopoVlanSet(subpath,config)
        return True
    
if __name__ == '__main__':
    pass
