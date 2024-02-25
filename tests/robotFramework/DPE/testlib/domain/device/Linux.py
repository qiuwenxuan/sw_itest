#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
日期 :  2015-8-21
作者 ： APP RF小组
'''
import copy , re, random,time
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
import AppBaseLib as _baselib

class Linux(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    zxins = dict()
    zxinsbk = dict()
    dutlib = None
    name = "Linux"
    def __init__(self):
        pass
    
    def __getObj(self, name):
        try:
            return BuiltIn().get_library_instance('name')
        except Exception:
            pass
        return None
        
    def __initlib(self,dut = None):
        if dut != None:
            if dut not in self.zxins:
                self.zxins[dut] = dict()
                self.zxins[dut]['ns'] = dict()
                self.zxins[dut]['int'] = dict()

        if self.dutlib == None:
            self.dutlib   = BuiltIn().get_library_instance('AppDut')
        return True

    def putfile(self,dut,src,dst):
        self.__initlib(dut)
        conn = self.dutlib.getConn(dut)
        conn.put_file(src,dst)

    def arpShow(self, dut):
        '''获取arp表
        
        | ret  = {
        |     '1.1.1.1' : {
        |         'ip'  : '1.1.1.1',
        |         'mac' : '001f.5310.521c',
        |         'arg' : 'H',             # US / 00:07:54
        |         'intf': 'fei-0/1/1/1',
        |         'vlanid-e' : '1',
        |         'vlanid-i' : '1',
        |         'intf-sub' : 'fei-0/1/1/1',
        |         },
        |     }
        '''
        ''' ip neigh
        cailei@debian:/mnt/d$ ip neigh
        172.17.0.2 dev docker0  FAILED
        10.0.2.2 dev enp0s3 lladdr 52:54:00:12:35:02 STALE
        192.168.155.1 dev enp0s8 lladdr 02:00:4c:4f:4f:50 REACHABLE
        '''
        self.__initlib(dut)
        buf = self.dutlib.process(dut,'ip -4 neigh')
        lines = buf.splitlines()
        arplist = {}
        for l in lines:
            ret = re.search(r"(\S+)\s+dev\s+(\S+)\s+([0-9A-Fa-f.]{18})\s+(\S+)",l)
            if ret:
                ip = ret.group(1)
                arplist[ip]['ip']  = ip
                arplist[ip]['age'] = ret.group(4)
                arplist[ip]['mac'] = ret.group(3)
                arplist[ip]['intf'] = ret.group(2)
        return arplist

    def neighShow(self, dut):
        '''获取arp表
        
        | ret  = {
        |     '1.1.1.1' : {
        |         'ip'  : '1.1.1.1',
        |         'mac' : '001f.5310.521c',
        |         'arg' : 'H',             # US / 00:07:54
        |         'intf': 'fei-0/1/1/1',
        |         'vlanid-e' : '1',
        |         'vlanid-i' : '1',
        |         'intf-sub' : 'fei-0/1/1/1',
        |         },
        |     }
        '''
        ''' ip neigh
        cailei@debian:/mnt/d$ ip neigh
        172.17.0.2 dev docker0  FAILED
        10.0.2.2 dev enp0s3 lladdr 52:54:00:12:35:02 STALE
        192.168.155.1 dev enp0s8 lladdr 02:00:4c:4f:4f:50 REACHABLE
        '''
        buf = self.dutlib.process(dut,'ip neigh')
        lines = buf.splitlines()
        arplist = {}
        for l in lines:
            ret = re.search(r"(\S+)\s+dev\s+(\S+)\s+lladdr\s+([0-9A-Fa-f.]{18})\s+(\S+)",l)
            if ret:
                ip = ret.group(1)
                arplist[ip]['ip']  = ip
                arplist[ip]['age'] = ret.group(4)
                arplist[ip]['mac'] = ret.group(3)
                arplist[ip]['intf'] = ret.group(2)
                arplist[ip]['state'] = ret.group(2)
        return arplist

    def ipShow(self, dut,intf=None):
        '''显示ip列表

        |   2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
        |   link/ether 08:00:27:62:0f:56 brd ff:ff:ff:ff:ff:ff
        |   inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic enp0s3
        |      valid_lft 81862sec preferred_lft 81862sec
        |   inet6 fe80::a00:27ff:fe62:f56/64 scope link 
        |      valid_lft forever preferred_lft forever         

        '''
        self.__initlib(dut)
        if intf:
            buf = self.dutlib.process(dut,"ip addr show dev %s"%intf)
        else:
            buf = self.dutlib.process(dut,"ip addr")
        lines = buf.splitlines()
        iplist = dict()
        intf = None
        for l in lines:
            ret = re.search(r"\d+\:\s+(\S+)\:\s*(.+)",l)
            if ret:
                intf = ret.group(1)
                iplist[intf] = {'ip':list(),'ipv6':list()}
                iplist[intf]['state'] = ret.group(2)
            i = l.split()
            if i[0] == 'link/ether' :
                iplist[intf]['mac'] = i[1]
            elif i[0] =='inet':
                iplist[intf]['ip'].append(i[1])
            elif i[0] =='inet6':
                iplist[intf]['ipv6'].append(i[1])
        return iplist

    def ipShowBrief(self, dut):
        '''显示ip列表

        |   lo               UNKNOWN        127.0.0.1/8 ::1/128 
        |   enp0s3           UP             10.0.2.15/24 fe80::a00:27ff:fe62:f56/64 
        |   enp0s8           UP             192.168.155.50/24 fe80::a00:27ff:fed6:af64/64 
        |   virbr0           DOWN           192.168.122.1/24 
        |   virbr0-nic       DOWN           
        |   docker0          DOWN           172.17.0.1/16 
        |   ovs-netdev       DOWN           
        |   br-ext           DOWN           

        '''
        self.__initlib(dut)
        buf = self.dutlib.process(dut,"ip -br addr")
        lines = buf.splitlines()
        iplist = dict()
        for i in lines:
            info = i.split()
            intf = info[0]
            iplist[intf]['state'] = info[1]
            if len(info) > 2: iplist[intf]['iplist'] = info[2:]
        return iplist

    def linkShowBrief(self, dut):
        '''显示接口列表

        |   lo               UNKNOWN        00:00:00:00:00:00 <LOOPBACK,UP,LOWER_UP> 
        |   enp0s3           UP             08:00:27:62:0f:56 <BROADCAST,MULTICAST,UP,LOWER_UP> 
        |   enp0s8           UP             08:00:27:d6:af:64 <BROADCAST,MULTICAST,UP,LOWER_UP> 
        |   virbr0           DOWN           52:54:00:86:f1:15 <NO-CARRIER,BROADCAST,MULTICAST,UP> 
        |   virbr0-nic       DOWN           52:54:00:86:f1:15 <BROADCAST,MULTICAST> 
        |   docker0          DOWN           02:42:60:b6:e4:86 <NO-CARRIER,BROADCAST,MULTICAST,UP> 
        |   ovs-netdev       DOWN           b2:40:90:28:62:cf <BROADCAST,MULTICAST,PROMISC> 
        |   br-ext           DOWN           08:00:27:25:bd:82 <BROADCAST,MULTICAST,PROMISC> 

        '''
        self.__initlib(dut)
        buf = self.dutlib.process(dut,"ip -br link")
        lines = buf.splitlines()
        linklist = dict()
        for i in lines:
            info = i.split()
            intf = info[0]
            linklist[intf]['state'] = info[1]
            if len(info) > 2: linklist[intf]['mac'] = info[2]
            if len(info) > 3: linklist[intf]['info'] = info[3]
        return linklist

    def getMacByIp(self, ip):
        '''通过IP获取到mac和设备名
        
        ret = ('dut1','001f.5310.521c')
        '''
        for dut in self.zxins:
            arp = self.arpShow(dut)
            if ip in arp :
                return (dut,arp[ip]['mac'])
        return(None,None)

    def bridgeIsExists(self,dut,name):
        '''是否配置过这个接口
        '''
        self.__initlib(dut) 
        if name not in self.zxins[dut]['int']:
            return True
        return False
    
    def bridgeGetList(self, dut):
        '''获取接口列表
        '''
        self.__initlib(dut)
        intfs = self.ipShow(dut)
        return intfs.keys()
        
    def getBridge(self,dut,index):
        '''
        '''
        intflist = self.bridgeGetList(dut)
        if index < len(intflist):
            return intflist[index]
        return None
        
    def gotoBridge(self, dut, name):
        '''创建桥和检查桥
        '''
        self.__initlib(dut)
        if name not in self.zxins[dut]['int']:
            self.zxins[dut]['int'][name] = dict()
        return True
            
    def setBridge(self, dut, name,config):
        '''配置接口参数
        '''
        self.__initlib(dut)
        val = self.zxins[dut]['int'][name]
        #如果vrf冲突，并且已经配置了地址,那么需要先删除地址
        #如果不是通过脚本配置，则报错
        if 'ipv4' in config:
            if config['ipv4'] == None:
                self.dutlib.process(dut,'no ip address')
                if 'ipv4' in val : del val['ipv4']
                if 'maskv4' in val : del val['maskv4']
            else:
                mask = config.get('maskv4','255.255.255.0')
                ip   = config['ipv4']
                val['ipv4']   = ip
                val['maskv4'] = mask
                self.dutlib.process(dut,'ip addr add %s dev %s'%(_baselib.appIpEx(ip,mask),name))
        if 'ipv6' in config:
            if config['ipv6'] == None:
                self.dutlib.process(dut,'no ipv6 address')
                self.dutlib.process(dut,'no ipv6 enable')
                if 'ipv6' in val : del val['ipv6']
                if 'masklen' in val : del val['masklen']
            else:
                mask = config.get('masklen',64)
                ipv6   = config['ipv6']
                val['ipv6']    = ipv6
                val['masklen'] = mask
                self.dutlib.process(dut,'ip addr add %s/%d dev %s'%(ipv6,int(mask),name))
        if 'mtu' in config:
            self.dutlib.process(dut,'ip link set dev %s mtu %d'%(name,int(config['mtu'])))
            val['mtu'] = config['mtu']
        if 'mac-address' in config:
            self.dutlib.process(dut,'ip link set dev %s address %s'%(name,config['mac-address']))
            val['mac-address'] = config['mac-address']
        return True
    
    def bridgeClear(self, dut, name,config=None):
        '''删除接口配置
        '''
        self.__initlib(dut)
        val = self.zxins[dut]['int'][name]
        #如果vrf冲突，并且已经配置了地址,那么需要先删除地址
        #如果不是通过脚本配置，则报错
        
        if 'ipv4' in config:
            if config['ipv4'] == None:
                self.dutlib.process(dut,'no ip address')
            else:
                mask = config.get('maskv4','255.255.255.0')
                ip   = config['ipv4']
                self.dutlib.process(dut,'ip addr del %s dev %s'% \
                    (_baselib.appIpEx(ip,mask),name))
        if 'ipv6' in config:
            if config['ipv6'] != None:
                mask = config.get('masklen',64)
                ipv6   = config['ipv6']
                self.dutlib.process(dut,'config interface ip remove %s %s/%s'% (name,ipv6,int(mask)))
            val.pop('ipv6',None)
            val.pop('masklen',None)
            self.dutlib.process(dut,'no ipv6 enable')
        if 'vrf' in config:
            self.dutlib.process(dut,'config interface vrf unbind %s %s'%(name))
            val.pop('vrf',None)
        return True
    
    def delBridge(self,dut,name,config=None):
        '''删除接口，或者初始化配置
        '''
        self.__initlib(dut)
        
        if name not in self.zxins[dut]['int']:
            self.zxins[dut]['int'][name] = dict()
        intdict = self.zxins[dut]['int'][name]
        if config == None:
            config  = copy.deepcopy(intdict)
        #删除子接口，虚接口
        if re.search(r"\.\d+",name):
            self.dutlib.process(dut,'no interface %s'%(name))
        elif re.search(r"tunnel\d+",name):
            self.dutlib.process(dut,'no interface %s'%(name))
        elif re.search(r"loopback\d+",name):
            self.dutlib.process(dut,'no interface %s'%(name))
        elif re.search(r"smartgroup\d+",name):
            self.dutlib.process(dut,'no interface %s'%(name))
        else:
            if 'ipv4' in config:
                self.dutlib.process(dut,'config interface ip remove %s %s'%\
                    (name,_baselib.appIpEx(intdict['ipv4'],intdict['maskv4'])))
                if 'ipv4' in intdict: del intdict['ipv4']
                if 'maskv4' in intdict: del intdict['maskv4']
            self.dutlib.process(dut,'config interface shutdown %s'%name)
        del self.zxins[dut]['int'][name]
        return True

    def bridgeBackup(self,dut):
        self.__initlib(dut)
        if dut not in self.zxinsbk:
            self.zxinsbk[dut] = []
        if dut not in self.zxins:
            self.zxinsbk[dut].append({})
            return True
        self.zxinsbk[dut].append(copy.deepcopy(self.zxins[dut]))
        return True

    def bridgeResume(self,dut):
        '''恢复bridge配置
        '''
        if dut not in self.zxinsbk:
            return False
        if dut not in self.zxins:
            return False
        va = copy.deepcopy(self.zxins[dut]['int'])
        bk = self.zxinsbk[dut][0].pop('int')

        if va == bk:
            return True

        logger.info("[bridge Resume]start")
        for i in va.keys():
            self.dutlib.rootConfigMode(dut)

            if i in bk and va[i] == bk[i]:
                del va[i]
                del bk[i]
                continue

            #删除新增的接口
            if i not in bk:
                self.delBridge(dut,i)
                continue

            #删除相同的参数
            for j in va[i].keys():
                if j in bk[i] and va[i][j] == bk[i][j]:
                    del bk[i][j]
                    del va[i][j]
            self.gotoBridge(dut,i)
            #删除额外配置的参数
            if len(va[i]) > 0:
                self.bridgeClear(dut,i,va[i])
            #设置被清掉的参数
            if len(bk[i]) > 0:
                self.setBridge(dut,i,bk[i])
            del va[i]
            del bk[i]

        if  len(bk) <= 0:
            return
        #增加被删除的实例
        for k,v in bk.items():
            self.gotoBridge(dut,k)
            self.setBridge(dut,k,v)
            self.dutlib.aboveMode(dut)
        logger.info("[Bridge Resume]end")
    
    def showBridge(self, dut, interface):
        '''
        获取接口出口的报文计数 
        输出格式：
        | ret = {        
        |        'inunicasts'    : 0,   #接口收到的mac为单播的报文数
        |        'eunicasts'     : 0,   #接口发出的mac为单播的报文数
        |        'inv4pkts'      : 0,   #接口收到的ipv4的报文数
        |        'ev4pkts'       : 0,   #接口发送的ipv4的报文数
        |        'inv6pkts'      : 0,   #接口收到的ipv6的报文数
        |        'ev6pkts'       : 0,   #接口发送的ipv6的报文数        
        |       }
        '''
        
        buf = self.dutlib.process(dut,"show interface %s" % interface)
        lines = buf.splitlines()
        ret=dict()
        for i in lines:
            res = re.search(r'IP MTU\s+(\d+)\s+bytes',i)
            if res:
                ret['ip-mtu']= res.group(1)
                continue
            res = re.search(r'^\s*MTU\s+(\d+)\s+bytes',i)
            if res:
                ret['mtu']= res.group(1)
                continue
            res = re.search(r'\s+(In_CRC_ERROR)\s+(\d+)\s+(In_Unicasts)\s+(\d+)',i)
            if res:
                ret['inunicasts'] = res.group(4)
                continue
            res = re.search(r'\s+(E_CRC_ERROR)\s+(\d+)\s+(E_Unicasts)\s+(\d+)',i)
            if res:
                ret['eunicasts'] = res.group(4)
                continue
            res = re.search(r'\s+(In_V4Pkts)\s+(\d+)\s+(In_V6Bytes)\s+(\d+)',i)
            if res:
                ret['inv4pkts'] = res.group(2)
                continue
            res = re.search(r'\s+(E_V4Pkts)\s+(\d+)\s+(E_V6Bytes)\s+(\d+)',i)
            if res:
                ret['ev4pkts'] = res.group(2)
                continue
            res = re.search(r'\s+(In_V6Pkts)\s+(\d+)\s+(In_UpsendCar_Drop)\s+(\d+)',i)
            if res:
                ret['inv6pkts'] = res.group(2)
                continue
            res = re.search(r'\s+(E_V6Pkts)\s+(\d+)',i)
            if res:
                ret['ev6pkts'] = res.group(2)
                continue
        return ret
    
    def interfaceShutdown(self,dut,intf):
        '''shutdown接口
        '''
        self.__initlib(dut)
        self.dutlib.process(dut,'ip link set %s down'%intf)
        
    def interfaceNoShutdown(self,dut,intf):
        '''no shutdown接口
        '''
        self.__initlib(dut)
        self.dutlib.process(dut,'ip link set %s up'%intf)

    def getDutByIpv4(self,ip):
        '''查询IP地址所在的设备名
        '''
        for dut in self.zxins:
            for intname in self.zxins[dut]['int']:
                if 'ipv4' in self.zxins[dut]['int'][intname]:
                    if self.zxins[dut]['int'][intname]['ipv4']==ip:
                        return dut
        return None

    def getInterfaceByIpv4(self,dut,ip):
        '''查询IP地址所在的接口名
        '''
        self.__initlib(dut)
        for intname in self.zxins[dut]['int']:
            if 'ipv4' in self.zxins[dut]['int'][intname]:
                if self.zxins[dut]['int'][intname]['ipv4']==ip:
                    return intname
        return None

    def getIpv4ByInterface(self,dut,intname):
        '''查询接口的IPV4地址
        '''
        self.__initlib(dut)
        if intname in self.zxins[dut]['int']:
            return self.zxins[dut]['int'][intname]['ipv4']
        return None    
     
    def getIpv4AndMaskByInterface(self,dut,intname):
        '''获取接口的地址以及掩码
        '''
        self.__initlib(dut)
        if intname in self.zxins[dut]['int']:
            return self.zxins[dut]['int'][intname]['ipv4'],self.zxins[dut]['int'][intname]['maskv4']
        buf = self.dutlib.process(dut,'ip -br addr show dev ' + intname)
        #enp0s3           UP             10.0.2.15/24 fe80::a00:27ff:febb:7fb7/64
        lines = buf.splitlines()
        for i in lines:
            ret = re.search( r"(\S+)\s*(\S*)\s*(\d+\.\d+\.\d+\.\d+)\/(\d+)",i)
            if ret:
                ipv4 = ret.group(3)
                logger.debug( "FIND ip : %s %s"%(intname,ipv4))
                if intname in self.zxins[dut]['int']:
                    self.zxins[dut]['int'][intname]['ipv4'] = ipv4
                return ret.group(1)
        return None,None
    
    def getInterfaceVlanID(self,dut,intname):
        '''查询接口的VLANID
        '''
        self.__initlib(dut)
        if intname in self.zxins[dut]['int']:
            if 'vlanid' in self.zxins[dut]['int'][intname]:
                return self.zxins[dut]['int'][intname]['vlanid']
        return None
    
    def getInterfaceVrf(self,dut,intname):
        '''查询接口的VRF
        '''
        self.__initlib(dut)
        if intname in self.zxins[dut]['int']:
            return self.zxins[dut]['int'][intname].get('vrf',None)
        return None
    
    def getInterfaceIpv4(self,dut,intname):
        '''查询接口的IPV4地址
        '''
        self.__initlib(dut)
        if intname in self.zxins[dut]['int']:
            return self.zxins[dut]['int'][intname].get('ipv4','public')
        return None
    
    def getInterfaceIpv4Mask(self,dut,intname):
        '''查询接口的IPV4掩码
        '''
        self.__initlib(dut)
        if intname in self.zxins[dut]['int']:
            return self.zxins[dut]['int'][intname].get('maskv4','public')
        return None

    def getInterfaceNet(self,dut,intname):
        '''查询接口的IPV4掩码
        '''
        self.__initlib(dut)
        ip,mask = self.getIpv4AndMaskByInterface(dut,intname)
        net= _baselib.IP(ip).make_net(mask)
        return net
    
    def getInterfaceIpv6(self,dut,intname):
        '''查询接口的IPV6地址
        '''
        self.__initlib(dut)
        if intname in self.zxins[dut]['int']:
            return self.zxins[dut]['int'][intname].get('ipv6','public')
        return None
    
    def getInterfaceIpv6Masklen(self,dut,intname):
        '''查询接口的IPV6掩码长度
        '''
        self.__initlib(dut)
        if intname in self.zxins[dut]['int']:
            return self.zxins[dut]['int'][intname].get('masklen','public')
        return None
    
    def getInterfaceMac(self,dut,intname):
        '''获取接口的mac地址
        '''
        intname = str(intname)
        self.__initlib(dut)
        if intname in self.zxins[dut]['int']:
            if 'mac' in self.zxins[dut]['int'][intname]:
                return self.zxins[dut]['int'][intname]['mac']
        buf = self.dutlib.process(dut,'ip link show dev ' + intname)
        lines = buf.splitlines()
        for i in lines:
            ret = re.search( r"link/ether\s*(\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})",i)
            if ret:
                mac = ret.group(1)
                logger.debug( "FIND MAC : %s %s"%(intname,mac))
            
                if intname in self.zxins[dut]['int']:
                    self.zxins[dut]['int'][intname]['mac'] = mac
                return ret.group(1)
        return None
    
    def addInterfaceConfig(self, dut, config):
        '''批量配置接口和VLAN
        '''
        self.__initlib(dut)
        for (k,v) in config.items():
            logger.debug('Config interface %s (%s)'%(k,str(v)))
            self.gotoBridge(dut,k)
            self.setBridge(dut,k,v)
            if 'dot1q' in v:
                #退出接口模式，设置dot1q值
                self.setDot1q(dut,k,v['dot1q'])
        
        return True

    def delInterfaceConfig(self,dut,config = None):
        '''批量删除接口配置
        '''
        intdict = self.zxins[dut]['int']
        if config == None:
            config = copy.deepcopy(intdict)
        for interface in config.keys():
            self.delInterface(dut,interface)
        return True
    
    def interfaceReloadConfig(self,dut,buf=False ):
        '''将接口的配置重新载到RF
        '''
        show = self.dutlib.showRun(dut,'if-intf')
        self.zxins[dut]['int'] = {}
        intdict = self.zxins[dut]['int']
        name = None
        for line in show:
            m = re.search(r"\s*interface\s+(\S+)",line)
            if m:
                name = m.group(1)
                intdict[name] = {}
                continue
            m = re.search(r"\s*ip address (\S+)\s+(\S+)",line)
            if m:
                intdict[name]['ipv4']   = m.group(1)
                intdict[name]['maskv4'] = m.group(2)
                continue
            m = re.search(r"\s*ipv6 address (\S+)\\(\S+)",line)
            if m:
                intdict[name]['ipv6']   = m.group(1)
                intdict[name]['masklen'] = int(m.group(2))
                continue
            m = re.search(r"\s*ipv6 enable",line)
            if m:
                logger.debug("[reload interface]ipv6 enable")
                continue
            m = re.search(r"\s*ip vrf forwarding (\S+)",line)
            if m:
                intdict[name]['vrf']   = m.group(1)
                continue
        #删除不关心的接口
        for int in intdict.keys():
            if int == 'mgmt_eth':
                del intdict[int]
            elif int.startswith('null') == 0:
                del intdict[int]
            elif int.startswith('spi') == 0:
                del intdict[int]
        logger.debug("Load interface configure ok!")
        
    def tunnelRunConfig(self, dut, config):
        self.__initlib(dut)
        for (k,v) in config.items():
            logger.debug('Config after interface %s (%s)'%(k,str(v)))
            self.gotoTunnel(dut,k)
            self.setTunnel(dut,k,v)
            self.dutlib.rootConfigMode(dut)
        return True
    
    def delNsConfig(self,dut,config=None):
        vrfdict = self.zxins[dut]['vrf']
        if config == None:
            config = copy.deepcopy(vrfdict)
        for vrf in config.keys():
            self.delVrf(dut,vrf)
        return True

    def addNsConfig(self, dut, config):
        self.__initlib(dut)
        for (k,v) in config.items():
            logger.debug('Config vrf %s (%s)'%(k,str(v)))
            self.gotoVrf(dut,k)
            self.setVrf(dut,k,v)
            self.dutlib.rootConfigMode(dut)
        return True
    
    def nsReloadConfig(self,dut,buf=False ):
        self.__initlib(dut)
        show = self.dutlib.showRun(dut,'vrf')
        if not len(show):
            return True
        logger.debug("vrfReloadConfig ERROR") 
                
    def linuxRunConfig(self, dut, config):
        '''运行linux配置字典
        
        关键字处在全局配置字典的最顶层:
        
        | 接口配置    | 'int' : { }   | 参考 Add Interface Config 关键字帮助 |
        | VRF实例配置 | 'ns' : { }   | 参考 Add ns Config 关键字帮助 |
        | 路由配置    | 'route' : { } | 参考 Add Route 关键字帮助 |
        | lacp配置    | 'lacp' : { }   | 参考 Lacp Run Config 关键字帮助 | 
        | lacp配置    | 'bridge' : { }   | 参考 bridge Run Config 关键字帮助 | 
        '''
        self.__initlib(dut)
        if not self.dutlib.configMode(dut):
            raise AssertionError("Can't enter config mode!")
        logger.debug("Config linux !!!!!")
        if 'ns' in config:
            self.addNsConfig(dut,config['ns'])
        if 'int' in config:
            self.addInterfaceConfig(dut,config['int'])
        if 'vlan' in config:
            self.vlanRunConfig(dut,config['vlan'])
        return True

    def linuxClearConfig(self,dut,config=None):
        '''删除linux已经配置的基本配置
        '''
        self.__initlib(dut)
        if config == None:
            config = copy.deepcopy(self.zxins[dut])
        if 'route' in config:
            for v in config['route']:
                self.delRoute(dut,v)
        if 'int' in config:
            self.delInterfaceConfig(dut,config['int'])
        if 'ns' in config:
            self.delNsConfig(dut,config['ns'])
        return True

    def linuxClearDut(self, dut, config = None):
        '''获取设备配置，然后再删除
        '''
        self.__initlib(dut)
        if not config:
            #不清除配置， 否则清空了其他人的配置
            return True
        #根据配置清

        return True

    def linuxReload(self, dut,buf=False):
        '''重载所有的配置
        '''
        self.nsReloadConfig(dut,buf)
        self.interfaceReloadConfig(dut,buf)

    def linuxBackup(self, dut):
        '''恢复当前配置
        '''
        if dut not in self.zxinsbk:
            self.zxinsbk[dut] = []
        if dut not in self.zxins:
            self.zxinsbk[dut].append({})
            return True
        self.zxinsbk[dut].append(copy.deepcopy(self.zxins[dut]))
        return True
    
    def linuxResume(self,dut):
        '''恢复当前配置 -- 未实现
        '''
        if dut not in self.zxinsbk:
            return False
        if dut not in self.zxins:
            return False
        va = copy.deepcopy(self.zxins[dut])
        bk = self.zxinsbk[dut].pop()
        
        if va == bk:
            return True
        
        logger.info("linux Resume]start")
        for i in va.keys():
            if i in bk and va[i] == bk[i]:
                del va[i]
                del bk[i]
                continue
            if i not in bk:
                raise AssertionError("Can not find %s"%i)
            
            #删除相同的参数
            for j in va[i].keys():
                if j in bk[i] and va[i][j] == bk[i][j]:
                    del bk[i][j]
                    del va[i][j]
        #清除多余的参数
        self.linuxClearConfig(dut,va)
        #配置被删除的参数
        self.linuxRunConfig(dut,bk)
        logger.info("[linux Resume]end")
