*** Settings ***
Suite Setup       清理测试仪
Suite Teardown    清理测试仪
Test Setup        清理测试仪
Test Teardown     清理测试仪
Force Tags        MATCH    FWD
Resource          ../../testlib/testlib.robot
Resource          ../../testlib/features/ovs.robot

*** Variables ***

*** Test Cases ***
ovs_match_00001
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_src=\

ovs_match_00002
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_dst=\

ovs_match_00003
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\

ovs_match_00004
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_src=\    dl_dst=\

ovs_match_00005
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_src=\    dl_type=\

ovs_match_00006
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_dst=\    dl_type=\

ovs_match_00007
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_src=\    dl_dst=\    dl_type=\

ovs_match_00008
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_src=\    dl_type=\

ovs_match_00009
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_dst=\    dl_type=\

ovs_match_00010
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_src=\    nw_dst=\    dl_type=\

ovs_match_00011
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_src=\    dl_src=\    dl_type=\

ovs_match_00012
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_src=\    dl_dst=\    dl_type=\

ovs_match_00013
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_dst=\    dl_src=\    dl_type=\

ovs_match_00014
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_dst=\    dl_dst=\    dl_type=\

ovs_match_00015
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_src=\    nw_dst=\    dl_src=\    dl_type=\

ovs_match_00016
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_src=\    nw_dst=\    dl_dst=\    dl_type=\

ovs_match_00017
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_src=\    dl_src=\    dl_dst=\    dl_type=\

ovs_vxlan_match_00001
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]
    验证ovs-hw-offload流量    fwd    ipv4    udp    vxlan

ovs_match_00018
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_dst=\    dl_src=\    dl_dst=\    dl_type=\

ovs_match_00019
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_src=\    nw_dst=\    dl_src=\    dl_dst=\    dl_type=\

ovs_match_00020
    [Documentation]    *set pass rule match udp_src and udp_dst to stream*
    [Tags]    UDP
    验证ovs-hw-offload流量    fwd    ipv4    udp    udp_src=2025    udp_dst=2026    nw_proto=17    dl_type=0x0800

ovs_match_00022
    [Documentation]    *set pass rule match udp_src and udp_dst to stream*
    [Tags]    UDP
    验证ovs-hw-offload流量    fwd    ipv4    udp    udp_src=2025    udp_dst=4789    nw_proto=17    dl_type=0x0800

ovs_match_00023
    [Documentation]    *set pass rule match udp_src and udp_dst to stream*
    [Tags]    UDP
    验证ovs-hw-offload流量    fwd    ipv4    udp    udp_src=2025    udp_dst=6081    nw_proto=17    dl_type=0x0800

ovs_vxlan_match_00001
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]
    验证ovs-tunnel-hw-offload流量    fwd    ipv4    udp    vxlan

ovs_match_00201
    [Documentation]    *set pass rule match dl_vlan to stream*
    [Tags]    没有预置表项
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_vlan=101

ovs_match_00202
    [Documentation]    *set pass rule match dl_vlan_pcp to stream*
    [Tags]    没有预置表项
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_vlan_pcp=7

ovs_match_00203
    [Documentation]    *set pass rule match vlan_tci to stream*
    [Tags]    没有预置表项
    验证ovs-hw-offload流量    fwd    ipv4    udp    vlan_tci=0x1123/0x1fff

ovs_match_00101
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst with mask to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv6    udp    ipv6_src=\    ipv6_dst=\    dl_type=0x86dd

ovs_match_00102
    [Documentation]    *set pass rule match dl_type to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv6    udp    dl_type=0x86dd

ovs_match_00136
    [Documentation]    *set pass rule match nw_proto to stream*
    [Tags]    HMP    IPV6    ok
    验证ovs-hw-offload流量    fwd    ipv6    HMP    nw_proto=20    dl_type=0x86dd

ovs_match_00140
    [Documentation]    *set pass rule match ip_dscp to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    ip_dscp=16    dl_type=0x0800

ovs_match_00141
    [Documentation]    *set pass rule match ip_dscp to stream*
    [Tags]    IPV6
    验证ovs-hw-offload流量    fwd    ipv6    udp    ip_dscp=32    dl_type=0x86dd

ovs_match_00144
    [Documentation]    *set pass rule match arp_op to stream*
    [Tags]    RAT    OVS    ARP
    验证ovs-hw-offload流量    fwd    arp    udp    dl_type=0x0806    arp_op=1    arp_spa=1.1.1.1    arp_tpa=2.2.2.2    arp_sha=00:11:11:22:22:33    arp_tha=00:11:11:22:22:44

ovs_match_00145
    [Documentation]    *set pass rule match tcp_src and tcp_dst to stream*
    [Tags]    TCP    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    tcp_src=1025    tcp_dst=1026    tcp_flags=syn    nw_proto=6    dl_type=0x0800

ovs_match_00146
    [Documentation]    *set pass rule match tcp_src and tcp_dst with mask to stream*
    [Tags]    TCP
    验证ovs-hw-offload流量    fwd    ipv4    tcp    tcp_src=0x100/0xff00    tcp_dst=0x1/0xff    tcp_flags=0x1/0xff    nw_proto=6    dl_type=0x0800

ovs_match_00151
    [Documentation]    *set pass rule match icmp_type and icmp_code to stream*
    [Tags]    ICMP
    验证ovs-hw-offload流量    fwd    ipv4    icmp    icmp_type=0    icmp_code=100    nw_proto=1    dl_type=0x0800

ovs_mod_00001
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_src=\

ovs_mod_00002
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_dst=\

ovs_mod_00003
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\

ovs_mod_00004
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_dst=\

ovs_mod_00005
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_nw_dst=\

ovs_mod_00006
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_src=\    -mod_dl_dst=\

ovs_mod_00007
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_dl_src=\

ovs_mod_00008
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_dl_dst=\

ovs_mod_00009
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_dst=\    -mod_dl_src=\

ovs_mod_00010
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_dst=\    -mod_dl_dst=\

ovs_mod_00011
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_src=\    -mod_dl_dst=\    -mod_nw_src=\

ovs_mod_00012
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_src=\    -mod_dl_dst=\    -mod_nw_dst=\

ovs_mod_00013
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_src=\

ovs_mod_00014
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_dst=\

ovs_mod_00015
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_src=\    -mod_dl_dst=\    -mod_nw_src=\    -mod_nw_dst=\

ovs_mod_00032
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_src=\    -mod_tp_dst=\

ovs_mod_00033
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_dst=\    -mod_tp_dst=\

ovs_mod_00034
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_tp_dst=\

ovs_mod_00035
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_dst=\    -mod_tp_dst=\

ovs_mod_00036
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_nw_dst=\    -mod_tp_dst=\

ovs_mod_00037
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_src=\    -mod_dl_dst=\    -mod_tp_dst=\

ovs_mod_00038
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_dl_src=\    -mod_tp_dst=\

ovs_mod_00039
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_dl_dst=\    -mod_tp_dst=\

ovs_mod_00040
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_dst=\    -mod_dl_src=\    -mod_tp_dst=\

ovs_mod_00041
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_dst=\    -mod_dl_dst=\    -mod_tp_dst=\

ovs_mod_00042
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_src=\    -mod_tp_src=\

ovs_mod_00043
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_dst=\    -mod_tp_src=\

ovs_mod_00044
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_tp_src=\

ovs_mod_00045
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_dst=\    -mod_tp_src=\

ovs_mod_00046
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_nw_dst=\    -mod_tp_src=\

ovs_mod_00047
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_src=\    -mod_dl_dst=\    -mod_tp_src=\

ovs_mod_00048
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_dl_src=\    -mod_tp_src=\

ovs_mod_00049
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_dl_dst=\    -mod_tp_src=\

ovs_mod_00050
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_dst=\    -mod_dl_src=\    -mod_tp_src=\

ovs_mod_00051
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_dst=\    -mod_dl_dst=\    -mod_tp_src=\

ovs_mod_00052
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_src=\    -mod_tp_src=\    -mod_tp_dst=\

ovs_mod_00053
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_dst=\    -mod_tp_src=\    -mod_tp_dst=\

ovs_mod_00054
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_tp_src=\    -mod_tp_dst=\

ovs_mod_00055
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_dst=\    -mod_tp_src=\    -mod_tp_dst=\

ovs_mod_00056
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_nw_dst=\    -mod_tp_src=\    -mod_tp_dst=\

ovs_mod_00057
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_src=\    -mod_dl_dst=\    -mod_tp_src=\    -mod_tp_dst=\

ovs_mod_00058
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_dl_src=\    -mod_tp_src=\    -mod_tp_dst=\

ovs_mod_00059
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_dl_dst=\    -mod_tp_src=\    -mod_tp_dst=\

ovs_mod_00060
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_dst=\    -mod_dl_src=\    -mod_tp_src=\    -mod_tp_dst=\

ovs_mod_00061
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_dst=\    -mod_dl_dst=\    -mod_tp_src=\    -mod_tp_dst=\

*** Keywords ***
