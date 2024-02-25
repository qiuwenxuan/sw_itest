#!/usr/bin/python
# -*- coding: utf-8 -*-
from email.policy import default
import sys , os , time , copy, re, random
import struct , binascii
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from binascii import b2a_hex
import scapy.all as _scapy
from scapy.layers.l2 import Ether

__path = os.path.realpath(os.path.join(__file__,'..','..','..')) 
if __path not in sys.path:sys.path.append(__path)

import base.AppBaseLib as _baselib

class OvsTestlib(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    
    def __init__(self):
        self.testerlib = None
    
    def __getindex(self):
        return str(time.time())
    
    def __initlib(self):
        '''外部调用函数需要先调用，避免没有初始好就执行
        '''
        if self.testerlib == None:
            self.dutlib = BuiltIn().get_library_instance('AppDut')
            self.testerlib = BuiltIn().get_library_instance('Tester')
            self.linuxlib   = BuiltIn().get_library_instance('Linux')
            self.ovslib  = BuiltIn().get_library_instance('Ovs')
            self.pmdlib  = BuiltIn().get_library_instance('Testpmd')
            self.topolib = BuiltIn().get_library_instance('Topology')
            self.jaguarlib = BuiltIn().get_library_instance('Jaguar')
            
    def __getHostFirst(self, host):
        if isinstance(host,str) :
            return host
        return host[0]
    
    def __getHostNum(self, host):
        if isinstance(host,str) :
            return 1
        return len(host)
    
    def __getHostList(self, host):
        if isinstance(host,str) :
            return [host]
        return host
    
    def __getHostListByDut(self, dut,port=1):
        #获取与设备连接的cha的host列表
        hostlist = []
        location = self.topolib.topoGetPort("{}.{}->{}.{}".format('cha',port,dut,port))
        hostlist = self.testerlib.findHostByLocation(location)
        return hostlist
    
    def __getHostFirstByDut(self, dut,port=1):
        #获取与设备连接的cha的host列表中一个
        hostlist = self.__getHostListByDut(dut,port)
        if len(hostlist):
            return hostlist[0]
        else:
            return None
    
    def __getDutByHost(self,host):
        '''获取Host连接的设备dut名称
        '''
        self.__initlib()
        firsthost = self.__getHostFirst(host)
        logger.debug(firsthost)
        ip = self.testerlib.getHostIpv4sutAddr(firsthost)
        logger.debug(ip)
        dut = self.linuxlib.getDutByIpv4(ip)
        logger.debug(dut)
        return dut
    
    def __isInputTun(self,config):
        #是否解封装方向
        if 'tun_port' not in config:
            return False
        if config['inport'] == config['tun_port']:
            return True
        return False

    def __isOutputTun(self,config):
        #是否封装方向
        if 'tun_port' not in config:
            return False
        if config['outport'] == config['tun_port']:
            return True
        return False

    def __streamOnly(self):
        only = BuiltIn().get_variable_value('${streamonly}',False)
        return only

    def __getProtocolByConfig(self, config):
        protocol = 'udp'
        if (config == None) or (len(config) <= 0):
            return protocol
        if 'protocol' in config:
            protocol = config['protocol']
        return protocol.lower()
    
    def __checkDefaultConfig(self, protocol, stream, flowType='ipv4' ):
        #nat 类型暂使用udp, 如果后续需要，可以改为nat-udp,nat-tcp,nat-icmp
        if 'nat' == protocol:
            protocol = 'udp'
        elif 'nat' in protocol:
            protocol = protocol[4:]
        if protocol == 'tcp':
            if 'TcpSrcPort' not in stream:
                stream['TcpSrcPort'] = '1000'
            if 'TcpDstPort' not in stream:
                stream['TcpDstPort'] = '1000'
        elif protocol == 'udp':
            if 'UdpSrcPort' not in stream:
                stream['UdpSrcPort'] = '1000'
            if 'UdpDstPort' not in stream:
                stream['UdpDstPort'] = '1000'
        elif protocol == 'icmp':
            if 'Icmptype' not in stream:
                stream['Icmptype'] = 'echo_request'
            if 'IcmpId' not in stream:
                stream['IcmpId'] = '0'
        if 'L4' not in stream:
            stream['L4'] = protocol
        if ('hostsrc' in stream) and ('EthDst' not in stream):
            #stream['EthDst'] = self.getHostGetwayMac(stream['hostsrc'])
            stream['EthDst'] = self.testerlib.getHostMac(stream['hostdst'])
        if flowType == '4in6':
            if 'framelen' not in stream:
                stream['framelen'] = '256'
            if 'L3' not in stream:
                stream['L3'] = 'IPv4InIPv6'
            if 'Ipv6SrcAddressMode' not in stream:
                stream['Ipv6SrcAddressMode'] = 'increment'
            if 'Ipv6SrcAddressCount' not in stream:
                stream['Ipv6SrcAddressCount'] = '1'
            if 'Ipv6SrcAddressStep' not in stream:
                stream['Ipv6SrcAddressStep'] = '::1'
            if 'L4' not in stream:
                stream['L4'] = 'IPv4'
            if 'IpSrcAddr' not in stream:
                stream['IpSrcAddr'] = '55.1.1.1'
            if 'IpSrcMask' not in stream:
                stream['IpSrcMask'] = '255.255.255.0'
            if 'IpSrcAddrMode' not in stream:
                stream['IpSrcAddrMode'] = 'increment'
            if 'IpSrcAddrCount' not in stream:
                stream['IpSrcAddrCount'] = '1'
            if 'IpSrcAddrStep' not in stream:
                stream['IpSrcAddrStep'] = '0.0.0.1'
            if 'IpSrcMask' not in stream:
                stream['IpSrcMask'] = '255.255.255.0'

    def __createOutStream(self, dut, hostsrc,hostdst,config=None):
        if config['direct'] not in ['out','both']: return
        if 'outprofile' in config : return True
        index = self.__getindex()
        pkttype     = self.__getProtocolByConfig(config)  #L4
        flowtype    = (config.get('flowtype','ipv4')).lower() #L3
        streamname  = config.get('outstream','outStream' + index)
        profilename = config.get('outprofile','port1ProfileOut' + index)
        FrameNum    = config.get('framenum',None)
        fps         = self.__getFpsByConfig(config)
        config['outstream']  = streamname
        config['outprofile'] = profilename
        config.setdefault('outprofile', profilename)
        firsthost = self.__getHostFirst(hostsrc)
        traffic = self.testerlib.getTrafficByHost(firsthost)
        
        #创建数据流
        conf = {
                profilename :{
                    'config' :{
                        'object' : traffic,
                        'Type' : 'Constant',
                        },
                    'stream' : {}
                    }
                }
        
        if fps != None:
            conf[profilename]['config']['TrafficLoad']     = fps
            conf[profilename]['config']['TrafficLoadUnit'] = 'fps'
            
        if FrameNum != None:
            conf[profilename]['config']['Type']      = 'Burst'
            conf[profilename]['config']['FrameNum']  = FrameNum

        streamNum = 1
        for hostname in self.__getHostList(hostsrc):
            stream = {
                      'hostsrc' : hostname,
                      'hostdst' : hostdst,
                      'flowType' : flowtype,
                      'L3': flowtype,
                      'L4': pkttype
                     }
            #处理config中的自定义信息
            if 'ipinc' in config:
                stream['IpSrcAddrMode'] = 'increment'
                stream['IpSrcAddrCount'] = config['ipinc']
                stream['IpSrcAddrStep'] = '0.0.0.1'
                
            if 'vlaninc' in config:
                stream['VlanIdMode'] = 'increment'
                stream['VlanIdCount'] = config['vlaninc']
                stream['VlanIdStep'] = 1
                
            if 'vlanid' in config:
                stream['VlanId'] = config['vlanid']
                
            if 'portinc' in config:
                if pkttype == 'tcp' :
                    stream['TcpSrcPortMode'] = 'increment'
                    stream['TcpSrcPortCount'] = config['portinc']
                    stream['TcpSrcPortStep'] = 1
                elif pkttype == 'udp' :
                    stream['UdpSrcPortMode'] = 'increment'
                    stream['UdpSrcPortCount'] = config['portinc']
                    stream['UdpSrcStep'] = 1
                else :
                    raise AssertionError("Known protocol %s"%pkttype)
                    
            if 'streamspecial' in config:
                stream.update(config['streamspecial'])

            if self.__isInputTun(config) :
                stream['tun_dl_src'] = self.testerlib.getHostMac(hostsrc)
                self.__setStreamTunnel(stream,config['tun_info'])

            for _flowconfig in config['flowRule']:
                '''根据流表规则创建一条流'''
                __stream = copy.deepcopy(stream)
                if 'output' in _flowconfig['action']:
                    if _flowconfig['action']['output'] != config['outport'] and _flowconfig['action']['output'] != 'drop':
                        continue
                self.__setStreamByFlow(dut, __stream, _flowconfig)
                #如果配置中指定的目的地址，流量也将设定为特定目的地址
                if "EthDst" in config:
                    __stream["EthDst"] = config["EthDst"]
                conf[profilename]['stream'][streamname+hostname+str(streamNum)] = __stream
                _flowconfig.setdefault('stream', streamname+hostname+str(streamNum))
                streamNum = streamNum + 1
            self.testerlib.createProfile(conf)
        return True

    def __createInStream(self, dut,hostsrc,hostdst,config):
        """ 暂不使用
            config参数：
                 'traffictime'   持续时间
                 'instream'      指定入向流名称
                 'domain'        测试指定的域
                 'softdomain'    测试指定的软线域
                 'cmtm'          指定的条目列表
            config返回
                 'instream'    创建的出向流名称
        """
        if config['direct'] not in ['in','both']: return True
        if 'inprofile' in config : return True
        index = self.__getindex()
        pkttype     = self.__getProtocolByConfig(config)  #L4
        flowtype    = (config.get('flowtype','ipv4')).lower() #L3
        streamname  = config.get('instream','inStream' + index)
        profilename = config.get('inprofile','inProfile' + index)
        FrameNum    = config.get('framenum',None)
        fps         = self.__getFpsByConfig(config)
        config['instream']  = streamname
        config['inprofile'] = profilename
        config.setdefault('inprofile', profilename)
        firsthost = self.__getHostFirst(hostdst)
        traffic = self.testerlib.getTrafficByHost(firsthost)
        
        #创建数据流
        conf = {
                profilename :{
                    'config' :{
                        'object' : traffic,
                        'Type' : 'Constant',
                        },
                    'stream' : {}
                    }
                }
        
        if fps != None:
            conf[profilename]['config']['TrafficLoad']     = fps
            conf[profilename]['config']['TrafficLoadUnit'] = 'fps'
            
        if FrameNum != None:
            conf[profilename]['config']['Type']      = 'Burst'
            conf[profilename]['config']['FrameNum']  = FrameNum

        streamNum = 1
        for hostname in self.__getHostList(hostdst):
            stream = {
                      'hostsrc' : hostname,
                      'hostdst' : hostsrc,
                      'flowType' : flowtype,
                      'L3': flowtype,
                      'L4': pkttype
                     }
            #处理config中的自定义信息
            if 'ipinc' in config:
                stream['IpSrcAddrMode'] = 'increment'
                stream['IpSrcAddrCount'] = config['ipinc']
                stream['IpSrcAddrStep'] = '0.0.0.1'
                
            if 'vlaninc' in config:
                stream['VlanIdMode'] = 'increment'
                stream['VlanIdCount'] = config['vlaninc']
                stream['VlanIdStep'] = 1
                
            if 'vlanid' in config:
                stream['VlanId'] = config['vlanid']
                
            if 'portinc' in config:
                if pkttype == 'tcp' :
                    stream['TcpSrcPortMode'] = 'increment'
                    stream['TcpSrcPortCount'] = config['portinc']
                    stream['TcpSrcPortStep'] = 1
                elif pkttype == 'udp' :
                    stream['UdpSrcPortMode'] = 'increment'
                    stream['UdpSrcPortCount'] = config['portinc']
                    stream['UdpSrcStep'] = 1
                else :
                    raise AssertionError("Known protocol %s"%pkttype)
                    
            if 'streamspecial' in config:
                stream.update(config['streamspecial'])

            if self.__isOutputTun(config) :
                stream['tun_dl_src'] = self.testerlib.getHostMac(hostsrc)
                self.__setStreamTunnel(stream,config['tun_info'])

            for _flowconfig in config['flowRule']:
                '''根据流表规则创建一条流'''
                __stream = copy.deepcopy(stream)
                if _flowconfig['action']['output'] != config['inport']:
                    continue
                self.__setStreamByFlow(dut, __stream, _flowconfig)
                conf[profilename]['stream'][streamname+hostname+str(streamNum)] = __stream
                _flowconfig.setdefault('stream', streamname+hostname+str(streamNum))
                streamNum = streamNum + 1
            self.testerlib.createProfile(conf)
        return True

    def __createCustomStream(self, dut, hostsrc,hostdst,flow=None):
        '''
        用户已经组织好scapy的报文格式,当前仿真环境使用
        '''
        #if config['direct'] not in ['out','both']: return
        if 'outprofile' in flow : return True
        index = self.__getindex()
        streamname  = flow.get('outstream','outStream' + index)
        profilename = flow.get('outprofile','port1ProfileOut' + index)
        FrameNum    = flow.get('framenum',None)
        fps         = self.__getFpsByConfig(flow)
        flow['outstream']  = streamname
        flow['outprofile'] = profilename
        flow.setdefault('outprofile', profilename)

        traffic = self.testerlib.getTrafficByPort(hostsrc)

        #创建数据流
        conf = {
                profilename :{
                    'config' :{
                        'object' : traffic,
                        'Type' : 'Constant',
                        },
                    'stream' : {}
                    }
                }
        
        if fps != None:
            conf[profilename]['config']['TrafficLoad']     = fps
            conf[profilename]['config']['TrafficLoadUnit'] = 'fps'
            
        if FrameNum != None:
            conf[profilename]['config']['Type']      = 'Burst'
            conf[profilename]['config']['FrameNum']  = FrameNum

        streamNum = 1
        for hostname in self.__getHostList(hostsrc):
            stream = {
                      'pkt': ''
                     }
            
                    
            if 'streamspecial' in flow:
                stream.update(flow['streamspecial'])

            if self.__isInputTun(flow) :
                stream['tun_dl_src'] = self.testerlib.getHostMac(hostsrc)
                self.__setStreamTunnel(stream,flow['tun_info'])

            stream['pkt'] = copy.deepcopy(flow['custompkt'])
            conf[profilename]['stream'][streamname+hostname+str(streamNum)] = stream
            flow.setdefault('stream', streamname+hostname+str(streamNum))
            self.testerlib.createProfile(conf)
        return True

     
    def getHostGetwayMac(self, host):
        '''获取Host的网关mac
        
            在测试仪上不能获取，使用dut中获取的方式
            
            测试仪主机名和mac获取混杂，所以放在testlib中
        '''
        self.__initlib()
        hostname = self.__getHostFirst(host)
        ip = self.testerlib.getHostIpv4sutAddr(hostname)
        _,mac = self.dutlib.AppGetMacByIp(ip)
        return mac

    def __getProtocolByConfig(self, config):
        '''nat-tcp/nat-udp/nat-icmp/tcp/udp/icmp
        '''
        protocol = 'udp'
        if (config == None) or (len(config) <= 0):
            return protocol
        if 'protocol' in config:
            protocol = config['protocol']
        return protocol.lower()
    
    def __getFpsByConfig(self,config):
        fps = config.get('fps',None)
        if fps != None:
            return str(fps)
        deffps = self.testerlib.testerGetDefFps()
        minfps = config.get('minfps',0)
        if int(minfps) > int(deffps):
            return str(minfps)
        return deffps
    
    def __getTrafficSleeptimeByConfig(self,config):
        time = config.get('sleep',None)
        if time != None:
            return int(time)
        time = self.testerlib.testerGetDefSleeptime()
        mintime = config.get('minsleep',2)
        if int(mintime) > int(time):
            return int(mintime)
        return int(time)

    def __setVlanByConfig(self, stream, flowconfig):
        if 'dl_vlan' in flowconfig: 
            stream['dl_vlan'] = flowconfig['dl_vlan']
        if 'dl_vlan_pcp' in flowconfig: 
            stream['dl_vlan_pcp'] = flowconfig['dl_vlan_pcp']
            stream.setdefault('dl_vlan',100)
        if 'vlan_tci' in flowconfig: 
            ret = re.search(r"(.+)\/(.+)", flowconfig['vlan_tci'])
            if ret:
                tciPrefix = ret.group(1)
                tciNet = ret.group(2)
                vlantci = int(tciPrefix,16) & int(tciNet,16)
            else:
                vlantci = int(flowconfig['vlan_tci'],16)       
            stream['vlan_pcp'] = vlantci & (0xE000)
            stream['vlan_cfi'] = vlantci & (0x1000)
            stream['vlan_vid'] = vlantci & (0x0fff)

    def __setEthByConfig(self, stream, flowconfig):
        if 'hostsrc' in stream:
            stream['EthSrc'] = self.testerlib.getHostMac(stream['hostsrc'])
        if 'hostdst' in stream:
            stream['EthDst'] = self.testerlib.getHostMac(stream['hostdst'])
        
        if 'dl_src' in flowconfig: 
            stream['EthSrc'] = _baselib.getMatchMac(flowconfig['dl_src'])
        if 'dl_dst' in flowconfig: 
            stream['EthDst'] = _baselib.getMatchMac(flowconfig['dl_dst'])
        

    def __setMplsByConfig(self, stream, flowconfig):
        mpls = {
            'mpls_label'  : '10',
            'mpls_tc'     : '0',
            'mpls_bos'    : '1',
            'mpls_ttl'    : '255',
        }
        if 'dl_type' in flowconfig and flowconfig['dl_type'] == '0x8847':
            stream['mpls'] = '0x8847'
            for k in mpls.keys() :
                if k in flowconfig:
                    stream[k] = flowconfig[k]
                else:
                    stream[k] = mpls[k]

    def __chgEthProStrToValue(self, flowtype):
        proto = {
            'ipv4'     : '0x0800',
            'ipv6'     : '0x86dd',
            'arp'      : '0x0806',
            'mpls'     : '0x8847'
        }
        if flowtype not in proto:
            return flowtype
        return proto[flowtype]

    def __chgProtoStrToValue(self, pkttype):
        proto = {
            'udp'     : '17',
            'tcp'     : '6',
            'dcn-meas'  : '19',
            'hmp'     : '20',
            'icmp'    : '1',
            'igmp'    : '2',
            'sctp'    : '132',
            'icmpv6'    : '58',
        }
        if pkttype not in proto:
            return int(pkttype)
        return proto[pkttype]

    def __chgIPNewFragStrToValue(self, fragtype):
        if fragtype == '':
            return
        frag = {
            'no'     : '0',
            'first'  : '1',
            'yes'    : '3',
            '0'      : '0',
            '1'      : '1',
            '3'      : '3',
        }
        return frag[fragtype]

    def __setIpv4ByConfig(self, stream, flowconfig):
        if stream['flowType'] != 'ipv4':
            return
        __ipv4 = {
            'nw_src'     : '178.0.0.1',
            'nw_dst'     : '178.0.0.2',
            'nw_ttl'     : '128',
            'nw_tos'     : '0'  , 
            'nw_proto'   : '17',
            'nw_frag'    : '0',
            'nw_flags'   : '0',
        }
        if flowconfig == None:
            return
        stream.update(__ipv4)
        if 'hostsrc' in stream:
            stream['nw_src'] = self.testerlib.getHostIpv4(stream['hostsrc'])
        if 'hostdst' in stream:
            stream['nw_dst'] = self.testerlib.getHostIpv4(stream['hostdst'])

        stream['nw_proto'] = self.__chgProtoStrToValue(stream['L4'])

        for k in __ipv4.keys() :
            if k in flowconfig:
                if k == 'nw_src':
                    stream['nw_src'] = _baselib.getMatchIpAddr(flowconfig[k])
                elif k == 'nw_dst':
                    stream['nw_dst'] = _baselib.getMatchIpAddr(flowconfig[k])
                else:             
                    stream[k] = flowconfig[k].lower()
        
        if 'ip_dscp' in flowconfig:
             stream['nw_tos'] = str(int(flowconfig['ip_dscp']) << 2)
        if 'nw_ecn' in flowconfig:
            stream['nw_tos'] = str(int(stream['nw_tos']) + int(flowconfig['nw_ecn']))
        if 'nw_frag' in flowconfig:
            stream['nw_frag'] = flowconfig['nw_frag'].lower() 
            stream['nw_frag'] = self.__chgIPNewFragStrToValue(stream['nw_frag'])   

    def __setIpv6ByConfig(self, stream, flowconfig):
        if stream['flowType'] != 'ipv6':
            return
        __ipv6 = {
            'ipv6_src'   : '11::11',
            'ipv6_dst'   : '22::22',
            'nw_ttl'     : '128',
            'nw_tos'     : '0'  , 
            'nw_proto'   : '0',
        }
        stream.update(__ipv6)
        if flowconfig == None:
            return
        #if 'hostsrc' in stream:
        #    stream['ipv6_src'] = self.testerlib.getHostIpv6(stream['hostsrc'])
        #if 'hostdst' in stream:
        #    stream['ipv6_dst'] = self.testerlib.getHostIpv6(stream['hostdst'])
        if 'ip_dscp' in flowconfig:
            stream['nw_tos'] = str(int(flowconfig['ip_dscp']) << 2)
        if 'nw_ecn' in flowconfig:
            stream['nw_tos'] = str(int(stream['nw_tos']) + int(flowconfig['nw_ecn']))

        stream['nw_proto'] = self.__chgProtoStrToValue(stream['L4'])

        for k in __ipv6.keys() :
            if k in flowconfig:
                if k == 'ipv6_src' or k == 'ipv6_dst':
                    stream[k] = _baselib.getMatchIpv6Addr(flowconfig[k])
                else:  
                    stream[k] = flowconfig[k]

    def __setArpByConfig(self, stream, flowconfig):
        __arp = {
            'arp_op': '1',
            'arp_spa': '1.1.1.1',
            'arp_tpa': '2.2.2.2',
            'arp_sha': '00:11:11:22:22:33',
            'arp_tha': '00:11:11:22:22:44 ',
        }
        if stream['flowType'] != 'arp':
            return
        stream.update(__arp)
        for k in __arp.keys() :
            if k in flowconfig:
                stream[k] = flowconfig[k]

    def __chgPortStrToInt(self,port):
        ret = re.search(r"(.+)[0-9]", port)
        if not ret:
            return
        ret = re.search(r"(.+)\/(.+)", port)
        if ret:
            portPrefix = ret.group(1)
            portNet = ret.group(2)
            portNum = int(portPrefix,16) & int(portNet,16)
        else:
            portNum = int(port)       
        return portNum  

    def __setUdpByConfig(self, stream, flowconfig):
        __udp = {
            'udp_src'     : 1000,
            'udp_dst'     : 1000
        }
        stream.update(__udp)
        if flowconfig == None:
            return
        for k in __udp.keys() :
            if k in flowconfig:
                stream[k] = self.__chgPortStrToInt(flowconfig[k])

    def __setTcpByConfig(self, stream, flowconfig):
        if stream['L4'] != 'tcp':
            return
        __tcp = {
            'tcp_src'     : 1000,
            'tcp_dst'     : 1000,
            'tcp_flags'   : 'S'
        }
        stream.update(__tcp)
        tcpflag = {
            1: 'F',
            2: 'S',
            4: 'R',
            8: 'P',
            16: 'A',
            32: 'U',
        }
      
        for k in __tcp.keys() :
            if k in flowconfig:
                if k == 'tcp_flags':
                    flag = self.__chgPortStrToInt(flowconfig[k])
                    if flag in tcpflag:
                        stream[k] = tcpflag[flag]
                    else:
                        stream[k] = flowconfig[k][0].upper()
                else:
                    stream[k] = self.__chgPortStrToInt(flowconfig[k])

    def __setSctpByConfig(self, stream, flowconfig):
        if stream['L4'] != 'sctp':
            return
        __sctp = {
            'sctp_src'     : 1000,
            'sctp_dst'     : 1000,
        }
        stream.update(__sctp)
        for k in __sctp.keys() :
            if k in flowconfig:
                stream[k] = self.__chgPortStrToInt(flowconfig[k]) 

    def __setIcmpByConfig(self, stream, flowconfig):
        if stream['L4'] != 'icmp':
            return

        __tmp = {
            'icmp_type': '0',
            'icmp_code': '0'
        }
        stream.update(__tmp)
        for k in __tmp.keys() :
            if k in flowconfig:
                stream[k] = int(flowconfig[k])

    def __setIcmp6ByConfig(self, stream, flowconfig):
        if stream['L4'] != 'icmpv6':
            return
        
        __tmp = {
            'icmpv6_type': '128',
            'icmpv6_code': '0',
            'nd_target': '1::1',
            'nd_sll': '',
            'nd_tll': '',
            'nd_reserved': '0',
            'nd_options_type': '0'
        }
        stream.update(__tmp)
        icmp6ndopts = {'1': 'nd_sll',
                       '2': 'nd_tll',
        }

        for k in __tmp.keys() :
            if k == 'nd_options_type' and k in flowconfig:
                stream[icmp6ndopts[flowconfig[k]]] = '00:11:22:33:44:55'
            elif k in flowconfig:
                if k == 'nd_target':
                    stream[k] = _baselib.getMatchIpv6Addr(flowconfig[k])
                else:
                    stream[k] = flowconfig[k]

    def __setL2ByConfig(self, stream, flowconf):
        self.__setEthByConfig(stream, flowconf)
        self.__setVlanByConfig(stream, flowconf)
        self.__setMplsByConfig(stream, flowconf)

    def __setL3ByConfig(self, stream, flowconf):
        if stream['L3'] == 'ipv4':
            self.__setIpv4ByConfig(stream, flowconf)
        elif stream['L3'] == 'ipv6':
            self.__setIpv6ByConfig(stream, flowconf)
        elif stream['L3'] == 'arp':
            self.__setArpByConfig(stream, flowconf)

    def __setL4ByConfig(self, stream, flowconf):
        if stream['L4'] == 'udp':
            self.__setUdpByConfig(stream, flowconf)
        elif stream['L4'] == 'tcp':
            self.__setTcpByConfig(stream, flowconf)
        elif stream['L4'] == 'sctp':
            self.__setSctpByConfig(stream, flowconf)
        elif  stream['L4'] == 'icmp':
            self.__setIcmpByConfig(stream, flowconf)
        elif  stream['L4'] == 'icmpv6':
            self.__setIcmp6ByConfig(stream, flowconf)
        
    def __setStreamByFlow(self, dut, stream, _flowconfig):
        '''根据flow的配置设置stream
        '''
        __match = _flowconfig['match']
        self.__setL2ByConfig(stream, __match)
        self.__setL3ByConfig(stream, __match)
        self.__setL4ByConfig(stream, __match)

    def __setStreamTunnel(self,stream,info):
        stream['tun_type'] = info['type']
        stream['tun_src'] = info['remote_ip']
        stream['tun_dst'] = info['local_ip']
        if 'in_key' in info:
            stream['tun_id'] = info['in_key']
            
        if 'key' in info:
            stream['tun_id'] = info['key']    
        stream['tun_dl_src'] = info['knl_mac']
        stream['tun_dl_dst'] = info['knl_mac']
        if 'hostsrc' in stream:
            stream['tun_dl_src'] = self.testerlib.getHostMac(stream['hostsrc'])

    def __getDefaultFlowConfig(self, dut,hostsrc, hostdst,config) :
        '''获取流规则的默认配置值
        '''
        #hostsrc = self.testerlib.getHostFirstByLocation(config['inport'])
        #hostdst = self.testerlib.getHostFirstByLocation(config['outport'])
        pkttype = self.__getProtocolByConfig(config)
        flowtype    = (config.get('flowtype','ipv4')).lower()
        _defaultFlowConf = {
                    'match' : {
                        'in_port'     : config["inport"],
                        'nw_src'      : self.testerlib.getHostIpv4(hostsrc),
                        'nw_dst'      : self.testerlib.getHostIpv4(hostdst),
                        'dl_src'      : self.testerlib.getHostMac(hostsrc),
                        'dl_dst'      : self.testerlib.getHostMac(hostdst),
                        'priority'    : '401',
                        'dl_type'     : self.__chgEthProStrToValue(flowtype),
                        'dl_vlan'     : '100',
                        'dl_vlan_pcp' : '7',                     
                        'nw_proto'    : self.__chgProtoStrToValue(pkttype),
                        'nw_tos'      : '68',
                        'ip_dscp'     : '62',
                        'ip_ecn'      : '2',
                        'nw_ecn'      : '3',
                        'nw_ttl'   : '255',
                        'ipv6_src'    : self.testerlib.getHostIpv6(hostsrc),
                        'ipv6_dst'    : self.testerlib.getHostIpv6(hostdst)
                        },
                    'action' : {
                        'type'        : 'fwd',
                        'mod_nw_src'  : self.testerlib.getHostIpv4New(hostsrc),
                        'mod_nw_dst'  : self.testerlib.getHostIpv4New(hostdst),
                        'mod_dl_src'  : self.topolib.topoGetMac(),
                        'mod_dl_dst'  : self.topolib.topoGetMac(),
                        'mod_tp_src'  : self.topolib.topoGetTpSrc(),
                        'mod_tp_dst'  : self.topolib.topoGetTpDst(),
                        'mod_nw_ttl'  : '10',
                        'mod_nw_tos'  : '64',
                        'mod_nw_ecn'  : '1',
                        'mod_vlan_vid'  : '111',
                        'mod_vlan_pcp'  : '1',
                        'dec_ttl'       :'',
                        'output' : config["outport"]
                       }
                }
        
        return _defaultFlowConf
    
    def __fillFlowConfigWithDefault(self, flow, defaultFlowRule) :
        '''检查 flow 配置，填入默认参数
        '''
        flow['match'].setdefault('in_port', defaultFlowRule['match']['in_port'])
        for k in flow['match'].keys() :
            if flow['match'][k] == '' :
                flow['match'][k] = defaultFlowRule['match'][k]
        flow.setdefault("action",dict())
        flow['action'].setdefault('type', 'fwd')
        for k in flow['action'].keys() :
            if flow['action'][k] == '' :
                flow['action'][k] = defaultFlowRule['action'][k]
        if flow['action']['type'] == 'fwd' :
            flow['action'].setdefault('output', defaultFlowRule['action']['output'])
        if flow['action']['type'] == 'drop' :
            flow['action'].setdefault('output', 'drop')

    def __runFlowByConfig(self, dut, hostsrc, hostdst, config):
        _defaultFlowRule = self.__getDefaultFlowConfig(dut,hostsrc, hostdst, config)
        
        _flowconfigList =  config.get('flowRule',list())
        for _flowconfig in _flowconfigList:
            self.__fillFlowConfigWithDefault(_flowconfig, _defaultFlowRule)
            if 'dl_vlan_pcp' in _flowconfig['match']:
                newFlowConf = copy.deepcopy(_flowconfig)
                newFlowConf['match']['dl_vlan_pcp'] = str(int(newFlowConf['match']['dl_vlan_pcp']) + 1)
                self.ovslib.setFlow(dut, config['inport_br'],newFlowConf)

            if (config['tun_port'] == None):
                self.ovslib.setFlow(dut, config['inport_br'], _flowconfig)
            else:
                self.ovslib.setFlow(dut, config['outport_br'], _flowconfig)

    def __clearFlowByConfig(self, dut, config):
        _flowconfigList =  config.get('flowRule',list())
        
        for _flowconfig in _flowconfigList:
            self.ovslib.flowClearConfig(dut,_flowconfig)

        self.ovslib.clearOvsPurge(dut)

    def __checkFlowByConfig(self, dut, config):
        tun_info = config.get('tun_info',None)
        tx1 = 0
        rx1 = 0
        tester = BuiltIn().get_variable_value("${tester}",'trex')
        if tester == 'renix':
            tx1,rx1 = self.testerlib.getPortStats(config['capture_port'])
            logger.info("Stats  :  %d %d "%(tx1,rx1))

        for _flowconfig in config['flowRule']:
            tx,rx = self.testerlib.getStreamStats(_flowconfig['stream'])       
            logger.info("Stats  :  %d %d "%(tx,rx))

            #renix测试仪pcap格式发包，stream上没有收包计数，使用端口计数
            if rx == 0 and rx1 > 0:
                rx = rx1

            if config['capture']:
                pkt_num = 0
                for i in range(0,1000):
                    pkt = self.testerlib.getCapturePacket(config['capture_port'])
                    if pkt == None : break
                    encap = self.__isOutputTun(config) #封装方向
                    decap = self.__isInputTun(config) #解封装方向
                    if self.ovslib.flowCheckPacket(dut,pkt['binary'],_flowconfig,encap,decap,tun_info) :
                        pkt_num += 1
                        if pkt_num == 1:
                            logger.info("[OvsTestlib]Capture match packet:")
                            logger.info(pkt)
                    if pkt_num >= 30: break
                logger.info("[OvsTestlib]Capture packet matched %d"%(pkt_num))
                BuiltIn().should_be_true(pkt_num >= 30 or pkt_num > rx - 2 ,"Fail: Packet can't match flow (%d)"%pkt_num)
            #if self.__isOutputTun(config):
            #   self.ovslib.checkTunEncapFlowByConfig(dut,tx,rx,_flowconfig,config)
            #else:             
            if config.get('hw_offload',False):
                self.ovslib.checkDpFlowByConfig(dut,tx,rx,_flowconfig,config.get("tun_info",None))
            else:
                self.ovslib.checkFlowByConfig(dut,tx,rx,_flowconfig)
                
        return True

    def __isChangePacket(self,config):
        #封装、解封装action
        if 'tun_port' in config:
            return True
        
        for f in config['flowRule']:
            if self.ovslib.isFlowChangePacket(f):
                return True
        return False

    def __checkConfig(self,config):
        # 如果没有流配置，需要初始化一个默认流
        if config.get('flowRule',None) == None:
            logger.warn('No flow rule in config !')
            config['flowRule'] = [{
                'match' : {'in_port': None},
                'action': {'output': None}
            }]
        #BuiltIn().should_be_true(config['outport_br'] == config['inport_br'], \
        #        "Input port and Out port is not match!")
        for r in config['flowRule']:
            if 'nw_ecn' in r['match'] and int(r['match']['nw_ecn']) == 2:
                logger.warn('nw_ecn is 2 :  bug for tester !')

    def testOvsFlow(self,config=None):
        '''测试flow生成 软件-网络组
        
        | 应用场景1 ：
        |                             +---------------+
        | PC1-SRC -- <hostsrc1> ---+  | +--dut1-----+ |                  
        |                          |--|-|fei1   fei2|-|----<hostdst> -- <PC2-DST>
        |            <hostsrc2> ---+  | +--CGN------+ |
        |                             +---------------+
        |
        | hostsrc1 | 入接口下一跳 |
        | hostsrc2 | 当下一跳为源地址时，可指定多个 |
        | OVS | 待测设备（dut1） |
        | fei1 | 入接口 |
        | fei2 | 出接口 |
        | hostdst | 出接口下一跳 |
        
        | 验证内容和步骤：
        | 步骤1  | 配置          | 按照参数指定   |
        | 步骤2  | 发送出向流    | 发送出向流           |
        | 步骤3  | 检查条目      | 检查期望的条目       |
        | 步骤4  | 检查出向报文  | 检查流的出入向统计   |
        | 步骤5  | 发送入向流    | 发送出向流           |
        | 步骤6  | 检查入向报文  | 检查流的出入向统计   |
        | 步骤7  | 检查          | 检查流的出入向统计   |
        | 步骤8  | 检查策略      | 参考 Domain Check关键字    |
        | 步骤9  | 删除额外配置  | 清案例额外配置       |
        
        | 关键参数信息：
        | 下一跳    | hostsrc，hostdst |
        | 流量      | srcip,ipinc,srcport等 |
        | ovs的配置 | pool,domain,user |
        | 功能 | 流量验证方向，是否验证老化 |
        
        | 必要参数默认值获取方法：
        | 测试仪PORT1 | hostsrc的接口 |
        | 测试仪PORT2 | hostdst的接口 |
        | fei1 | hostsrc网关地址查询 |
        | dut1 | hostsrc网关地址查询 |
        | dut2 | hostsrc网关地址查询 |
        | fei2 | hostdst网关地址查询 |
        
        Config Keys:
        | 参数名 | 默认值 | 说明 |
        | dut       | hostsrc直连设备 | 单机或者主设备（默认取hostsrc直连dut） |           |
        | flowRule  | None     | 协议( inport=dpdk0 action：output=dpdk1) |
        | protocol  | udp      | 协议(udp/tcp/icmp/nat-tcp/tcp-udp) |           |
        
        流量参数
        | stream    | None     | 预置流名称 |
        | flowtype  | ipv4     | 流类型(ipv4/ipv6/geneve/4in6) |
        | srcip     | hostsrc  | 源地址 |
        | srcport   | 1000     | 源端口 |
        | destip    | hostdst  | 目的地址 |
        | destport  | 1000     | 目的端口 |
        
        config 可以输出的信息：
        
        | flow        | 流列表               |
        
        host 如果是列表，需要保证都是同一个网关ip
        dut        默认取hostsrc直连的设备
        
        注： 不要创建太多的条目， 避免入向流量创建太多
             预置策略仅用于配置， 或判断是否需要检查
        '''
        '''
        config = {
            'flowtype' : 'ipv4',
            'protocol' : 'udp',
            'flowRule' : [
                {
                    'match' : {
                        'in_port'  : '',
                        'nw_src'   : '',
                        'nw_dst'   : '',
                        'dl_dst'   : '',
                        'priority' : '',
                        'dl_type'  : ''
                        },
                    'action' : {
                        'type'   : ''
                       },
                },
                {
                    'match' : {
                        'in_port' : 'dpdk0',
                        'nw_dst' : '178.0.0.3',
                        'dl_dst' : '08:00:27:bb:c0:3c',
                        'priority' : '401',
                        'dl_type' : '0x0800'
                        },
                    'action' : {
                        'type'   : 'drop'
                       },
                }
            ]
        }

        '''
        logger.debug('[testOvsFlow] --------start test-------')
        if config == None :         
            config = {
            'flowtype' : 'ipv4',
            'protocol' : 'udp',
            'flowRule' : list()
            }
        config.setdefault('flowtype','ipv4')
        config.setdefault('protocol','udp')
        config.setdefault('direct','out') 

        '''underlay'''
        #dst = BuiltIn().get_variable_value("$ethdst","04:02:03:04:05:06")
           
        self.__initlib()
        #获取当前路径
        _a = self.topolib.TopoGetLastToptype()
        itype = self.dutlib.dutGetType(_a)
        config['duttype'] = itype
        
        BuiltIn().should_not_be_empty(_a,"[OvsTestlib]No device")
        hostsrc = self.__getHostFirstByDut(_a,1)
        hostdst = self.__getHostFirstByDut(_a,2)

        if "inport" not in config:
            port  = self.topolib.topoGetPort(_a+".1->cha")
            config['inport'] = self.ovslib.getRealPort(_a,port)
            
        if "outport" not in config:
            port = self.topolib.topoGetPort(_a+".2->cha")
            config['outport'] = self.ovslib.getRealPort(_a,port)

        BuiltIn().should_be_true(hostsrc != None,"Can't find Host Source!")
        BuiltIn().should_be_true(hostdst != None,"Can't find Host Destination!")
        BuiltIn().should_be_true(config['inport'] != None,"Can't find inport!")
        BuiltIn().should_be_true(config['outport'] != None,"Can't find outport!")
        
        logger.info("Input Port  : %s"%config['inport'])
        logger.debug("Host Source : %s"%hostsrc)
        logger.debug("Host Dest   : %s"%hostdst)
        logger.info("Input Port  : %s"%config['inport'])
        logger.info("Output Port : %s"%config['outport'])
        info = self.ovslib.getOvsInfo(_a)
        logger.info("Other_config : %s"%str(info['other_config']))
        config['inport_br'] = self.ovslib.getBridgeByPort(_a,config['inport'])
        config['outport_br'] = self.ovslib.getBridgeByPort(_a,config['outport'])

        if 'tun_port' not in config :
            config['tun_port'] = self.ovslib.findInterfaceFirstTunnel(_a)
            config['tun_br']   = self.ovslib.getBridgeByPort(_a,config['tun_port'])
            config['tun_patch']= None #连通inport或outport的接口
            
        #如果有隧道，并且2个端口不在同一个网桥中，测试隧道功能
        if (config['inport_br'] != config['outport_br']) and (config['tun_port'] != None):
            config['tun_info'] = self.ovslib.ovsGetTunnelInfo(_a,config['tun_port'])
            logger.debug("Tunnel Port  : %s"%config['tun_port'])
            logger.debug("Tunnel Br    : %s"%config['tun_br'])
            logger.info(config['tun_info'])
            config['tun_outport_br'] = config['tun_info'].get('knl_intf',None)
            if config['tun_outport_br'] == config['inport_br']:
                #入接口和tunnel出口在同一个网桥,需要修改入接口
                config['tun_outport'] = config['inport']
                if config['tun_br'] == config['outport_br']:
                    config['inport'] = config['tun_port']
                else:
                    #查找两个网桥是否通过patch连通，如果连通则修改网桥
                    p1,p2 = self.ovslib.findPatch(_a,config['tun_br'],config['outport_br'])
                    BuiltIn().should_be_true(p1!=None,"Can't find Patch for %s and %s"%(config['tun_br'],config['outport_br']))
                    logger.info("Find Patch port %s-%s"%(p1,p2))
                    config['tun_patch'] = p1
                    config['tun_port'] = p2
                    config['inport'] = config['tun_port']
                config['inport_br'] = config['outport_br']
                '''overlay 解封装'''
                #dst = BuiltIn().get_variable_value("$ethdst","00:02:03:04:05:06")
            if config['tun_outport_br'] == config['outport_br']:
                #出接口和tunnel出口在同一个网桥
                config['tun_outport'] = config['outport']
                if config['tun_br'] == config['inport_br']:
                    config['outport'] = config['tun_port']
                else:
                    p1,p2 = self.ovslib.findPatch(_a,config['tun_br'],config['inport_br'])
                    BuiltIn().should_be_true(p1!=None,"Can't find Patch for %s and %s"%(config['tun_br'],config['inport_br']))
                    logger.info("Find Patch port %s-%s"%(p1,p2))
                    config['tun_patch'] = p1
                    config['tun_port'] = p2
                    config['outport'] = config['tun_port']
                config['outport_br'] = config['inport_br']
                #dst = BuiltIn().get_variable_value("$ethdst","04:02:03:04:05:06")
            
            #inline方式配置静态ARP
            #self.ovslib.setTnlArp(_a)
            self.ovslib.showTnlArp(_a)
        #不测试隧道就测试普通功能
        else :
            config['tun_port'] = None
            
        #if dst != None:
        #    config['EthDst'] = dst
        if 'EthDst' in config and 'flowRule' in config :
            for i in config['flowRule']:
                if 'eth_dst' in i['match'] :
                    i['match']['eth_dst'] = config['EthDst']
                if 'dl_dst' in i['match'] :
                    i['match']['dl_dst'] = config['EthDst']    
                            
        config['capture'] = self.__isChangePacket(config)    
        self.__checkConfig(config)
                
        #根据入参配置
        cfg = self.__runFlowByConfig(_a,hostsrc,hostdst,config)
        self.__createOutStream(_a,hostsrc,hostdst,config)
        self.__createInStream(_a,hostsrc,hostdst,config)
        self.testerlib.saveConfig()
        tt = self.__getTrafficSleeptimeByConfig(config)
        outprofile = config['outprofile']
        portdst = self.testerlib.getHostRealPort(hostdst)
        #self.ovslib.ovsLoggerDebug(_a,config['inport_br'])
        ok = 0
        success_num = 0
        for i in range(0,5): #如果失败则尝试5次, 统计计数存在问题，没有清除
            try:
                if config['capture']:
                    #logger.info("[No.%d]: start Capture!"%(i))
                    self.testerlib.startCapture(portdst)
                    config['capture_port'] = portdst
                #发流
                #logger.debug("[No.%d]: infomation of before stream !"%i)
                #self.testerlib.testerLoggerDebug()
                config['capture_port'] = portdst
                self.testerlib.startProfile(outprofile)
                logger.info("[No.%d]: Start traffic time %d!"%(i,tt))
                time.sleep(tt)
                logger.debug("[No.%d]: infomation at stream on !"%i)
                self.testerlib.testerLoggerDebug()
                self.ovslib.ovsLoggerDebug(_a,config['inport_br'])
                if 'tun_outport_br' in config :
                    self.ovslib.ovsLoggerDebug(_a,config['tun_outport_br'])
                self.testerlib.stopProfile(outprofile)
                if config['capture']:
                    logger.info("[No.%d]: Stop Capture!"%(i))
                    self.testerlib.stopCapture(portdst)
                    status = self.testerlib.getCaptureStatus(portdst)
                    logger.info(status)
                #根据输入验证结果
   
                if self.__checkFlowByConfig(_a,config) != True and success_num >= 1: #已经成功offload后正常不会失败
                    logger.info("[No.%d]: Check flow fail!, not continuous success"%i)
                    break
                
                success_num = success_num + 1
                logger.info("[No.%d]: Check flow ok! success num : %d"%(i, success_num))
                if (success_num >= 2):     #连续成功两次，防止中间有震荡
                    ok = 1
                    break
                logger.info("[No.%d]: Check flow ok!"%i)
            except Exception :
                logger.info("[No.%d]: Check error, Exception!!!"%i)
                self.testerlib.testerLoggerDebug()
                self.ovslib.ovsLoggerDebug(_a,config['inport_br'])
        self.__clearFlowByConfig(_a,config)
        BuiltIn().should_be_true(ok,"[testOvsFlow]Check flow Error!")
        logger.info("[testOvsFlow] -----------test ok----------")

    def __runPmdFlowByConfig(self, dut, hostsrc, hostdst, config):
        _defaultFlowRule = self.__getDefaultFlowConfig(dut,hostsrc, hostdst, config)
        flowtype    = (config.get('flowtype','ipv4')).lower()
        _flowconfigList =  config.get('flowRule',list())
        for _flowconfig in _flowconfigList:
            self.__fillFlowConfigWithDefault(_flowconfig, _defaultFlowRule)
            _flow = self.pmdlib.flowTransOvsToDpdkRule(_flowconfig,flowtype)
            ruleid = self.pmdlib.setFlow(dut,config['inport'],_flow)
            _flowconfig['ruleid'] = ruleid
    
    def __clearPmdFlowByConfig(self, dut, config):
        if config == None :
            return
        _flowconfigList =  config.get('flowRule',list())
        for _flowconfig in _flowconfigList:
            self.pmdlib.flowDestroy(dut,config['inport'],_flowconfig['ruleid'])

    def __checkPmdFlowByConfig(self, dut, config):
        for _flowconfig in config['flowRule']:
            tx,rx = self.testerlib.getStreamStats(_flowconfig['stream'])
            if 'ruleid' not in _flowconfig:
                AssertionError("Can't find ruleid for flow")
            if config['capture']:
                pkt_num = 0
                for i in range(0,1000):
                    pkt = self.testerlib.getCapturePacket(config['capture_port'])
                    if pkt == None : break
                    tun = self.__isOutputTun(config)
                    if self.ovslib.flowCheckPacket(dut,pkt['binary'],_flowconfig,tun) :
                        pkt_num += 1
                        if pkt_num == 1:
                            logger.info("[OvsTestlib]Capture match packet:")
                            logger.info(pkt)
                    if pkt_num >= 50: break
                logger.info("[OvsTestlib]Capture packet matched %d"%(pkt_num))
                BuiltIn().should_be_true(pkt_num >= 50 or pkt_num > rx - 2 ,"Packet can't match flow (%d)"%pkt_num)
            self.pmdlib.checkFlowByConfig(dut, tx, rx,config['inport'],_flowconfig)

    def testPmdFlow(self,config=None):
        '''测试flow生成 软件-网络组
        '''
        logger.debug('[testOvsFlow] --------start test-------')
        if config == None :         
            config = {
            'flowtype' : 'ipv4',
            'protocol' : 'udp',
            'tun_type' : 'geneve',
            'flowRule' : list()
            }      
        self.__initlib()
        config.setdefault('flowtype','ipv4')
        config.setdefault('protocol','udp')
        config.setdefault('direct','out') 

        dst = BuiltIn().get_variable_value("${ethdst}","04:02:03:04:05:06")
        if dst != None:
            config['EthDst'] = dst
        if 'EthDst' in config and 'flowRule' in config :
            for i in config['flowRule']:
                if 'eth_dst' in i['match'] :
                    i['match']['eth_dst'] = config['EthDst']
                if 'dl_dst' in i['match'] :
                    i['match']['dl_dst'] = config['EthDst']

        #获取当前路径
        _a = self.topolib.TopoGetLastToptype()
        itype = self.dutlib.dutGetType(_a)
        config['duttype'] = itype
        if itype != 'testpmd':
            logger.warn("[testPmdFlow] the device %s(%s) type is not testpmd!"%(_a,itype))
            return
        BuiltIn().should_not_be_empty(_a,"[OvsTestlib]No device")
        hostsrc = self.__getHostFirstByDut(_a,1)
        hostdst = self.__getHostFirstByDut(_a,2)
        config['lib'] = self.pmdlib
        
        if "inport" not in config:
            port  = self.topolib.topoGetPort(_a+".1->cha")
            config['inport'] = self.pmdlib.getRealPort(_a,port)
            
        if "outport" not in config:
            port = self.topolib.topoGetPort(_a+".2->cha")
            config['outport'] = self.pmdlib.getRealPort(_a,port)
        

        BuiltIn().should_be_true(hostsrc != None,"Can't find Host Source!")
        BuiltIn().should_be_true(hostdst != None,"Can't find Host Destination!")
        BuiltIn().should_be_true(config['inport'] != None,"Can't find inport!")
        BuiltIn().should_be_true(config['outport'] != None,"Can't find outport!")
        config['capture'] = self.__isChangePacket(config)
        logger.info("Input Port  : %s"%config['inport'])
        logger.debug("Host Source : %s"%hostsrc)
        logger.debug("Host Dest   : %s"%hostdst)
        logger.info("Input Port  : %s"%config['inport'])
        logger.info("Output Port : %s"%config['outport'])
        if 'tun_port' not in config :
            config['tun_port'] = None
                
        #根据入参配置
        if not self.__streamOnly():
            cfg = self.__runPmdFlowByConfig(_a,hostsrc,hostdst,config)
        self.__createOutStream(_a,hostsrc,hostdst,config)
        self.testerlib.saveConfig()
        tt = self.__getTrafficSleeptimeByConfig(config)
        outprofile = config['outprofile']
        portdst = self.testerlib.getHostRealPort(hostdst)
        #self.ovslib.ovsLoggerDebug(_a,config['inport_br'])
        ok = 0
        for i in range(0,2): #如果失败则尝试5次, 统计计数存在问题，没有清除
            try:
                if config['capture']:
                    #logger.info("[No.%d]: start Capture!"%(i))
                    self.testerlib.startCapture(portdst)
                    config['capture_port'] = portdst
                #发流
                #logger.debug("[No.%d]: infomation of before stream !"%i)
                #self.testerlib.testerLoggerDebug()
                self.testerlib.startProfile(outprofile)
                logger.info("[No.%d]: Start traffic time %d!"%(i,tt))
                time.sleep(tt)
                logger.debug("[No.%d]: infomation at stream on !"%i)
                self.testerlib.testerLoggerDebug()
                self.testerlib.stopProfile(outprofile)
                if config['capture']:
                    logger.info("[No.%d]: Stop Capture!"%(i))
                    self.testerlib.stopCapture(portdst)
                    status = self.testerlib.getCaptureStatus(portdst)
                    logger.info(status)
                #根据输入验证结果
                if not self.__streamOnly():
                    self.__checkPmdFlowByConfig(_a,config)
                logger.info("[No.%d]: Check flow ok!"%i)
                ok = 1
                break
            except Exception :
                logger.info("[No.%d]: Check error!"%i)
                self.testerlib.testerLoggerDebug()
        if not self.__streamOnly():
            self.__clearPmdFlowByConfig(_a,config)
        BuiltIn().should_be_true(ok,"[testOvsFlow]Check flow Error!")
        logger.info("[testOvsFlow] -----------test ok----------")

    def __jaguarCheckFlowByConfig(self, dut, flowConfig):
        tx,rx = self.testerlib.getStreamStats(flowConfig['stream'])
        logger.warn("Stats  :  tx = %d, rx = %d "%(tx,rx))

        tester = BuiltIn().get_variable_value("${tester}",'trex')        
        if (tester == 'renix'): #renix 文件格式发包stream上没有rx统计，需要获取端口上的计数
            tx1,rx1 = self.testerlib.getPortStats(flowConfig['capture_port'])
            logger.warn("Stats  :  tx1 = %d, rx1 = %d"%(tx1,rx1))
        
        #drop
        if flowConfig['chkpkt'] == None:
            flowConfig.setdefault('action', 'drop')
            flowConfig.setdefault('capture', 'False')
            
        if flowConfig.get('capture', True) == True:
            pkt_num = 0
            for i in range(0,1000):
                pkt = self.testerlib.getCapturePacket(flowConfig['capture_port'])
                if pkt == None : break
                if self.jaguarlib.jaguarCheckPacket(dut,pkt['binary'],flowConfig) == True:
                    pkt_num += 1
                    if pkt_num == 1:
                        logger.info("[OvsTestlib]Capture match packet:")
                        logger.info(pkt)
                if pkt_num >= 100: break
            logger.info("[OvsTestlib]Capture packet matched %d"%(pkt_num))
            BuiltIn().should_be_true(pkt_num != 0 and (pkt_num >= 10 or pkt_num > rx - 2),"Packet can't match flow (%d)"%pkt_num)
            rx = pkt_num

        self.jaguarlib.jaguarCheckFlowByConfig(dut,tx,rx,flowConfig)  

    
    def testSimDevConf(self,config=None, version=None, multi=False):
        logger.debug('[testSimDevConf] --------start test-------')
        self.__initlib()
        #获取当前路径
        _a = self.topolib.TopoGetLastToptype()
        if version == None:
            self.jaguarlib.jaguarClearConfigAll(_a)      
        BuiltIn().should_not_be_empty(_a,"[OvsTestlib]No device")
        self.jaguarlib.jaguarRunConfig(_a, config)
        ok = self.jaguarlib.jaguarCheckConfig(_a, True)
        BuiltIn().should_be_true(ok,"[testSimDevConf]Check sim config Error!")
        self.jaguarlib.jaguarClearConfig(_a, config)

    def testSimDevFlow(self,config=None, flow=None):
        logger.debug('[testSimDevFlow] --------start test-------')
        self.__initlib()
        #获取当前路径
        _a = self.topolib.TopoGetLastToptype()
        __config = config
        if 'packet' in config:
            flow = config['packet']
        if 'corsica' in config:
            __config = config['corsica']
        BuiltIn().should_not_be_empty(_a,"[testSimDevFlow]No device")
        portsrc = self.testerlib.findPortByLocation(self.topolib.topoGetPort("{}.{}->{}.{}".format('cha',1,_a,1)))
        portdst = self.testerlib.findPortByLocation(self.topolib.topoGetPort("{}.{}->{}.{}".format('cha',2,_a,2)))
        
        #flow['capture'] = self.__isChangePacket(flow)

        logger.debug("Host Source : %s"%portsrc)
        logger.debug("Host Dest   : %s"%portdst)
       
        #self.jaguarlib.jaguarClearConfigAll(_a)
     
        self.jaguarlib.jaguarRunConfig(_a, __config)
        jaguar_config = copy.deepcopy(config)
  
        #ok = self.jaguarlib.jaguarCheckConfig(_a, True)
        #BuiltIn().should_be_true(ok,"[testSimDevFlow]Check sim config Error!")
    
        self.__createCustomStream(_a, portsrc, portdst, flow)
        
        tt = self.__getTrafficSleeptimeByConfig(config)
        outprofile = flow['outprofile']
        self.testerlib.saveConfig()
        #self.ovslib.ovsLoggerDebug(_a,config['inport_br'])
        ok = 0
        for i in range(0,2): #如果失败则尝试5次, 统计计数存在问题，没有清除
            try:
                if flow.get('capture', True):
                    #logger.info("[No.%d]: start Capture!"%(i))
                    self.testerlib.startCapture(portdst)
                    flow['capture_port'] = portdst
                flow['capture_port'] = portdst
                #发流
                #logger.debug("[No.%d]: infomation of before stream !"%i)
                #self.testerlib.testerLoggerDebug()
                self.testerlib.startProfile(outprofile)
                logger.info("[No.%d]: Start traffic time %d!"%(i,tt))
                time.sleep(tt)
                logger.debug("[No.%d]: infomation at stream on !"%i)
                self.testerlib.testerLoggerDebug()
                #self.ovslib.ovsLoggerDebug(_a,config['inport_br'])
                #if 'tun_outport_br' in config :
                #    self.ovslib.ovsLoggerDebug(_a,config['tun_outport_br'])
                self.testerlib.stopProfile(outprofile)
                if flow.get('capture', True):
                    logger.info("[No.%d]: Stop Capture!"%(i))
                    self.testerlib.stopCapture(portdst)
                    status = self.testerlib.getCaptureStatus(portdst)
                    logger.warn(status)
                #根据输入验证结果
                self.__jaguarCheckFlowByConfig(_a,flow)
                logger.info("[No.%d]: Check flow ok!"%i)
                ok = 1
                break
            except Exception :
                logger.warn("[No.%d]: Check flow Error and retry!"%i)
                #self.testerlib.testerLoggerDebug()
                #self.ovslib.ovsLoggerDebug(_a,config['inport_br'])

        #性能测试要保证接收端口有流量
        if 'performance' in config:
            self.testPerformance(config,portdst,flow) 
        self.jaguarlib.jaguarClearConfig(_a,__config)
        BuiltIn().should_be_true(ok,"[testSimDevFlow]Check flow Error!")
        logger.info("[testSimDevFlow] -----------test ok----------")

    def testPerformance(self,config=None, port=None,flow=None):
        '''如果测试流量正常，开始测试
        '''
        logger.debug('[testSimDevFlow] --------start test-------')
        self.__initlib()
        tt = self.__getTrafficSleeptimeByConfig(config)
        outstream = flow['outstream']
        self.testerlib.saveConfig()
        ok = 0
        current = 10
        laststat  = None
        okstat = 0
        errorstat = 100
        for i in range(0,10):
            try:
                self.testerlib.setStreamSpeed(outstream,'persent',current)
                self.testerlib.startStream(outstream)
                logger.info("[No.%d]: Start traffic time %d!"%(i,tt))
                time.sleep(tt) #跳过初始一段不稳定期
                info = self.testerlib.getPortStatsMore(port,clear=1)
                time.sleep(tt)
                info = self.testerlib.getPortStatsMore(port)
                laststat = info
                rxerror = False
                for j in range(0,10): #检查5s一直收包为0则失败退出
                    time.sleep(0.5)
                    info = self.testerlib.getPortStatsMore(port)
                    if info['rx'] == 0:
                        logger.warn("[No.%d]: Rx Error %s!"%(j,str(info)))
                        rxerror = True
                        continue
                    rxerror = False
                    if laststat['rx_bps'] > 0 and (info['rx_bps'] -laststat['rx_bps']) / laststat['rx_bps'] < 0.01:
                        laststat = info
                        break
                    laststat = info
                
                if rxerror: break
                drop  = (info['tx_bps'] -info['rx_bps']) / info['tx_bps'] > 0.01
                if not drop : 
                    okstat = info['RxUtil']
                else :
                    errorstat = info['RxUtil']
                if errorstat - okstat < 0.01: ok =1
                
                if i == 0: # 第一次数据 是100
                    current = info['RxUtil']
                elif i == 1 :
                    if drop : 
                        current = info['RxUtil'] - 5
                    else : 
                        current = info['RxUtil'] + 5
                else:
                    current = (okstat + errorstat)/2
                if current < 0.01 :  current = 0.01
                elif current > 100 :  current = 100
                logger.debug("[No.%d]: infomation at stream on !"%i)
                self.testerlib.testerLoggerDebug()
                self.testerlib.stopStream(outstream)
                if ok : break
            except Exception :
                logger.warn("[No.%d]: Check flow Error and retry!"%i)
        if ok :
            laststat.pop('Result')
            logger.warn("Speed info : %s"%laststat)

if __name__ == '__main__':
    pass
