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
COSSW-16174 验证MATCH项eth_001
    [Documentation]    *match l2 src mac to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    dl_src=\

COSSW-16175 验证MATCH项eth_002
    [Documentation]    *match l2 dst mac to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    dl_dst=\

COSSW-16176 验证MATCH项eth_003
    [Documentation]    *match l2 proto type to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    dl_type=\

COSSW-16177 验证MATCH项eth_004
    [Documentation]    *match l2 src mac and dst mac to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    dl_src=\    dl_dst=\

COSSW-16178 验证MATCH项eth_005
    [Documentation]    *match l2 src mac and proto type to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    dl_src=\    dl_type=\

COSSW-16179 验证MATCH项eth_006
    [Documentation]    *match l2 dst mac and proto type to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    dl_dst=\    dl_type=\

COSSW-16180 验证MATCH项eth_007
    [Documentation]    *match l2 src dst mac and proto type to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    dl_src=\    dl_dst=\    dl_type=\

COSSW-16181 验证MATCH项eth_008
    [Documentation]    *match l2 src mac with full match mask to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    dl_src=00:0B:C4:A8:22:B0/ff:ff:ff:ff:ff:ff

COSSW-16182 验证MATCH项eth_009
    [Documentation]    *match l2 src mac and proto type with full match mask to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    dl_src=00:0B:C4:A8:22:B0/ff:ff:ff:ff:ff:ff    dl_type=\   

COSSW-16183 验证MATCH项eth_0010
    [Documentation]    *match l2 dst mac with full match mask to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    dl_dst=04:02:03:04:05:06/ff:ff:ff:ff:ff:ff

COSSW-16184 验证MATCH项eth_0011
    [Documentation]    *match l2 dst mac and proto type with full match mask to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    icmp    dl_dst=04:02:03:04:05:06/ff:ff:ff:ff:ff:ff    nw_proto=1    dl_type=\       

COSSW-16185 验证MATCH项eth_0012
    [Documentation]    *match l2 src mac with mask to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    icmp    dl_src=00:0B:C4:A8:22:B0/ff:ff:ff:ff:ff:00    nw_proto=1    dl_type=\

COSSW-16186 验证MATCH项eth_0013
    [Documentation]    *match l2 dst mac with mask to stream*
    [Tags]    ok   
    验证ovs-hw-offload流量    fwd    ipv4    icmp    dl_dst=02:0B:C4:A8:22:B0/ff:ff:ff:ff:00:00    nw_proto=1    dl_type=\  

COSSW-16187 验证MATCH项eth_0014
    [Documentation]    *match l2 dst mac with mask to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    icmp    dl_src=00:0B:C4:A8:22:B0/ff:ff:ff:ff:ff:00    dl_dst=02:0B:C4:A8:22:B0/ff:ff:ff:ff:ff:00    nw_proto=1    dl_type=\  

COSSW-16188 验证MATCH项eth_0015
    [Documentation]    *match l2 src dst mac and proto type to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    dl_src=00:0B:C4:A8:22:B0/ff:ff:ff:ff:ff:00    dl_dst=02:0B:C4:A8:22:B0/ff:ff:ff:ff:ff:00    dl_type=\

COSSW-16189 验证MATCH项ipv4_001
    [Documentation]    *match l3 src ip and proto type to stream*
    [Tags]    ok 
    验证ovs-hw-offload流量    fwd    ipv4    0    nw_src=\    dl_type=\

COSSW-16190 验证MATCH项ipv4_002
    [Documentation]    *match l3 dst ip and proto type to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    nw_dst=\    dl_type=\

COSSW-16191 验证MATCH项ipv4_003
    [Documentation]    *match l3 src dst ip and proto type to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    nw_src=\    nw_dst=\    dl_type=\

COSSW-16192 验证MATCH项ipv4_004
    [Documentation]    *match l2 src mac and proto type & l3 src ip to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    nw_src=\    dl_src=\    dl_type=\

COSSW-16193 验证MATCH项ipv4_005
    [Documentation]    *match l2 dst mac and proto type & l3 src ip to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    nw_src=\    dl_dst=\    dl_type=\

COSSW-16194 验证MATCH项ipv4_006
    [Documentation]    *match l2 src mac and proto type & l3 dst ip to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    nw_dst=\    dl_src=\    dl_type=\

COSSW-16195 验证MATCH项ipv4_007
    [Documentation]    *match l2 dst mac and proto type & l3 dst ip to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    nw_dst=\    dl_dst=\    dl_type=\

COSSW-16196 验证MATCH项ipv4_008
    [Documentation]    *match l2 src mac and proto type & l3 src and dst ip to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    nw_src=\    nw_dst=\    dl_src=\    dl_type=\

COSSW-16197 验证MATCH项ipv4_009
    [Documentation]    *match l2 dst mac and proto type & l3 src and dst ip to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    nw_src=\    nw_dst=\    dl_dst=\    dl_type=\

COSSW-16198 验证MATCH项ipv4_010
    [Documentation]    *match l2 src and dst mac and proto type & l3 src ip to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    nw_src=\    dl_src=\    dl_dst=\    dl_type=\

COSSW-16199 验证MATCH项ipv4_012
    [Documentation]    *match l2 src and dst mac and proto type & l3 dst ip to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    nw_dst=\    dl_src=\    dl_dst=\    dl_type=\

COSSW-16200 验证MATCH项ipv4_013
    [Documentation]    *match l2 src and dst mac and proto type & l3 src and dst ip to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    nw_src=\    nw_dst=\    dl_src=\    dl_dst=\    dl_type=\

COSSW-16201 验证MATCH项ipv4_014
    [Documentation]    *match l3 src ip and proto type to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    nw_src=1.1.1.1/24    dl_type=\

COSSW-16202 验证MATCH项ipv4_015
    [Documentation]    *match l3 dst ip and proto type to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    nw_dst=2.2.2.2/24    dl_type=\

COSSW-16203 验证MATCH项ipv4_016
    [Documentation]    *match l3 src ip and proto type to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    nw_src=3.3.3.3/24    nw_dst=4.4.4.4/24    dl_type=\

COSSW-16204 验证MATCH项ipv4_017
    [Documentation]    *match l3 src ip and proto type to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    nw_src=5.5.5.5/23    nw_dst=66.66.66.66/25    dl_type=\  

COSSW-16205 验证MATCH项ipv4_018
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst with mask to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    nw_src=1.1.1.0/24    dl_src=00:0B:C4:A8:22:B0/ff:ff:ff:ff:00:00    nw_dst=2.2.2.0/24    dl_type=\        

COSSW-16206 验证MATCH项udp_001
    [Documentation]    *set pass rule match udp_src and udp_dst to stream*
    [Tags]    ok    decap nok    COSSW-15872    
    验证ovs-hw-offload流量    fwd    ipv4    udp    udp_src=2025    udp_dst=2026    nw_proto=17    dl_type=\

COSSW-16207 验证MATCH项udp_002
    [Documentation]    *set pass rule match udp_src and udp_dst to stream*
    [Tags]    nok    P4 not support(vxlan)
    验证ovs-hw-offload流量    fwd    ipv4    udp    udp_src=2025    udp_dst=4789    nw_proto=17    dl_type=\

COSSW-16208 验证MATCH项udp_003
    [Documentation]    *set pass rule match udp_src and udp_dst to stream*
    [Tags]    nok    P4 not support
    验证ovs-hw-offload流量    fwd    ipv4    udp    udp_src=2025    udp_dst=6081    nw_proto=17    dl_type=\

COSSW-16209 验证MATCH项udp_004
    [Documentation]    *set pass rule match udp_src with mask to stream*
    [Tags]    ok   
    验证ovs-hw-offload流量    fwd    ipv4    udp    udp_src=0x7d1/0xff0    nw_proto=17    dl_type=\

COSSW-16210 验证MATCH项udp_005
    [Documentation]    *set pass rule match udp_dst with mask to stream*
    [Tags]    ok   
    验证ovs-hw-offload流量    fwd    ipv4    udp    udp_dst=0x1b00/0x0f00    nw_proto=17    dl_type=\

COSSW-16211 验证MATCH项udp_006
    [Documentation]    *set pass rule match udp_src and udp_dst with mask to stream*
    [Tags]    ok   
    验证ovs-hw-offload流量    fwd    ipv4    udp    udp_src=0x1110/0xff00    udp_dst=0x1210/0xff00    nw_proto=17    dl_type=\

COSSW-16212 验证MATCH项ipv6_001
    [Documentation]    *match ipv6 to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv6    HMP    nw_proto=20    dl_type=0x86dd

COSSW-16213 验证MATCH项ipv6_002
    [Documentation]    *match ipv6  nw_proto to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv6    HMP    nw_proto=20    ipv6_src=\    dl_type=0x86dd

COSSW-16214 验证MATCH项ipv6_003
    [Documentation]    *match ipv6  nw_proto to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv6    HMP    nw_proto=20    ipv6_dst=\    dl_type=0x86dd    

COSSW-16215 验证MATCH项ipv6_004
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst with mask to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv6    HMP    nw_proto=20    ipv6_src=\    ipv6_dst=\    dl_type=0x86dd    

COSSW-16216 验证MATCH项ipv6_005
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst with mask to stream*
    [Tags]   ok
    验证ovs-hw-offload流量    fwd    ipv6    HMP    ipv6_src=1111::1111:1/50    dl_type=0x86dd      

COSSW-16217 验证MATCH项ipv6_006
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst with mask to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv6    HMP    ipv6_src=2222::2222:2/55    dl_type=0x86dd   

COSSW-16218 验证MATCH项ipv6_007
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst with mask to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv6    HMP    ipv6_src=1111::1111:1/64    ipv6_dst=2222::2222:2/64    dl_type=0x86dd   

COSSW-16219 验证MATCH项ipv6_008
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst with mask to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv6    HMP    ipv6_src=33::1/16    ipv6_dst=44::1/16    dl_type=0x86dd

COSSW-16220 验证MATCH项tcp_001
    [Documentation]    *set pass rule match tcp_src and tcp_dst to stream*
    [Tags]    ok    
    验证ovs-hw-offload流量    fwd    ipv4    tcp    tcp_src=1025    tcp_dst=1026    nw_proto=6    dl_type=0x0800

COSSW-16221 验证MATCH项tcp_002
    [Documentation]    *set pass rule match tcp_src and tcp_dst to stream*
    [Tags]    ok    
    验证ovs-hw-offload流量    fwd    ipv4    tcp    tcp_src=1025    tcp_dst=1026    tcp_flags=syn    nw_proto=6    dl_type=0x0800

COSSW-16222 验证MATCH项tcp_003
    [Documentation]    *set pass rule match tcp_src and tcp_dst with mask to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    tcp_src=0x1100/0x0f00    tcp_dst=0x7d1/0xff00    tcp_flags=0x1/0xff    nw_proto=6    dl_type=0x0800

COSSW-16223 验证MATCH项tcp_004
    [Documentation]    *set pass rule match tcp_src and tcp_dst with mask to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    tcp_src=0x1110/0xff00    tcp_dst=0x7d1/0xfff    tcp_flags=0x1/0xff    nw_proto=6    dl_type=0x0800

COSSW-16224 验证MATCH项tcp_005
    [Documentation]    *set pass rule match sctp_src and sctp_dst with mask to stream*
    [Tags]    nok    P4 not support
    验证ovs-hw-offload流量    fwd    ipv4    sctp    sctp_src=0x1110/0xff00    sctp_dst=0x7d2/0xfff    nw_proto=132    dl_type=0x0800

COSSW-16225 验证MATCH项vlan_001
    [Documentation]    *set pass rule match dl_vlan to stream*
    [Tags]    ok  
    验证ovs-hw-offload流量    fwd    ipv4    0    dl_vlan=101

COSSW-16226 验证MATCH项vlan_002
    [Documentation]    *set pass rule match dl_vlan_pcp to stream*
    [Tags]    ok    
    验证ovs-hw-offload流量    fwd    ipv4    0    dl_vlan_pcp=7

COSSW-16227 验证MATCH项vlan_003
    [Documentation]    *set pass rule match vlan_tci to stream*
    [Tags]    ok    
    验证ovs-hw-offload流量    fwd    ipv4    0    vlan_tci=0x1123/0xff

COSSW-16228 验证MATCH项dscp_001
    [Documentation]    *set pass rule match ip_dscp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    ip_dscp=16    nw_ecn=1    dl_type=\

COSSW-16229 验证MATCH项dscp_002
    [Documentation]    *set pass rule match ip_dscp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv6    HMP    ip_dscp=32    nw_ecn=1    dl_type=0x86dd

COSSW-16230 验证MATCH项dscp_003
    [Documentation]    *set pass rule match nw_ecn to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    nw_ecn=1    dl_type=\

COSSW-16231 验证MATCH项dscp_004
    [Documentation]    *set pass rule match nw_ecn to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv6    HMP    nw_ecn=1    dl_type=0x86dd

COSSW-16232 验证MATCH项frag_001
    [Documentation]    *set pass rule match nw_frag to stream*
    [Tags]    dpe not support
    验证ovs-hw-offload流量    fwd    ipv4    0    nw_frag=yes    dl_type=\

COSSW-16233 验证MATCH项frag_002
    [Documentation]    *set pass rule match nw_frag to stream*
    [Tags]    dpe not support 
    验证ovs-hw-offload流量    fwd    ipv6    0    nw_frag=yes    dl_type=0x86dd

COSSW-16234 验证MATCH项ttl_001
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]     ok
    验证ovs-hw-offload流量    fwd    ipv4    0    nw_ttl=\       dl_type=\

COSSW-16235 验证MATCH项ttl_002
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]     ok   
    验证ovs-hw-offload流量    fwd    ipv6    HMP    nw_ttl=\      dl_type=\

COSSW-16236 验证MATCH项arp_001
    [Documentation]    *set pass rule match arp_op to stream*
    [Tags]    ovs not support
    验证ovs-hw-offload流量    fwd    arp    udp    dl_type=0x0806    arp_op=1    arp_spa=1.1.1.1    arp_tpa=2.2.2.2    arp_sha=00:11:11:22:22:33    arp_tha=00:11:11:22:22:44

COSSW-16237 验证MATCH项arp_002
    [Documentation]    *set pass rule match arp_op to stream*
    [Tags]    ovs not support
    验证ovs-hw-offload流量    fwd    arp    udp    dl_type=0x0806

COSSW-16238 验证MATCH项arp_003
    [Documentation]    *set pass rule match arp_op to stream*
    [Tags]    ovs not support
    验证ovs-hw-offload流量    fwd    arp    udp    dl_type=0x0806    arp_op=1

COSSW-16239 验证MATCH项icmp_001
    [Documentation]    *set pass rule match icmp_type and icmp_code to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    icmp    icmp_type=0    icmp_code=100    nw_proto=1    dl_type=0x0800

*** Keywords ***
