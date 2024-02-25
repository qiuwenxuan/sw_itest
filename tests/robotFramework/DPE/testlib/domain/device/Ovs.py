#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
日期 :  2015-8-21
作者 ： APP RF小组
'''
import copy , re, random, time, os, subprocess, sys
from os import linesep
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from scapy.layers.inet6 import IPv6

__path = os.path.realpath(os.path.join(__file__,'..','..','..','base')) 
if __path not in sys.path:sys.path.append(__path)

import AppBaseLib as _baselib
from pprint import pprint
import json
from scapy.all import *

class Ovs(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    zxins = dict()
    zxinsbk = dict()
    dutlib = None
    name = "Ovs"
    drivers=['vfio-pci','uio_pci_generic','igb_uio']
    dbtables = ["Controller","Bridge","Queue","Open_vSwitch","NetFlow","IPFIX",
        "CT_Zone","QoS","Datapath","SSL","Port","sFlow","Flow_Sample_Collector_Set",
        "CT_Timeout_Policy","Mirror","Flow_Table","AutoAttach","Interface","Manager"]

    def __init__(self):
        self.ovsdb = dict()
        self.ovstable = dict()
        self.ovsvxlantable = dict()
        self.ovsinfo = dict()
    
    def __getObj(self, name):
        try:
            return BuiltIn().get_library_instance(name)
        except Exception:
            logger.warn("Can't find library %s"%name)
        return None
        
    def __initlib(self,dut = None):
        if self.dutlib == None:
            self.dutlib   = BuiltIn().get_library_instance('AppDut')
            self.linuxlib   = self.__getObj('Linux')
        if dut != None:
            if dut not in self.zxins:
                self.zxins[dut] = dict()
                self.zxins[dut]['bridge'] = dict()
                self.zxins[dut]['port'] = dict()
                self.zxins[dut]['flow'] = dict()
                self.__initOvs(dut)
                
        return True

    def __initOvs(self,dut):
        '''每个终端只初始化一次
        '''
        self.ovsdb[dut] = {'Force':True}
        self.ovstable[dut] = list()
        self.ovsinfo[dut] = dict()
        try:
            self.ovsinfo[dut]['ovs'] = True
            self.ovsinfo[dut]['ovs-vsctl'] = self.dutlib.process(dut,"which ovs-vsctl")
            self.dutlib.process(dut,"ovs-vsctl show")
        except Exception:
            self.ovsinfo[dut]['ovs'] = False
            return
        self.ovsdbUpdate(dut) #读取db的配置信息
        info = self.getOvsInfo(dut)
        self.ovsinfo[dut].update(info)

    def __splitBracket(self,line):
        ret = []
        ilist = line.split(',')
        l,r = 0,0
        left = ""
        for i in ilist:
            if i == '':continue
            l += i.count('(')
            r += i.count(')')
            left = i if left == '' else left+','+i
            if l != r:
                continue
            else :
                ret.append(left)
                left = ''
        return ret

    def isFlowChangePacket(self,flow):
        action = flow.get('action',dict())
        mod_action = ['dec_ttl','set_field']
        for i in action.keys():
            if 'mod' in i or i in mod_action:
                return True
        return False
    
    def getPktTTL(self,dut,flow):
        ttl = 128
        if 'match' in flow:
            match = flow['match']
        if 'action' in flow:
            action = flow['action']
        for k in match:           
            if k == 'nw_ttl':
                ttl = int(match[k])

        for k in action: 
            if k == 'mod_nw_ttl':
                ttl = int(action[k])
            if k == 'dec_ttl':
                ttl = ttl -1
        return ttl           

    def flowFraseOfruleToRule(self,ofrule):

        '''翻译offload字典为统一格式,剔除不需要比较项

        rule_dict = {'match':dict(),'action':dict()}
        match = rule_dict['match']
        action = rule_dict['action']

        for k,v in ofrule['match'].items():
            if 'ipv4' == k:
                for k1,v1 in v:
                    match['ip_'+k1] = v1
            
        for k,v in ofrule['action'].items():
            if 'xx' == k:
                for k1,v1 in v:
                    match
        '''     
        __flowdict = copy.deepcopy(ofrule)

        match  = __flowdict['match']
        action = __flowdict['action']
        __trans = {
            'EthSrc' : 'eth_src',
            'EthDst' : 'eth_dst',
            'dl_src' : 'eth_src',
            'dl_dst' : 'eth_dst',
            'nw_src' : 'ip_src',
            'nw_dst' : 'ip_dst',
            'tcp_src': 'tp_src',
            'tcp_dst': 'tp_dst',
            'udp_src': 'tp_src',
            'udp_dst': 'tp_dst',
            'sctp_src': 'tp_src',
            'sctp_dst': 'tp_dst',
        }
        for k,v in __trans.items():
            if k in match:
                match[v] = match[k]
                match.pop(k)
        if 'nw_proto' not in match:
            if 'eth_type' in match:
                if match['eth_type'] == '0x0800':
                    match['eth_type'] = 'ip'
                elif match['eth_type'] == '0x86dd':
                    match['eth_type'] = 'ipv6'
                elif match['eth_type'] == '0x8847':
                    match['eth_type'] = 'mpls'
                elif match['eth_type'] == '0x0806':
                    match['eth_type'] = 'arp'
                match['dl_type'] = match['eth_type']
                match.pop('eth_type',None)
        else:
            match.pop('eth_type',None)

        if 'recirc_id' in match:
            match.pop('recirc_id',None)
        if 'packet_type' in match:
            match.pop('packet_type',None)
        if 'type' in match:
            match.pop('type',None)

        if 'ipv4' in match:
            ipv4_dict = match['ipv4']
            if 'src' in ipv4_dict:
                match['ip_src'] = ipv4_dict['src']
            if 'dst' in ipv4_dict:    
                match['ip_dst'] = ipv4_dict['dst']
            if 'proto' in ipv4_dict:
                match['nw_proto'] = ipv4_dict['proto']
            if 'tos' in ipv4_dict:
                match['tos'] = ipv4_dict['tos']
            if 'frag' in ipv4_dict:
                match['frag'] = ipv4_dict['frag']
            if 'ttl' in ipv4_dict:
                match['ttl'] = ipv4_dict['ttl']
            match.pop('ipv4',None)
        
        if 'ipv6' in match:
            ipv6_dict = match['ipv6']
            if 'src' in ipv6_dict:
                match['ipv6_src'] = ipv6_dict['src']
            if 'dst' in ipv6_dict:    
                match['ipv6_dst'] = ipv6_dict['dst']
            if 'proto' in ipv6_dict:
                match['nw_proto'] = ipv6_dict['proto']  
            if 'tclass' in ipv6_dict:
                match['tclass'] = ipv6_dict['tclass']
            if 'frag' in ipv6_dict:
                match['frag'] = ipv6_dict['frag']   
            if 'hlimit' in ipv6_dict:
                match['ttl'] = ipv6_dict['hlimit']                         
            match.pop('ipv6',None)

        if 'udp' in match:
            udp_dict = match['udp']
            if 'src' in udp_dict:
                match['tp_src'] = udp_dict['src']
            if 'dst' in udp_dict:
                match['tp_dst'] = udp_dict['dst']
            match.pop('udp',None)

        if 'tcp' in match:
            tcp_dict = match['tcp']
            if 'src' in tcp_dict:
                match['tp_src'] = tcp_dict['src']
            if 'dst' in tcp_dict:
                match['tp_dst'] = tcp_dict['dst']
            match.pop('tcp',None)
 
        if 'sctp' in match:
            tcp_dict = match['sctp']
            if 'src' in tcp_dict:
                match['tp_src'] = tcp_dict['src']
            if 'dst' in tcp_dict:
                match['tp_dst'] = tcp_dict['dst']
            match.pop('tcp',None) 
            
        if 'tp_src' in match:             
            tmp = re.search(r"(.+)\/(.+)", match['tp_src'])
            if tmp:
                portPrefix = tmp.group(1)
                portNet = tmp.group(2)
                match['tp_src'] = str(hex(int(portPrefix))) + '/' + str(hex(int(portNet,16)))

        if 'tp_dst' in match:             
            tmp = re.search(r"(.+)\/(.+)", match['tp_dst'])
            if tmp:
                portPrefix = tmp.group(1)
                portNet = tmp.group(2)
                match['tp_dst'] = str(hex(int(portPrefix))) + '/' + str(hex(int(portNet,16)))

        if 'eth' in match:
            eth_dict = match['eth']
            if 'src' in eth_dict:
                match['eth_src'] = eth_dict['src']
            if 'dst' in eth_dict:
                match['eth_dst'] = eth_dict['dst']
            if 'type' in eth_dict:
                match['eth_type'] = eth_dict['type']
            match.pop('eth',None)

        if 'vlan' in match:
            vlan_dict = match['vlan']
            if 'vid' in vlan_dict:
                match['vlan_id'] = vlan_dict['vid']
            if 'pcp' in vlan_dict:
                match['vlan_pcp'] = vlan_dict['pcp']  
            match.pop('vlan',None)              

        if 'eth_src' in match: match['eth_src'] = match['eth_src'].lower()
        if 'eth_dst' in match: match['eth_dst'] = match['eth_dst'].lower()
        if 'eth_src' in match:
            tmp = re.search(r'(\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})\/(\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})', match['eth_src'])
            if tmp:
                match['eth_src'] = _baselib.getMatchMac(match['eth_src'])
                match['eth_src'] = match['eth_src'].lower()
        if 'eth_dst' in match:
            tmp = re.search(r'(\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})\/(\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})', match['eth_dst'])
            if tmp:
                match['eth_dst'] = _baselib.getMatchMac(match['eth_dst'])
                match['eth_dst'] = match['eth_dst'].lower()
                
        if 'ip_src' in match:
            tmp = re.search(r"(.+)\/(.+)", match['ip_src'])
            if tmp:
                match['ip_src'] = _baselib.getMatchIpAddr(match['ip_src'])
        if 'ip_dst' in match:
            tmp = re.search(r"(.+)\/(.+)", match['ip_dst'])
            if tmp:
                match['ip_dst'] = _baselib.getMatchIpAddr(match['ip_dst'])                
 
        if 'ipv6_src' in match:
            tmp = re.search(r"(.+)\/(.+)", match['ipv6_src'])
            '''
            已经以计算后得值显示，直接取前半段比较
            11::1000:0:0:1/ffff:ffff:ffff:ffff::
            '''
            if tmp:
                match['ipv6_src'] = tmp.group(1)
        if 'ipv6_dst' in match:
            tmp = re.search(r"(.+)\/(.+)", match['ipv6_dst'])
            if tmp:
                match['ipv6_dst'] = tmp.group(1)
                
        if 'icmp' in match:
            icmp_dict = match['icmp']
            if 'type' in icmp_dict:
                match['icmp_type'] = icmp_dict['type']
            if 'code' in icmp_dict:
                match['icmp_code'] = icmp_dict['code']  
            match.pop('icmp',None)  
             
        if  'tunnel' in match:
            match.pop('tunnel',None)
        
        if  'encap' in match:
            match.pop('encap',None)

        if 'type' in action:
            action['output'] = action['type']
            action.pop('type',None)

        if 'push_vlan' in action:
            push_vlan_action = action['push_vlan']
            if 'vid' in push_vlan_action:
                action['mod_vlan_vid'] = push_vlan_action['vid']
            if 'pcp' in push_vlan_action:
                action['mod_vlan_pcp'] = push_vlan_action['pcp'] 
            action.pop('push_vlan',None)

        if 'set_eth' in action:
            eth_set_action = action['set_eth']
            if 'src' in eth_set_action:
                action['mod_dl_src'] = eth_set_action['src']
            if 'dst' in eth_set_action:
                action['mod_dl_dst'] = eth_set_action['dst']
            action.pop('set_eth',None)

        if 'set_ipv4' in action:
            ipv4_set_action = action['set_ipv4']
            if 'src' in ipv4_set_action:
                action['mod_nw_src'] = ipv4_set_action['src']
            if 'dst' in ipv4_set_action:
                action['mod_nw_dst'] = ipv4_set_action['dst']
            if 'ttl' in ipv4_set_action:
                action['set_ttl'] = ipv4_set_action['ttl']    
            if 'tos' in ipv4_set_action:
                action['mod_nw_tos'] = ipv4_set_action['tos']                  
            action.pop('set_ipv4',None)

        if 'set_ipv6' in action:
            ipv6_set_action = action['set_ipv6']
            if 'src' in ipv6_set_action:
                action['mod_nw_src'] = ipv6_set_action['src']
            if 'dst' in ipv6_set_action:
                action['mod_nw_dst'] = ipv6_set_action['dst']
            if 'hlimit' in ipv6_set_action:
                action['set_ttl'] = ipv6_set_action['hlimit']    
            if 'tclass' in ipv6_set_action:
                action['mod_nw_tos'] = ipv6_set_action['tclass'] 
            action.pop('set_ipv6',None)

        if 'set_tp' in action:
            tp_set_action = action['set_tp']
            if 'src' in tp_set_action:
                action['mod_tp_src'] = tp_set_action['src']
            if 'dst' in tp_set_action:
                action['mod_tp_dst'] = tp_set_action['dst']
            action.pop('set_tp',None)
                            
        return __flowdict


    def flowFraseRuleToDict(self,rule):
        '''转换流的字符串格式规则为字典格式规则

        | cookie=0x0, duration=2.170s, table=0, n_packets=0, n_bytes=0, in_port=2 actions=output:dpdk0
        | cookie=0x0, duration=9.652s, table=0, n_packets=0, n_bytes=0, priority=0 actions=NORMAL
        | cookie=0,priority=40001,ip,in_port=2,nw_src=1.1.1.13,nw_dst=1.1.1.12 actions=output:4
        | cookie=0x0, duration=3.059s, table=0, n_packets=95, n_bytes=11820, in_port=dpdk0 actions=mod_dl_src:00:01:00:00:00:04,output:vxlan0
         
        '''
        rule_dict = {'match':dict(),'action':dict()}
        match = rule_dict['match']
        action = rule_dict['action']
        action['type'] = 'fwd'
        _rule = re.sub(r"\s","",rule)
        _re = re.search(r"(.+)actions=(.+)",_rule)
        if not _re :
            raise AssertionError("Flow : rule error ")
        match_info = _re.group(1).strip()
        action_info = _re.group(2).strip()
        for i in match_info.split(',') :
            _re = re.search(r"(.+)=(.+)",i)
            if _re :
                match[_re.group(1)] = _re.group(2).strip("\"")
            elif "ip" in i:
                match['dl_type']=i
            elif "mpls" in i:
                match['dl_type']=i
            elif "arp" in i:
                match['dl_type']=i
            elif "tcp" in i:
                match['nw_proto']='6'
            elif "udp" in i:
                match['nw_proto']='17'
            elif "sctp" in i:
                match['nw_proto']='132'
            elif "icmp" in i:
                match['nw_proto']='1'
            elif "icmpv6" in i:
                match['nw_proto']='58'
          
        for i in action_info.split(","):
            if not len(i) : continue
            _re = re.search(r"([^:]+):(.+)",i)
            if _re :
                action[_re.group(1)] = _re.group(2).strip("\"")
            else:
                action['type'] = i.lower()
        if 'n_packets' in match:
            rule_dict['stats'] = dict()
            for k in ['duration','n_packets','n_bytes']:
                rule_dict['stats'][k] = match.pop(k,None)
        return rule_dict

    def flowTransArgToDict(self,*args,**argds):
        '''输入转换为流字典格式规则

        | -tp-src=1.1.1.1 | +mod_tp_src=1.1.1.1 |

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
            info[k.lstrip('+-').lower()] = v
        
        logger.info('[ovs]transform flow:'+str(ret))
        return ret

    def flowTransToRule(self,ruledict) :
        '''转换字典格式规则为字符串格式规则
        '''
        ret = ""
        if ruledict == None: return ret

        for k,v in ruledict['match'].items():
            ret += "%s=%s,"%(k,v)
        ret += "action="
        if 'type' in ruledict['action'] and ruledict['action']['type'] != '' and ruledict['action']['type'] != 'fwd':
            ret += ruledict['action']['type']
            return ret
        else :
            if isinstance(ruledict['action'],dict):
                for k,v in ruledict['action'].items():
                    if k != 'type':
                        ret += "%s:%s,"%(k,v)
                ret = ret.rstrip(',')
            else:
                ret += ruledict['action']
        return ret

    def flowTransForCommon(self,flowdict):
        '''字典格式流参数归一化
        '''
        __flowdict = copy.deepcopy(flowdict)
        match  = __flowdict['match']
        __trans = {
            'dl_src' : 'eth_src',
            'dl_dst' : 'eth_dst',
            'nw_src' : 'ip_src',
            'nw_dst' : 'ip_dst',
        }
        for k,v in __trans.items():
            if k in match:
                match[v] = match[k]
                match.pop(k)
        return __flowdict

    def __flowTransForPacket(self,flowconfig):
        '''翻译流为统一格式,删除冲突项
        '''
        __flowdict = copy.deepcopy(flowconfig)
        match  = __flowdict['match']
        __trans = {
            'EthSrc' : 'eth_src',
            'EthDst' : 'eth_dst',
            'dl_src' : 'eth_src',
            'dl_dst' : 'eth_dst',
            'dl_vlan' : 'vlan_id',
            'dl_vlan_pcp' : 'vlan_pcp',
            'nw_src' : 'ip_src',
            'nw_dst' : 'ip_dst',
            'tcp_src': 'tp_src',
            'tcp_dst': 'tp_dst',
            'udp_src': 'tp_src',
            'udp_dst': 'tp_dst',
            'sctp_src': 'tp_src',
            'sctp_dst': 'tp_dst',
        }
        for k,v in __trans.items():
            if k in match:
                match[v] = match[k]
                match.pop(k)
        #if 'nw_proto' not in match:
        if 'dl_type' in match:
            if match['dl_type'] == '0x0800':
                match['dl_type'] = 'ip'
            elif match['dl_type'] == '0x86dd':
                match['dl_type'] = 'ipv6'
            elif match['dl_type'] == '0x8847':
                match['dl_type'] = 'mpls'
            elif match['dl_type'] == '0x0806':
                match['dl_type'] = 'arp'
        #else:
        #    match.pop('dl_type',None)
        
        if 'vlan_tci' in match:
            n1,n2 = match['vlan_tci'].split('/')
            #if int(n2,16) & 0xfff == 0xfff:
            match['vlan_id'] = str(int(n1,16) & int(n2,16)) + '/' + n2
            match.pop('vlan_tci')
        
        if 'eth_src' in match: match['eth_src'] = match['eth_src'].lower()
        if 'eth_dst' in match: match['eth_dst'] = match['eth_dst'].lower()
        if 'eth_src' in match:
            tmp = re.search(r'(\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})\/(\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})', match['eth_src'])
            #if tmp and tmp.group(2) == 'ff:ff:ff:ff:ff:ff':
            #    match['eth_src'] = tmp.group(1)
            if tmp:
                match['eth_src'] = _baselib.getMatchMac(match['eth_src'])  
                match['eth_src'] = match['eth_src'].lower()  
                  
        if 'eth_dst' in match:
            tmp = re.search(r'(\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})\/(\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})', match['eth_dst'])
            #if tmp and tmp.group(2) == 'ff:ff:ff:ff:ff:ff':
            #    match['eth_dst'] = tmp.group(1)
            if tmp:
                match['eth_dst'] = _baselib.getMatchMac(match['eth_dst'])  
                match['eth_dst'] = match['eth_dst'].lower()  
                       
        if 'ip_src' in match:
            tmp = re.search(r'(\d+\.\d+\.\d+\.\d+)\/(\d+)', match['ip_src'])
            if tmp:
                match['ip_src'] = _baselib.getMatchIpAddr(match['ip_src'])
        if 'ip_dst' in match:
            tmp = re.search(r'(\d+\.\d+\.\d+\.\d+)\/(\d+)', match['ip_dst'])
            if tmp:
                match['ip_dst'] = _baselib.getMatchIpAddr(match['ip_dst'])

        if 'ipv6_src' in match:
            tmp = re.search(r"(.+)\/(.+)", match['ipv6_src'])
            if tmp:
                match['ipv6_src'] = _baselib.getMatchIpv6Addr(match['ipv6_src'])
        if 'ipv6_dst' in match:
            tmp = re.search(r"(.+)\/(.+)", match['ipv6_dst'])
            if tmp:
                match['ipv6_dst'] = _baselib.getMatchIpv6Addr(match['ipv6_dst'])

        tmp_dscp = 0
        if 'dl_type' in match and match['dl_type'] == 'ip':
            if 'ip_dscp' in match:           
                tmp_dscp = int(match['ip_dscp']) << 2
                match['tos'] = str(hex(tmp_dscp))
                match.pop('ip_dscp')
            if 'nw_ecn' in match:
                match['tos'] = str(hex(tmp_dscp + int(match['nw_ecn'])))
                if tmp_dscp == 0:
                    match['tos'] += '/0x3'
                    
                match.pop('nw_ecn')
            if 'nw_ttl' in match:
                match['ttl'] = match['nw_ttl']
                match.pop('nw_ttl')

        tmp_dscp = 0
        if 'dl_type' in match and match['dl_type'] == 'ipv6':
            if 'ip_dscp' in match:           
                tmp_dscp = int(match['ip_dscp']) << 2
                match['tclass'] = str(hex(tmp_dscp))
                match.pop('ip_dscp')
            if 'nw_ecn' in match:
                match['tclass'] = str(hex(tmp_dscp + int(match['nw_ecn'])))
                if tmp_dscp == 0:
                    match['tclass'] += '/0x3'
                match.pop('nw_ecn')
            if 'nw_ttl' in match:
                match['ttl'] = match['nw_ttl']
                match.pop('nw_ttl')
                
        if 'tcp_flags' in match:
            tmp = re.search(r"(.+)\/(.+)", match['tcp_flags'])
            if tmp: 
                tcpflag = int(tmp.group(1),16) & int(tmp.group(2),16)
                tcpflagStr = {
                    1: 'fin',
                    2: 'syn',
                    4: 'rst',
                    8: 'psh',
                    16: 'ack',
                    32: 'urg',
                    64: 'ece',
                    128: 'cwr',
                }
                tmp_str = ''
                for k in tcpflagStr.keys():
                    if k & tcpflag:
                        tmp_str += '+' + tcpflagStr[k]
                    else:
                        tmp_str += '-' + tcpflagStr[k]
                match['tcp_flags'] = tmp_str
                #match['tcp_flags'] = tcpflagStr[tcpflag]
            #match.pop('tcp_flags')
            
        if 'tp_src' in match:             
            tmp = re.search(r"(.+)\/(.+)", match['tp_src'])
            if tmp:
                portPrefix = tmp.group(1)
                portNet = tmp.group(2)
                portPrefix = int(portPrefix,16) & int(portNet,16)
                match['tp_src'] = str(hex(portPrefix)) + '/' + str(hex(int(portNet,16)))

        if 'tp_dst' in match:             
            tmp = re.search(r"(.+)\/(.+)", match['tp_dst'])
            if tmp:
                portPrefix = tmp.group(1)
                portNet = tmp.group(2)
                portPrefix = int(portPrefix,16) & int(portNet,16)
                match['tp_dst'] = str(hex(portPrefix)) + '/' + str(hex(int(portNet,16)))
            
        action  = __flowdict['action']  
        if 'ttl' in match:
            ttl = match['ttl']
        else:
            ttl = '128'
          
        for k in action:
            if k == 'mod_dl_src':
                action['mod_dl_src'] = action['mod_dl_src'].lower()

            if k == 'mod_dl_dst':
                action['mod_dl_dst'] = action['mod_dl_dst'].lower()
                
            if k == 'mod_nw_ttl':
                ttl = action['mod_nw_ttl']      
            
            if k == 'dec_ttl':
                ttl = str(int(ttl) - 1)
                
                
        if 'mod_nw_ttl' in action: 
            action['set_ttl'] = ttl 
            action.pop('mod_nw_ttl') 
        if 'dec_ttl' in action:   
            action['set_ttl'] = ttl 
            action.pop('dec_ttl') 
                                      
        return __flowdict

    def __ovsTableList(self,dut):
        buf = self.dutlib.process(dut,"ovs-vsctl list interface")

    def __ovsTableListUpdate(self,dut):
        '''获取tables表
        '''
        if len(self.ovstable[dut]) > 0:
            return
        buf = self.dutlib.process(dut,"ovsdb-client list-tables -f json")
        js = json.loads(buf)
        for k in js['data'] :
            if isinstance(k,list): 
                self.ovstable[dut].append(k[0])
        return

    def ovsdbForceUpdate(self,dut):
        self.__initlib(dut)
        self.ovsdb[dut]['Force'] = True

    def ovsdbUpdate(self, dut,table=None,force=False):
        '''刷新ovs库配置
        
        table : Bridge Interface Port
        '''
        self.__initlib(dut)
        self.__ovsTableListUpdate(dut)
        db = self.ovsdb[dut]
        if not (force or db['Force']):
            if table == None and len(db) > 0:
                return
            elif table !=None and table in db.keys():
                return
        if db['Force']: table = None
        db['Force'] = False
        add = table if table else ""
        buf = self.dutlib.process(dut,"ovsdb-client -f json dump %s"%(add))
        lines = buf.splitlines()
        for l in lines:
            js = json.loads(l)
            key = js["caption"].replace(" table","")
            db[key]= copy.deepcopy(js)
        return

    def __ovsdbTransDate(self,data):
        '''转换db数据的格式为python格式
        '''
        ret = data
        if isinstance(data,list):
            if data[0] == 'map':
                ret = dict()
                for k in data[1]:
                    ret[k[0]] = k[1]
            elif data[0] == 'uuid':
                ret = data[1]
            elif data[0] == 'set':
                ret = data[1]
        return ret

    def __ovsdbTrans(self,headings,data):
        '''转换db数据的列表格式为字典格式
        '''
        ret = dict()
        for j,v in enumerate(headings):
            ret[v] = self.__ovsdbTransDate(data[j])
        return ret

    def __ovsdbGetKeyIndex(self,dut,table,key):
        '''获取db表项字段的索引
        '''
        __table = self.ovsdb[dut][table]
        return __table['headings'].index(key)

    def __ovsdbSearch(self,dut,table,key,value):
        '''在表中查找一个内容
        '''
        self.ovsdbUpdate(dut, table)
        __table = self.ovsdb[dut][table]
        __index = self.__ovsdbGetKeyIndex(dut,table,key)
        for i in __table['data']:
            if i[__index] != value:
                continue
            return i
        return None

    def __ovsdbSearchByKeys(self,dut,table,**args):
        '''在表中查找匹配的所有项
        '''
        self.ovsdbUpdate(dut, table)
        __table = self.ovsdb[dut][table]
        idict = dict()
        ret = list()
        for j,v in enumerate(__table['headings']):
            idict[v] = j
        for i in __table['data']:
            ok = True
            for k,v in args.items():
                if i[idict[k]] != v:
                    ok = False
                    break
            if ok:
                ret.append(i)
        return ret

    def __ovsdbGetUUIDDict(self,dut,table,key):
        '''按uuid作为key,返回信息
        '''
        self.ovsdbUpdate(dut, table)
        ret = dict()
        __table = self.ovsdb[dut][table]
        if __table['headings'][0] != '_uuid':
            return ret
        __index = __table['headings'].index(key)
        for i in __table['data']:
            ret[i[0][1]] = i[__index]
        return ret

    def __ovsdbGetUUID(self,dut,table,key,value):
        '''查询uuid
        '''
        self.ovsdbUpdate(dut, table)
        __table = self.ovsdb[dut][table]
        if __table['headings'][0] != '_uuid':
            return None
        __index = __table['headings'].index(key)
        for i in __table['data']:
            if value == i[__index]:
                return i[0][1]
        return None

    def ovsdbSearch(self,dut,table,key,value):
        '''在表中查找一个表内容
        '''
        self.__initlib(dut)
        ret = self.__ovsdbSearch(dut, table,key,value)
        if None == ret : return None
        __heading = self.ovsdb[dut][table]['headings']
        return self.__ovsdbTrans(__heading,ret)
    
    def __getBridgeByPortUUID(self, dut, port_uuid):
        self.ovsdbUpdate(dut, 'Bridge')
        bridge_data = self.ovsdb[dut]['Bridge']['data']
        for i in bridge_data:
            ports = self.__ovsdbTransDate(i[16])
            if isinstance(ports,list):
                if port_uuid in [k[1] for k in ports]:
                    return i[13]
            else:
                if port_uuid == ports[1]:
                    return i[13]
        return None

    def getNewBridgeName(self):
        return "br_"+str(random.randint(10000,99999))

    def getNewPortName(self,br='any'):
        return "p_%s"%(str(random.randint(10000,99999)))
    
    def isAutoName(self,name):
        #if name.startswith("auto_"):    return True
        if re.match(r"(br|p)_\d{5}",name) :
            return True
        return False

    def getOvsInfo(self,dut):
        self.ovsdbUpdate(dut, "Open_vSwitch")
        __table = self.ovsdb[dut]["Open_vSwitch"]
        info = self.__ovsdbTrans(__table['headings'],__table['data'] [0])
        return info

    def getOvsVersion(self,dut):
        '''获取 ovs版本信息
        '''
        self.__initlib(dut)
        if 'version' in self.ovsinfo[dut]:
            return self.ovsinfo[dut]['version']
        info= self.getOvsInfo(dut)
        version = {
            'dpdk' : info.get('dpdk_version',''),
            'dpdk_initialized' : info.get('dpdk_initialized',False)
        }
        buf   = self.dutlib.process(dut,"ovs-vswitchd --version ")
        lines = buf.splitlines()
        for l in lines:
            __ret = re.search(r"ovs-vswitchd \(Open vSwitch\)\s*([\d.]+)",l)
            if __ret:
                version['ovs'] = __ret.group(1)
        self.ovsinfo[dut]['version'] = version
        return version

    def isOvsHwOffload(self,dut):
        info= self.getOvsInfo(dut)
        ret = info['other_config'].get('hw-offload','false')
        if ret.lower() == 'true' :
            ret = True
        else :
            ret = False
        return ret

    def getBridgeByPort(self,dut,intname):
        self.__initlib(dut)
        if intname == None: return None
        portuuid = self.__ovsdbGetUUID(dut,"Port","name",intname)
        if portuuid == None: return None
        bridge = self.__getBridgeByPortUUID(dut, portuuid)
        return bridge

    def getBridges(self,dut):
        self.__initlib(dut)
        bdict = self.__ovsdbGetUUIDDict(dut,"Bridge","name")
        return bdict.values()

    def getPorts(self,dut):
        self.__initlib(dut)
        bdict = self.__ovsdbGetUUIDDict(dut,"Port","name")
        return bdict.values()

    def getPortsByBridge(self,dut,bridge):
        info = self.ovsdbSearch(dut,"Bridge","name",bridge)
        if None == info : return list()
        uuids = self.__ovsdbGetUUIDDict(dut,'Port','name')
        if not isinstance(info['ports'],list):
            return [uuids[info['ports']]]
        return [uuids[k[1]] for k in info['ports']]

    def getInterfacesByPort(self,dut,Port):
        info = self.ovsdbSearch(dut,"Port","name",Port)
        if None == info : return list()
        uuids = self.__ovsdbGetUUIDDict(dut,'Interface','name')
        if not isinstance(info['interfaces'],list):
            return [uuids[info['interfaces']]]
        return [uuids[k[1]] for k in info['interfaces']]

    def getInterfacesByBridge(self,dut,bridge):
        ports = self.getPortsByBridge(dut,bridge)
        ret = list()
        for port in ports:
            ints = self.getInterfacesByPort(dut,port)
            ret += ints
        return ret
    
    def getPatchPeer(self,dut,intf):
        info = self.getInterfaceInfo(dut,intf)
        if info == None: return None
        if info['type'] != "patch" : return None
        if 'options' not in info : return None
        if 'peer' not in info['options'] : return None
        return info['options']['peer']

    def findPatch(self,dut,br1,br2):
        patchs = self.findInterface(dut,br1,'patch')
        if len(patchs) > 0:
            for p in patchs:
                peer = self.getPatchPeer(dut,p)
                br = self.getBridgeByPort(dut,peer)
                if br == br2:
                    return p,peer
        return None,None

    def findInterfaceFirstTunnel(self,dut,bridge=None):
        self.ovsdbUpdate(dut, 'Interface')
        tunnle = ['gre','geneve','vxlan','stt','lisp','erspan','ip6erspan']
        __table = self.ovsdb[dut]['Interface']
        __index = __table['headings'].index('type')
        __name  = __table['headings'].index('name')
        for i in __table['data']:
            if i[__index] in tunnle:
                if bridge :
                    br=self.getBridgeByPort(dut,i[__name])
                    if br != bridge :
                        continue
                return i[__name]
        return None

    def findInterface(self,dut,bridge=None,itype=None):
        self.ovsdbUpdate(dut, 'Interface')
        __table = self.ovsdb[dut]['Interface']
        __type  = __table['headings'].index('type')
        __name  = __table['headings'].index('name')
        ret = list()
        for i in __table['data']:
            if itype and i[__type] != itype:
                continue
            if bridge :
                br=self.getBridgeByPort(dut,i[__name])
                if br != bridge :
                    continue
            ret.append(i[__name])
        return ret

    def ovsGetTunnelInfo(self,dut,tun_port=None):
        br = self.getBridgeByPort(dut,tun_port)
        info = self.getInterfaceInfo(dut,tun_port)
        ret = info["options"]
        ipinfo = self.linuxlib.ipShow(dut)
        intf = None
        ip = None
        for k,v in ipinfo.items():
            if 'ip' not in v and 'ipv6' not in v: continue
            
            if 'ip' in v:
                for j in v['ip']:
                    if ret['local_ip'] in j:
                        intf = k
                        ip = j
            if 'ipv6' in v:
                for j in v['ipv6']:
                    if ret['local_ip'] in j:
                        intf = k
                        ip = j
        ret['bridge'] = br
        ret['knl_intf'] = intf
        ret['knl_mac'] = ipinfo[intf]['mac'] if intf else None
        ret['mac_in_use'] = info['mac_in_use']
        ret['knl_ipex'] = ip
        ret['type'] = info['type']
        return ret

    def getInterfaceInfo(self,dut,intname):
        self.__initlib(dut)
        ret = dict()
        if isinstance(intname,int):
            ret = self.ovsdbSearch(dut,"Interface","ofport",intname)
        else :    
            ret = self.ovsdbSearch(dut,"Interface","name",intname)
        return ret

    def getInterfaceName(self,dut,intf):
        info = self.getInterfaceInfo(dut,int(intf))
        return info['name'] if info else None

    def getInterfaceType(self,dut,itype):
        '''获取接口的类型（dpdk，vxlan）
        '''
        info = self.getInterfaceInfo(dut,itype)
        return info['type'] if info else None

    def getInterfaceMac(self,dut,intf):
        '''获取接口的mac地址
        '''
        info = self.getInterfaceInfo(dut,intf)
        return info['mac_in_use'] if info else None

    def __devGetPciByArg(self,dpdkarg):
        if dpdkarg == None : return None
        _re = re.search(r"([0-9A-Fa-f:]{5,10}\.[0-9A-Fa-f])",dpdkarg)
        if _re : 
            return _re.group(0)
        return None

    def isPci(self,port):
        '''检查配置是否一个pci地址
        '''
        pci = self.__devGetPciByArg(port)
        if pci == None:
            return False
        return True

    def getRealPort(self,dut,port):
        '''根据参数，找到实际的ovs端口
        '''
        if self.isPci(port):
            return self.getPortByPci(dut,port)
        else:
            pinfo = self.ovsdbSearch(dut,"Interface","name",port)
            #非pci端口需要创建，如果找不到就报错退出
            BuiltIn().should_be_true(pinfo != None,"Can't find port %s"%port)
            return port

    def devGetList(self,dut):
        '''获取设备列表
        
        | ret  = {
        |     '0000:00:09.0' : {
        |         'pci'  : '0000:00:09.0',
        |         'name' : '82540EM Gigabit Ethernet Controller 100e',
        |         'if' : 'enp0s3',
        |         'drv': 'vfio-pci',
        |         'unused' : 'e1000',
        |         'dpdk' : True,
        |         },
        |     }
        '''
        ''' dpdk-devbind.py --status-dev net  , dpdk: vfio-pci,uio_pci_generic,igb_uio
        Network devices using DPDK-compatible driver
        ============================================
        0000:00:09.0 '82540EM Gigabit Ethernet Controller 100e' drv=vfio-pci unused=e1000
        0000:00:0a.0 '82540EM Gigabit Ethernet Controller 100e' drv=vfio-pci unused=e1000

        Network devices using kernel driver
        ===================================
        0000:00:03.0 '82540EM Gigabit Ethernet Controller 100e' if=enp0s3 drv=e1000 unused=vfio-pci *Active*
        0000:00:08.0 '82540EM Gigabit Ethernet Controller 100e' if=enp0s8 drv=e1000 unused=vfio-pci *Active*
        0000:00:10.0 'Virtio network device 1000' if=enp0s16 drv=virtio-pci unused=vfio-pci
        0000:00:11.0 '82540EM Gigabit Ethernet Controller 100e' if=enp0s17 drv=e1000 unused=vfio-pci
        '''
        self.__initlib(dut)
        buf = self.dutlib.process(dut,'dpdk-devbind.py --status-dev net')
        lines = buf.splitlines()
        niclist = {}
        for l in lines:
            ret = re.search(r"([0-9A-Fa-f:.]{12})\s+\'(.*)\'\s+if=(.*)\s+drv=(.*)\s+unused=(\S*)",l)
            if ret:
                pci = ret.group(1)
                niclist[pci] = dict()
                
                niclist[pci]['pci']  = ret.group(1)
                niclist[pci]['name'] = ret.group(2)
                niclist[pci]['if'] = ret.group(3)
                niclist[pci]['drv'] = ret.group(4)
                niclist[pci]['unused'] = ret.group(5)
                niclist[pci]['dpdk']  = niclist[pci]['drv'] in self.drivers
                continue
            ret = re.search(r"([0-9A-Fa-f:.]{7,12})\s+\'(.*)\'\s+drv=(.*)\s+unused=(\S*)",l)
            if ret:
                pci = ret.group(1)
                niclist[pci] = dict()
                niclist[pci]['dpdk']  = ret.group(3) in self.drivers
                niclist[pci]['pci']  = ret.group(1)
                niclist[pci]['name'] = ret.group(2)
                niclist[pci]['drv'] = ret.group(3)
                niclist[pci]['dpdk']  = niclist[pci]['drv'] in self.drivers
                continue
        return niclist

    def __fraseStrToDict(self,line):
        '''解析字符串为字典
        '''
        idict = {} 
        for i in self.__splitBracket(line) :
            if '(' not in i:
                for j in i.split(','):
#                    if '=' not in j :
#                        idict['type'] = j
#                        continue
                    if ':' in j:
                        k,v = i.split(':',1)
                        idict[k] = v
                    if '=' in j:
                        k,v = j.split('=',1)
                        idict[k] = v
                    idict['type'] = j
                continue
            k,v = i.split('(',1)
            v = v[:-1]
            if '=' not in v:
                idict[k] = v
            else:
                idict[k] = dict()
                if '(' in v: 
                    idict[k].update(self.__fraseStrToDict(v))
                else:
                    for j in v.split(','):
                        if '=' not in j : continue
                        k2,v2 = j.split('=',1)
                        idict[k][k2] = v2

            if 'set' in idict:
                temp_dict = idict['set']
                if 'eth' in temp_dict:
                    idict['set_eth'] = temp_dict['eth']
                if 'ipv4' in temp_dict:
                    idict['set_ipv4'] = temp_dict['ipv4']
                if 'ipv6' in temp_dict:
                    idict['set_ipv6'] = temp_dict['ipv6']
                if  'udp' in temp_dict:
                    idict['set_tp'] = temp_dict['udp']
                if  'tcp' in temp_dict:
                    idict['set_tp'] = temp_dict['tcp']

                idict.pop('set', None)

        return idict

    def flowFraseDpflowTOdictTest(self,dpflow):
        ''' 转换快表到字典
        root@work:~# ovs-appctl dpif/dump-flows  br-ext
        recirc_id(0),in_port(2),packet_type(ns=0,id=0),eth(src=08:00:27:f9:11:96,dst=00:01:00:00:00:03),eth_type(0x0806), packets:0, bytes:0, used:never, actions:4
        recirc_id(0),in_port(4),packet_type(ns=0,id=0),eth(src=00:01:00:00:00:03,dst=ff:ff:ff:ff:ff:ff),eth_type(0x0806),arp(sip=192.168.2.10,tip=192.168.2.55,op=1), packets:0, bytes:0, used:never, actions:2

        recirc_id(0),in_port(dpdk0),packet_type(ns=0,id=0),eth(src=00:01:00:00:00:02),eth_type(0x0800),ipv4(tos=0x1/0x3,frag=no), packets:93, bytes:11904, used:0.012s, actions:set(eth(src=00:01:00:00:00:04)),clone(tnl_push(tnl_port(vxlan_sys_4789),header(size=50,type=4,eth(dst=00:01:00:00:00:03,src=08:00:27:f9:11:96,dl_type=0x0800),ipv4(src=192.168.2.55,dst=192.168.2.10,proto=17,tos=0x1,ttl=64,frag=0x4000),udp(src=0,dst=4789,csum=0x0),vxlan(flags=0x8000000,vni=0x64)),out_port(br-ext)),dpdk1)
        recirc_id(0),in_port(dpdk0),packet_type(ns=0,id=0),eth(src=00:01:00:00:00:02),eth_type(0x0806), packets:2, bytes:120, used:0.368s, actions:set(eth(src=00:01:00:00:00:04)),clone(tnl_push(tnl_port(vxlan_sys_4789),header(size=50,type=4,eth(dst=00:01:00:00:00:03,src=08:00:27:f9:11:96,dl_type=0x0800),ipv4(src=192.168.2.55,dst=192.168.2.10,proto=17,tos=0,ttl=64,frag=0x4000),udp(src=0,dst=4789,csum=0x0),vxlan(flags=0x8000000,vni=0x64)),out_port(br-ext)),dpdk1)

        'ovs-appctl dpif/dump-flows --names br-ext'
        recirc_id(0),in_port(br-ext),packet_type(ns=0,id=0),eth(src=08:00:27:f9:11:96,dst=00:01:00:00:00:03),eth_type(0x0806), packets:0, bytes:0, used:never, actions:dpdk1
        recirc_id(0),in_port(dpdk1),packet_type(ns=0,id=0),eth(src=00:01:00:00:00:03,dst=ff:ff:ff:ff:ff:ff),eth_type(0x0806),arp(sip=192.168.2.10,tip=192.168.2.10,op=1), packets:1, bytes:60, used:3.394s, actions:br-ext
        recirc_id(0),in_port(dpdk1),packet_type(ns=0,id=0),eth(src=00:01:00:00:00:03,dst=ff:ff:ff:ff:ff:ff),eth_type(0x0806),arp(sip=192.168.2.10,tip=192.168.2.55,op=1), packets:0, bytes:0, used:never, actions:br-ext
        '''
        rule_dict = {'match':dict(),'action':dict()}
        _rule = re.sub(r"\s","",dpflow)
        _re = re.search(r"(.+)actions:(.+)",_rule)
        if not _re :
            raise AssertionError("Flow : rule error ")
        match_info = _re.group(1).strip()
        action_info = _re.group(2).strip()
        rule_dict['match'] = self.__fraseStrToDict(match_info)
        rule_dict['action'] = self.__fraseStrToDict(action_info)
        if 'type' in rule_dict['action']:
            port = rule_dict['action']['type']
#            port = self.getInterfaceName(port)
            if port !=None :  #判断type是一个接口
                rule_dict['action']['type']=port
        return rule_dict

    def flowFraseDpflowTOdict(self,dpflow):
        ''' 转换快表到字典
        root@work:~# ovs-appctl dpif/dump-flows  br-ext
        recirc_id(0),in_port(2),packet_type(ns=0,id=0),eth(src=08:00:27:f9:11:96,dst=00:01:00:00:00:03),eth_type(0x0806), packets:0, bytes:0, used:never, actions:4
        recirc_id(0),in_port(4),packet_type(ns=0,id=0),eth(src=00:01:00:00:00:03,dst=ff:ff:ff:ff:ff:ff),eth_type(0x0806),arp(sip=192.168.2.10,tip=192.168.2.55,op=1), packets:0, bytes:0, used:never, actions:2

        recirc_id(0),in_port(dpdk0),packet_type(ns=0,id=0),eth(src=00:01:00:00:00:02),eth_type(0x0800),ipv4(tos=0x1/0x3,frag=no), packets:93, bytes:11904, used:0.012s, actions:set(eth(src=00:01:00:00:00:04)),clone(tnl_push(tnl_port(vxlan_sys_4789),header(size=50,type=4,eth(dst=00:01:00:00:00:03,src=08:00:27:f9:11:96,dl_type=0x0800),ipv4(src=192.168.2.55,dst=192.168.2.10,proto=17,tos=0x1,ttl=64,frag=0x4000),udp(src=0,dst=4789,csum=0x0),vxlan(flags=0x8000000,vni=0x64)),out_port(br-ext)),dpdk1)
        recirc_id(0),in_port(dpdk0),packet_type(ns=0,id=0),eth(src=00:01:00:00:00:02),eth_type(0x0806), packets:2, bytes:120, used:0.368s, actions:set(eth(src=00:01:00:00:00:04)),clone(tnl_push(tnl_port(vxlan_sys_4789),header(size=50,type=4,eth(dst=00:01:00:00:00:03,src=08:00:27:f9:11:96,dl_type=0x0800),ipv4(src=192.168.2.55,dst=192.168.2.10,proto=17,tos=0,ttl=64,frag=0x4000),udp(src=0,dst=4789,csum=0x0),vxlan(flags=0x8000000,vni=0x64)),out_port(br-ext)),dpdk1)

        'ovs-appctl dpif/dump-flows --names br-ext'
        recirc_id(0),in_port(br-ext),packet_type(ns=0,id=0),eth(src=08:00:27:f9:11:96,dst=00:01:00:00:00:03),eth_type(0x0806), packets:0, bytes:0, used:never, actions:dpdk1
        recirc_id(0),in_port(dpdk1),packet_type(ns=0,id=0),eth(src=00:01:00:00:00:03,dst=ff:ff:ff:ff:ff:ff),eth_type(0x0806),arp(sip=192.168.2.10,tip=192.168.2.10,op=1), packets:1, bytes:60, used:3.394s, actions:br-ext
        recirc_id(0),in_port(dpdk1),packet_type(ns=0,id=0),eth(src=00:01:00:00:00:03,dst=ff:ff:ff:ff:ff:ff),eth_type(0x0806),arp(sip=192.168.2.10,tip=192.168.2.55,op=1), packets:0, bytes:0, used:never, actions:br-ext
        '''
        rule_dict = {'match':dict(),'action':dict()}
        _rule = re.sub(r"\s","",dpflow)
        _re = re.search(r"(.+)actions:(.+)",_rule)
        if not _re :
            raise AssertionError("Flow : rule error ")
        match_info = _re.group(1).strip()
        action_info = _re.group(2).strip()
        rule_dict['match'] = self.__fraseStrToDict(match_info)
        rule_dict['action'] = self.__fraseStrToDict(action_info)
        return rule_dict
		
    def showDpifFlows(self,dut,bridge,itype=None):
        self.__initlib(dut)
        buf = self.dutlib.process(dut,"ovs-appctl dpif/dump-flows %s"%bridge)
        lines = buf.splitlines()
        ret = list()
        for l in lines:
            tmp = self.flowFraseDpflowTOdict(l)
            if tmp : ret.append(tmp)
        return ret
	
    def showDpFlowsMore(self,dut):
        #offloaded
        self.__initlib(dut)
        buf = self.dutlib.process(dut,"ovs-appctl dpctl/dump-flows --names -m")
        lines = buf.splitlines()
        ret = list()
        for l in lines:
            f = self.flowFraseDpflowTOdict(l)
            ret.append(f)
        return ret
    
    def showDpFlowsTest(self,dut,itype=""):
        #offloaded
        self.__initlib(dut)
        if itype!= None:
            itype = "--type=%s"%itype
        buf = self.dutlib.process(dut,"ovs-appctl dpctl/dump-flows --names %s"%(itype))
        lines = buf.splitlines()
        ret = list()
        for l in lines:
            f = self.flowFraseDpflowTOdict(l)
            ret.append(f)
        return ret

    def showDpFlows(self,dut):
        self.__initlib(dut)
        buf = self.dutlib.process(dut,"ovs-appctl dpctl/dump-flows --names type=offloaded")
        logger.debug("offload: %s"%(buf))
        lines = buf.splitlines()
        ret = list()
        str = "flow-dump from pmd on cpu core"
        for l in lines:
            if (str not in l):
                f = self.flowFraseDpflowTOdict(l)
                ret.append(f)
        return ret

    def showTnlArp(self,dut):
        self.__initlib(dut)
        buf = self.dutlib.process(dut,"ovs-appctl tnl/arp/show")
        lines = buf.splitlines()
        ret = list()
        for l in lines:
            _re = re.search(r'(\S+)\s+(\S+)\s+(\S+)',l)
            if _re:
                ret.append({
                    'ip'  : _re.group(1),
                    'mac' : _re.group(2),
                    'bridge' : _re.group(3)
                })
        return ret        

    def showFlows(self,dut,bridge):
        '''获取流表项
        '''
        self.__initlib(dut)
        buf = self.dutlib.process(dut,"ovs-ofctl dump-flows %s --names"%(bridge))
        lines = buf.splitlines()
        ret = list()
        for l in lines:
            rule = self.flowFraseRuleToDict(l)
            ret.append(rule)
        return ret

    def showPortStats(self,dut,bridge,port=None):
        self.__initlib(dut)
        buf = self.dutlib.process(dut,"ovs-ofctl dump-ports %s --names"%(bridge))
        lines = buf.splitlines()
        ret = dict()
        port = None
        for l in lines:
            tmp = re.search(r"\s*port\s+(\S*)\:(.+)",l)
            if tmp :
                port = tmp.group(1)
                ret[port]= dict()
                l = tmp.group(2)
            if port == None: continue
            _rule = re.sub(r"\s","",l)
            for k in _rule.split(","):
                s = k.split("=")
                ret[port][s[0]] = s[1]
        return ret
    
    def gotoBridge(self,dut,name,config):
        '''创建网桥
        
        table : ovs-vsctl add-br br-ext -- set bridge br-ext datapath_type=netdev
                ovs-vsctl add-br br-int -- set bridge br-int datapath_type=netdev 
                -- br-set-external-id br-int bridge-id br-int -- set bridge br-int fail-mode=standalone
        '''
        self.__initlib(dut)
        val = self.zxins[dut]['bridge']
        if name in val.keys():
            return
        t = config.get("type","netdev")
        self.dutlib.process(dut,"ovs-vsctl add-br %s -- set bridge %s datapath_type=%s"%(name,name,t))
        val[name] = {'type':t,
                    'flow':list(),
                    'port':dict()
                    }
    
    def __getPciPorts(self,dut):
        self.ovsdbUpdate(dut,"Interface")
        plist = self.__ovsdbSearchByKeys(dut,"Interface",type='dpdk')
        idx = self.__ovsdbGetKeyIndex(dut,'Interface','options')
        iname = self.__ovsdbGetKeyIndex(dut,'Interface','name')
        idict = dict()
        for p in plist:
            options = self.__ovsdbTransDate(p[idx])
            arg = options.get('dpdk-devargs',None)
            pci = self.__devGetPciByArg(arg)
            idict[pci] = p[iname]
        return idict

    def getPortByPci(self,dut,pci):
        pcis = self.__getPciPorts(dut)
        if pci in pcis:
            return pcis[pci]
        if '0000:'+pci in pcis:
            return pcis['0000:'+pci]
        return None

    def ovsPortsRelease(self,dut,pcis=None):
        '''强制释放端口
            仅释放PCI端口
        '''
        if pcis == None: 
            return
        if not isinstance(pcis,list):
            pcis = [pcis]
        curpcis = self.__getPciPorts(dut)
        for pci in pcis:
            port = curpcis.pop(pci,None) or curpcis.pop('0000:'+pci,None)
            if port == None:
                 continue
            bri = self.getBridgeByPort(dut,port)
            self.delPort(dut,bri,port)
        self.ovsdbUpdate(dut,force=True)

    def setOvsConfig(self,dut,config):
        self.__initlib(dut)
        if 'hw-offload' in config:
            tmp = str(config.get['hw-offload']).lower()
            self.dutlib.process(dut, 'ovs-vsctl  set Open-vSwitch . other_config:hw-offload=%s'%(tmp))

        self.ovsdbUpdate(dut,force=True)

    def clearOvsConfig(self,dut,config):
        self.__initlib(dut)
        if 'hw-offload' in config:
            tmp = str(config.get['hw-offload']).lower()
            self.dutlib.process(dut, 'ovs-vsctl  set Open-vSwitch . other_config hw-offload')

        self.ovsdbUpdate(dut,force=True)

    def clearOvsPurge(self,dut):
        self.__initlib(dut)
        self.dutlib.process(dut, 'ovs-appctl revalidator/purge')

    def gotoBridge(self,dut,name,config):
        '''创建网桥

        table : ovs-vsctl add-br br-ext 
                    -- set bridge br-ext datapath_type=netdev 
                    -- br-set-external-id br-ext bridge-id br-ext 
                    -- set bridge br-ext fail-mode=standalone
        '''
        self.__initlib(dut)
        val = self.zxins[dut]['bridge']

        #如果网桥已经创建则返回
        brs = self.getBridges(dut)
        if name in brs :
            return

        t = config.get("datapath_type",'netdev')
        
        _order  = "ovs-vsctl --may-exist add-br %s "%name
        _order += "-- set bridge %s datapath_type=%s "%(name,t)
        if 'external-id' in config:
            _order += "-- br-set-external-id %s bridge-id %s "%(name,name)
        if 'fail-mode' in config:
            m = config.get("failmode","standalone")
            _order += "-- set bridge %s fail-mode=%s"%(name,m)
        self.dutlib.process(dut,_order)
        val[name] = copy.deepcopy(config)
        val[name]['port'] = dict()   #仅记录端口，不记录配置
        self.setBridge(dut,name,config)
            
        self.ovsdbForceUpdate(dut)
        
    def setBridge(self,dut,name,config):
        self.__initlib(dut)
        val = self.zxins[dut]['bridge']
        if 'flow' in config:
            for v in config['flow']:
                self.setFlow(dut,name,v)
        if 'port' in config:
            for k,v in config['port'].items():
                self.gotoPort(dut,name,k,v)
    
    def clearBridge(self,dut,name,config):
        self.__initlib(dut)
        val = self.zxins[dut]['bridge']
        if 'flow' in config:
            for v in config['flow']:
                self.clearFlow(dut,name,v)
        if 'port' in config:
            for k,v in config['port'].items():
                self.delPort(dut,name,k)
        self.ovsdbForceUpdate(dut)

    def delBridge(self,dut,name):
        '''删除网桥
        '''
        self.__initlib(dut)
        val = self.zxins[dut]['bridge']
        val_port = self.zxins[dut]['port']
        self.dutlib.process(dut,"ovs-vsctl del-br %s"%(name))
        if name not in val:
            return
        for k,_ in val[name].get('port',dict()):
            val_port.pop(k,None)
        val.pop(name,None)
        self.ovsdbForceUpdate(dut)

    def gotoPort(self,dut,bridge,name,config):
        '''创建端口
        ovs-vsctl add-port br-ext dpdk0 -- set Interface dpdk0 type=dpdk 
                   options:dpdk-devargs=0000:00:08.0 
                   options:n_rxq_desc=256 
                   options:n_txq_desc=256 
                   ofport_request=1
        '''
        self.__initlib(dut)

        val = self.zxins[dut]['port']
        if name in val:
            self.setPort(dut,name,config)
            return
        t = config.get("type","dpdk")
        _order = "ovs-vsctl --may-exist add-port %s %s -- set Interface %s type=%s"%(bridge,name,name,t)
        
        if 'options' in config:
            for k,v in  config['options'].items():
                _order += " options:%s=%s"%(k,v)
        if 'ofport_request' in config:
             _order += " ofport_request=%s"%format(config['ofport_request'])
        
        self.dutlib.process(dut,_order)
        
        if name not in val.keys():
            val[name]=dict()
        val[name].update(config)
        self.ovsdbForceUpdate(dut)
    
    def setPort(self,dut,name,config):
        self.__initlib(dut)
        _order = "ovs-vsctl set-port %s"%(name)
        
        if "options" in config:
            for k,v in  config['options'].items():
                _order += " options:%s=%s".format(k,v)
        self.dutlib.process(dut,_order)
        self.ovsdbForceUpdate(dut)

    def setInterface(self,dut,name,config):
        self.__initlib(dut)
        _order = "ovs-vsctl set Interface %s"%(name)

        if "options" in config:
            for k,v in  config['options'].items():
                _order += " options:%s=%s"%(k,v)

        if "other_config" in config:
            for k,v in  config['other_config'].items():
                _order += " other_config:%s=%s"%(k,v)
        self.dutlib.process(dut,_order)
        self.ovsdbForceUpdate(dut)

    def clearInterface(self,dut,name,config):
        self.__initlib(dut)

    def clearPort(self,dut,name,config):
        self.__initlib(dut)

    def delPort(self,dut,bridge,name):
        '''删除端口
        '''
        self.__initlib(dut)
        var_br   = self.zxins[dut]['bridge']
        val_port = self.zxins[dut]['port']
        if bridge == None:
            bridge = self.getBridgeByPort(dut,name)
        if bridge == name :
            return
        if bridge == None:
            logger.warn("Can't find bridge for %s"%name)
            return
        self.dutlib.process(dut,"ovs-vsctl del-port %s %s"%(bridge,name))
        if bridge in var_br:
            var_br[bridge]['port'].pop(name,None)
        val_port.pop(name,None)
        self.ovsdbForceUpdate(dut)
    
    def setFlow(self,dut,bridge,rule):
        '''流表配置
        '''
        self.__initlib(dut)
        idict = self.zxins[dut]['flow']  #主要用于校验
        idict.setdefault(bridge,list())
        __rule = self.flowTransToRule(rule)
        self.dutlib.process(dut,'ovs-ofctl add-flow %s %s'% \
                    (bridge,__rule))
        idict[bridge].append(__rule)
        
    def clearFlow(self,dut,bridge,rule=None):
        '''清除流表
        '''
        self.__initlib(dut)
        idict = self.zxins[dut]['flow']
        idict.setdefault(bridge,list())
 
        __rule = self.flowTransToRule(rule)
        if rule and 'priority' in rule:
            self.dutlib.process(dut,'ovs-ofctl --strict del-flows %s %s'% \
                    (bridge,__rule))
        else:
            self.dutlib.process(dut,'ovs-ofctl del-flows %s %s'% \
                    (bridge,__rule))
        if __rule == "":
            idict[bridge] = list()
        else :
            idict[bridge].pop(__rule)    

    def ovsCheckConfig(self,dut):
        '''检查配置 未完成
        '''
        self.__initlib(dut)
        self.ovsdbUpdate(dut)
        for k,v in self.zxins[dut]['bridge']:
            binfo = self.__ovsdbSearch(dut,'Bridge','name',k)
            BuiltIn().should_be_true(binfo!=None,"Can't find Bridge %s"%k)

    def ovsRunConfig(self, dut, config):
        '''运行ovs配置字典
        
        关键字处在全局配置字典的最顶层:
        
        | 接口配置    | 'port' : { }   | 参考 Add Port Config 关键字帮助 |
        | 路由配置    | 'flow' : { } | 参考 Add Flow 关键字帮助 |
        '''
        self.__initlib(dut)

        #if not self.dutlib.configMode(dut):
        #    raise AssertionError("Can't enter config mode!")
        logger.debug("Config ovs !!!!!")
        if 'bridge' in config:
            for k,v in config['bridge'].items():
                self.gotoBridge(dut,k,v)
        if 'port' in config:
            for k,v in config['port'].items():
                self.setPort(dut,k,v)
        if 'interface' in config:
            for k,v in config['interface'].items():
                self.setInterface(dut,k,v)
        if 'flow' in config:
            for k in config['flow'].keys():
                for l in config['flow'][k]:
                    self.setFlow(dut,k,config['flow'][k][l])
        return True

    def ovsClearConfig(self,dut,config=None):
        '''删除ovs已经配置的基本配置
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

    def ovsClearDut(self, dut, config = None):
        '''获取设备配置，然后再删除
        '''
        self.__initlib(dut)
        if not config:
            #不清除配置， 否则清空了其他人的配置
            return True
        #根据配置清

        return True

    def ovsReload(self, dut,buf=False):
        '''重载所有的配置
        '''
        pass
    
    def ovsBackup(self, dut):
        '''恢复当前配置
        '''
        if dut not in self.zxinsbk:
            self.zxinsbk[dut] = []
        if dut not in self.zxins:
            self.zxinsbk[dut].append({})
            return True
        self.zxinsbk[dut].append(copy.deepcopy(self.zxins[dut]))
        return True
    
    def ovsResume(self,dut):
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
        
        logger.info("ovs Resume]start")
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
        self.ovsClearConfig(dut,va)
        #配置被删除的参数
        self.ovsRunConfig(dut,bk)
        logger.info("[ovs Resume]end")

    def ovsCleanAuto(self,dut):
        '''删除自动化创建的端口
        '''
        self.__initlib(dut)
        for p in self.getPorts(dut):
            if self.isAutoName(p):
                self.delPort(dut,None,p)
        for br in self.getBridges(dut):
            if self.isAutoName(br):
                self.delBridge(dut,br)
    
    def setFlowDefault(self,dut,bridge):
        self.setFlow(dut,bridge,{'match':{'priority':0},'action':{'type':'normal'}})
    
    def clearFlowDefault(self,dut,bridge):
        self.clearFlow(dut,bridge,{'match':{'priority':0},'action':{'type':'normal'}})

    def gotoBridgeWithProperty(self,dut,name,config):
        '''兼容性
        '''
        self.gotoBridge(dut,name,config)

    def delFlowsByBridge(self,dut,name):
        '''兼容性
        '''
        self.clearFlow(dut,name)

    def flowRunConfig(self, dut, config):
        '''运行ovs配置字典
        
        关键字处在全局配置字典的最顶层:
        
        | 接口配置    | 'port' : { }   | 参考 Add Port Config 关键字帮助 |
        | 路由配置    | 'flow' : { } | 参考 Add Flow 关键字帮助 |
        '''
        self.__initlib(dut)
        #if not self.dutlib.configMode(dut):
        #    raise AssertionError("Can't enter config mode!")
        logger.debug("Config ovs !!!!!")

        if 'bridge' in config:
            for k,v in config['bridge']:
                self.gotoBridge(dut,k,v)
                self.setBridge(dut,k,v)
              
        #根据inport和outport获取网桥名称
        if 'bridge' not in config:
            bridge = self.getBridgeByPort(dut, config['match']['in_port'])
        logger.debug("bridge name %s!", bridge)

        logger.debug("config ovs start and show")
        self.setFlow(dut, bridge, config)

    def flowClearConfig(self, dut, config):
        '''运行ovs配置字典
        
        关键字处在全局配置字典的最顶层:
        
        | 接口配置    | 'port' : { }   | 参考 Add Port Config 关键字帮助 |
        | 路由配置    | 'flow' : { } | 参考 Add Flow 关键字帮助 |
        '''
        self.__initlib(dut)

        #根据inport和outport获取网桥名称
        if 'bridge' not in config:
            bridge = self.getBridgeByPort(dut, config['match']['in_port'])
        self.dutlib.process(dut, 'ovs-appctl revalidator/purge')
        self.dutlib.process(dut,'ovs-ofctl del-flows %s'% (bridge))

    def ovsLoggerDebug(self,dut,bridge):
        self.__initlib(dut)
        if bridge == None:
            return
        logger.debug("==============ovs info %s==============="%str(bridge))
        logger.debug(self.dutlib.process(dut,'ovs-ofctl dump-flows %s --names'%bridge))
        logger.debug(self.dutlib.process(dut,'ovs-ofctl dump-ports %s'%bridge))
        #logger.debug(self.dutlib.process(dut,'ovs-appctl dpif/dump-flows --names %s'%bridge))
        logger.debug(self.dutlib.process(dut,'ovs-appctl dpctl/dump-flows -m'))
        logger.debug(self.dutlib.process(dut,'ovs-appctl tnl/arp/show'))

    def findFirstFlows(self, dut, bridge, flowconfig):
        self.__initlib(dut)
        ovs_flow = self.showFlows(dut, bridge)
        __flow = self.__flowTransForPacket(flowconfig)
        
        expected_match_set = set(__flow['match'].items())
        __flow['action'].pop("type",None)
        expected_action_set = set(__flow['action'].items())
        for i in ovs_flow:
            i = self.__flowTransForPacket(i)
            x = expected_match_set.issubset(set(i['match'].items()))
            y = expected_action_set.issubset(set(i['action'].items()))
            if x and y :
                logger.debug("Find a matched flow!")
                return i
            else:
                if not x :
                    logger.warn("The match of flow is not matched!")
                if not y :
                    logger.warn("The action of flow is not matched!")
                logger.debug(" --------------- Check flow faild ----------------")
                logger.debug(expected_match_set)
                logger.debug(i)
                continue
        return None

    def findFirstDpFlows(self, dut, bridge, flowconfig,tunnel=None):
        self.__initlib(dut)
        offload_flow = self.showDpFlows(dut)

        inport = flowconfig['match']['in_port']
        outport = flowconfig['action']['output']
        inport_info = self.getInterfaceInfo(dut,inport)
        encap = False
        if inport_info['type'] == 'dpdk':
            encap = True
        
        __flow = self.__flowTransForPacket(flowconfig)

        expected_match_set = set(__flow['match'].items())
#        vxlan_decap_match_set = {('in_port', 'patch-tun')}
            
        if 'type' in __flow['action']: 
            action =   __flow['action']['type']
                
        if encap == False:
            if tunnel['type'] == 'vxlan':
                expected_match_set.remove(('in_port', 'patch-tun'))
                expected_match_set.add(('in_port', 'vxlan_sys_4789'))
            if tunnel['type'] == 'geneve':
                expected_match_set.remove(('in_port', 'patch-tun'))
                expected_match_set.add(('in_port', 'genev_sys_6081'))
            if tunnel['type'] == 'gre':
                expected_match_set.remove(('in_port', 'patch-tun'))
                expected_match_set.add(('in_port', 'gre_sys'))                

        __flow['action'].pop("type",None)
        expected_action_set = set(__flow['action'].items())
        for i in offload_flow:
            i = self.flowFraseOfruleToRule(i)
            if 'clone' in i['action'] and 'tnl_push' in i['action']['clone']:
                i['action'].pop('clone',None) 
                offload_action_set = set(i['action'].items())
                offload_action_set.add(('output', outport))
            else:
                offload_action_set = set(i['action'].items())
                
            offload_match_set = set(i['match'].items())
            
            x = expected_match_set.issubset(offload_match_set)
            y = expected_action_set.issubset(offload_action_set)
            if x and y :
                logger.debug("Find a matched offload flow!")
                logger.debug("expected_match: %s "%(expected_match_set))
                logger.debug("actual match: %s "%(offload_match_set))
                logger.debug("expected_action_set: %s "%(expected_action_set))
                logger.debug("offload_action_set: %s "%(offload_action_set))                               
                return i
            else:
                '''
                if not x :
                   logger.warn("The match of offload flow is not matched!")
                if not y :
                    logger.warn("The action of offload flow is not matched!")
                '''
                logger.debug(" --------------- Check flow faild ----------------")
                logger.debug("expected_match: %s "%(expected_match_set))
                logger.debug("actual match: %s "%(offload_match_set))
                logger.debug("expected_action_set: %s "%(expected_action_set))
                logger.debug("offload_action_set: %s "%(offload_action_set))                   
                continue
        return None

    def findFirstTunnelEncapDpFlows(self, dut, bridge, flowconfig, config, tunnel=None):
        self.__initlib(dut)
        offload_flow = self.showDpFlows(dut)

        '''
        set_offload_flow = set(offload_flow)

        set_offload_flow['match'].pop("recirc_id",None)
        set_offload_flow['match'].pop("type",None)
        set_offload_flow['match'].pop("frag",None)
        offload_flow['match'].pop("frag",None)

        last_offload_flow = self.flowFraseOfruleToRule(offload_flow)
        '''
        
        __flow = self.__flowTransForPacket(flowconfig)

        expected_match_set = set(__flow['match'].items())
        vxlan_decap_match_set = {('in_port', 'patch-tun')}

        if 'mod_dl_src' in __flow['action']:
             __flow['action']['mod_dl_src'] = __flow['action']['mod_dl_src'].lower()

        if 'mod_dl_dst' in __flow['action']:
             __flow['action']['mod_dl_dst'] = __flow['action']['mod_dl_dst'].lower()

        if (vxlan_decap_match_set.issubset(expected_match_set)):
            expected_match_set.remove(('in_port', 'patch-tun'))
            expected_match_set.add(('in_port', 'vxlan_sys_4789'))

        __flow['action'].pop("type",None)
        expected_action_set = set(__flow['action'].items())
        for i in offload_flow:
            i = self.flowFraseOfruleToRule(i)
            offload_match_set = set(i['match'].items())
            offload_action_set = ()

            if 'clone' in i['action']:
                if 'tnl_push' in i['action']['clone']:
                    if i['action']['clone']['tnl_push']['tnl_port'] == 'vxlan_sys_4789':
                        offload_action_set = {('output', 'patch-tun')}
                            
#                    offload_action_set = set(i['action'].items())
            x = expected_match_set.issubset(offload_match_set)
            y = expected_action_set.issubset(offload_action_set)
            if x and y :
                logger.debug("Find a matched offload flow!")
                return i
            else:
                '''
                if not x :
                    logger.warn("The match of offload flow is not matched!")
                if not y :
                    logger.warn("The action of offload flow is not matched!")
                '''
                logger.debug(" --------------- Check flow faild ----------------")
                logger.debug(expected_match_set)
                logger.debug(i)
                continue
        logger.debug(" --------------- Check flow offloaded faild ----------------")
        return None



    def checkTunEncapFlowByConfig(self,dut,tx,rx,flowconfig,config):
        self.__initlib(dut)
        bridge = self.getBridgeByPort(dut, flowconfig['match']['in_port'])

        match_id = self.findFirstTunnelEncapDpFlows(dut, bridge, flowconfig, config)
        if match_id == None:
            offload_flow = self.showDpFlows(dut)
            if offload_flow != None:
                logger.debug(offload_flow)
                logger.debug(flowconfig)
            BuiltIn().should_be_true(match_id != None,
                    "[ovs]Can't find flow!")

        n_packet = int(match_id['match']['packets'])
        if 'n_packet_last' in flowconfig:
            n_packet = n_packet - flowconfig['n_packet_last']
        flowconfig['n_packet_last'] = n_packet
        logger.info("[ovs]flow n_packet:%d rx:%d tx:%d"%(n_packet,rx,tx))
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
    
    def OvsIsOffload(self):
        offload  = BuiltIn().get_variable_value('${offload}',False)
        tags = BuiltIn().get_variable_value("@{TEST_TAGS}",list())
        if offload and 'offload' in tags:
            return True
        return False

    def checkDpFlowByConfig(self,dut,tx,rx,flowconfig,tunnel=None):
        self.__initlib(dut)
        bridge = self.getBridgeByPort(dut, flowconfig['match']['in_port'])

        match_id = self.findFirstDpFlows(dut, bridge, flowconfig,tunnel=tunnel)
        if match_id == None:
            offload_flow = self.showDpFlows(dut)
            if offload_flow != None:
                logger.debug(offload_flow)
                logger.debug(flowconfig)
                match_id = self.findFirstDpFlows(dut, bridge, flowconfig,tunnel=tunnel)
        BuiltIn().should_be_true(match_id != None,
                "[ovs]Can't find flow!")
        
        n_dpe_packet = 0
        n_packet = int(match_id['match']['packets'])
        if 'dpe_packets' in match_id['match']:
            n_dpe_packet = int(match_id['match']['dpe_packets'])
            logger.debug("Find dpe_packets info!")
            
        if 'n_dpe_packet_last' in flowconfig:
            n_dpe_packet = n_dpe_packet - flowconfig['n_dpe_packet_last']
        if 'n_packet_last' in flowconfig:
            n_packet = n_packet - flowconfig['n_packet_last']        

        if 'n_dpe_packet_last' in flowconfig:
            flowconfig['n_dpe_packet_last'] = flowconfig['n_dpe_packet_last'] + n_dpe_packet
        else:
            flowconfig['n_dpe_packet_last'] = n_dpe_packet
        if 'n_packet_last' in flowconfig:
            flowconfig['n_packet_last'] = flowconfig['n_packet_last'] + n_packet 
        else:
            flowconfig['n_packet_last'] = n_packet
            
        logger.info("[ovs]flow n_packet:%d n_dpe_packet:%d rx:%d tx:%d"%(n_packet,n_dpe_packet,rx,tx))
        action = flowconfig['action'].get('type','fwd')
        if action == 'drop':
            if int(tx) >= int(n_packet) and (n_packet > 0) and int(rx) == 0:
                logger.debug("[ovs] flow table success")
                return True
            else:
                raise AssertionError("[ovs] flow table failed")        
        else:
            #有杂包，会导致n_packet较大
            #硬件转发的数量应该和收到的n_packet几乎相等，保证中间不断快速转发流量
            BuiltIn().should_be_true((n_dpe_packet == n_packet) and (rx > 2) and (n_dpe_packet > 0), \
                    "[ovs]flow table failed %d != %d"%(int(rx),int(n_packet)))
        '''       
        if 'dpe_packets' in match_id['match']:
            n_packet = int(match_id['match']['dpe_packets'])
            logger.debug("Find dpe_packets info!")
        else :
            n_packet = int(match_id['match']['packets'])
        if 'n_packet_last' in flowconfig:
            n_packet = n_packet - flowconfig['n_packet_last']
        flowconfig['n_packet_last'] = n_packet
        logger.info("[ovs]flow n_packet:%d rx:%d tx:%d"%(n_packet,rx,tx))
        action = flowconfig['action'].get('type','fwd')
        if action == 'drop':
            if int(tx) >= int(n_packet) and (n_packet > 0) and int(rx) == 0:
                logger.debug("[ovs] flow table success")
                return True
            else:
                raise AssertionError("[ovs] flow table failed")
        else:
            #有杂包，会导致n_packet较大
            BuiltIn().should_be_true((int(rx) + 2  > n_packet/2) and (rx > 2) and (n_packet > 0), \
                    "[ovs]flow table failed %d != %d"%(int(rx),int(n_packet)))
        '''
        
    def checkFlowByConfig(self,dut,tx,rx,flowconfig):
        self.__initlib(dut)
        bridge = self.getBridgeByPort(dut, flowconfig['match']['in_port'])

        match_id = self.findFirstFlows(dut, bridge, flowconfig)
        if match_id == None:
            ovs_flow = self.showFlows(dut, bridge)
            logger.debug(ovs_flow)
            logger.debug(flowconfig)
            BuiltIn().should_be_true(match_id != None,
                    "[ovs]Can't find flow!")
        
        n_packet = int(match_id['stats']['n_packets'])
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
            
    def flowCheckPacketTunlHead(self,dut,pktinfo=None,tun_info=None):
        tun_type = tun_info['type'].upper()
        tun = pktinfo.payload[Ether].underlayer
         #检查字段是否配置，并检查报文结果
        check_error = lambda x,y : \
            True if x.upper() != y.upper() else False                
            
        if tun_type == 'NVGRE':
            tun_type = 'GRE'
            
        if tun.name != tun_type:
            logger.warn("tun.name = %s" %tun.name)
            logger.warn("tun_type = %s" %tun_type)            
            return False                     
        if check_error(tun_info['knl_mac'], pktinfo.src) :
            logger.warn("tun_info['knl_mac'] = %s" %tun_info['knl_mac'])
            logger.warn("pktinfo.src = %s" %pktinfo.src)
            return False
        if check_error(tun_info['remote_ip'], pktinfo.payload.dst) :
            logger.warn("tun_info['remote_ip'] = %s" %tun_info['remote_ip'])
            logger.warn("pktinfo.payload.dst = %s" %pktinfo.payload.dst)            
            return False  
        if check_error(tun_info['local_ip'], pktinfo.payload.src) :
            logger.warn("tun_info['local_ip'] = %s" %tun_info['local_ip'])
            logger.warn("pktinfo.payload.src = %s" %pktinfo.payload.src)            
            return False 
        
        if tun_type == 'VXLAN' or tun_type == 'GENEVE':
            if check_error(tun_info['out_key'], str(tun.vni)) :
                logger.warn("tun_info['out_key'] = %s" %tun_info['out_key'])
                logger.warn("tun.vni = %s" %str(tun.vni))                  
                return False  
            
        if tun_type == 'GRE': 
            if check_error(tun_info['out_key'], str(tun.key)) :
                logger.warn("tun_info['out_key'] = %s" %tun_info['out_key'])
                logger.warn("tun.key = %s" %str(tun.key))                 
                return False
            
        if tun_type == 'NVGRE':    
            if tun.chksum_present != 0 :
                logger.warn("tun.chksum_present = %s" %str(tun.chksum_present))
                return False
            if tun.key_present != 1 :
                logger.warn("tun.key_present = %s" %str(tun.key_present))
                return False
            if tun.seqnum_present != 0 :
                logger.warn("tun.seqnum_present = %s" %str(tun.seqnum_present))
                return False
            if tun.proto != 0x6558 :
                logger.warn("tun.proto = %s" %str(tun.proto))
                return False
        logger.info("flowCheckPacketTunlHead success!!!")                 
        return True 
        
    def flowCheckPacket(self,dut,pkt,flow,encap=False,decap=False,tun_info=None):
        '''检查报文和流是否匹配
        '''
        self.__initlib(dut)
        action = flow['action']
        match = flow['match']
        #trex工具发包
        pktinfo = Ether(pkt)
        #renix工具发包
        #pktinfo = pkt
        
        head = pktinfo
        tun = None
        if Ether in pktinfo.payload:
            tun = pktinfo.payload[Ether].underlayer
        if encap : #校验封装头
            if tun == None and pktinfo.payload[Ether].type != 0x0806: 
                logger.error("not tunnel pkt!")
                return False
            check_tun = self.flowCheckPacketTunlHead(dut, pktinfo, tun_info)
            if check_tun == False:
                logger.error("check tunnel fail!")
                return False   
            
            head = tun.payload
        if decap : #校验解封装
            if tun != None: return False
        
        #检查字段是否配置，并检查报文结果
        check_error = lambda x,y : \
            True if x in action and action[x].upper() != y else False

        #logger.info("head.src = %s"%str(head.src))
        #logger.info("head.dst = %s"%str(head.dst))
        '''
        if 'mod_dl_src' in action:
            logger.info("action['mod_dl_src'] = %s" %action['mod_dl_src'])
            logger.info("head.src = %s"%str(head.src))

        if 'mod_dl_dst' in action:
            logger.info("action['mod_dl_dst'] = %s" %action['mod_dl_dst'])
            logger.info("head.dst = %s"%str(head.dst))
        '''

        #检查Ether层修改
        if check_error('mod_dl_src', head.src.upper()) :
            logger.info("action['mod_dl_src'] = %s" %action['mod_dl_src'])
            logger.info("pkt['mod_dl_src'] = %s" %head.src)
            return False
        if check_error('mod_dl_dst', head.dst.upper()) :
            logger.info("action['mod_dl_dst'] = %s" %action['mod_dl_dst'])
            logger.info("pkt['mod_dl_dst'] = %s" %head.dst)
            return False
        
        #检查VLAN修改
        vlankey = ['mod_vlan_vid','mod_vlan_pcp']
        
        if len([k for k in vlankey if k in action]) > 0:
            if type(head.payload) not in [Dot1Q] : return False
                  
            if check_error('mod_vlan_vid', str(head.payload.vlan)) :
                logger.info("action['mod_vlan_vid'] = %s" %action['mod_vlan_vid'])
                logger.info("pkt['mod_vlan_vid'] = %s" %head.payload.id)
                return False        
            if check_error('mod_vlan_pcp', str(head.payload.prio)) :
                logger.info("action['mod_vlan_pcp'] = %s" %action['mod_vlan_pcp'])
                logger.info("pkt['mod_vlan_pcp'] = %s" %head.payload.prio)
                return False  
        
        #检查L3层修改
        if type(head.payload) in [Dot1Q] : payload = head.payload.payload
        else: payload = head.payload
                 
        l3key = ['mod_nw_src','mod_nw_dst','mod_nw_ttl','dec_ttl','mod_nw_tos']
        l4key = ['mod_tp_src','mod_tp_dst']

        #logger.info("head.payload.src = %s"%str(head.payload.src))
        #logger.info("head.payload.dst = %s"%str(head.payload.dst))

        '''
        if 'mod_nw_src' in action:
            logger.info("action['mod_nw_src'] = %s" %action['mod_nw_src'])
            logger.info("head.payload.src = %s"%str(head.payload.src))

        if 'mod_nw_dst' in action:
            logger.info("action['mod_nw_dst'] = %s" %action['mod_nw_dst'])
            logger.info("head.payload.dst = %s"%str(head.payload.dst))

        if 'mod_tp_src' in action:
            logger.info("action['mod_tp_src'] = %s" %action['mod_tp_src'])

        if 'mod_tp_dst' in action:
            logger.info("action['mod_tp_dst'] = %s" %action['mod_tp_dst'])
        '''
        if len([k for k in l3key if k in action]) > 0:
            if type(payload) not in [IP,IPv6] : return False         
            #logger.error("pkt['dec_ttl'] = %s" %payload.ttl)
            ttl = self.getPktTTL(dut,flow)
                            
            if check_error('mod_nw_src', payload.src) :
                logger.info("action['mod_nw_src'] = %s" %action['mod_nw_src'])
                logger.info("pkt['mod_nw_src'] = %s" %payload.src)
                return False
            if check_error('mod_nw_dst', payload.dst) :
                logger.info("action['mod_nw_dst'] = %s" %action['mod_nw_dst'])
                logger.info("pkt['mod_nw_dst'] = %s" %payload.dst)
                return False
                       
            if type(payload) == IP:
                if (payload.ttl != ttl):
                    logger.info("pkt['ttl'] = %s" %payload.ttl)
                    return False
                if check_error('mod_nw_tos', str(payload.tos)) :
                    logger.info("action['mod_nw_tos'] = %s" %action['mod_nw_tos'])
                    logger.info("pkt['mod_nw_tos'] = %s" %payload.tos) 
                    return False                                       
            if type(payload) == IPv6:
                if  (payload.hlim != ttl):
                    logger.info("pkt['ttl'] = %s" %payload.hlim) 
                    return False
                if check_error('mod_nw_tos', str(payload.tc)) :
                    logger.info("action['mod_nw_tos'] = %s" %action['mod_nw_tos'])
                    logger.info("pkt['mod_nw_tos'] = %s" %payload.tc) 
                    return False                
                 
        #检查L4层修改
        if len([k for k in l4key if k in action]) > 0:
            headl4 = payload.payload
            if type(headl4) not in [UDP,TCP,SCTP] : return False
   
            if check_error('mod_tp_src', str(headl4.sport)) :
                logger.info("action['mod_tp_src'] = %s" %action['mod_tp_src'])
                logger.info("pkt['mod_tp_src'] = %s" %headl4.sport)
                return False
            if check_error('mod_tp_dst', str(headl4.dport)) :
                logger.info("action['mod_tp_dst'] = %s" %action['mod_tp_dst'])
                logger.info("pkt['mod_tp_dst'] = %s" %headl4.dport)
                return False
        return True

    def get_current_time(self):
        tm = time.time()
        timestamp = str(tm).split('.')[0]
        return timestamp

    def convert(self, time_string):
        time_string = str(time_string).strip()
        try:
            time_strp = time.strptime(time_string, '%Y/%m/%d %H:%M:%S.%f')

        except ValueError:
            time_strp = time.strptime(time_string, '%Y/%m/%d %H:%M:%S')
        return int(time.mktime(time_strp))

    def convert_mtime(self, time_string):
        time_string = str(time_string).strip()
        try:
            sec1 = str(time_string).split('.')[1]
            if len(sec1) > 6:
                time_string = time_string[:-(len(sec1)-6)]
            sec2 = int(sec1) / 10**len(str(sec1))
            time_strp = time.strptime(time_string, '%Y/%m/%d %H:%M:%S.%f')
            microtimestamp = int((time.mktime(time_strp) + sec2)*1000)
            return microtimestamp
        except IndexError:
            time_strp = time.strptime(time_string, '%Y/%m/%d %H:%M:%S')
            microtimestamp = int(time.mktime(time_strp) * 1000)
            return microtimestamp

    def get_file_time(self, file_name):
        # _get_file_time asserts file_name containing legal time string, otherwise will raise exception
        ch_list = [str(i) for i in range(10)] + ['-']
        time_str = ''
        for ch in file_name:
            if ch in ch_list:
                time_str += ch
        assert len(time_str) == 15
        return int(time.mktime(time.strptime(time_str, '%Y%m%d-%H%M%S')))

    def check_between_time(self, file_name, keyword, start_time_stamp, end_time_stamp=0, match_count=1,
                       search_tar=True, rtnTimeStamp=False, assertFlag=False):
        if end_time_stamp == 0:
            end_time_stamp=int(time.time())+1
        else:
            end_time_stamp = int(end_time_stamp)
        start_time_stamp = int(start_time_stamp)
        line_time = 0
        line_mtime = 0

        total_count = 0
        if isinstance(keyword,list):
            target = ''
            for k in keyword:
                k = k + ".*"
                target += k
            keyword = target
        print("should Match %s" %keyword)
        log_folder = '/home/jaguar/test/vxlan_test'
        file_name = os.path.basename(file_name)
        #if file_name == 'TmFileScan.log':
        #    file_name = ConfigIDCE.getCorespFilePath(log_mode, 7)
        logger.info("check %s in file %s/%s"%(keyword, log_folder, file_name))
        cmd_keyword = 'zgrep'

        count = 0
        pflag = 0
        with open(os.path.join(log_folder, file_name), errors='replace') as fin:
            content = fin.readlines()
            line_time_str=''
            for line in content:
                #line_time_str = line[:line.find('(')].strip()
                #line_time_str = line.strip()
                try:
                    if re.search(keyword, line):
                        #line_time = self.convert(line_time_str)
                        count += 1
                        logger.info("Found in active log: %s" % line)
                except ValueError:
                    pass
            #logger.info("last timestamp in log is %d" % (self.convert_mtime(line_time_str)))
        if count == 0:
            logger.info("Not found in active log.")
        total_count += count

        return total_count

    def run_sys_command(self, command):
        """ run sys command and save log to sys_command.log
        @Param:

        command:    Command used to call

        Return:
            
        If now error occur, it will return True
        """
        logger.info("Run system command Cmdline: %s." %command)
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, encoding='utf8')
        except UnicodeEncodeError as e:
            print('Unicode Error, may contails chinese, use gbk to encode command')
            process = subprocess.Popen(command.encode("gbk"), shell=True, stdout=subprocess.PIPE, encoding='utf8')
        stdoutmsg = process.stdout.read()
        log_file_path = '/home/jaguar/test/testlog/sys_command.log'
        log_file = open(log_file_path, 'w')
        log_file.write(stdoutmsg)
        log_file.close()
        logger.info("Output:\n%s" % stdoutmsg)
        if "Can\'t open file" in stdoutmsg:
            logger.error("Failed to call run command and save log.")
            return False
        return True
        
    def setBridgeIpAddrBackup(self,dut,bridge,name,config):
        '''配置网桥IP地址
        ip addr add 192.168.239.2/24 dev br-ext
        ip link set br-ext up
        '''
        self.__initlib(dut)
        t = config.get("type","dpdk")
        if t != 'vxlan' and t != 'geneve':
            return

        mac = self.getInterfaceMac(dut, 'dpdk0')
        if 'options' in config:
            self.ovsvxlantable[dut] = copy.deepcopy(config['options'])
            for k,v in  config['options'].items():
                if k == 'local_ip':
                    #self.dutlib.process(dut,'ovs-vsctl set Bridge br-ext other_config:hwaddr="%s"'% \
                    #            (mac))
                    #self.dutlib.process(dut,'ovs-vsctl set Bridge br-ext other_config:hwaddr=a2:d7:57:2e:9b:4e')
                    #self.dutlib.process(dut,'ip addr add %s/24 dev br-ext'% \
                    #            (v))
                    #self.dutlib.process(dut,'ip link set br-ext up'% \
                    #            ())
                    self.dutlib.process(dut,'ovs-vsctl set Bridge br-int other_config:hwaddr="%s"'% \
                                (mac))
                    self.dutlib.process(dut,'ip addr add %s/24 dev br-int'% \
                                (v))
                    self.dutlib.process(dut,'ip link set br-int up'% \
                                ())

    def setBridgeIpAddr(self,dut,bridge,config):
        '''配置网桥IP地址
        ip addr add 192.168.239.2/24 dev br-ext
        ip link set br-ext up
        '''
        self.__initlib(dut)
        mac = self.getInterfaceMac(dut, bridge)
      
        self.dutlib.process(dut,'ovs-vsctl set Bridge %s other_config:hwaddr="%s"'% \
                                (bridge,mac))
       
        self.dutlib.process(dut,'ip addr add %s dev %s'%(config['ip'],bridge))
        self.dutlib.process(dut,'ip link set %s up'%bridge)

if __name__ == '__main__':
    ovslib = Ovs()
    idict = dict()
    idict = ovslib.flowFraseDpflowTOdict("recirc_id(0),in_port(dpdk0),packet_type(ns=0,id=0),eth(src=00:01:00:00:00:02),eth_type(0x0806), packets:2, bytes:120, used:0.368s, actions:set(eth(src=00:01:00:00:00:04)),clone(tnl_push(tnl_port(vxlan_sys_4789),header(size=50,type=4,eth(dst=00:01:00:00:00:03,src=08:00:27:f9:11:96,dl_type=0x0800),ipv4(src=192.168.2.55,dst=192.168.2.10,proto=17,tos=0,ttl=64,frag=0x4000),udp(src=0,dst=4789,csum=0x0),vxlan(flags=0x8000000,vni=0x64)),out_port(br-ext)),dpdk1)")
    pprint(idict)
