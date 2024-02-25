#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket , traceback
import os, sys, time, re, copy
import struct, binascii

__path = os.path.realpath(os.path.join(__file__,'..','..')) 
if __path not in sys.path:sys.path.append(__path)

from renix_py_api.renix import *
from scapy.all import *

from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

import IPy
import AppBaseLib as _baselib

''' 流配置接口，以OVS的配置为基准进行配置：
        https://www.man7.org/linux/man-pages/man7/ovs-fields.7.html
'''


''' for TestCenter
from TestCenter.TestCenter import TestCenter
from TestCenter.TestCenterShell import TestCenterShell
from TestCenter.TclInter import root
'''

'''

NTX : CreateTestPort -PortLocation 101/5 -PortName ::CHASSIS1/1/5 -PortType ETHERNET -object CHASSIS1
NTX : CreateHost -HostName host1 -MacAddr 00:01:00:00:00:01 -Ipv4Addr 31.1.1.2 -Ipv4Mask 24 -Ipv4sutAddr 31.1.1.1 -Arpd enable -FlagPing enable -object CHASSIS1/1/5
NTX : CreateSubInt -SubIntName cha1Vlan -object CHASSIS1/1/5
NTX : ConfigPort -VlanTag 0x8100 -VlanId 1 -object cha1Vlan
NTX : CreateHost -HostName host1Vlan -MacAddr 00:01:00:00:00:03 -Ipv4Addr 132.1.1.2 -Ipv4Mask 24 -Ipv4sutAddr 132.1.1.1 -Arpd enable -FlagPing enable -object cha1Vlan
NTX : CreateTraffic -TrafficName port1Traffic -object CHASSIS1/1/5
NTX : CreateStaEngine -StaEngineName port1StaEngine -StaType Statistics -object ::CHASSIS1/1/5
NTX : SendArpRequest -object host1
NTX : SendArpRequest -object host1Vlan
NTX : CreateProfile -Name port1ProfileOut -Type Burst -TrafficLoad 10 -TrafficLoadUnit fps -FrameNum 6 -object port1Traffic
NTX : CreateStream -StreamName outStream -ProfileName port1ProfileOut -framelen 100 -EthDst 001f.5310.521c -EthSrc 00:01:00:00:00:01 -L2 Ethernet -L3 IPv4 -IpSrcAddr 31.1.1.2 -IpSrcMask 255.255.255.0 -IpSrcAddrMode increment -IpSrcAddrCount 1 -IpSrcAddrStep 0.0.0.1 -IpDstAddr 132.1.1.2 -IpDstMask 255.255.255.0 -IpDstAddrMode increment -IpDstAddrCount 1 -IpDstAddrStep 0.0.0.1 -IpProtocolType udp -L4 UDP -UdpSrcPort 1000 -UdpSrcPortMode increment -UdpSrcStep 1 -UdpSrcPortCount 1 -UdpDstPort 1000 -UdpDstPortMode increment -UdpDstPortStep 1 -UdpDstPortCount 1 -object port1Traffic
NTX : StartTraffic -ProfileList port1ProfileOut -object CHASSIS1/1/5
NTX : StopTraffic -ProfileList port1ProfileOut -object CHASSIS1/1/5
NTX : GetPortStats -TxSignature txframe -RxSignature rxframe -object port1StaEngine
NTX : GetStreamStats -StreamName outStream -TxFrames txframe -RxFrames rxframe -object port1StaEngine
NTX : CreateProfile -Name port1ProfileIn -Type Burst -TrafficLoad 10 -TrafficLoadUnit fps -FrameNum 6 -object port1Traffic
NTX : CreateStream -StreamName inStream -ProfileName port1ProfileIn -framelen 100 -EthDst 001f.5310.521c -EthSrc 00:01:00:00:00:03 -L2 Ethernet_Vlan -vlanId 1 -L3 IPv4 -IpSrcAddr 132.1.1.2 -IpSrcMask 255.255.255.0 -IpSrcAddrMode increment -IpSrcAddrCount 1 -IpSrcAddrStep 0.0.0.1 -IpDstAddr 10.1.1.1 -IpDstMask 255.255.255.0 -IpDstAddrMode increment -IpDstAddrCount 1 -IpDstAddrStep 0.0.0.1 -IpProtocolType udp -L4 UDP -UdpSrcPort 1000 -UdpSrcPortMode increment -UdpSrcStep 1 -UdpSrcPortCount 1 -UdpDstPort 2112 -UdpDstPortMode increment -UdpDstPortStep 1 -UdpDstPortCount 1 -object port1Traffic
NTX : CreateStream -StreamName inStreamAbnormal -ProfileName port1ProfileIn -framelen 100 -EthDst 001f.5310.521c -EthSrc 00:01:00:00:00:03 -L2 Ethernet_Vlan -vlanId 1 -L3 IPv4 -IpSrcAddr 1.1.1.1 -IpSrcMask 255.255.255.0 -IpSrcAddrMode increment -IpSrcAddrCount 1 -IpSrcAddrStep 0.0.0.1 -IpDstAddr 10.1.1.1 -IpDstMask 255.255.255.0 -IpDstAddrMode increment -IpDstAddrCount 1 -IpDstAddrStep 0.0.0.1 -IpProtocolType udp -L4 UDP -UdpSrcPort 1000 -UdpSrcPortMode increment -UdpSrcStep 1 -UdpSrcPortCount 1 -UdpDstPort 2112 -UdpDstPortMode increment -UdpDstPortStep 1 -UdpDstPortCount 1 -object port1Traffic
NTX : StartTraffic -ProfileList port1ProfileIn -object CHASSIS1/1/5
NTX : StopTraffic -ProfileList port1ProfileIn -object CHASSIS1/1/5
NTX : GetPortStats -TxSignature txframe -RxSignature rxframe -object port1StaEngine
NTX : GetStreamStats -StreamName inStream -TxFrames txframe -RxFrames rxframe -object port1StaEngine
NTX : GetPortStats -TxSignature txframe -RxSignature rxframe -object port1StaEngine

'''

class Tester(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ins = None
    socket = None
    ip     = None
    port   = 9090
    defaulttester = 'CHASSIS1'
    vxlanHeadLen = 50
    def __init__(self):
        #配置信息
        self.ins = {
            'port'   :dict(),
            'subint' :dict(),
            'host'   :{},
            'traffic':{},
            'profile':{},
            'engin' : {}
            }
        self.shell = None

    def __trex_testerConnect(self, ip):
        '''连接测试仪
        
        目前仅支持一个测试仪
        '''
        logger.info("Connect tester %s"%ip)
        initialize()
        chassis = ConnectChassisCommand(ip)
        chassis.execute()
        self.sys_entry = get_sys_entry()
        self.shell = self.sys_entry
        return True

    def __trex_hostconfig(self,config):
        ''' 从trex的port上获取信息进行填充
            {'ether': {'dst': '0a:00:27:00:00:12',
                    'src': '08:00:27:00:f6:06',
                    'state': 'configured'},
            'ipv4': {'dst': '192.168.136.1',
                    'src': '192.168.136.100',
                    'state': 'resolved'},
            'ipv6': {'enabled': False}}
        '''
        value = copy.deepcopy(config)
        tport = self.__trex_getPort(config['object'])
        port_layer = self.shell.get_port(tport).get_layer_cfg()
        if ('MacAddr' not in config) or ('auto' in  config['MacAddr']):
            value['MacAddr'] = port_layer['ether']['src']
        if ('Ipv4Addr' not in config) or ('auto.' in  config['Ipv4Addr']):
            ipvar = Ipv4(port_layer['ipv4']['src']).V()
            ipvar[3] = int(config['Ipv4Addr'][5:])
            value['Ipv4Addr'] = str(Ipv4(ipvar))
        if ('Ipv4Mask' not in config) or ('auto' in str(config['Ipv4Mask'])):
            value['Ipv4Mask'] = 24
        if ('Ipv4sutAddr' not in config) or ('auto' in  config['Ipv4sutAddr']):
            value['Ipv4sutAddr'] = port_layer['ipv4']['dst']
        return value

    def __trex_emu_profile(self):
        '''根据host创建emu的profile,并加载
            'host1': {
                    'object' : 'port1',
                    'MacAddr'  : 'auto',
                    'Ipv4Addr' : 'auto.101', #@ip4.24@inprefix1.inipv42
                    'Ipv4Mask' : '24',
                    'Ipv4sutAddr' :'auto',#@ip4.24@inprefix1.inipv41
                    'Arpd' : 'enable',
                    'FlagPing' :'enable',
                    'Ipv6Addr' :'auto',
                    'Ipv6Mask' :'64',
                    'Ipv6sutAddr' : 'auto'
                    },
        '''
        client_dict = dict()
        for k,v in self.ins['host'].items():
            port = v['object']
            client_dict.setdefault(port,list())
            mac = Mac(v['MacAddr'])
            ipv4 = Ipv4(v['Ipv4Addr'])
            ipv4_dg = Ipv4(v['Ipv4sutAddr'])
            emu_client = EMUClientObj(mac = mac.V(),
                                    ipv4 = ipv4.V(),
                                    ipv4_dg = ipv4_dg.V(),
                                    plugs = {'arp': {'enable': True},'icmp':{}})
            client_dict[port].append(emu_client)
        ns_list = list()
        for k,v in client_dict.items():
            if len(v) <= 0: continue
            tport = self.__trex_getPort(k)
            ns_key = EMUNamespaceKey(vport = tport)
            emu_ns = EMUNamespaceObj(ns_key  = ns_key,
                         clients = v)
            ns_list.append(emu_ns)
        
        profile = EMUProfile(ns = ns_list, def_ns_plugs = {'arp': {'enable': True},'icmp':{},'ipv6':{}})
        self.emu.load_profile(profile = profile)

    def __trex_getHardwarePort(self,tport):
        self.sys_entry.get()
        hardware_manager = self.sys_entry.get_children('HardwareManager')[0]
        hardware_chassis = hardware_manager.get_children('HardwareChassis')[0]
        for hardwarecard in hardware_chassis.get_children('HardwareCard'):
            ports = hardwarecard.get_children()
            for i in ports:
                if i.Location != tport.Location: continue
                return i
        return None

    def __trex_createPort(self, name, config):
        location = config.get("PortLocation")
        location_real = "//%s/%s"%(self.ip,location)
        tport = Port(upper=self.sys_entry, Location=location_real)
        port_h = self.__trex_getHardwarePort(tport)
        if port_h.ReserveState != EnumReserveState.AVAILABLE:
            if port_h.ReserveState == EnumReserveState.RESERVED:
                raise AssertionError("Port %s State: %s(%s)"%(location_real,port_h.ReserveState.name,port_h.OwnerId))
            else:
                raise AssertionError("Port %s State: %s"%(location_real,port_h.ReserveState.name))
        BringPortsOnlineCommand(PortList=[tport.handle]).execute()
        if 'FIBER' in tport.PortCfgType.name:  #直连host需要配置FEC为0
            ConfigurePortsCommand(PortList=tport.handle, FecType=0,DataPathMode=1).execute()

        #配置混杂，保证host的仿真
        self.ins['port'][name] = copy.deepcopy(config)
        self.ins['port'][name]['realname']  = name
        self.ins['port'][name]['trexport']  = tport
        return True

    def __trex_ClearPort(self,name,config=None):
        config = self.ins['port'][name]
        location = config.get("PortLocation")
        port = int(location.split("/")[1])
        self.shell.reset(ports=port)
        self.ins['port'].pop(name)

    def __trex_resetPort(self,name):
        portinfo = self.ins['port'][name]
        config = copy.deepcopy(portinfo)
        return self.__trex_createPort(name,config)

    def __trex_getPortList(self):
        portlist = list()
        for v in self.ins['port'].values():
            if 'trexport' in v:
                portlist.append(v['trexport'])
        return portlist

    def __trex_getPort(self,portname):
        config = self.ins['port'][portname]
        if config !=None :
            port = config.get('trexport',None)
            return port
        return None

    def __trex_getStreamStateId(self,name):
        profile = self.__getStreamProfile(name)
        streamobj = self.ins['profile'][profile]['stream'][name]
        stream = streamobj['trex_stream']
        return stream

    def __trex_edit(self,config,ilist=None):
        keymap = {
            "eth_src":'ethernetII_1.sourceMacAdd',
            "eth_dst":'ethernetII_1.destMacAdd',
            "eth_type":'ethernetII_1.protocolType',
            'ip_src':'ipv4_1.source',
            'ip_dst':'ipv4_1.destination'
        }
        ret = ""
        if ilist == None:
            ilist = config.keys()

        for i in ilist:
            if i not in keymap: continue
            ret += " %s=%s"%(keymap[i],str(config[i]))
        ret = ret.strip()
        return ret

    def __trex_getUnit(self,profile,stream):
        unitmap = {
            'fps' : EnumFrameLoadUnit.FRAME_PER_SEC,
            'persent': EnumFrameLoadUnit.PERCENT
        }
        unit = profile.get('TrafficLoadUnit','fps')
        unit = stream.get('StreamLoadUnit',unit)
        unit = unitmap.get(unit,'pps')
        load = profile.get('TrafficLoad',"1")
        load = int(stream.get('StreamLoad',load))
        return unit,load

    def __trex_setUnit(self,profile,stream):
        unitmap = {
            'fps' : EnumFrameLoadUnit.FRAME_PER_SEC,
            'persent': EnumFrameLoadUnit.PERCENT
        }
        unit ,load = self.__trex_getUnit(profile,stream)
        tstream = stream['trex_stream']
        stream_template_load_profile = tstream.get_children('StreamTemplateLoadProfile')[0]
        stream_template_load_profile.edit(Unit=unit)
        stream_template_load_profile.edit(Rate=int(load))
        

    def __trex_createStreamByScapy(self,port,profileName,streamName,config):
        profile = self.ins['profile'][profileName]['config']
        l = int(config.get("framelen",128))
        tport = self.__trex_getPort(port)
        self.__trex_checkStreamMode(tport)
        stream = StreamTemplate(upper=tport)

        L4Type = config.get('L4',"").lower()
        L3Type = config.get('L3',"").lower()
        L2Type = config.get('L2',"").lower()

        base_pkt = None
        if L2Type == 'Ethernet':
            L2Pkt = Ether(src=config['eth_src'],dst=config['eth_dst'])
        elif L2Type == 'Ethernet_vlan':
            eth = Ether(src=config['eth_src'],dst=config['eth_dst'])
            vlan = Dot1Q()
            if 'vlan_vid' in config : vlan.vlan = int(config['vlan_vid'])
            if 'vlan_cfi' in config : vlan.id   = int(config['vlan_cfi'])
            if 'vlan_pcp' in config : vlan.prio = int(config['vlan_pcp'])
            L2Pkt = eth/vlan
        elif L2Type == 'Ethernet_mpls':
            eth = Ether(src=config['eth_src'],dst=config['eth_dst'])
            mpls = MPLS(label=int(config['mpls_label']),cos=int(config['mpls_tc']),
                        s=int(config['mpls_bos']),ttl=int(config['mpls_ttl']))
            L2Pkt = eth/mpls
        else:
            eth = Ether()

        if L3Type == 'ipv4':
            L3Pkt = IP(src=config['ip_src'],dst=config['ip_dst'], proto=int(config['nw_proto']))
            if 'nw_tos' in config   : L3Pkt.tos = int(config['nw_tos'])
            if 'nw_ttl' in config   : L3Pkt.ttl = int(config['nw_ttl'])
            if 'nw_frag' in config  : L3Pkt.flags = int(config['nw_frag'])

        elif L3Type == 'ipv6':
            L3Pkt = IPv6(src=config['ipv6_src'],dst=config['ipv6_dst'],hlim=int(config['nw_ttl']),tc=int(config['nw_tos']),nh=int(config['nw_proto']))
        elif L3Type == 'arp':
            L3Pkt = ARP()
            L3Pkt.op = int(config['arp_op'])
            L3Pkt.hwsrc = config['arp_sha']
            L3Pkt.hwdst = config['arp_tha']
            L3Pkt.psrc = config['arp_spa']
            L3Pkt.pdst = config['arp_tpa']
            #(op=int(arpdata['arp_op']),hwsrc=arpdata['arp_sha'],hwdst=arpdata['arp_tha'],psrc=arpdata['arp_spa'],pdst=arpdata['arp_tpa'])
        else:
            L3Pkt = ''

        if L4Type == 'udp':
            L4Pkt = UDP(sport=config['udp_src'],dport=config['udp_dst'])
        elif L4Type == 'tcp':
            L4Pkt = TCP(sport=config['tcp_src'],dport=config['tcp_dst'],flags=config['tcp_flags'])
        elif L4Type == 'sctp':
            L4Pkt = SCTP(sport=config['sctp_src'],dport=config['sctp_dst'])
        elif L4Type == 'icmp':
            L4Pkt = ICMP(type=int(config['icmp_type']),code=int(config['icmp_code']))
        elif L4Type == 'icmpv6':
            L4Pkt = self.__getIcmp6Pkt(config)
        else:
            L4Pkt = ''
        
        base_pkt = L2Pkt
        if L3Pkt != '':
            base_pkt = base_pkt/L3Pkt
        if L4Pkt != '':
            base_pkt = base_pkt/L4Pkt

        if 'tun_type' in config:
            base_pkt,l = self.__trex_addTunlHead(config, l, base_pkt)

        pad = (l-len(base_pkt))*"x"
        base_pkt = base_pkt/pad
        logger.info(linehexdump(base_pkt,onlyhex=1,dump=1))

        unit,load = self.__trex_getUnit(profile,config)

        file = os.path.join(os.getenv('TEMP'),"tester_renix.pcap")
        wrpcap(file,base_pkt)
        CreateStreamFromPcapCommand(PortList=tport.handle,FilePath=file,RxPortList=tlist).execute()
        
        stream = tport.get_children('StreamTemplate')[0]
        stream_template_load_profile = stream.get_children('StreamTemplateLoadProfile')[0]
        stream_template_load_profile.edit(Unit=unit)
        stream_template_load_profile.edit(Rate=int(load))

        config['trex_stream'] = stream

        return True

    '''
	#该方式__trex_edit映射待补充，暂不使用
    def __trex_createStream(self,port,profileName,streamName,config):
        profile = self.ins['profile'][profileName]['config']
        l = int(config.get("framelen",128))
        tport = self.__trex_getPort(port)
        self.__trex_checkStreamMode(tport)
        stream = StreamTemplate(upper=tport)

        L4Type = config.get('L4',"").lower()
        L3Type = config.get('L3',"").lower()
        L2Type = config.get('L2',"").lower()

        base_pkt = None
        if L2Type == 'ethernet':
            L2Pkt = self.__trex_edit(config,['eth_src','eth_dst'])
        elif L2Type == 'Ethernet_vlan':
            eth = self.__trex_edit(config,['eth_src','eth_dst'])
            vlan = Dot1Q()
            if 'vlan_vid' in config : vlan.vlan = int(config['vlan_vid'])
            if 'vlan_cfi' in config : vlan.id   = int(config['vlan_cfi'])
            if 'vlan_pcp' in config : vlan.prio = int(config['vlan_pcp'])
            L2Pkt = eth + " " + vlan
        elif L2Type == 'ethernet_mpls':
            eth = self.__trex_edit(config,['eth_src','eth_dst'])
            mpls = self.__trex_edit(config,['mpls_label','mpls_tc','mpls_bos','mpls_ttl'])
            L2Pkt = eth + " " + mpls
        else:
            eth = ''

        if L3Type == 'ipv4':
            L3Pkt = self.__trex_edit(config,['ip_src','ip_dst', 'nw_proto'])
            if 'nw_tos' in config   : L3Pkt += " " + self.__trex_edit(config,['nw_tos'])
            if 'nw_ttl' in config   : L3Pkt += " " + self.__trex_edit(config,['nw_ttl'])
            if 'nw_frag' in config  : L3Pkt += " " + self.__trex_edit(config,['nw_frag'])

        elif L3Type == 'ipv6':
            L3Pkt =  self.__trex_edit(config,['ipv6_src','ipv6_dst','nw_ttl','nw_tos','nw_proto'])
        elif L3Type == 'arp':
            L3Pkt = self.__trex_edit(config,['arp_op','arp_sha','arp_tha','arp_spa','arp_tpa'])
        else:
            L3Pkt = ''

        if L4Type == 'udp':
            L4Pkt = self.__trex_edit(config,['udp_src','udp_dst'])
        elif L4Type == 'tcp':
            L4Pkt = self.__trex_edit(config,['tcp_src','tcp_dst','tcp_flags'])
        elif L4Type == 'sctp':
            L4Pkt = self.__trex_edit(config,['sctp_src','sctp_dst'])
        elif L4Type == 'icmp':
            L4Pkt = self.__trex_edit(config,['icmp_type','icmp_code'])
        elif L4Type == 'icmpv6':
            L4Pkt = self.__getIcmp6Pkt(config)
        else:
            L4Pkt = ''
        
        base_pkt = L2Pkt
        if L3Pkt != '':
            base_pkt = base_pkt + " " + L3Pkt
        if L4Pkt != '':
            base_pkt = base_pkt + " " + L4Pkt

        if 'tun_type' in config:
            base_pkt,l = self.__trex_addTunlHead(config, l, base_pkt)

        #pad = (l-len(base_pkt))*"x"
        #base_pkt = base_pkt/pad
        logger.info(linehexdump(base_pkt,onlyhex=1,dump=1))

        file = os.path.join(os.getenv('TEMP'),"tester_renix.pcap")
        wrpcap(file,base_pkt)

        stream.edit(FixedLength=l)
        UpdateHeaderCommand(Stream=stream.handle,Parameter= base_pkt).execute()
        
        unit,load = self.__trex_getUnit(profile,config)
        stream_template_load_profile = stream.get_children('StreamTemplateLoadProfile')[0]
        stream_template_load_profile.edit(Unit=unit)
        stream_template_load_profile.edit(Rate=int(load))
        
        config['trex_stream'] = stream
        return
    '''
    def __trex_createStream(self,port,profileName,streamName,config):
        profile = self.ins['profile'][profileName]['config']
        l = int(config.get("framelen",128))
        tport = self.__trex_getPort(port)
        tportlist = self.__trex_getPortList()
        tlist = [t.handle for t in tportlist]
        self.__trex_checkStreamMode(tport)
        stream = StreamTemplate(upper=tport)
        unitmap = {
            'fps' : 'pps'
        }
        L4Type = config['L4']
        L3Type = config['L3']
        L2Type = config['L2']

        base_pkt = None
        if L2Type == 'Ethernet':
            L2Pkt = Ether(src=config['eth_src'],dst=config['eth_dst'])
        elif L2Type == 'Ethernet_vlan':
            eth = Ether(src=config['eth_src'],dst=config['eth_dst'])
            vlan = Dot1Q()
            if 'vlan_vid' in config : vlan.vlan = int(config['vlan_vid'])
            if 'vlan_cfi' in config : vlan.id   = int(config['vlan_cfi'])
            if 'vlan_pcp' in config : vlan.prio = int(config['vlan_pcp'])
            L2Pkt = eth/vlan
        elif L2Type == 'Ethernet_mpls':
            eth = Ether(src=config['eth_src'],dst=config['eth_dst'])
            mpls = MPLS(label=int(config['mpls_label']),cos=int(config['mpls_tc']),
                        s=int(config['mpls_bos']),ttl=int(config['mpls_ttl']))
            L2Pkt = eth/mpls
        else:
            eth = Ether()

        if L3Type == 'ipv4':
            L3Pkt = IP(src=config['ip_src'],dst=config['ip_dst'], proto=int(config['nw_proto']))
            if 'nw_tos' in config   : L3Pkt.tos = int(config['nw_tos'])
            if 'nw_ttl' in config   : L3Pkt.ttl = int(config['nw_ttl'])
            if 'nw_frag' in config  : L3Pkt.flags = int(config['nw_frag'])

        elif L3Type == 'ipv6':
            L3Pkt = IPv6(src=config['ipv6_src'],dst=config['ipv6_dst'],hlim=int(config['nw_ttl']),tc=int(config['nw_tos']),nh=int(config['nw_proto']))
        elif L3Type == 'arp':
            L3Pkt = ARP()
            L3Pkt.op = int(config['arp_op'])
            L3Pkt.hwsrc = config['arp_sha']
            L3Pkt.hwdst = config['arp_tha']
            L3Pkt.psrc = config['arp_spa']
            L3Pkt.pdst = config['arp_tpa']
            #(op=int(arpdata['arp_op']),hwsrc=arpdata['arp_sha'],hwdst=arpdata['arp_tha'],psrc=arpdata['arp_spa'],pdst=arpdata['arp_tpa'])
        else:
            L3Pkt = ''

        if L4Type == 'udp':
            L4Pkt = UDP(sport=config['udp_src'],dport=config['udp_dst'])
        elif L4Type == 'tcp':
            L4Pkt = TCP(sport=config['tcp_src'],dport=config['tcp_dst'],flags=config['tcp_flags'])
        elif L4Type == 'sctp':
            L4Pkt = SCTP(sport=config['sctp_src'],dport=config['sctp_dst'])
        elif L4Type == 'icmp':
            L4Pkt = ICMP(type=int(config['icmp_type']),code=int(config['icmp_code']))
        elif L4Type == 'icmpv6':
            L4Pkt = self.__getIcmp6Pkt(config)
        else:
            L4Pkt = ''
        
        base_pkt = L2Pkt
        if L3Pkt != '':
            base_pkt = base_pkt/L3Pkt
        if L4Pkt != '':
            base_pkt = base_pkt/L4Pkt

        if 'tun_type' in config:
            base_pkt,l = self.__trex_addTunlHead(config, l, base_pkt)
            
        pad = (l-len(base_pkt))*"x"
        base_pkt = base_pkt/pad
       
        logger.info(linehexdump(base_pkt,onlyhex=1,dump=1))
        unit,load = self.__trex_getUnit(profile,config)
        file = os.path.join(os.getenv('TEMP'),"tester_renix.pcap")
 
        wrpcap(file,base_pkt)
        CreateStreamFromPcapCommand(PortList=tport.handle,FilePath=file,RxPortList=tlist).execute()
        
        
        stream = tport.get_children('StreamTemplate')[-1]
        stream_template_load_profile = stream.get_children('StreamTemplateLoadProfile')[0]
        stream_template_load_profile.edit(Unit=unit)
        stream_template_load_profile.edit(Rate=int(load))
        
        config['trex_stream'] = stream

        return True

    def __trex_checkStreamMode(self,tport):
        #设置为基于流来计算负载
        stream_port_config = tport.get_children('StreamPortConfig')[0]
        if stream_port_config.LoadProfileType != EnumLoadProfileType.STREAM_BASE:
            stream_port_config.edit(LoadProfileType=EnumLoadProfileType.STREAM_BASE)
        return

    def __trex_createCustomStream(self,port,profileName,streamName,config):
        profile = self.ins['profile'][profileName]['config']
        #l = int(config.get("framelen",128))
        tport = self.__trex_getPort(port)
        tportlist = self.__trex_getPortList()
        tlist = [t.handle for t in tportlist]
        self.__trex_checkStreamMode(tport)
        
        unit,load = self.__trex_getUnit(profile,config)

        file = os.path.join(os.getenv('TEMP'),"tester_renix.pcap")
        pkt = config['pkt']
        wrpcap(file,pkt)
        CreateStreamFromPcapCommand(PortList=tport.handle,FilePath=file,RxPortList=tlist).execute()
        
        #新创建的流在最后
        stream = tport.get_children('StreamTemplate')[-1]
        stream_template_load_profile = stream.get_children('StreamTemplateLoadProfile')[0]
        stream_template_load_profile.edit(Unit=unit)
        stream_template_load_profile.edit(Rate=int(load))
        config['trex_stream'] = stream
        return True

    def testerConnect(self, ip, port=None,itype='trex'):
        self.ip = ip
        return self.__trex_testerConnect(ip)
        
    def __sendorder(self,order,recv=0):
        return self.__sendorderSim(order,recv)
    
    def __createPort(self, name, config):
        return self.__trex_createPort(name,config)

    def __clearPort(self, name, config):
        return self.__trex_ClearPort(name,config)

    def __sendorderSim(self,order,recv=0):
        if self.shell == None :
            raise AssertionError('Not connect!')
        logger.info('[SIM TESTER]' + order)
        return None

    def TesterGetInfo(self):
        '''获取测试仪配置
        '''
        return self.ins
    
    def __creatset(self, set):
        ret = ''
        for (k,v) in set.items():
            if k == 'object':
                ret = ret + ' -object ' + str(v)
            else:
                ret = '-' + k + ' ' + str(v) + ' ' + ret
        return ' ' + ret
    
    def __getVxlanHead(self,config):
        vxlanEth = Ether(src=config['tun_dl_src'],dst=config['tun_dl_dst'])
        vxlanIp = IP(src=config['tun_src'],dst=config['tun_dst'])
        #checksum错误，解封装后失败
        vxlanUdp = UDP(sport=52161,dport=4789,chksum=0) 
        return  vxlanEth/vxlanIp/vxlanUdp/VXLAN(vni=int(config['tun_id']))
    
    def __getGeneveHead(self,config):
        geneveEth = Ether(src=config['tun_dl_src'],dst=config['tun_dl_dst'])
        geneveIp = IP(src=config['tun_src'],dst=config['tun_dst'])
        geneveUdp = UDP(sport=52161,dport=6081) 
        return  geneveEth/geneveIp/geneveUdp/GENEVE(vni=int(config['tun_id']))

    def __getGreHead(self,config):
        greEth = Ether(src=config['tun_dl_src'],dst=config['tun_dl_dst'])
        greIp = IP(src=config['tun_src'],dst=config['tun_dst'])
        return  greEth/greEth/GRE()
    
    def __getNvgreHead(self,config):
        '''
        GRE 头中的 C flag 和 S flag 必须置 0 ， K flag 必须置 1 ，原来 GRE 头中的 Key 字段被用来存放 Virtual Subnet ID (VSID) 和 Flow ID 。
        Protocol Type ： 16bit ，固定值是 0x6558 ，表示是 NVGRE 报文。
        '''
        nvgreEth = Ether(src=config['tun_dl_src'],dst=config['tun_dl_dst'])
        nvgreIp = IP(src=config['tun_src'],dst=config['tun_dst'])
        nvgrekey = config['vs_id'] << 8
        nvgrekey = nvgrekey + config['flow_id']
        return  nvgreEth/nvgreIp/GRE(chksum_present=0,key_present=1,seqnum_present=0,proto=0x6558,key=nvgrekey)    
    
    def __trex_addTunlHead(self,config,l,pkt):
        if config['tun_type'] == 'vxlan':
            tunlHead = self.__getVxlanHead(config)
        elif config['tun_type'] == 'geneve':
            tunlHead = self.__getGeneveHead(config)
        elif config['tun_type'] == 'gre':
            tunlHead = self.__getGreHead(config)
        elif config['tun_type'] == 'nvgre':
            tunlHead = self.__getNvgreHead(config)
        pkt = tunlHead/pkt
        l = l+self.vxlanHeadLen
        return pkt,l

    def __getIcmp6Pkt(self,config):
        icmpType = {
            '128': 'ICMPv6EchoRequest',
            '129': 'ICMPv6EchoReply',
            '135': 'ICMPv6ND_NS',
            '136': 'ICMPv6ND_NA'
        }
        fun = icmpType[config['icmpv6_type']]
        if fun == 'ICMPv6ND_NS':
            pkt = ICMPv6ND_NS(type=135,code=int(config['icmpv6_code']),res=int(config['nd_reserved']),tgt=config['nd_target'])
            if config['nd_sll'] != '':
                pkt /= ICMPv6NDOptSrcLLAddr(lladdr=config['nd_sll'])
            if config['nd_tll'] != '':
                pkt /= ICMPv6NDOptDstLLAddr(lladdr=config['nd_tll'])
        elif fun == 'ICMPv6ND_NA':
            pkt = ICMPv6ND_NA(type=136,code=int(config['icmpv6_code']),res=int(config['nd_reserved']),tgt=config['nd_target'])
        return pkt

    def __getHostConfig(self, name):
        if name in self.ins['host']:
            return self.ins['host'][name]
        else :
            return None
    
    def isPortCreated(self, port):
        if port in self.ins['port']:
            return True
        return False

    def getPortNameByLocation(self,name):
        return self.__findPortname(name)

    def __findPortname(self, name):
        obj = name
        if obj not in self.ins['port']:
            for i in self.ins['port']:
                if obj == self.ins['port'][i]["PortLocation"]:
                    obj = i
        if obj in self.ins['port']:
            if 'realname' in self.ins['port'][obj]:
                obj = self.ins['port'][obj]['realname']
        return obj

    def __createHost(self, name, config):
        '''创建一个端口(暂不支持)
        '''
        #value = self.__trex_hostconfig(config)
        self.ins['host'][name] = copy.deepcopy(config)
        return True

    def __createSubPort(self, name, config):
        obj = self.__findPortname(config['object'])
        self.__sendorder( "CreateSubInt -SubIntName " + name + " -object "+ obj)
        if 'config' in config:
            self.__sendorder( "ConfigPort " + self.__creatset(config['config']) +
                             " -object " + name)
        self.ins['subint'][name] = copy.deepcopy(config)
        return True

    def __getStreamProfile(self, stream):
        for profile in self.ins['profile']:
            if stream in self.ins['profile'][profile]['stream']:
                return profile
        raise AssertionError("Can not find profile of stream %s"%(stream))
        return None

    def __getTrafficPort(self, name):
        logger.debug(self.ins['traffic'])
        if name in self.ins['traffic']:
            return self.ins['traffic'][name]['object']
        for p,v in self.ins['port'].items():
            if 'traffic' in v and v['traffic'] == name:
                return p
        raise AssertionError("Can not find port of traffic %s"%(name))
    
    def __getStatEngByPort(self, port):
        logger.debug(self.ins['engin'])
        for k,v in self.ins['engin'].items():
            if v['object'] != port:
                continue
            if 'engtype' in v and v['engtype'] == 'Analysis':
                continue
            return k
        if port in self.ins['port'] and 'statisticsEng' in self.ins['port'][port]:
            return self.ins['port'][port]['statisticsEng']
        raise AssertionError("Can not find port %s"%(port))
    
    def __getAnalyzerEngByPort(self, port):
        logger.debug(self.ins['engin'])
        for k,v in self.ins['engin'].items():
            if v['object'] != port:
                continue
            if 'engtype' in v and v['engtype'] == 'Analysis':
                return k
        if port in self.ins['port'] and 'analyzerEng' in self.ins['port'][port]:
            return self.ins['port'][port]['analyzerEng']
        raise AssertionError("Can not find port %s"%(port))
    
    def __createTraffic(self, name, config):
        self.__sendorder( "CreateTraffic -TrafficName " + name + self.__creatset(config))
        self.ins['traffic'][name] = copy.deepcopy(config)
        return True

    def __transferStream(self,config):
        '''
        额外定义的字段, 创建流的时候，不能包含这些字段
            flowType   --  报文类型 ipv4/ipv6/4in6
            hostsrc    --  指定发出的host
            hostdst    --  指定目的host
        '''
        #需要转换的key
        __trans = {
            'EthSrc' : 'eth_src',
            'EthDst' : 'eth_dst',
            'dl_src' : 'eth_src',
            'dl_dst' : 'eth_dst',
            'nw_src' : 'ip_src',
            'nw_dst' : 'ip_dst',
            'vlanid' : 'vlan_vid',
            'dl_vlan': 'vlan_vid',
            'dot1q'  : 'vlan_vid',
            'dl_vlan_pcp' : 'vlan_pcp',
            'IpSrcAddr' : 'ip_src',
            'IpDstAddr' : 'ip_dst',
            'Ipv6SrcAddress' : 'ipv6_src',
            'Ipv6DstAddress' : 'ipv6_dst',
            'UdpSrcPort' : 'udp_src',
            'UdpDstPort' : 'udp_dst',
            'TcpDstPort' : 'tcp_src',
            'TcpSrcPort' : 'tcp_dst',
            'TcpFlagSyc' : '_____',
            'TcpFlagAck' : '_____',
            'IcmpType' : '_____',
            'IcmpId' : 'icmp_code',
        }
        
        value = copy.deepcopy(config)
        flowType = config.pop('flowType', 'ipv4')
        for k,v in __trans.items():
            if k in value:
                value.setdefault(v,value[k])
                value.pop(k)
        if 'vlan_tci' in value:
            value['vlan_pcp'] = value['vlan_tci'] & (0xE000)
            value['vlan_cfi'] = value['vlan_tci'] & (0x1000)
            value['vlan_vid'] = value['vlan_tci'] & (0x0fff)
            value.pop('vlan_tci')
        #根据指定的host来设置默认配置
        if 'hostsrc' in config :
            host = self.__getHostConfig(config['hostsrc'])
            if host == None :
                raise AssertionError("Can not find host\"%s\""%(config['hostsrc']))
            del value['hostsrc']
            logger.trace("find host : %s"%(str(host)))
            if 'dl_src' not in value:
                value['dl_src'] = host['MacAddr']
            if flowType == 'ipv4':
                if 'ip_src' not in value:
                    value['ip_src'] = host['Ipv4Addr']
                    if 'hostdst' not in value and  'ip_dst' not in value:
                        value['ip_dst'] = host['Ipv4sutAddr']
            elif (flowType == '4in6') or (flowType == 'ipv6'):
                if 'ipv6_src' not in value:
                    value['ipv6_src'] = host['Ipv6Addr']
            if flowType == '4in6':
                if 'ipv6_dst' not in value:
                    value['ipv6_dst'] = host['Ipv6sutAddr']
            if 'vlan_vid' not in value:
                vlanid = self.getHostVlan(config['hostsrc'])
                if vlanid :
                    value['vlan_vid'] = vlanid
        if 'hostdst' in config :
            host = self.__getHostConfig(config['hostdst'])
            if host == None :
                raise AssertionError("Can not find host\"%s\""%(config['hostdst']))
            del value['hostdst']
            logger.trace("find host : %s"%(str(host)))
            if (flowType == '4in6') or (flowType == 'ipv4'):
                if 'ip_dst' not in value:
                    value['ip_dst'] = host['Ipv4Addr']
            #elif flowType == 'ipv6':
                #if 'ipv6_dst' not in value:
                    #value['ipv6_dst'] = host['Ipv6Addr']
        if 'L3' not in value:
            if flowType.lower() == 'ipv4':
                value['L3'] = 'IPv4'
            elif flowType.lower() == 'ipv6':
                value['L3'] = 'IPv6'
            elif flowType.lower() == '4in6':
                value['L3'] = 'IPv4inIPv6'
            elif flowType.lower() == '6in4':
                value['L3'] = 'IPv6inIPv4'
            else:
                value['L3'] = flowType
        if 'L4' in value and 'IpProtocolType' not in value:
            value['IpProtocolType'] = value['L4'].lower()
        if 'L2' not in value:
            if 'vlan_vid' in value:
                value['L2'] = 'Ethernet_vlan'
            elif 'mpls' in value:
                value['L2'] = 'Ethernet_mpls'
            else:
                value['L2'] = 'Ethernet'
        return value

    def __createStream(self,profileName,streamName,config={}):
        '''创建流
        '''
        logger.trace("Create Stream : %s %s %s"%(profileName,streamName,str(config)))
        value = self.__transferStream(config)
        value['framelen'] = config.get('framelen','128')
        if 'eth_dst' not in value:
                raise AssertionError("Can not find eth_dst")
        traffic = self.__getProfileTraffic(profileName)
        port = self.__getTrafficPort(traffic)
        self.__trex_createStream(port,profileName,streamName,value)
        self.ins['profile'][profileName]['stream'][streamName] = value
        return True

    def __createCustomStream(self,profileName,streamName,config={}):
        '''创建流
        '''
        logger.trace("Create Stream : %s %s %s"%(profileName,streamName,str(config)))

        traffic = self.__getProfileTraffic(profileName)
        port = self.__getTrafficPort(traffic)
        self.__trex_createCustomStream(port,profileName,streamName,config)
        self.ins['profile'][profileName]['stream'][streamName] = config
        return True

    def __getProfileTraffic(self, profile):
        if profile in self.ins['profile']:
            logger.debug(self.ins['profile'][profile])
            info = self.ins['profile'][profile]['config']
            if 'port' in info:
                return self.ins['port'][info['port']]['traffic']
            return info['object']
        raise AssertionError("Can not find traffic of profile %s"%(profile))
        return None
    
    def testerGetDefFps(self):
        fpsdef = 10
        try:
            fpsdef  = BuiltIn().get_variable_value('${fps}','10')
        except Exception:
            pass
        return str(fpsdef)
    
    def testerGetDefSleeptime(self):
        time = 3
        try:
            time  = BuiltIn().get_variable_value('${sleep}','3')
        except Exception:
            pass
        logger.info("Default sleep : %s"%time)
        return str(time)
    
    def testerGetFasterFps(self):
        fpsfaster = '200'
        try:
            fpsfaster  = BuiltIn().get_variable_value('${fpsfaster}','200')
        except Exception:
            pass
        return str(fpsfaster)
    
    def __createProfile(self, profileName, config):
        if 'config' in config:
            if 'TrafficLoad'  not in config['config']:
                fpsdef    = self.testerGetDefFps()
                config['config']['TrafficLoad'] = fpsdef
                logger.info("[SIM TESTER]Set default fps : %s"%fpsdef)
            if config['config']['TrafficLoad'].lower() == 'faster':
                fpsfaster = self.testerGetFasterFps()
                config['config']['TrafficLoad'] = fpsfaster
                logger.info("[SIM TESTER]Set faster fps : %s"%fpsfaster)
            if 'TrafficLoadUnit'  not in config['config']:
                config['config']['TrafficLoadUnit'] = 'fps'
            if 'Type' in config['config']:
                if config['config']['Type']=='Burst':
                    if 'FrameNum' not in config['config']:
                        config['config']['FrameNum'] = '2'
            traffic = None
            if 'port' in config['config']:
                traffic = self.ins['port'][config['config']['port']]['traffic']
                del config['config']['port']
                config['config']['object'] = traffic
            self.__sendorder( "CreateProfile -Name " + profileName + self.__creatset(config['config']))
        if profileName not in self.ins['profile']:
            self.ins['profile'][profileName] = {'config':{},'stream':{}}
        self.ins['profile'][profileName]['config'] = copy.deepcopy(config['config'])
        if 'stream' in config:
            for streamName in config['stream']:
                if 'pkt' in config['stream'][streamName]:
                    self.__createCustomStream(profileName,streamName,config['stream'][streamName])
                else:
                    self.__createStream(profileName,streamName,config['stream'][streamName])
        return True

    def __createStaEngine(self,name,config):
        self.engine = name
        self.__sendorder('CreateStaEngine -StaEngineName %s -StaType %s -object %s' % (name,config['engtype'],config['object']))
        engtype = config.get("engtype","Statistics")
        portdict = self.ins['port'][config['object']]
        port = portdict['realname']
        tsport = self.__trex_getPort(port)
        if 'Statistics' == engtype:
            page0,page1 = None,None
            for p in self.sys_entry.get_children('PageResultView'):
                if p.DataClassName == 'PortStats':
                    page0 = p
                elif p.DataClassName == 'StreamStats':
                    page1 = p
            if page0 == None or page1 == None:
                CreateResultViewCommand(DataClassName=StreamStats.cls_name()).execute()
                CreateResultViewCommand(DataClassName=PortStats.cls_name()).execute()
                page0 = self.sys_entry.get_children('PageResultView')[0]
                page1 = self.sys_entry.get_children('PageResultView')[1]
                SubscribeResultCommand(ResultViewHandles=[page0.handle,page1.handle]).execute()
                for p in self.sys_entry.get_children('PageResultView'):
                    if p.DataClassName == 'PortStats':
                        page0 = p
                    elif p.DataClassName == 'StreamStats':
                        page1 = p
            CommitCommand().execute()
            config['page0'] = page0
            config['page1'] = page1
        elif 'Analysis' == engtype:
            cap_conf_1 = tsport.get_children('CaptureConfig')[0]
            cap_conf_1.edit(CaptureMode=EnumCaptureMode.ALL, 
                CacheCapacity=EnumCacheCapacity.Cache_64KB, 
                BufferFullAction=EnumBufferFullAction.WRAP, 
                #CapturedPacketCount=1000,
                StartingFrameIndex=1, 
                AttemptDownloadPacketCount=1000
                )

        self.ins['engin'][name] = copy.copy(config)
        
    def createTestPort(self, location):
        ''' 创建测试仪端口
         location  =  101/5
        '''
        pass

    def SendArpRequest(self,host= None):
        if host == None:
            for name in self.ins['host']:
                self.SendArpRequest(name)
            return True
        host = str(host)
        if host not in self.ins['host']:
            raise AssertionError("Can not find host \"%s\""%(host))
        rc = 1
        logger.debug("[tester]SendArpRequest %s"%str(rc))
        return True
    
    def findPortByLocation(self, location):
        for k,v in self.ins['port'].items():
            if 'PortLocation' in v and v['PortLocation'] == location:
                return k
        return None
    
    def findHostByLocation(self, location):
        port = self.findPortByLocation(location)
        return self.findHostByPort(port)
    
    def findHostByPort(self, port):
        hostlist = []
        for k,v in self.ins['host'].items():
            if 'object' in v and v['object'] == port:
                hostlist.append(k)
        return hostlist

    def getHostFirstByLocation(self,location):
        hostlist = self.findHostByLocation(self,location)
        if len(hostlist) > 0:
            return hostlist[0]
        return None

    def chaConfig(self,config):
        ''' 根据配置字典配置测试仪
        '''
        logger.debug("[SIM TESTER]------chaConfig-------")
        logger.debug(id(self))
        if 'cha' not in config:
            return False
        if "port" in config['cha']:
            for (port,conf) in config['cha']['port'].items():
                self.__createPort(port,conf)
        if "subint" in config['cha']:
            for (port,conf) in config['cha']['subint'].items():
                self.__createSubPort(port,conf)
        if "host" in config['cha']:
            for (host,conf) in config['cha']['host'].items():
                self.__createHost(host,conf)
                self.SendArpRequest(host) #先学好mac
        if "traffic" in config['cha']:
            for (name,conf) in config['cha']['traffic'].items():
                self.__createTraffic(name,conf)
        if "profile" in config['cha']:
            for (name,conf) in config['cha']['profile'].items():
                self.__createProfile(name,conf)
        if "staEngine" in config['cha']:
            for (name,conf) in config['cha']['staEngine'].items():
                if conf['object'] != 'portNone':
                    self.__createStaEngine(name,conf)
        logger.debug("[SIM TESTER]-----chaConfig--end-----")
        return True

    def chaClearConfig(self,config):
        ''' 根据配置字典配置测试仪
        '''
        logger.debug("[SIM TESTER]------chaClearConfig-------")
        logger.debug(id(self))
        if 'cha' not in config:
            return False
        if "port" in config['cha']:
            for (port,conf) in config['cha']['port'].items():
                self.__clearPort(port,conf)
				
    def resetPort(self,name):
        return self.__trex_resetPort(name)

    def createProfile(self,config):
        for (name,conf) in config.items():
            self.__createProfile(name,conf)
        return True

    def createStream(self,profile,config):
        for (streamName,streamConf) in config.items():
            self.__createStream(profile,streamName,streamConf)
        return True

    def setStreamSpeed(self,name,unit,load):
        profile = self.__getStreamProfile(name)
        streamobj = self.ins['profile'][profile]['stream'][name]
        streamobj['StreamLoadUnit'] = unit
        streamobj['StreamLoad'] = load
        self.__trex_setUnit(profile,streamobj)

    def startProfile(self,name,clear=0):
        ''' 开始运行流
        '''
        # -clearStatics
        #StartTraffic -ProfileList port1ProfileOut -object CHASSIS1/1/5
        clearstr = ''
        if clear:
            clearstr = ' -clearstatistic 1'
        name = str(name)
        traffic = self.__getProfileTraffic(name)
        port = self.__getTrafficPort(traffic)
        tport = self.__trex_getPort(port)
        prof = self.ins['profile'][name]
        for _,v in prof['stream'].items():
            stream = v['trex_stream']
            logger.warn("start stream Name :"+stream.handle)
            StartStreamCommand(StreamList=stream.handle).execute()

    def stopProfile(self,name):
        ''' 停止运行流
        '''
        #StopTraffic -ProfileList port1ProfileIn -object CHASSIS1/1/5
        name = str(name)
        traffic = self.__getProfileTraffic(name)
        port = self.__getTrafficPort(traffic)
        tport = self.__trex_getPort(port)
        prof = self.ins['profile'][name]
        for _,v in prof['stream'].items():
            stream = v['trex_stream']
            logger.warn("stop stream Name :"+stream.handle)
            StopStreamCommand(StreamList=stream.handle).execute()
        
    def workProfile(self,name,trafficTime=3):
        name = str(name)
        self.startProfile(name)
        if trafficTime > 0:
            time.sleep(trafficTime)
        self.stopTraffic(name)

    def getStream(self,name):
        ''' 获取流的配置信息
        '''
        profile = self.__getProfileTraffic(name)
        stream = copy.deepcopy(self.ins['profile'][profile]['stream'][name])
        return stream

    def configStream(self,name,conf):
        profile = self.__getStreamProfile(name)
        traffic = self.__getProfileTraffic(profile)
        for (k,v) in conf.items():
            self.ins['profile'][profile]['stream'][name][k] = v
        self.__sendorder( "ConfigStream -StreamName " + name +
                         ' -ProfileName ' + profile +
                         self.__creatset(conf) +
                         ' -object ' + traffic)

    def configStreamByProfile(self,name,conf):
        profile = self.__getStreamProfile(name)
        for stream in self.ins['profile'][profile]['stream']:
            self.configStream(self,stream,conf)

    def getHostIpv4sutAddr(self,hostname):
        host = self.__getHostConfig(hostname)
        if 'Ipv4sutAddr' in host:
            return host['Ipv4sutAddr']
        return None

    def getHostIpv6sutAddr(self,hostname):
        host = self.__getHostConfig(hostname)
        if 'Ipv6sutAddr' in host:
            return host['Ipv6sutAddr']
        return None
    
    def getHostIpv4Ex(self,hostname):
        #'1.1.1.1/24'
        host = self.__getHostConfig(hostname)
        ip = None
        mask = None
        if 'Ipv4Addr' not in host:
            return None
        if 'Ipv4Mask' in host:
            return None
        return _baselib.appIpEx(host['Ipv4Addr'],host['Ipv4Mask'])
    
    def getHostIpv4(self,hostname):
        host = self.__getHostConfig(hostname)
        if 'Ipv4Addr' in host:
            return host['Ipv4Addr']
        return None
    
    def getHostIpv4Mask(self,hostname):
        host = self.__getHostConfig(hostname)
        if 'Ipv4Mask' in host:
            return host['Ipv4Mask']
        return None

    def getHostNet(self,hostname):
        ip = self.getHostIpv4(hostname)
        mask = self.getHostIpv4Mask(hostname)
        net= _baselib.IP(ip).make_net(mask)
        return net

    def getHostIpv6(self,hostname):
        host = self.__getHostConfig(hostname)
        if 'Ipv6Addr' in host:
            return host['Ipv6Addr']
        return None
    
    def getHostIpv6Mask(self,hostname):
        host = self.__getHostConfig(hostname)
        if 'Ipv6Mask' in host:
            return host['Ipv6Mask']
        return None
    
    def getHostIpv6Prefix(self,hostname):
        host = self.__getHostConfig(hostname)
        if 'Ipv6Mask' not in host:
            return None
        if 'Ipv6Addr' not in host:
            return None
        net = _baselib.natIpPrefix(host['Ipv6Addr'],host['Ipv6Mask'])
        return net
    
    def getHostGetwayMac_NO(self, hostname):
        '''
        暂时无法取到网关的mac，采用testlib中的获取方法
        '''
        pass

    def getHostMac(self,hostname):
        host = self.__getHostConfig(hostname)
        if 'MacAddr' in host:
            return host['MacAddr']
        return None

    def getIntVlan(self, name):
        '''获取接口的vlan
        '''
        if name in self.ins['subint']:
            if 'config' in self.ins['subint'][name]:
                return self.ins['subint'][name]['config'].get('VlanId',0)
        return 0

    def getHostVlan(self,hostname):
        host = self.__getHostConfig(hostname)
        if 'object' in host:
            return self.getIntVlan(host['object'])
        return None
    
    def getHostPort(self, hostname):
        host = self.__getHostConfig(hostname)
        if 'object' in host:
            return host['object']
        
    def getHostRealPort(self, hostname):
        host = self.__getHostConfig(hostname)
        if 'object' not in host:
            return None
        port = host['object']
        if port in self.ins['subint']:
            return self.ins['subint'][port]['object']
        return port
    
    def getTrafficByPort(self, portname):
        '''一般只会创建一个traffic
        
        根据port获取traffic
        '''
        if portname in self.ins['port']:
            for i in self.ins['traffic']:
                if self.ins['traffic'][i].get('object', None) == portname:
                    return i
            return self.ins['port'][portname].get('traffic',None)
        raise AssertionError("Can not find traffic from %s!"%portname)
    
    def getTrafficByHost(self, hostname):
        port = self.getHostRealPort(hostname)
        traffic = self.getTrafficByPort(port)
        return traffic
    def findHostByIp(self, ):
        pass
    
    def findHostIp(self, ipnet):
        hostlist = self.ins['host']
        iplist = {}
        ip = IPy.IP(ipnet)
        if ip.version() == 4:
            for h in hostlist:
                ipv4 = self.getHostIpv4(h)
                if ipv4 != None and ipv4 in ip:
                    iplist[ipv4] = h
                ipv4 = self.getHostIpv4sutAddr(h)
                if ipv4 != None and ipv4 in ip:
                    iplist[ipv4] = h
        else:
            for h in hostlist:
                ipv6 = self.getHostIpv6(h)
                if ipv6 != None and ipv6 in ip:
                    iplist[ipv6] = h
                ipv6 = self.getHostIpv6sutAddr(h)
                if ipv6 != None and ipv6 in ip:
                    iplist[ipv6] = h
        return iplist

    def getHostIpv4New(self,hostname):
        host = self.__getHostConfig(hostname)
        if host == None : return None
        
        ipv4 = host.get('Ipv4Addr',None)
        if ipv4 != None:
            ipv4=IPy.IP(ipv4)
            ipv4 = ipv4.make_net(host.get('Ipv4Mask',24))
            ipv4list = list(self.findHostIp(str(ipv4)).keys())
            
        ipv4new = None
        for ip in ipv4[1:]:
            if str(ip) not in ipv4list:
                ipv4new = str(ip)
                break
        return ipv4new

    def getHostIpv6New(self,hostname):
        host = self.__getHostConfig(hostname)
        if host == None : return []
        
        ipv6 = host.get('Ipv6Addr',None)  
        if ipv6 != None:
            ipv6=IPy.IP(ipv6)
            ipv6 = ipv6.make_net(host.get('Ipv6Mask',64))
            ipv6list = list(self.findHostIp(str(ipv6)).keys())
            
        ipv6new = None
        for ip in range(1,1000):
            if str(ipv6[ip]) not in ipv6list:
                ipv6new = str(ipv6[ip])
                break
        return ipv6new

    def cloneHost(self,hostname,num=1):
        num = int(num)
        host = self.__getHostConfig(hostname)
        if host == None : return []
        
        ipv4 = host.get('Ipv4Addr',None)
        ipv6 = host.get('Ipv6Addr',None)
        if ipv4 != None:
            ipv4=IPy.IP(ipv4)
            ipv4 = ipv4.make_net(host.get('Ipv4Mask',24))
            ipv4list = list(self.findHostIp(str(ipv4)).keys())
            
        if ipv6 != None:
            ipv6=IPy.IP(ipv6)
            ipv6 = ipv6.make_net(host.get('Ipv6Mask',64))
            ipv6list = list(self.findHostIp(str(ipv6)).keys())
            
        hostlist = []
        for i in range(0,num):
            name = hostname + '_c'+str(i)
            config = copy.deepcopy(host)
            if ipv4 != None:
                ipv4new = None
                for ip in ipv4[1:]:
                    if str(ip) not in ipv4list:
                        ipv4new = str(ip)
                        break
                config['Ipv4Addr'] = ipv4new
                ipv4list.append(ipv4new)
            if ipv6 != None:
                ipv6new = None
                for ip in range(1,1000):
                    if str(ipv6[ip]) not in ipv6list:
                        ipv6new = str(ipv6[ip])
                        break
                config['Ipv6Addr'] = ipv6new
                ipv6list.append(ipv6new)
            self.__createHost(name,config)
            hostlist.append(name)
        return hostlist
        
    def startTraffic(self,name,port=None):
        ''' Nothing
        
        请使用 startProfile
        '''
        profile = self.__getStreamProfile(name)
        traffic = self.__getProfileTraffic(profile)
        port = self.__getTrafficPort(traffic)
        port = self.ins['port'][port]['realname']
        tsport = self.__trex_getPort(port)
        StartAllStreamCommand(HandleList=[tsport.handle])

    def stopTraffic(self,name,port=None):
        ''' Nothing
        
        请使用 stopProfile
        '''
        profile = self.__getStreamProfile(name)
        traffic = self.__getProfileTraffic(profile)
        port = self.__getTrafficPort(traffic)
        port = self.ins['port'][port]['realname']
        tsport = self.__trex_getPort(port)
        StopAllStreamCommand(HandleList=[tsport.handle])

    def workTraffic(self,name,trafficTime=3):
        ''' Nothing
        
        请使用 workProfile
        '''
        pass

    def startStream(self, name):
        ''' 开始运行流
        '''
        profile = self.__getStreamProfile(name)
        streamobj = self.ins['profile'][profile]['stream'][name]
        stream = streamobj['trex_stream']
        StartStreamCommand(StreamList=stream.handle).execute()

    def stopStream(self, name):
        ''' 停止运行流
        '''
        profile = self.__getStreamProfile(name)
        streamobj = self.ins['profile'][profile]['stream'][name]
        stream = streamobj['trex_stream']
        StopStreamCommand(StreamList=stream.handle).execute()

    def workStream(self,name,trafficTime=3):
        ''' 运行流指定的时间
        '''
        name = str(name)
        self.startStream(name)
        if trafficTime > 0:
            time.sleep(trafficTime)
        self.stopStream(name)

    def startCapture(self,port):
        portdict = self.ins['port'][port]
        port = portdict['realname']
        tsport = self.__trex_getPort(port)
        cap_conf_1 = tsport.get_children('CaptureConfig')[0]
        logger.warn({
            'count' : cap_conf_1.CapturedPacketCount,
            'state' : cap_conf_1.CaptureState.name,
            'mode'  : cap_conf_1.CaptureMode.name,
            'cache' : cap_conf_1.CacheCapacity.name,
        })
        StartCaptureCommand(CaptureConfigs=cap_conf_1.handle).execute()

        portdict['cap_packets'] = dict()
        portdict['cap_status'] = dict()
        logger.info('[tester]startCapture ')

    def stopCapture(self,port):
        portdict = self.ins['port'][port]
        port = portdict['realname']
        tsport = self.__trex_getPort(port)
        cap_conf_1 = tsport.get_children('CaptureConfig')[0]
        StopCaptureCommand(CaptureConfigs=cap_conf_1.handle).execute()
        filename = "tester_renix_tmp_packet_"+str(time.time())+".pcap"
        file = os.path.join(os.getenv('TEMP'),filename)
        DownloadCaptureDataCommand(CaptureConfigs=cap_conf_1.handle, 
                FileDir=os.getenv('TEMP'), 
                FileName=filename, 
                MaxDownloadDataCount=1000).execute()
        if cap_conf_1.CapturedPacketCount == 0:
            return
        while cap_conf_1.DownloadedPacketCount <= 0 or cap_conf_1.CurrentDataFile == '':
            time.sleep(0.3)
        file = cap_conf_1.CurrentDataFile
        pkts = rdpcap(file,-1)
        for i in range(0,len(pkts)):
            portdict['cap_packets'][i] = pkts[i]

        return

    def getCapturePacket(self,port,idx=None):
        '''获取报文
        '''
        '''获取抓到的报文
            {'binary': b'\xff\xff\xff\xff\xff\xff\x00\x01\x00\x00\x00\x02\x08\x06\x00\x01'
                b'\x08\x00\x06\x04\x00\x01\x00\x01\x00\x00\x00\x02\xb9]\x86\x02'
                b'\x00\x00\x00\x00\x00\x00\xb9]\x86\x03',
            'index': 11,
            'origin': 'TX',
            'port': 0,
            'ts': 88405.35035384286}
            状态
            {8: {'bytes': 336, 'count': 8, 'filter': {'bpf': '', 'rx': 0, 'tx': 3}, 'id': 8, 'limit': 1000, 'matched': 12, 'mode': 'fixed', 'state': 'ACTIVE'}}
        '''
        portdict = self.ins['port'][port]
        if 'cap_packets' not in portdict:
            return None
        if idx == None:
            idlist =list(portdict['cap_packets'].keys())
            if len(idlist) == 0: return None
            idlist.sort()
            idx = idlist[0]
        if idx not in portdict['cap_packets']:
            return None
        pkt = portdict['cap_packets'].pop(idx)
        return {'binary':pkt}
    
    def getCaptureStatus(self,port):
        portdict = self.ins['port'][port]
        port = portdict['realname']
        tsport = self.__trex_getPort(port)
        cap_conf_1 = tsport.get_children('CaptureConfig')[0]
        ret = {
            'count' : cap_conf_1.CapturedPacketCount,
            'state' : cap_conf_1.CaptureState.name,
            'mode'  : cap_conf_1.CaptureMode.name,
            'cache' : cap_conf_1.CacheCapacity.name,
        }
        return ret

    def getStreamStatsMore(self, name,clear=0):
        #获取所有port累积信息
        stream = self.__trex_getStreamStateId(name)
        for p in self.sys_entry.get_children('PageResultView'):
            if p.DataClassName == 'StreamStats':
                page_result_view = p
        result_query = page_result_view.get_children()[0]
        stats = result_query.get_children('StreamStats')
        result = None
        for i in stats:
            if stream.Name == i.StreamBlockID:
                result = i
                break
        resultState = dict()
        if result != None:
            resultState['tx'] = result.TxStreamFrames
            resultState['rx'] = result.RxStreamFrames
            resultState['rx_bps'] = result.RxBitRate
            resultState['tx_bps'] = result.TxBitRate
            resultState['tx_pps'] = result.TxFrameRate
            resultState['rx_pps'] = result.RxFrameRate
            #resultState['RxPauseFrames'] = result.RxPauseFrames
            resultState['RxPktLossCount'] = result.RxLossStreamFrames
            resultState['RealtimeLossRate'] = result.RealtimeLossRate

        if clear:
            ClearResultCommand(ResultViewHandles=page_result_view.handle).execute()

        logger.warn("[tester]Stream %s : "%(name,str(result)))
        return resultState

    def getPortStatsMore(self, name,clear=0):
        statEng = self.__getStatEngByPort(name)
        tport = self.__trex_getPort(name)
        for p in self.sys_entry.get_children('PageResultView'):
            if p.DataClassName == 'PortStats':
                page_result_view = p
        result_query = page_result_view.get_children()[0]
        stats = result_query.get_children('PortStats')
        result = None
        for i in stats:
            if tport.handle == i.PortHandle:
                result = i
                break

        resultState = dict()
        if result != None:
            resultState['tx'] = result.TxTotalFrames
            resultState['rx'] = result.RxTotalFrames
            resultState['rx_bps'] = result.RxBitRate
            resultState['tx_bps'] = result.TxBitRate
            resultState['tx_pps'] = result.TxFrameRate
            resultState['rx_pps'] = result.RxFrameRate
            resultState['RxUtil'] = result.RxUtil
            resultState['TxUtil'] = result.TxUtil
            resultState['Result'] = result
            #resultState['RxPauseFrames'] = result.RxPauseFrames
            #resultState['RxPktLossCount'] = result.RxLossStreamFrames
            #resultState['RealtimeLossRate'] = result.RealtimeLossRate

        if clear:
            ClearResultCommand(ResultViewHandles=page_result_view.handle).execute()

        logger.warn("[tester]Port %s : %s"%(name,str(result)))
        return resultState

    def getStreamStats(self, name,port=None,clear=1):
        #获取所有port累积信息
        (tx,rx) = (0,0)
        stream = self.__trex_getStreamStateId(name)
        for p in self.sys_entry.get_children('PageResultView'):
            if p.DataClassName == 'StreamStats':
                page_result_view = p
        result_query = page_result_view.get_children()[0]
        stats = result_query.get_children('StreamStats')
        result = None
        for i in stats:
            if stream.Name == i.StreamBlockID:
                result = i
                break
        if result != None:
            tx = result.TxStreamFrames
            rx = result.RxStreamFrames
        logger.info("[tester]Stream %s : tx %d rx %d"%(name,tx,rx))
        if clear:
            ClearResultCommand(ResultViewHandles=page_result_view.handle).execute()
        return tx,rx

    def getPortStats(self, name):
        statEng = self.__getStatEngByPort(name)
        (tx,rx) = (0,0)
        tport = self.__trex_getPort(name)
        for p in self.sys_entry.get_children('PageResultView'):
            if p.DataClassName == 'PortStats':
                page_result_view = p
        result_query = page_result_view.get_children()[0]
        stats = result_query.get_children('PortStats')
        result = None
        for i in stats:
            if tport.handle == i.PortHandle:
                result = i
                break
        if result != None:
            tx = result.TxTotalFrames
            rx = result.RxTotalFrames
        ClearResultCommand(ResultViewHandles=page_result_view.handle).execute()    
        return tx,rx

    def streamShouldRXeqTX(self,name):
        tx,rx = self.getStreamStats(name)
        BuiltIn().should_be_true(tx>0,"Stream %s tx is zero"%name)
        BuiltIn().should_be_true(rx>0,"Stream %s rx is zero"%name)
        BuiltIn().should_be_true(rx*2 >= tx,"Stream %s check error,rx %d, tx %d"%(name,rx,tx))

    def streamShouldRXeqZero(self,name):
        tx,rx = self.getStreamStats(name)
        BuiltIn().should_be_true(tx>0,"Stream %s tx is zero"%name)
        BuiltIn().should_be_true(rx == 0,"Stream %s rx is not zero %d"%(name,rx))

    def profileShouldRXeqTx(self, name):
        streams = self.ins['profile'][name]['stream']
        for s in streams.keys():
            self.streamShouldRXeqTX(s)
        
    def profileShouldRXeqZero(self, name):
        streams = self.ins['profile'][name]['stream']
        for s in streams.keys():
            self.streamShouldRXeqZero(s)

    def ResetSession(self):
        StopAllStreamCommand().execute()
        try:
            StopAllCaptureCommand().execute()
        except Exception:
            pass    
        for k,v in self.ins['port'].items():
            tport = self.__trex_getPort(k)
            for s in tport.get_children('StreamTemplate'):
                s.delete()

    def testerLoggerDebug(self):
        self.saveConfig()

    def CleanupTest(self):
        ResetROMCommand().execute()
        
    def saveConfig(self):
        try:
            #在实际测试仪中会保存配置为xml
            SaveTestCaseCommand(TestCase='D:/renix_test.xcfg').execute()
        except Exception:
            pass
    
if __name__ == '__main__':
    config = {
        'cha' :{
            'port' : {
                'port1' : {
                    'PortLocation' :  '2/3',
                    'PortType'     : 'Fiber',
                    'FecType'     : 0,
                    }
                },
            'staEngine' :{
                'port1Sta':{'engtype': 'Statistics','object': 'port1'},
                'port1Ana':{'engtype': 'Analysis','object':'port1'}
            },
            'traffic' :{
                "port1Traffic" : {
                    'object': 'port1'
                }
            },
            'profile' : {
                'profile1' :{
                    'config' :{
                        'object' : 'port1Traffic',
                        'Type' : 'Constant',
                        'TrafficLoad':'1',
                        'TrafficLoadUnit':'fps'
                        },
                    'stream' : {
                        'stream1' : {
                                'pkt' : Ether(dst='00:01:00:00:01:01',src='00:01:00:00:01:02')/IP(src='172.0.1.1',dst='172.0.1.2')/UDP(),
                                'L2' : 'Ethernet',
                                'L3' : 'IPV4',
                                'EthDst' : '00:1f:53:10:52:1c',
                                'EthSrc' : '00:01:00:00:00:03',
                                'IpSrcAddr' : '192.168.239.100',
                                'IpSrcMask' : '255.255.255.0',
                                'IpDstAddr' : '192.168.239.1',
                                'IpDstMask' : '255.255.255.0',
                                'framelen' : '200',
                                'StreamLoad':'1',
                                'StreamLoadUnit':'fps'
                            },
                        }
                    }
                }
            },
        }
    tester = Tester()
    tester.testerConnect("10.20.25.250")
    tester.chaConfig(config)
    #tester.SendArpRequest('host1')
    #tester.SendArpRequest('host2')
    #tester.SendArpRequest('host3')
    tester.startCapture('port1')
    tester.startProfile('profile1')
    time.sleep(10)
    tester.stopProfile('profile1')
    tester.stopCapture('port1')
    tester.getStreamStats('stream1')
    tester.getStreamStats('stream1','port2')
    tester.getPortStats('port1')
    tester.getPortStats('port1')
    #tester.ResetSession()
    print ('OK')
    
