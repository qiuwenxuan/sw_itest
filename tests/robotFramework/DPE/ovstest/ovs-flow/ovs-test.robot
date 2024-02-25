*** Settings ***
#Suite Setup       创建静态路由环境    ${A}    ${B}    line=1
#Suite Teardown    路由环境清配置
Suite Setup       Tester Connect    ${cha1ip}
Suite Teardown    清理测试仪    
Resource          ../../testlib/testlib.robot
Library           SSHLibrary

*** Variables ***

*** Test Cases ***
route-static
    [Setup]
    log    ==${A} ${B}
    ${config}    Create Dictionary    path=${A}->${B}
    testRouteStatic    ${config}

ovs_test_00001
    [Tags]    RAT    OVS
    Open Connection    ${HOST}
    Login    ${USERNAME}    ${PASSWORD}
    ${config}    Create Dictionary    type=netdev
    Ovs.gotoBridge    ${A}    br-int    ${config} 

ovs_test_00002
    [Documentation]    *set pass rule to stream* 
    [Tags]    RAT    OVS
    dutConnect    dut1    ip=${dut1ip}    port=${dut1port}    username=${dut1user}    password=${dut1password}    type=${dut1type}
    ${config}    Create Dictionary    type=netdev
    Ovs.gotoBridge    dut1    br-ext    ${config}
    ${options}    Create Dictionary    dpdk-devargs=0000:00:08.0    n_rxq_desc=256    n_txq_desc=256
    ${config}    Create Dictionary    type=dpdk    options=${options}    ofport_request=${1}
    Ovs.gotoPort    dut1    br-ext    dpdk0    ${config}
    ${options}    Create Dictionary    dpdk-devargs=0000:00:0a.0    n_rxq_desc=256    n_txq_desc=256
    ${config}    Create Dictionary    type=dpdk    options=${options}    ofport_request=${1}
    Ovs.gotoPort    dut1    br-ext    dpdk1    ${config}
    Ovs.setFlow    dut1    br-ext    in_port=1,action=output:2
    ${chaconfig}    chaipv4config.Get Config
    Cha Config    ${chaconfig}
    Send Arp Request    host1
    Ovs.delBridge    dut1    br-ext

ovs_test_00003
    [Documentation]    *set block rule match mac to stream*
    [Tags]    RAT    OVS
    dutConnect    dut1    ip=${dut1ip}    port=${dut1port}    username=${dut1user}    password=${dut1password}    type=${dut1type}
    ${config}    Create Dictionary    type=netdev
    Ovs.gotoBridge    dut1    br-ext    ${config}
    ${options}    Create Dictionary    dpdk-devargs=0000:00:08.0    n_rxq_desc=256    n_txq_desc=256
    ${config}    Create Dictionary    type=dpdk    options=${options}    ofport_request=${1}
    Ovs.gotoPort    dut1    br-ext    dpdk0    ${config}
    ${options}    Create Dictionary    dpdk-devargs=0000:00:0a.0    n_rxq_desc=256    n_txq_desc=256
    ${config}    Create Dictionary    type=dpdk    options=${options}    ofport_request=${1}
    Ovs.gotoPort    dut1    br-ext    dpdk1    ${config}
    Ovs.setFlow    dut1    br-ext    priority=1,in_port=1,dl_dst=08:00:27:d8:e1:ab,action=drop
    #run sys command    ovs-ofctl dump-flows br-ext
    ${chaconfig}    chaipv4config.Get Config
    Cha Config    ${chaconfig}
    ${config}    Create Dictionary    object=port1Traffic    Type=Constant    TrafficLoadUnit=fps    TrafficLoad=1
    ${stream1}    Create Dictionary    flowType=ipv4    framelen=128    EthSrc=001f.5310.521c    EthDst=08:00:27:d8:e1:ab    ethtype=0x0800
    ...    IpSrcAddr=101.0.0.1    IpDstAddr=101.0.0.2    UdpSrcPort=1000    UdpDstPort=1000    UdpSrcPortMode=increment    UdpSrcPortStep=1    UdpSrcPortCount=10
    ${stream}    Create Dictionary    stream1=${stream1}
    ${profile}    Create Dictionary    config=${config}    stream=${stream}
    ${profile1}    Create Dictionary    profile=${profile}
    Tester.createProfile    ${profile1}
    Tester.startProfile    profile
    sleep    10
    Tester.stopProfile    profile
    #Send Arp Request    host1
    #getStreamStats    stream1    port1
    #getStreamStats    stream1    port2
    #Ovs.delBridge    dut1    br-ext

ovs_test_00004
    [Documentation]    *set pass rule match ip protocol to stream*
    [Tags]    RAT    OVS
    dutConnect    dut1    ip=${dut1ip}    port=${dut1port}    username=${dut1user}    password=${dut1password}    type=${dut1type}
    ${config}    Create Dictionary    type=netdev
    Ovs.gotoBridge    dut1    br-ext    ${config}
    ${options}    Create Dictionary    dpdk-devargs=0000:00:08.0    n_rxq_desc=256    n_txq_desc=256
    ${config}    Create Dictionary    type=dpdk    options=${options}    ofport_request=${1}
    Ovs.gotoPort    dut1    br-ext    dpdk0    ${config}
    ${options}    Create Dictionary    dpdk-devargs=0000:00:0a.0    n_rxq_desc=256    n_txq_desc=256
    ${config}    Create Dictionary    type=dpdk    options=${options}    ofport_request=${1}
    Ovs.gotoPort    dut1    br-ext    dpdk1    ${config}
    Ovs.setFlow    dut1    br-ext    priority=1,in_port=2,dl_type=0x0800,nw_dst=101.0.0.2,action=output:1
    #run sys command    ovs-ofctl dump-flows br-ext
    showDumpFlows    dut1    br-ext
    ${chaconfig}    chaipv4config.Get Config
    Cha Config    ${chaconfig}
    ${config}    Create Dictionary    object=port1Traffic    Type=Constant    TrafficLoadUnit=fps    TrafficLoad=1
    ${stream1}    Create Dictionary    flowType=ipv4    framelen=128    EthSrc=001f.5310.521c    EthDst=08:00:27:a2:42:de
    ...    IpSrcAddr=101.0.0.1    IpDstAddr=101.0.0.2    UdpSrcPort=1000    UdpDstPort=1000      L2=Ethernet    L3=IPv4    L4=UDP    IpProtocolType=udp
    ${stream}    Create Dictionary    stream1=${stream1}
    ${profile}    Create Dictionary    config=${config}    stream=${stream}
    ${profile1}    Create Dictionary    profile=${profile}
    Tester.createProfile    ${profile1}
    Tester.startProfile    profile
    sleep    10
    Tester.stopProfile    profile
    #Send Arp Request    host1 
    #getStreamStats    stream1    port1
    #getStreamStats    stream1    port2
    #Ovs.delBridge    dut1    br-ext

ovs_test_00005
    [Documentation]    *set 2 different ovs rule to match stream original tester*
    [Tags]    RAT    OVS
    dutConnect    dut1    ip=${dut1ip}    port=${dut1port}    username=${dut1user}    password=${dut1password}    type=${dut1type}
    ${config}    Create Dictionary    type=netdev
    Ovs.gotoBridge    dut1    br-ext    ${config}
    ${options}    Create Dictionary    dpdk-devargs=0000:00:08.0    n_rxq_desc=256    n_txq_desc=256
    ${config}    Create Dictionary    type=dpdk    options=${options}    ofport_request=${1}
    Ovs.gotoPort    dut1    br-ext    dpdk0    ${config}
    ${options}    Create Dictionary    dpdk-devargs=0000:00:0a.0    n_rxq_desc=256    n_txq_desc=256
    ${config}    Create Dictionary    type=dpdk    options=${options}    ofport_request=${1}
    Ovs.gotoPort    dut1    br-ext    dpdk1    ${config}
    Ovs.setFlow    dut1    br-ext    priority=1,in_port=2,dl_type=0x0800,nw_dst=101.0.0.2,action=output:1
    Ovs.setFlow    dut1    br-ext    priority=2,in_port=2,dl_dst=08:00:27:a2:42:de,action=drop
    showDumpFlows    dut1    br-ext
    ${chaconfig}    chaipv4config.Get Config
    Cha Config    ${chaconfig}
    ${config}    Create Dictionary    object=port1Traffic    Type=Constant    TrafficLoadUnit=fps    TrafficLoad=1
    ${stream1}    Create Dictionary    flowType=ipv4    framelen=128    EthSrc=001f.5310.521c    EthDst=08:00:27:a2:42:de
    ...    IpSrcAddr=101.0.0.1    IpDstAddr=101.0.0.2    UdpSrcPort=1000    UdpDstPort=1000      L2=Ethernet    L3=IPv4    L4=UDP    IpProtocolType=udp
    ${stream}    Create Dictionary    stream1=${stream1}
    ${profile}    Create Dictionary    config=${config}    stream=${stream}
    ${profile1}    Create Dictionary    profile=${profile}
    Tester.createProfile    ${profile1}
    Tester.startProfile    profile
    sleep    10
    Tester.stopProfile    profile

ovs_test_00006
    [Documentation]    *set 2 different ovs rule to match stream trex*
    [Tags]    RAT    OVS
    dutConnect    dut1    ip=${dut1ip}    port=${dut1port}    username=${dut1user}    password=${dut1password}    type=${dut1type}
    ${config}    Create Dictionary    type=netdev
    Ovs.gotoBridge    dut1    br-ext    ${config}
    ${options}    Create Dictionary    dpdk-devargs=0000:00:08.0    n_rxq_desc=256    n_txq_desc=256
    ${config}    Create Dictionary    type=dpdk    options=${options}    ofport_request=${1}
    Ovs.gotoPort    dut1    br-ext    dpdk0    ${config}
    ${options}    Create Dictionary    dpdk-devargs=0000:00:0a.0    n_rxq_desc=256    n_txq_desc=256
    ${config}    Create Dictionary    type=dpdk    options=${options}    ofport_request=${1}
    Ovs.gotoPort    dut1    br-ext    dpdk1    ${config}
    Ovs.setFlow    dut1    br-ext    priority=1,in_port=1,dl_type=0x0800,nw_dst=178.0.0.2,action=output:2
    #Ovs.setFlow    dut1    br-ext    priority=2,in_port=1,dl_dst=08:00:27:a2:42:de,action=drop
    showDumpFlows    dut1    br-ext
    ${chaconfig}    chaipv4config.Get Config
    Cha Config    ${chaconfig}
    ${chaconfig}    chaipv4config.Get Profile
    Cha Config    ${chaconfig}
    SendArpRequest
    startProfile    profile1
    Sleep    15s
    stopProfile    profile1
    profileShouldRXeqTx    profile1
    #profileShouldRXeqZero    profile1

ovs_test_00007
    [Documentation]    *stream*
    [Tags]    RAT    OVS
    ${chaconfig}    chaipv4config.Get Config
    Cha Config    ${chaconfig}
    ${config}    Create Dictionary    object=port1Traffic    TrafficLoad=1    TrafficLoadUnit=fps    Type=Constant    FrameNum=2    port=port1
    ${stream1}    Create Dictionary    hostsrc=host1    hostdst=host2    flowType=ipv4    framelen=128    EthSrc=${EMPTY}    EthDst=${EMPTY}    ethtype=${EMPTY}
    ...    vlanid=${EMPTY}    VlanIdMode=${EMPTY}    VlanIdCount=${EMPTY}    VlanIdStep=${EMPTY}    IpSrcAddr=${EMPTY}    IpSrcAddrMode=increment    IpSrcAddrCount=100
    ...    IpSrcAddrStep=0.0.0.1    IpDstAddr=${EMPTY}    IpDstAddrMode=increment    IpDstAddrCount=100    IpDstAddrStep=0.0.0.1    Ipv6SrcAddress=${EMPTY}    Ipv6SrcAddressMode=${EMPTY}
    ...    Ipv6SrcAddressCount=${EMPTY}    Ipv6SrcAddressStep=${EMPTY}    Ipv6DstAddress=${EMPTY}    UdpSrcPort=${EMPTY}    UdpDstPort=${EMPTY}    UdpSrcPortMode=${EMPTY}    UdpSrcPortStep=${EMPTY}
    ...    UdpSrcPortCount=${EMPTY}    TcpDstPort=${EMPTY}    TcpSrcPort=${EMPTY}    TcpSrcPortMode=${EMPTY}    TcpSrcPortStep=${EMPTY}    TcpSrcPortCount=${EMPTY}    IcmpType=${EMPTY}
    ...    IcmpId=${EMPTY}    CustomHeader=${EMPTY}    HexString=${EMPTY}
    ${stream}    Create Dictionary    stream1=${stream1}
    ${profile}    Create Dictionary    config=${config}    stream=${stream}
    createProfile    ${profile}
    createStream    ${profile}    config

ovs_test_00008
    [Documentation]    *stream*
    [Tags]    RAT    OVS
    ${chaconfig}    chaipv4config.Get Config
    Cha Config    ${chaconfig}
    ${config}    Create Dictionary    object=port1Traffic    Type=Constant    TrafficLoadUnit=fps    TrafficLoad=1
    ${stream1}    Create Dictionary    flowType=ipv4    framelen=128    EthSrc=001f.5310.521c    EthDst=08:00:27:a2:42:de
    ...    IpSrcAddr=101.0.0.1    IpDstAddr=101.0.0.2    UdpSrcPort=1000    UdpDstPort=1000      L2=Ethernet    L3=IPv4    L4=UDP    IpProtocolType=udp
    ${stream}    Create Dictionary    stream1=${stream1}
    ${profile}    Create Dictionary    config=${config}    stream=${stream}
    ${profile1}    Create Dictionary    profile=${profile}
    Tester.createProfile    ${profile1}
    Tester.startProfile    profile
    sleep    10
    Tester.stopProfile    profile

ovs_test_00009
    [Documentation]    *setup vxlan env and ovs-ofctl dump-flows*
    [Tags]    RAT    OVS
    #add Bridge br-int/br-tun/br-ext
    dutConnect    dut1    ip=${dut1ip}    port=${dut1port}    username=${dut1user}    password=${dut1password}    type=${dut1type}
    ${config}    Create Dictionary    type=netdev    failmode=standalone
    Ovs.gotoBridge    dut1    br-int    ${config}
    Ovs.gotoBridge    dut1    br-tun    ${config}
    Ovs.gotoBridge    dut1    br-ext    ${config}
    #add Port for Bridge br-ext
    ${options}    Create Dictionary    dpdk-devargs=0000:00:08.0    n_rxq_desc=1024    n_txq_desc=1024
    ${config}    Create Dictionary    type=dpdk    options=${options}    ofport_request=${1}
    Ovs.gotoPort    dut1    br-ext    dpdk0    ${config}
    #add Port for Bridge br-tun
    ${options}    Create Dictionary    remote_ip="192.168.2.10"    local_ip="192.168.2.55"    in_key=100    out_key=100
    ${config}    Create Dictionary    type=vxlan    options=${options}
    Ovs.gotoPort    dut1    br-tun    vxlan0    ${config}
    ${options}    Create Dictionary    peer=patch-tun
    ${config}    Create Dictionary    type=patch    options=${options}
    Ovs.gotoPort    dut1    br-tun    patch-int    ${config}
    #add Port for Bridge br-int
    ${options}    Create Dictionary    peer=patch-int
    ${config}    Create Dictionary    type=patch    options=${options}    ofport_request=${1}
    Ovs.gotoPort    dut1    br-int    patch-tun    ${config}
    ${options}    Create Dictionary    dpdk-devargs=eth_jmnd0,iface=/tmp/sock0,client=1,queues=4
    ${config}    Create Dictionary    type=dpdk    options=${options}    ofport_request=${2}
    Ovs.gotoPort    dut1    br-int    net_jmnd0    ${config}
    ${options}    Create Dictionary    dpdk-devargs=eth_jmnd1,iface=/tmp/sock1,client=1,queues=4
    ${config}    Create Dictionary    type=dpdk    options=${options}    ofport_request=${3}
    Ovs.gotoPort    dut1    br-int    net_jmnd1    ${config}
    ${options}    Create Dictionary    dpdk-devargs=eth_jmnd2,iface=/tmp/sock2,client=1,queues=4
    ${config}    Create Dictionary    type=dpdk    options=${options}    ofport_request=${4}
    Ovs.gotoPort    dut1    br-int    net_jmnd2    ${config}
    ${options}    Create Dictionary    dpdk-devargs=eth_jmnd3,iface=/tmp/sock3,client=1,queues=4
    ${config}    Create Dictionary    type=dpdk    options=${options}    ofport_request=${5}
    Ovs.gotoPort    dut1    br-int    net_jmnd3    ${config}
    #Set Interface pmd-rxq-affinity
    ${options}    Create Dictionary    n_rxq=4
    ${otherconfig}    Create Dictionary    pmd-rxq-affinity="0:4,1:5,2:6,3:7"
    ${config}    Create Dictionary    options=${options}    other_config=${otherconfig}
    Ovs.setInterface    dut1    dpdk0    ${config}
    Ovs.setInterface    dut1    net_jmnd0    ${config}
    Ovs.setInterface    dut1    net_jmnd1    ${config}
    Ovs.setInterface    dut1    net_jmnd2    ${config}
    Ovs.setInterface    dut1    net_jmnd3    ${config}
    #showDumpFlows    dut1    br-ext

*** Keywords ***
