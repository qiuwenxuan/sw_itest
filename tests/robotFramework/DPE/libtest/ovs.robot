*** Settings ***
Suite Setup       连接设备1
Resource          ../testlib/testlib.robot

*** Test Cases ***
ovsdb更新
    ovsdbUpdate    ${A}

创建端口
    ${config}    Create Dictionary    type=netdev
    Ovs.gotoBridge    ${A}    br-int-test    ${config}
    Ovs.delBridge    ${A}    br-int-test

获取DPDK设备
    ${result}    Ovs.devGetList    ${A}
    log    ${result}

获取隧道接口
    ${result}    Ovs.findInterfaceFirstTunnel    ${A}    br-ext
    log    ${result}
    ${result}    Ovs.findInterfaceFirstTunnel    ${A}    br-int
    log    ${result}

获取端口信息
    ${result}    Ovs.getInterfaceInfo    ${A}    dpdk0
    log    ${result}
    ${result}    Ovs.getInterfaceType    ${A}    dpdk0
    log    ${result}
    ${result}    Ovs.getInterfaceMac    ${A}    dpdk0
    log    ${result}
    ${result}    Ovs.getBridgeByPort    ${A}    dpdk0
    log    ${result}
    ${result}    Ovs.getPortsByBridge    ${A}    br-ext
    log    ${result}
    ${result}    Ovs.getInterfacesByBridge    ${A}    br-ext
    log    ${result}
    ${result}    Ovs.showPortStats    ${A}    br-ext
    log    ${result}

OVS流设置
    ${result}    Ovs.flowTransArgToDict    in_port=dpdk0    -type=fwd    -outport=dpdk1
    log    ${result}
    ${result}    Ovs.flowFraseRuleToDict    cookie=0x0,duration=2.170s, table=0,n_packets=0,n_bytes=0,in_port=2 actions=output:dpdk0
    log    ${result}
    ${result}    Ovs.flowFraseRuleToDict    cookie=0x0,duration=9.652s, table=0,n_packets=0,n_bytes=0,priority=0 actions=NORMAL
    log    ${result}

获取DPDK端口
    ${result}    findInterface    ${A}    itype=dpdk
    log    ${result}

转换流为字典
    ${result}    flowFraseDpflowTOdict    recirc_id(0),in_port(dpdk0),packet_type(ns=0,id=0),eth(src=00:01:00:00:00:02),eth_type(0x0806), packets:2, bytes:120, used:0.368s, actions:set(eth(src=00:01:00:00:00:04)),clone(tnl_push(tnl_port(vxlan_sys_4789),header(size=50,type=4,eth(dst=00:01:00:00:00:03,src=08:00:27:f9:11:96,dl_type=0x0800),ipv4(src=192.168.2.55,dst=192.168.2.10,proto=17,tos=0,ttl=64,frag=0x4000),udp(src=0,dst=4789,csum=0x0),vxlan(flags=0x8000000,vni=0x64)),out_port(br-ext)),dpdk1)
    log    ${result}

释放端口
    ${result}    ovsPortsRelease    ${A}    0000:00:0a.0
    log    ${result}

获取信息
    ${result}    getOvsInfo    ${A}
    log    ${result}

配置OVS环境
    初始化拓扑TOP11-TOPO
    创建OVS环境    ${A}
    清除OVS环境    ${A}
    清理测试仪

配置OVS-one环境
    初始化拓扑TOP11-TOPO
    创建OVS-ONE环境    ${A}
    清理测试仪

配置OVS-two环境
    初始化拓扑TOP11-TOPO
    创建OVS-DOUBLE环境    ${A}    -tun_type=vxlan
    清理测试仪

配置OVS-three环境
    初始化拓扑TOP11-TOPO
    创建OVS-THREE环境    ${A}    -tun_type=vxlan
    清理测试仪
