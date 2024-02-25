#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy , os,sys,re, random , copy
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger

__path = os.path.realpath(os.path.join(__file__,'..','..','..'))
if __path not in sys.path:sys.path.append(__path)

import base.AppBaseLib as _baselib

class Topology(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    iphigh = 184
    ipv6high = 500
    iplow  = 1
    mac = 1
    virtualiplow  = 1
    vlanid = 0
    tp_src = 2000
    tp_dst = 2100
    def __init__(self):
        '''
        物理拓扑记录的是物理连接信息 ， 不应该在初始化后改变
        拓扑类提供查找或获取端口信息
        提供全局动态资源获取（网络，IP地址，MAC地址，vlanid的分配）
        
        cha(host1)---A --- B --- C---cha(host2)
                     \         /
                      \       /
                       \     /
                        \   /
                          D
                    
                devices = {'A' : {'mngip': '1.1.1.1','port':'2001','type':'rosng'},
                           'cha1' : {'mng': '2.2.2.2','port':'9090',type:'cha'},
                   }
                topo = {
                     'tree' : { 'A' :{
                                   'B': [{'porta':'fei-0/1/1/1','portb':'fei-0/2/1/1'}]
                                   }
                                'B' : {
                                   'A': [{'porta':'fei-0/2/1/1','portb':'fei-0/1/1/1'}] 
                                   }
                        },
                    #线段信息
                    'line' : {
                        'A->B' : [],
                        }
                    #单设备的虚口信息不存top结构中，但是sg属于设备间的，可以存入top
                    'port':{
                            'A->B':set(['fei-0/1/1/1']),
                            'B->A':set(['fei-0/2/1/1']),
                            'cha->A':set(['101/ovsbr0']), 测试仪中端口存的是location信息
                    },
                    #虚拟port应放置到业务中，而非topo中
                    'virtualport':{
                            'A->B':set(['fei-0/1/1/1.1','smartgroup1','smartgroup1.1']),
                            'B->A':set(['fei-0/2/1/1.1']),
                    },
             }
        '''
        self.devalias = dict()
        self.devices = dict()
        self.topo = dict()
        self.net = dict()
        self.net6 = dict()
        self.lastgetpath = None
        self.env=dict()

    def __initlib(self):
        self.devlib = BuiltIn().get_library_instance('AppDevice')
        self.dutlib = BuiltIn().get_library_instance('AppDut')
        self.testerlib = BuiltIn().get_library_instance('Tester')

    def __var(self,name,default=None):
        ret = BuiltIn().get_variable_value('${'+name+'}',default)
        return ret

    def __splitePort(self, port):
        '''只支持下面几种输入方式
           A              ret: (A,None)
           A.1            ret: (A,1)
           A.fei-0/20/0/1 ret: (A,fei-0/20/0/1)
           A.dut1port     ret: (A,dut1port1)
           cha            ret: (cha,None)
           A.port1  这种方式不支持，仅支持上述几种方式
        '''
        if '.' not in port:
            return (port,None)
        if '->' in port or '<-' in port: #port仍然为多段的 则直接返回
            return (port,None)
        ret = re.search(r'(\S+?)\.(\S*)',port)
        if ret:
            if not ret.group(2) :
                return (ret.group(1),None)
            else:
                return (ret.group(1),ret.group(2))
        else:
            raise AssertionError("split port error %s"%port)
        
    def _combinePort(self, a,pa):
        if pa == None:
            return a
        return "{}.{}".format(a,pa)
    
    def _spliteDevice(self, path):
        # A.1->B.1  ret: A,B,type=<-> <- ->,1,1
        # A.1       ret:(A,None,None,1,None)
        # A         ret:(A,None,None,None,None)
        if '->' not in path and '<-' not in path:
            (a,pa) = self.__splitePort(path)
            return (a,None,None,pa,None)
        
        ret = re.match(r"(\S+?)(<->|<-|->)(\S+)",path)
        if ret:
            (a,pa) = self.__splitePort(ret.group(1))
            t = ret.group(2)
            
            (b,pb) = self.__splitePort(ret.group(3))
            return (a,b,t,pa,pb)
        return (None,None,None,None,None)
    
    def _combineDevice(self,a,b,t,pa,pb):
        if t != None:
            return self._combinePort(a,pa) + t + self._combinePort(b,pb)
        else:
            return self._combinePort(a,pa)

    def topoClear(self):
        '''清除所有拓扑信息
        
        | 正常不会被使用，topo在初始化后不应该改变
         
        '''
        xxx
    
    def topoRunConfig(self, config):
        '''执行配置
        
        | config = {
        |     'A' : {},
        |     'cha1'   : {}    
        | }
        '''
        self.__initlib()
        for dev,v in config.items():
            typedev = self.devices[dev]['type']
            if 'cha' == typedev:
                self.testerlib.chaConfig(config)
            else:
                self.devlib.appRunConfig(dev,v)
        return True

    def topoClearConfig(self, config):
        '''清除topo配置
        '''
        self.__initlib()
        for dev,v in config.items():
            typedev = self.devices[dev]['type']
            if 'cha' == typedev:
                self.testerlib.chaClearConfig({dev:v})  #清除设备配置
                pass
            else:
                self.devlib.appRunConfig(dev,v)
        return True
    
    def topoSplitePath(self, path):
        '''将路径分为子段
        
         | cha -- A --- B --- C -- cha 
         | (A->B->C)  ret: [A->B,B->C]
         | (A.1->B.2->C) ret: [A.1->B,B.2->C]
        '''
        num = 10
        ret = []
        (_a,_b,_t,_pa,_pb) = self._spliteDevice(path)
        while (num > 0) :
            num -= 1
            (a,b,t,pa,pb) = self._spliteDevice(_b)
            if _a != None and a != None:
                ret.append(self._combineDevice(_a,a,_t,_pa,None))
            if t == None:
                break
            (_a,_b,_t,_pa,_pb) = (a,b,t,pa,pb)
        logger.debug("topoSplitePath: path %s, %s"%(str(path),str(ret)))
        return ret
    
    def topoDevType(self, path):
        '''获取左侧设备类型
            rosng / cha / cisco
        '''
        (a,b,t,pa,pb) = self._spliteDevice(path)
        if a not in self.devices:
            raise AssertionError("Can't find device {}".format(a))
        return self.devices[a]['type']
    
    def topoCheckDeviceType(self, path,devtype):
        '''获取左侧设备类型
            sonic / rosng / cha / cisco
        '''
        (a,b,t,pa,pb) = self._spliteDevitce(path)
        if a not in self.devices:
            raise AssertionError("Can't find device {}".format(a))
        return self.devices[a]['type'] == devtype

    def topoDevIsCha(self, dev):
        '''判断设备是否测试仪
        '''
        if dev not in self.devices:
            return None
        typedev = self.devices[dev]['type']
        if typedev == 'cha':
            return True
        return False

    def topoDevIsRosng(self, dev):
        '''判断设备是否基于ROSNG的设备
        '''
        if dev not in self.devices:
            return None
        typedev = self.devices[dev]['type']
        if typedev == 'rosng':
            return True
        return False
    
    def topoPathDirectAll(self, path):
        '''获取直连路径所有的物理链路
        '''
        if not self.topoPathIsDirect(path):
            raise AssertionError("not direct path %s"%path)
        (a,b,t,pa,pb) = self._spliteDevice(path)
        if pa != None or pb != None:
            return [path]
        port = self.topo['port']

        if a+'->'+ b not in port:
            return None
        ret = []
        portnum = self.topoGetPortNum(a+'->'+ b)
        for i in range(1,portnum+1):
            ret.append(self._combineDevice(a,b,t,i,i))
        return ret
    
    def topoPathIsSingle(self, path):
        #判断path是否单段
        ret = False
        pathlist = self.topoSplitePath(path)
        if len(pathlist) <= 0 : ret = False
        if len(pathlist) == 1 : ret = True
        return ret
    
    def topoPathIsDirect(self, path):
        #判断path是否单段 并且是物理上直连
        ret = False
        if not self.topoPathIsSingle(path):
            return ret
        port = self.topo['port']
        (a,b,t,pa,pb) = self._spliteDevice(path)
        if a+'->'+ b not in port:
            return False
        return True
    
    def __devRead(self):
        _dev_list = dict()
        for dut in ["dut1","dut2","dut3","dut4","cha1","cha2"]:
            _dev_list[dut.upper()] = {
                'ip' :  self.__var(dut+'ip'),
                'port' : self.__var(dut+'port',None),
                'restful' : self.__var(dut+'restful',8090),
                'protocol' : self.__var(dut+'protocol',"ssh"),
                'type' : self.__var(dut+'type',"cha"),
                'username'  :  self.__var(dut+'user',""),
                'password'  :  self.__var(dut+'password',"")
            }
        return _dev_list

    def topoLoad(self, toponame=None):
        '''拓扑初始化: 从TOP_env中获取拓扑
        | toponame = 'top21', 'top40', 'top10'
        '''
        _dev = self.__devRead()
        if toponame == 'cha':
            self.topoCreateDeviceByConfig('_A',_dev['CHA1'])
        elif toponame == 'dut':
            self.topoCreateDeviceByConfig('_A',_dev['DUT1'])
        elif toponame == 'top11':
            self.topoCreateDeviceByConfig('_A',_dev['DUT1'])
            self.topoCreateDeviceByConfig('cha',_dev['CHA1'])
            self.topoCreateLine('_A.{}<->cha.{}'.format(self.__var('dut1port101'),self.__var('cha1port1')))
            self.topoCreateLine('_A.{}<->cha.{}'.format(self.__var('dut1port102'),self.__var('cha1port2')))
        elif toponame == 'top12':
            self.topoCreateDeviceByConfig('_A',_dev['DUT1'])
            self.topoCreateDeviceByConfig('cha1',_dev['CHA1'])
            self.topoCreateDeviceByConfig('cha2',_dev['CHA2'])
            self.topoCreateLine('_A.{}<->cha1.{}'.format(self.__var('dut1port101'),self.__var('cha1port1')))
            self.topoCreateLine('_A.{}<->cha2.{}'.format(self.__var('dut1port201'),self.__var('cha2port1')))
        elif toponame == 'top21':
            self.topoCreateDeviceByConfig('_A',_dev['DUT1'])
            self.topoCreateDeviceByConfig('_B',_dev['DUT2'])
            self.topoCreateDeviceByConfig('cha',_dev['CHA1'])
            
            self.topoCreateLine('_A.{}<->_B.{}'.format(self.__var('dut1port1'),self.__var('dut2port1')))
            if self.__var('dut1port2',"") != "":
                self.topoCreateLine('_A.{}<->_B.{}'.format(self.__var('dut1port2'),self.__var('dut2port2')))
            self.topoCreateLine('_A.{}<->cha.{}'.format(self.__var('dut1port101'),self.__var('cha1port1')))
            self.topoCreateLine('_B.{}<->cha.{}'.format(self.__var('dut2port102'),self.__var('cha1port2')))
            if self.__var('dut1port6',"") != "":
                self.topoCreateLine('_A.{}<->_B.{}'.format(self.__var('dut1port6'),self.__var('dut2port6')))
            if self.__var('dut1port7',"") != "":
                self.topoCreateLine('_A.{}<->_B.{}'.format(self.__var('dut1port7'),self.__var('dut2port7')))

        else:
            raise AssertionError("Unknow top name {}".format(toponame))
    
    def topoCreateDevice(self, dev, mngip,port=22,dut='',typedev='sonic',username='who',password='who',docker=None):
        '''拓扑初始化: 增加设备名称
        '''
        #'A' : {'mngip': '1.1.1.1','port':'2001','type':'rosng','dut':'dut1'}
        #type = rosng cha cisco xxx linux
        self.devices.setdefault(dev,dict())
        self.devices[dev]['mngip'] = mngip
        self.devices[dev]['port'] = port
        self.devices[dev]['type'] = typedev
        self.devices[dev]['username'] = username
        self.devices[dev]['password'] = password
        self.devices[dev]['docker'] = docker
        return True

    def topoCreateDeviceByConfig(self, dev, config=dict()):
        '''拓扑初始化: 增加设备名称
        '''
        #config {'mngip': '1.1.1.1','port':'2001','type':'rosng','dut':'dut1'}
        #type = rosng cha cisco xxx linux
        self.devices.setdefault(dev,dict())
        self.devices[dev]['mngip'] = config["ip"]
        self.devices[dev]['port'] = config["port"]
        self.devices[dev]['type'] = config['type']
        self.devices[dev]['restful'] = config.get("restful",None)
        self.devices[dev]['docker'] = config.get('docker',None)
        self.devices[dev]['username'] = config.get('username',None)
        self.devices[dev]['password'] = config.get('password',None)
        return True

    def topoCreateLine(self, line):
        '''拓扑初始化: 增加设备间连接
            注： 必须指定实际的接口
        '''
        # 创建时必须指定端口
        # example: A.fei-0/20/0/6<->B.fei-0/20/0/7
        self.topo.setdefault('tree',dict())
        self.topo.setdefault('port',dict())

        port = self.topo['port']
        (a,b,t,pa,pb) = self._spliteDevice(line)
        BuiltIn().should_be_true(pa != None,"A port is None(%s)"%line)
        BuiltIn().should_be_true(pb != None,"B port is None(%s)"%line)
        logger.info("LINE(%s): %s %s %s %s %s"%(line,a,b,t,pa,pb))
        #print "path(%s): %s %s %s %s %s"%(line,a,b,t,pa,pb)
        '''
        tree.setdefault(a,dict())
        tree[a].setdefault(b,list())
        tree.setdefault(b,dict())
        tree[a].setdefault(b,list())
        if pa and pb:
            tree[a][b].append({'porta':pa,'portb':pb})
            tree[b][a].append({'porta':pb,'portb':pa})
        '''
        port.setdefault(a+'->'+b,list())
        port.setdefault(b+'->'+a,list())
        port[a+'->'+b].append(pa)
        port[b+'->'+a].append(pb)
        logger.debug("topo port: %s"%str(self.topo['port']))
        return True
    
    def __devConnect(self, dev):
        '''连接设备
        '''
        dev = self.__devGetReal(dev)
        if dev not in self.devices:
            raise AssertionError("Can't find this dev '{}'!".format(dev))
        devinfo = self.devices[dev]
        if 'mngip' not in self.devices[dev]:
            raise AssertionError("DEV {} has not mng ipaddress!".format(dev))
        logger.info("Connect DEV {} : {}".format(dev,devinfo))
        if self.topoDevIsCha(dev):
            t = devinfo.get('type','trex')
            if 'port' in devinfo:
                self.testerlib.testerConnect(devinfo['mngip'],devinfo['port'],t)
            else:
                self.testerlib.testerConnect(devinfo['mngip'],t)
            #todo : 创建端口
        else:
            config = copy.deepcopy(devinfo)
            config['ip'] = config.pop('mngip')
            self.dutlib.dutConnectConfig(dev,config)

    def __devDisconnect(self, dev):
        '''断开设备  （暂不支持）
        '''
        dev = self.__devGetReal(dev)
        if dev not in self.devices:
            raise AssertionError("Can't find this dev '{}'!".format(dev))
        devinfo = self.devices[dev]
        logger.info("Disconnect DEV {} : {}".format(dev,devinfo))
        xxx
        
    def __devGetReal(self,dev):
        #根据别名获取实际的设备名
        ret = dev
        if dev in self.devalias:
            ret = self.devalias[dev]
        if ret not in self.devices:
            raise AssertionError("Can't find the dev({})!".format(dev))
        return ret
    
    def topoDevAlias(self, name,dev):
        #为设备名设置一个别名
        dev = self.__devGetReal(dev)
        self.devalias[name] = dev

    def topoDevSet(self,*args):
        #连接设备（列表）
        self.__initlib()
        for dev in args:
            self.__devSet(dev)

    def topoDevConnect(self, *args):
        #连接设备（列表）
        self.__initlib()
        for dev in args:
            self.__devConnect(dev)
        
    def topoDevConnectAll(self):
        #连接topo中的所有设备
        self.__initlib()
        for k in self.devices.keys():
            self.__devConnect(k)
    
    def topoDevDisconnectAll(self):
        #关闭所有设备的连接
        self.__initlib()
        for k in self.devices.keys():
            self.__devDisconnect(k)
    
    def topoCreateVirtualPortLine(self, line):
        # 创建虚拟端口（子接口，gre等）
        # 理论上应当在配置中查找，而不是在topology中查找........
        # example: A.fei-0/20/0/6.1<->B.fei-0/20/0/7.1

        self.topo.setdefault('virtualport',dict())
        port = self.topo['virtualport']
        (a,b,t,pa,pb) = self._spliteDevice(line)
        BuiltIn().should_be_true(pa != None,"A port is None(%s)"%line)
        BuiltIn().should_be_true(pb != None,"B port is None(%s)"%line)
        logger.info("LINE(%s): %s %s %s %s %s"%(line,a,b,t,pa,pb))
        port.setdefault(a+'->'+b,set())
        port.setdefault(b+'->'+a,set())
        if pa not in port[a+'->'+b]:
            port[a+'->'+b].add(pa)
        if pb not in port[b+'->'+a]:
            port[b+'->'+a].add(pb)
        logger.debug("topo port: %s"%str(self.topo['virtualport']))
        return True
    
    def topoGetVirtualPort(self, path):
        #获取设备间的虚口信息， 注：不应当放到topo，而是放到业务中 
        # A->B 返回任意一个端口
        port = self.topo['virtualport']
        (a,b,t,pa,pb) = self._spliteDevice(path)
        if pa != None:
            return pa
        if a+'->'+ b not in port:
            return None
        return list(port[a+'->'+ b])[0]
    
    def topoGetPath(self, nodeA, nodeB):
        #获取 （A<->D)间的路径 [A<->B<->D，A<->C<->D)
        pass
    
    def topGetRealPath(self, path):
        #获取实际路径的端口信息 
        # 例子: 
        #       A.1->B 返回 A B -> fei-0/20/1/1 None
        #       A.1<->B.1 返回 A B -> fei-0/20/1/1 fei-0/20/2/1
        #       A->B   返回  A B -> None None
        (a,b,t,pa,pb) = self._spliteDevice(path)
        if pa == None and pb == None : pa = pb = '1'
        inp  = list(self.topo['port'][a+'->'+ b])
        outp = list(self.topo['port'][b+'->'+ a])
        if pa in inp : pa = str(inp.index(pa)+1)
        if pb in inp : pb = str(inp.index(pb)+1)
        if pa == None : pa = pb
        if pb == None : pb = pa
        ret = re.match(r'^(\d+)$',pa)
        if ret:
            pa = inp[int(ret.group(1))-1]
        ret = re.match(r'^(\d+)$',pb)
        if ret:
            pb = outp[int(ret.group(1))-1]
        logger.info("path(%s): %s %s %s %s %s"%(path,a,b,t,pa,pb))
        return (a,b,t,pa,pb)
    
    def topoGetChaportAliasName(self, loc):
        _intf =  _topenv.env['INTF_LST']
        for k,v in _intf.items():
            if 'cha' in k and v == loc:
                return k
        return None
    
    def topoGetPort(self, path):
        #获取端口的实际值 A.2->B 返回A的与B设备连接的第二个端口
        # A->B 返回任意一个端口
        port = self.topo['port']
        (a,b,_,pa,_) = self.topGetRealPath(path)
        if pa != None:
            return pa
        if a+'->'+ b not in port:
            return None
        return list(port[a+'->'+ b])[0]
    
    def topoGetAllPort(self, path):
        '''获取接口，仅使用于单向的path
        '''
        port = self.topo['port']
        (a,b,_,_,_) = self._spliteDevice(path)
        if a+'->'+ b not in port:
            return None
        return copy.deepcopy(port[a+'->'+ b])
    
    def topoGetPortNum(self, path):
        port = self.topo['port']
        (a,b,_,_,_) = self._spliteDevice(path)
        if a+'->'+ b not in port:
            return 0
        return len(port[a+'->'+ b])
    
    def topoGetAllPortOppositePath(self, path):
        '''用于获取指定路径的反向路径上的所有接口
           eg： A->B  指的获取A到B设备的，B设备上的所有接口
        '''
        port = self.topo['port']
        (a,b,_,_,_) = self._spliteDevice(path)
        if b+'->'+ a not in port:
            return None
        return copy.deepcopy(port[b+'->'+ a])
    
    def topoGetVlanid(self):
        self.vlanid += 1
        return self.vlanid

    def topoGetMac(self, name=None):
        self.mac += 1
        self.mac = self.mac % (0xff)
        return "00:01:00:00:00:%02X"%(self.mac)

    def topoGetTpSrc(self, name=None):
        self.tp_src += 1
        return str(self.tp_src)     
    
    def topoGetTpDst(self, name=None):
        self.tp_dst += 1
        return str(self.tp_dst)

    def topoGetNet(self, name=None,prefix=24,t=4):
        '''获取随机的网段(不会和之前重复)
        
        | name 网络的别名或者是网段
        | A.B.C.D , 分配A,随机B,C , IP递增D
        | 返回值 : 1.1.1.0/24
        
        _TOPOBASE_loopback  :  默认loopback网段
        '''
        
        if name != None :
            if re.search(r"\d+\.\d+\.\d+\.\d+\/\d+",name):
                return name 
        if name in self.net:
            return self.net[name]
        self.iphigh += 1
        b = random.randint(0,255)
        c = random.randint(0,255)
        #net = "{}.{}.{}.{}/{}".format(self.iphigh,b,c,self.iplow,prefix)
        ip = "{}.{}.{}.{}".format(self.iphigh,b,c,self.iplow)
        subnet,_= _baselib.appSubNet(ip,prefix)
        net = subnet+'/'+ str(prefix)
        logger.info("[Topology]Alloc network %s"%net)
        if name:
            self.net.setdefault(name,net)
        else:
            self.net.setdefault(net,net)
        return net

    def topoGetNetv6(self, name=None,prefix=96):
        '''获取随机的网段(不会和之前重复)
        
        | name 网络的别名或者是网段
        | A.B.C.D , 分配A,随机B,C , IP递增D
        | 返回值 : 1.1.1.0/24
        
        _TOPOBASE_loopback  :  默认loopback网段
        '''
        
        if name != None :
            if re.search(r"\d+\.\d+\.\d+\.\d+\/\d+",name):
                return name 
        if name in self.net6:
            return self.net6[name]
        self.iphigh += 1
        b = random.randint(0,255)
        c = random.randint(0,255)
        #net = "{}.{}.{}.{}/{}".format(self.iphigh,b,c,self.iplow,prefix)
        ip = "{}:{}:{}::{}".format(self.iphigh,b,c,self.iplow)
        subnet,_= _baselib.appSubNet(ip,prefix)
        net = subnet+'/'+ str(prefix)
        logger.info("===net %s"%net)
        if name:
            self.net6.setdefault(name,net)
        else:
            self.net6.setdefault(net,net)
        return net

    def topoGetNetRandIP(self, name):
        #根据网段，随机生成一个IP
        net = self.topoGetNet(name)
        if net == None:
            net = name
        self.iplow += 1
        ipnet = _baselib.IP(net,make_net=True)
        ip = ipnet[self.iplow&0xff]
        logger.info("Create a ip {} by {}({})".format(ip, net, name))
        return str(ip)

    def topoGetNetRandIPv6(self, name):
        #根据网段，随机生成一个IP
        net = self.topoGetNetv6(name)
        if net == None:
            net = name
        self.iplow += 1
        ipnet = _baselib.IP(net,make_net=True)
        ip = ipnet[self.iplow&0xff]
        logger.info("Create a ip {} by {}({})".format(ip, net, name))
        return str(ip)

    def topoGetDev(self):
        return self.devices.keys[0]

    def TopoGetTop4Type1(self):
        # cha---_A --_B---_D---cha
        #       |         |
        #       ---_C------
        self.lastgetpath = ('_A','_B','_C','_D')
        return self.lastgetpath
    
    def TopoGetTop2Type1(self):
        # cha---_A --_B---cha
        self.lastgetpath = ('_A','_B')
        return self.lastgetpath
    
    def TopoGetTop1Type1(self):
        self.lastgetpath = '_A'
        return self.lastgetpath
    
    def TopoGetLastToptype(self):
        #todo获取当前设备组网的path  后续根据算法选择出当前路径
        return self.lastgetpath
    
    
if __name__ == '__main__':
    
    t = Topology()
   # t.topGetRealPath('A.fei-0/20/0/1.1<->B.fei-0/20/0/1.1')
    #t.topoSplitePath("A->B->C")
    print  ("path:","A->B.1->C.2->D")
    t.topoSplitePath("A->B.1->C.2->D")
    print  ("path:","A.1->B.1->C.2->D->E->F")
    t.topoSplitePath("A.1->B.1->C.2->D->E->F")
    '''
    net = t.topoGetNet()
    t.topoGetNetRandIP(net)
    t.topoGetNetRandIP(net)
    t.topoGetNetRandIP(net)
    
    net = t.topoGetNet()
    t.topoGetNetRandIP(net)
    t.topoGetNetRandIP(net)
    t.topoGetNetRandIP(net)
    
    net = t.topoGetNet("loopback")
    t.topoGetNetRandIP(net)
    t.topoGetNetRandIP(net)
    t.topoGetNetRandIP(net)
    
    print ("===net========",str(t.net))
    
    t = Topology()
    t.topoGetRandIP()
    t.topoGetRandIP()
    t.iplow = 1
    t.topoGetRandIP()
 
    print "====",_topenv.env['INTF_LST']
    t = Topology()
    t.topGetRealPath('A.dut1port1<->char.host1')
    
    #创建top结构以及设备信息
    t.topoCreateDevice('A','10.42.119.55','2001')
    t.topoCreateDevice('B','10.42.119.55','2003')
    t.topoCreateDevice('C','10.42.119.55','2004')
    
    t.topoCreateLine('A.dut1port1<->B.dut2port1')
    t.topoCreateLine('B.dut2port2<->C.dut3port1')
    t.topoCreateLine('A.dut1port2->cha')
    t.topoCreateLine('C.dut3port2->cha')
    t.topoCreateLine('A.fei-0/20/0/1->B.fei-0/20/0/2')
      
    print "device: ",str(t.devices)
    print "topo: ",str(t.topo)
    
    print "============real path=================="
    t.topGetRealPath('A.dut1port1<->B.dut2port1')
    t.topGetRealPath('A.1<->B.1')
    t.topGetRealPath('A<->B')
    t.topGetRealPath('A.port1->B.1')
    t.topGetRealPath('A.1->B')
    t.topGetRealPath('A.dut1port1')
 
    #配置设备
    conf = t.TopoGetPortconfig('A.1<->B.1')
    t.topoRunConfig(conf)
    '''