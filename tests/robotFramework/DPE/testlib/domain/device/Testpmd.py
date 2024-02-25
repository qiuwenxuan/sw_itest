#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
日期 :  2015-8-21
作者 ： APP RF小组
'''
import copy , re, random, time, os, subprocess, sys
from pprint import pprint
from os import linesep
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger

__path = os.path.realpath(os.path.join(__file__,'..','..','..','base')) 
if __path not in sys.path:sys.path.append(__path)

import AppBaseLib as _baselib

class Testpmd(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    zxins = dict()
    zxinsbk = dict()
    dutlib = None
    name = "Testpmd"

    def __init__(self):
        pass
    
    def __getObj(self, name):
        try:
            return BuiltIn().get_library_instance(name)
        except Exception:
            pass
        return None
        
    def __initlib(self,dut = None):
        if self.dutlib == None:
            self.dutlib   = BuiltIn().get_library_instance('AppDut')
            self.linuxlib   = BuiltIn().get_library_instance('Linux')
            self.ovslib   = BuiltIn().get_library_instance('Ovs')  #使用ovs的流表公共库
        if dut != None:
            if dut not in self.zxins:
                self.zxins[dut] = dict()
                self.zxins[dut]['info'] = None
                self.zxins[dut]['summary'] = None
                self.zxins[dut]['tunnel'] = dict()
                self.zxins[dut]['flow'] = dict()
                self.dutlib.pmdConnect(dut)
                self.getPortSummary(dut)
        return True

    def flowFraseRuleToDict(self,rule):
        '''转换流的字符串格式规则为字典格式规则

        | port_id is 1 / eth src is 03:00:00:00:00:00 dst is 02:00:00:00:00:00 / 
        |           ipv4 src is 11.11.11.1 dst is 11.11.11.2 proto is 0x11 /udp src is 0x400 dst is 0x500 
        |           / end actions port_id is 2 / end

        '''
        rule_dict = {'match':dict(),'action':dict()}
        match = rule_dict['match']
        action = rule_dict['action']
        action['type'] = 'fwd'
        rule = re.sub(r"\s+"," ",rule)
        fs = rule.split('/')
        will = None
        for i in fs:
            i = i.strip()
            if i == 'end' : break
            k,v = i.split(' ',1)
            if k == 'end':
                k,v = v.split(' ',1)
                if k == 'actions':
                    will = action
            elif k == 'port_id':
                v = k+' '+v
                will = match
            else :
                match[k] = dict()
                will = match[k]
            ls = re.split(r'\s+',v)
            while len(ls) >= 3 :
                a = ls.pop(0)
                b = ls.pop(0)
                c = ls.pop(0)
                if b != 'is': break
                will[a] = c
        if 'port_id' in match:
            match['port'] = match.pop('port_id')
        if 'port_id' in action:
            action['port'] = action.pop('port_id')
        return rule_dict

    def flowTransArgToDict(self,*args,**argds):
        '''输入转换为流字典格式规则

        | -port=1 | eth.src=1.1.1.1 | port=2

        |        config = {
        |           'match' : {},
        |           'action': {}
        |           }
        |
        '''
        ret = {
            'match':dict(),
            'action':dict()
            }
        key = None
        info = None
        #logger.info(str(args))
        for i in args:
            info = ret['action'] if i.startswith('-') else ret['match']
            if key == None and len(i) >= 0:
                if '=' in i:
                    tmp = re.search(r'(\S+)=(\S*)',i)
                    if tmp:
                        key = tmp.group(1).lower()
                        val = tmp.group(2)
                        key = i.lstrip('-').lower()
                        info[key] = val if len(val) > 0 else ''
                        key = None
                else:
                    key = i.lstrip('-').lower()
                    info[key] = ''
            else:
                if key != None:
                    ret[key] = i
                    key = None
        for k,v in argds.items():
            info = ret['action'] if k.startswith('-') else ret['match']
            k = k.lstrip('+-').lower()
            if '.' in info:
                k1,k2 = k.split('.',1)
                info.setdefault(k1,dict())
                info[k1][k2] = v
        
        logger.info('[testpmd]transform flow:'+str(ret))
        return ret

    def flowTransToRule(self,ruledict) :
        '''转换字典格式规则为字符串格式规则
        '''
        '''flow create 2 transfer ingress pattern eth src is 10:12:12:12:12:21 / end actions port_id id 3 / end
        '''
        ret = ""
        if ruledict == None: return ret
        match = ruledict['match']
        action = ruledict['action']
        if 'port' in match:
            ret += 'port_id is %s /'%(str(match['port']))
        for k in ['eth', 'ipv4','ipv6','udp', 'tcp']:
            if k not in match: continue
            ret += "%s "%k
            for j,v in match[k].items():
                if '/' in v:
                    _a,_b = v.split('/')
                    ret += "%s spec %s %s mask %s "%(j,_a,j,_b)
                else:    
                    ret += "%s is %s "%(j,v)
            ret += "/ "
        ret += "end actions "
        if 'port' in action:
            ret += 'port_id id %s '%(str(action['port']))
        #if 'type' in action and 'fwd' != action['type']:
        for k,v in action.items():
            if k in ['type','port']: continue
            ret += "%s is %s "%(k,v)
        ret += '/ end'
        return ret

    def flowTransOvsToDpdkRule(self,ruledict,flowtype='ipv4'):
        ''' Ovs流表规则转换为Testpmd流规则
        '''
        __map = {  # dl_src dl-> eth , nw_src -> ipv4 src
                "dl" : "eth",
                "nw" : "ipv4"
            }
        __mapipv6 = {  # dl_src dl-> eth , nw_src -> ipv4 src
                "dl" : "eth",
                "nw" : "ipv6"
            }
        __default = {
            'ipv4' :{'src' : '1.1.1.1/0.0.0.0'},
            'ipv6' :{'src' : '11::11/0'}
            }
        ret = {"match":dict(),"action":dict()}
        if ruledict == None: return ret
        match = ruledict['match']
        action = ruledict['action']
        ret_match = ret['match']
        ret_action = ret['action']

        if 'ip_dscp' in match or 'nw_ecn' in match:
            match.setdefault('nw_tos', '0')
            if 'ip_dscp' in match:
                nw_tos = int(match['ip_dscp']) << 2
                match.pop('ip_dscp')
            if 'nw_ecn' in match:
                nw_tos = nw_tos+int(match['nw_ecn'])
                match.pop('nw_ecn')
            match['nw_tos'] = str(nw_tos)

        map =  __map 
        if flowtype == 'ipv6':  
            map =  __mapipv6

        for k,v in match.items():
            __a,__b = k.split("_")
            if __a in map:
                ret_match.setdefault(map[__a],dict())
                ret_match[map[__a]][__b] = v
            else:
                ret_match.setdefault(__a,dict())
                ret_match[__a][__b] = v
        for k,v in action.items():
            if 'output' == k:
                ret_action['port'] = v
            elif 'type' == k:
                ret_action['type'] = v
        if flowtype == 'ipv4' :
            if 'ipv4' not in ret_match:
                ret_match['ipv4'] = copy.deepcopy(__default['ipv4'])
        if flowtype == 'ipv6' :
            if 'ipv6' not in ret_match:
                ret_match['ipv6'] = copy.deepcopy(__default['ipv6'])
        return ret

    def getPortId(self,dut,port):
        '''获取端口索引
        '''
        self.__initlib(dut)
        info = self.getPortSummary(dut)
        for k,v in info.items():
            if self.ovslib.isPci(port):
                if v['name'][-7:] == port[-7:]:
                    return k
            elif(v['name'] == port):
                return k
        return int(port)

    def getPortSummary(self,dut,port=None):
        ''' 获取端口摘要信息
        '''
        '''
        Number of available ports: 4
        Port MAC Address       Name         Driver         Status   Link
        0    52:54:00:D6:23:1D 0000:00:15.0 net_virtio     up       Unknown
        1    52:54:00:F5:DD:6C 0000:00:16.0 net_virtio     up       Unknown
        2    52:54:00:E4:1C:3D 0000:00:17.0 net_virtio     up       Unknown
        3    52:54:00:78:1E:26 0000:00:18.0 net_virtio     up       Unknown
        '''
        self.__initlib(dut)
        summary = self.zxins[dut]['summary']
        if summary != None:
            if port == None:
                return summary
            else :
                return summary[int(port)]
        buf = self.dutlib.pmdProcess(dut,'show port summary all')
        lines = buf.splitlines()
        nicdict = dict()
        port = None
        for l in lines:
            ret = re.search(r"\s*(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)",l)
            if ret:
                port = int(ret.group(1))
                nicdict[port] = dict()
                nicdict[port]['id'] = ret.group(1)
                nicdict[port]['mac'] = ret.group(2)
                nicdict[port]['name'] = ret.group(3)
                nicdict[port]['driver'] = ret.group(4)
                nicdict[port]['state'] = ret.group(5)
                nicdict[port]['link'] = ret.group(6)
        if len(nicdict) > 0 :
            self.zxins[dut]['summary'] = copy.deepcopy(nicdict)
        else :
            for l in lines :
                logger.info("[getPortSummary]"+l)
            raise AssertionError("====Can't find any port!")
        return nicdict

    def getPortInfo(self,dut,port=None):
        ''' 获取端口信息(执行偶尔会出现错误，可能是打印信息太多)
        '''
        '''
        ********************* Infos for port 1  *********************
        MAC address: 08:00:27:7C:23:C0
        Device name: 0000:00:0a.0
        Driver name: net_e1000_em
        Firmware-version: not available
        Connect to socket: 0
        memory allocation on the socket: 0
        Link status: down
        Link speed: None
        Link duplex: half-duplex
        Autoneg status: Off
        MTU: 1500
        Promiscuous mode: enabled
        Allmulticast mode: disabled
        Maximum number of MAC addresses: 15
        Maximum number of MAC addresses of hash filtering: 0
        VLAN offload:
        strip off, filter off, extend off, qinq strip off
        No RSS offload flow type is supported.
        Minimum size of RX buffer: 256
        Maximum configurable length of RX packet: 16128
        Maximum configurable size of LRO aggregated packet: 0
        Current number of RX queues: 1
        Max possible RX queues: 1
        Max possible number of RXDs per queue: 4096
        Min possible number of RXDs per queue: 32
        RXDs number alignment: 8
        Current number of TX queues: 1
        Max possible TX queues: 1
        Max possible number of TXDs per queue: 4096
        Min possible number of TXDs per queue: 32
        TXDs number alignment: 8
        Max segment number per packet: 255
        Max segment number per MTU/TSO: 255
        '''
        self.__initlib(dut)

        info = self.zxins[dut]['info']
        if info != None:
            if port == None:
                return info
            else :
                return info[int(port)]
        trans = {"MAC address":"mac",
                 "Device name":"name",
                 "Driver name":"driver"
                }
        buf = self.dutlib.pmdProcess(dut,'show port info all')
        lines = buf.splitlines()
        nicdict = dict()
        port = None
        lastl = None
        for l in lines:
            logger.info("[getPortInfo]"+l)
            ret = re.search(r"\*{10}\*+\s+Infos for port\s*(\d+)\s*\*{10}\*+",l)
            if ret:
                port = int(ret.group(1))
                nicdict[port] = dict()
                nicdict[port]['id'] = port
                continue
            if port == None:
                continue
            if ':' not in l:
                l = lastl + l
            if ':' not in l :
                continue
            k,v = l.split(':',1)
            k = trans.get(k,k)
            nicdict[port][k] = v.strip()
            lastl = l
        return nicdict

    def getPortStats(self,dut,port=None):
        ''' 获取端口信息
        '''
        '''
        ######################## NIC statistics for port 0  ########################
        RX-packets: 128        RX-missed: 0          RX-bytes:  34944
        RX-errors: 0
        RX-nombuf:  0         
        TX-packets: 0          TX-errors: 0          TX-bytes:  0

        Throughput (since last show)
        Rx-pps:            0          Rx-bps:           16
        Tx-pps:            0          Tx-bps:            0
        ############################################################################
        '''
        self.__initlib(dut)
        add = 'all'
        if port != None : port = self.getPortId(dut,port)
        buf = self.dutlib.pmdProcess(dut,'show port stats %s'%add)
        lines = buf.splitlines()
        niclist = {}
        for l in lines:
            ret = re.search(r"\#{10}\#+.*port\s*(\d+)\s*\#+",l)
            if ret:
                port = int(ret.group(1))
                niclist[port] = dict()
                continue
            if port == None:
                continue
            for r in re.finditer(r"(\S+)\s*:\s*(\S+)",l):
                niclist[port][r.group(1)] = r.group(2)
        if add != 'all':
            return niclist[port]
        return niclist
		
    def flowQuery(self,dut,port,ruleid,info):
        '''查询流表信息
        '''
        '''
        testpmd> flow query 2 0 count
        COUNT:
        hits_set: 1
        bytes_set: 1
        hits: 8361
        bytes: 1070208
        testpmd>
        '''
        buf = self.dutlib.pmdProcess(dut,'flow query %d %d %s'%(int(port),int(ruleid),info))
        lines = buf.splitlines()
        ret = dict()
        for l in lines:
            tmp = re.search(r"\s*(\S+)\s*:\s*(\d+)",l)
            if tmp:
                ret[tmp.group(1)] = int(tmp.group(2))
        return ret

    def flowList(self,dut,port):
        '''查询流表信息
        '''
        '''
        testpmd> flow list 2
        ID      Group   Prio    Attr    Rule
        0       0       0       i-t     ETH IPV6 => PORT_ID
        '''
        buf = self.dutlib.pmdProcess(dut,'flow query %d %d %s'%(int(port),int(ruleid),info))
        lines = buf.splitlines()
        ret = dict()
        for l in lines:
            tmp = re.search(r"\s*(\d+)\s+(\d+)\s+(\d+)\s+(\S+)\s+(\S.+)",l)
            if tmp:
                ruleid = tmp.group(1)
                ret[ruleid]['id'] = int(tmp.group(1))
                ret[ruleid]['group'] = int(tmp.group(2))
                ret[ruleid]['prio'] = int(tmp.group(3))
                ret[ruleid]['attr'] = tmp.group(4)
                ret[ruleid]['rule'] = tmp.group(5)
        return ret

    def setFlow(self,dut,port,rule):
        '''流表配置
        '''
        '''
        Flow rule #1 created
        '''
        self.__initlib(dut)
        idict = self.zxins[dut]['flow']  #主要用于校验
        idict.setdefault(port,dict())
        __rule = self.flowTransToRule(rule)
        buf = self.dutlib.pmdProcess(dut,'flow create %s transfer ingress pattern %s'% \
                    (port,__rule))
        lines = buf.splitlines()
        ruleid = None
        for l in lines:
            tmp = re.search(r"Flow rule #(\d+) created",l)
            if tmp:
                ruleid = int(tmp.group(1))
        if ruleid == None:
            raise AssertionError("Create rule error!")
        idict[port][ruleid] = __rule
        return ruleid
    
    def clearFlow(self,dut,port,rule):
        '''清除流表
        '''
        self.__initlib(dut)
        idict = self.zxins[dut]['flow']
        idict.setdefault(port,dict())
        __rule = self.flowTransToRule(rule)
        ruleid = None
        for k,v in idict[port].items():
            if v == __rule:
                ruleid = k
                break
        if ruleid == None:
            return
        self.flowDestroy(dut,port,ruleid)

    def flowDestroy(self,dut,port,ruleid):
        '''删除流表
        '''
        self.__initlib(dut)
        idict = self.zxins[dut]['flow']
        idict.setdefault(port,dict())
        self.dutlib.pmdProcess(dut,'flow destroy %s rule %s'%(port,ruleid))
        if ruleid in idict : idict[port].pop(ruleid)

    def flowFlush(self,dut,port=None):
        '''删除所有流
        '''
        self.__initlib(dut)
        idict = self.zxins[dut]['flow']
        if port == None:
            for k in idict.keys():
                self.flowFlush(self,dut,k)
            return
        idict.setdefault(port,dict())
        self.dutlib.pmdProcess(dut,'flow flush %s'%(port))
        idict[port].clear()

    def flowClearConfig(self,dut,port,config):
        self.__initlib(dut)
        for k in config:
            self.clearFlow(dut,port,k)

    def checkFlowByConfig(self,dut,tx,rx,port,flowconfig):
        self.__initlib(dut)
        if 'ruleid' not in flowconfig :
            AssertionError("Can't find ruleid!")
        ruleid = flowconfig['ruleid']
        info = self.flowQuery(dut,port,ruleid,"count")
        n_packet = int(info['hits'])
        if 'n_packet_last' in flowconfig:
            n_packet = n_packet - flowconfig['n_packet_last']
        flowconfig['n_packet_last'] = n_packet
        logger.info("[ovs]Check flow n_packet:%d rx:%d tx:%d"%(n_packet,tx,rx))
        action = flowconfig['action'].get('type','fwd')
        if action == 'drop':
            if int(tx) == int(n_packet) and int(rx) == 0:
                logger.debug("[ovs] flow table success")
                return True
            else:
                raise AssertionError("[ovs] flow table failed")
        else:
            #有杂包，会导致n_packet较大
            BuiltIn().should_be_true((int(rx) + 2  > n_packet/2) and (rx > 2), \
                    "[ovs]flow table failed %d != %d"%(int(rx),int(n_packet)))

    def pmdCheckConfig(self,dut):
        '''检查配置 未完成
        '''
        self.__initlib(dut)

    def pmdRunConfig(self, dut, config):
        '''运行pmd配置字典
        
        关键字处在全局配置字典的最顶层:
        
        | 接口配置    | 'port' : { }   | 参考 Add Port Config 关键字帮助 |
        | 路由配置    | 'flow' : { } | 参考 Add Flow 关键字帮助 |
        '''
        self.__initlib(dut)

        #if not self.dutlib.configMode(dut):
        #    raise AssertionError("Can't enter config mode!")
        logger.debug("Config pmd !!!!!")
        if 'tunnel' in config:
            for k,v in config['bridge'].items():
                self.gotoBridge(dut,k,v)
        if 'flow' in config:
            for k in config['flow'].keys(): #port
                for l in config['flow'][k].keys():
                    self.setFlow(dut,k,config['flow'][k][l])
        return True

    def pmdClearConfig(self,dut,config=None):
        '''删除pmd已经配置的基本配置
        '''
        self.__initlib(dut)
        if config == None:
            config = copy.deepcopy(self.zxins[dut])
        if 'port' in config:
            for k,v in config['port'].items():
                self.delPort(dut,None,k)
        if 'bridge' in config:
            for k,v in config['bridge'].items():
                self.delBridge(dut,k)
        return True

    def pmdClearDut(self, dut, config = None):
        '''获取设备配置，然后再删除
        '''
        self.__initlib(dut)
        if not config:
            #不清除配置， 否则清空了其他人的配置
            return True
        #根据配置清

        return True

    def pmdReload(self, dut,buf=False):
        '''重载所有的配置
        '''
        pass
    
    def pmdBackup(self, dut):
        '''恢复当前配置
        '''
        if dut not in self.zxinsbk:
            self.zxinsbk[dut] = []
        if dut not in self.zxins:
            self.zxinsbk[dut].append({})
            return True
        self.zxinsbk[dut].append(copy.deepcopy(self.zxins[dut]))
        return True
    
    def pmdResume(self,dut):
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
        
        logger.info("pmd Resume]start")
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
        self.pmdClearConfig(dut,va)
        #配置被删除的参数
        self.pmdRunConfig(dut,bk)
        logger.info("[pmd Resume]end")

    def getRealPort(self,dut,port):
        return self.getPortId(dut,port)

if __name__ == '__main__':
    pmdlib = Testpmd()
    rule1 = '''port_id is 1 / eth src is 03:00:00:00:00:00 dst is 02:00:00:00:00:00 / 
                  ipv4 src is 11.11.11.1 dst is 11.11.11.2 proto is 0x11 /udp src is 0x400 dst is 0x500 
                  / end actions port_id is 2 / end
                  '''
    info = pmdlib.flowFraseRuleToDict(rule1)
    pprint(info)
    dict = pmdlib.flowTransToRule(info)
    pprint(dict)