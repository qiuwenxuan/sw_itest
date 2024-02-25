*** Settings ***
Suite Setup       清理测试仪
Suite Teardown    清理测试仪
Test Setup        清理测试仪
Test Teardown     清理测试仪
Force Tags        MATCH    ACTION
Resource          ../../testlib/testlib.robot
Resource          ../../testlib/features/ovs.robot

*** Variables ***

*** Test Cases ***
ovs_drop_001
    [Documentation]    *match l2 src mac and dst mac to stream action drop*
    [Tags]    ok
    验证ovs-hw-offload流量    drop    ipv4    0   dl_src=\    dl_dst=\    -type=drop

ovs_drop_002
    [Documentation]    *match l3 src dst ip and proto type to stream action drop*
    [Tags]    ok
    验证ovs-hw-offload流量    drop    ipv4    0    nw_src=\    nw_dst=\    dl_type=\    -type=drop

ovs_drop_003
    [Documentation]    *set pass rule match udp_src and udp_dst to stream action drop*
    [Tags]    ok    decap nok    COSSW-15872    
    验证ovs-hw-offload流量    drop    ipv4    udp    udp_src=2025    udp_dst=2026    nw_proto=17    dl_type=\    -type=drop

ovs_drop_004
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst with mask to stream action drop*
    [Tags]    ok
    验证ovs-hw-offload流量    drop    ipv6    HMP    nw_proto=20    ipv6_src=\    ipv6_dst=\    dl_type=0x86dd    -type=drop    

ovs_drop_005
    [Documentation]    *set pass rule match tcp_src and tcp_dst to stream action drop*
    [Tags]    ok    
    验证ovs-hw-offload流量    drop    ipv4    tcp    tcp_src=1025    tcp_dst=1026    nw_proto=6    dl_type=0x0800    -type=drop

ovs_drop_006
    [Documentation]    *set pass rule match sctp_src and sctp_dst with mask to stream action drop*
    [Tags]    nok    COSSW-11352    SCTP
    验证ovs-hw-offload流量    drop    ipv4    sctp    sctp_src=0x100/0xff00    sctp_dst=0x100/0xff00    nw_proto=132    dl_type=0x0800    -type=drop

ovs_drop_007
    [Documentation]    *set pass rule match dl_vlan to stream action drop*
    [Tags]    nok    p4 not support(vxlan)
    验证ovs-hw-offload流量    drop    ipv4    icmp    dl_vlan=101    dl_type=0x8100    -type=drop

ovs_drop_008
    [Documentation]    *set pass rule match icmp_type and icmp_code to stream action drop*
    [Tags]    ok
    验证ovs-hw-offload流量    drop    ipv4    icmp    icmp_type=0    icmp_code=100    nw_proto=1    dl_type=0x0800    -type=drop

*** Keywords ***
