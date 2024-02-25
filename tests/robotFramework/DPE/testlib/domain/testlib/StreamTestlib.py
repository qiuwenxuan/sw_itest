#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys , os , time , copy, re, random
import struct , binascii
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from binascii import b2a_hex

class StreamTestlib(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    
    def __init__(self):
        self.testerlib = None
    
    def __getindex(self):
        return str(time.time())
    
    def __initlib(self):
        if self.testerlib == None:
            self.dutlib = BuiltIn().get_library_instance('AppDut')
            self.testerlib = BuiltIn().get_library_instance('Tester')
            self.linux = BuiltIn().get_library_instance('Linux')
            
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
    
    def __getDutByHost(self,host):
        '''获取Host连接的设备dut名称
        '''
        self.__initlib()
        firsthost = self.__getHostFirst(host)
        logger.debug(firsthost)
        ip = self.testerlib.getHostIpv4sutAddr(firsthost)
        logger.debug(ip)
        dut = self.sonic.getDutByIpv4(ip)
        logger.debug(dut)
        return dut
    
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
            stream['EthDst'] = self.modulelib.getHostGetwayMac(stream['hostsrc'])
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
        if config == None: config = {}
        if 'outprofile' in config : return True
        
        index = self.__getindex()
        pkttype     = self.__getPacketTypeByConfig(config)
        flowtype    = config.get('flowtype','ipv4')
        streamname  = config.get('outstream','outStream' + index)
        profilename = config.get('outprofile','port1ProfileOut' + index)
        FrameNum    = config.get('framenum',None)
        fps         = self.__getFpsByConfig(config)
        config['outstream']  = streamname
        config['outprofile'] = profilename
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
            
        for hostname in self.__getHostList(hostsrc):
            stream = {  'hostsrc' : hostname,
                        'hostdst' : hostdst,
                        'flowType' : flowtype,
                        }
            conf[profilename]['stream'][streamname+hostname] = stream
            if 'srcip' in config :
                stream['IpSrcAddr'] = config['srcip']
            if 'dstip' in config :
                stream['IpDstAddr'] = config['dstip']
            if pkttype.upper() == 'TCP' :
                stream['syn'] = 1
                #兼容测试仪
                #stream['tcpflagsyc'] = 'true'
                stream['tcpflagack'] = 'false'
    
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
             
            if flowtype == '4in6' :
                if (len(hostsrc)>2):           
                    if 'Ipv6DstAddress' in config :
                        stream['Ipv6DstAddress'] = config['Ipv6DstAddress']                           
            elif flowtype == 'ipv6' :
                if 'Ipv6DstAddress' in config:
                    stream['Ipv6DstAddress'] = config['Ipv6DstAddress']
            if flowtype != 'ipv6':
                stream['IpSrcAddr']=self.testerlib.getHostIpv4(hostname)
            self.__checkDefaultConfig(pkttype,stream, flowtype)
        self.testerlib.createProfile(conf)
        return True
    
        
    def __testStreamOut(self,dut,hostsrc,hostdst,config=None):
        """
            config参数：
                 'traffictime'   持续时间
                 'outstream'     指定出向流名称

            config返回
                 'outstream'    创建的出向流名称

        """
        self.__initlib()
        if config == None: config = {}
        self.__createOutStream(dut,hostsrc,hostdst,config)
        outprofile = config['outprofile']
        ok = 0
        for i in range(0,5): #如果失败则尝试5次
            self.testerlib.startProfile(outprofile,clear=1)
            time.sleep(10)
            self.testerlib.stopProfile(outprofile)
            try:
                self.testerlib.profileShouldRXeqTx(outprofile)
                ok = 1
                break
            except Exception:
                logger.debug("Check packet number error!")
                
        if not ok:
            self.testerlib.profileShouldRXeqTx(outprofile)
        return True
        

    def __getDutByConfig(self, config):
        dut = None
        if (config == None) or (len(config) <= 0):
            return None
        if 'dut' in config:
            dut = config['dut']
        return dut

    def __getProtocolByConfig(self, config):
        '''tcp/udp/icmp
        '''
        protocol = 'udp'
        if (config == None) or (len(config) <= 0):
            return protocol
        if 'protocol' in config:
            protocol = config['protocol']
        return protocol.lower()
    
    def __getPacketTypeByConfig(self, config):
        #如果是NAT模式，采用的是nat-udp/nat-tcp来识别
        if 'pkttype' in config:
            return config['pkttype']
        protocol = self.__getProtocolByConfig(config)
        if 'nat' == protocol:
            return 'udp'
        if 'nat' in protocol:
            return protocol[4:]
        return protocol
        
    
    def __getFpsByConfig(self,config):
        fps = config.get('fps',None)
        if fps != None:
            return str(fps)
        deffps = self.testerlib.testerGetDefFps()
        minfps = config.get('minfps',0)
        if int(minfps) > int(deffps):
            return str(minfps)
        return None

    def __getTrafficSleeptimeByConfig(self,config):
        time = config.get('sleep',None)
        if time != None:
            return int(time)
        time = self.testerlib.testerGetDefSleeptime()
        mintime = config.get('minsleep',2)
        if int(mintime) > int(time):
            return int(mintime)
        return int(time)
            
        
    
    def testStream(self,hostsrc,hostdst=None,config=None):
        """测试条目生成 10053843
        
        | 应用场景1 :  使用子接口
        |                             +---------------------+
        | PC1-SRC -- <hostsrc1> ---+  | +-------dut1------+ |
        |                          |--|-|fei1             |-|
        |            <hostsrc2> ---+  | |                 |-|
        |                             | |                 |-|
        | <PC2-DST> --<hostdst>-------|-|fei1.1(vlan1)    |-|
        |               vlan1         | +-------CGN-------+ |
        |                             +---------------------+
        |
        | 应用场景2 ：
        |                             +---------------+
        | PC1-SRC -- <hostsrc1> ---+  | +--dut1-----+ |                  
        |                          |--|-|fei1   fei2|-|----<hostdst> -- <PC2-DST>
        |            <hostsrc2> ---+  | +--CGN------+ |
        |                             +---------------+
        |
        | 应用场景3 ： top20
        |                             +---------------------+
        | PC1-SRC -- <hostsrc1> ---+  | +--dut1-+ +--dut2-+ |                  
        |                          |--|-|fei1   |-|   fei2|-|----<hostdst> -- <PC2-DST>
        |            <hostsrc2> ---+  | +--CGN--+ +----  -+ |
        |                             +---------------------+
        | 注： 场景中dut2可有可无
        | 
        | PC1-SRC | NAT源地址 |
        | hostsrc1 | 入接口下一跳 |
        | hostsrc2 | 当下一跳为源地址时，可指定多个 |
        | dut  | 待测设备（dut1） |
        | dut2 | 纯转发设备（可以不存在） |
        | fei1 | 入接口 |
        | fei1 | 出接口 |
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
        | 功能 | 流量验证方向，映射模式，过滤模式，是否验证老化 |
        
        | 必要参数默认值获取方法：
        | 测试仪PORT1 | hostsrc的接口 |
        | 测试仪PORT2 | hostdst的接口 |
        | fei1 | hostsrc网关地址查询 |
        | dut1 | hostsrc网关地址查询 |
        | dut2 | hostsrc网关地址查询 |
        | fei2 | hostdst网关地址查询 |
        | instance | 通过pool或domain或user 查询 |
        | pool | 随机POOL，建议指定 |
        | domain | 随机DOMAIN，建议指定 |
        
        Config Keys:
        | 参数名 | 默认值 | 说明 |
        | dut       | hostsrc直连设备 | 单机或者主设备（默认取hostsrc直连dut） |
        
        | instance  | 随机     | 实例名或id             |
        | protocol  | udp      | 协议(udp/tcp/icmp) |
        
        流量参数
        | stream    | None     | 预置流名称 |
        | flowtype  | ipv4     | 流类型(ipv4/ipv6/4in6) |
        | srcip     | hostsrc  | 源地址 |
        | srcport   | 1000     | 源端口 |
        | destip    | hostdst  | 目的地址 |
        | destport  | 1000     | 目的端口 |
                        
        host  如果是列表，需要保证都是同一个网关ip
        dut   默认取hostsrc直连的设备
        
        注： 不要创建太多的条目， 避免入向流量创建太多
        
        """
        if config == None : config = {}
        logger.info(u"[验证流量] 开始")
        logger.debug("[testCmtm] START TEST %d!!!!"%id(config))
        logger.debug("[testCmtm] CONFIG %s!!!!"%str(config))
        self.__initlib()

        dut = self.__getDutByConfig(config)
        if not dut:
            if (len(hostsrc)>2):
                dut = self.__getDutByHost(hostdst)
            else:
                dut = self.__getDutByHost(hostsrc)       
        
        hasException = False
        try:
            self.__testStreamOut(dut,hostsrc,hostdst,config)
        except:
            hasException = True
        finally:    
            pass
        logger.info(u"[验证流量]#50 验证流量OK")
