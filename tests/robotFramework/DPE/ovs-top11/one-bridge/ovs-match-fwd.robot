*** Settings ***
Suite Setup       清理测试仪
Suite Teardown    清理测试仪
Test Setup        清理测试仪
Test Teardown     清理测试仪
Force Tags        MATCH    FWD
Resource          ../../testlib/testlib.robot

*** Variables ***

*** Test Cases ***
ovs_match_00001
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证三层流量    fwd    ipv4    udp    nw_src=\    dl_src=\    nw_dst=\    dl_dst=\    dl_type=\

ovs_match_00002
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst with mask to stream*
    验证三层流量    fwd    ipv4    udp    nw_src=1.1.1.0/24    dl_src=00:0B:C4:A8:22:B0/ff:ff:ff:ff:ff:ff    nw_dst=2.2.2.0/24    dl_dst=00:0B:C4:A8:22:B0/ff:ff:ff:ff:ff:ff    dl_type=0x0800

ovs_match_00003
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst with mask to stream*
    验证三层流量    fwd    ipv6    udp    ipv6_src=11::1    ipv6_dst=22::1    dl_type=0x86dd

ovs_match_00005
    [Documentation]    *set pass rule match dl_type to stream*
    验证三层流量    fwd    ipv6    udp    dl_type=0x86dd

ovs_match_00006
    [Documentation]    *set pass rule match dl_vlan to stream*
    验证三层流量    fwd    ipv4    udp    dl_vlan=101

ovs_match_00007
    [Documentation]    *set pass rule match dl_vlan_pcp to stream*
    验证三层流量    fwd    ipv4    udp    dl_vlan_pcp=7

ovs_match_00008
    [Documentation]    *set pass rule match vlan_tci to stream*
    验证三层流量    fwd    ipv4    udp    vlan_tci=0x1123/0x1fff

ovs_match_00009
    [Documentation]    *set pass rule match mpls_label to stream*
    验证三层流量    fwd    ipv4    udp    mpls_label=222    dl_type=0x8847

ovs_match_00010
    [Documentation]    *set pass rule match mpls_tc to stream*
    验证三层流量    fwd    ipv4    udp    mpls_tc=1    dl_type=0x8847

ovs_match_00011
    [Documentation]    *set pass rule match mpls_bos to stream*
    验证三层流量    fwd    ipv4    udp    mpls_bos=1    dl_type=0x8847

ovs_match_00012
    [Documentation]    *set pass rule match mpls_ttl to stream*
    验证三层流量    fwd    ipv4    udp    mpls_ttl=55    dl_type=0x8847

ovs_match_00013
    [Documentation]    *set pass rule match nw_proto to stream*
    [Tags]    DCN-MEAS
    验证三层流量    fwd    ipv4    DCN-MEAS    nw_proto=19    dl_type=0x0800

ovs_match_00014
    [Documentation]    *set pass rule match nw_proto to stream*
    [Tags]    HMP    IPV6
    验证三层流量    fwd    ipv6    HMP    nw_proto=20    dl_type=0x86dd

ovs_match_00015
    [Documentation]    *set pass rule match nw_ttl to stream*
    [Tags]    UDP
    验证三层流量    fwd    ipv4    udp    nw_ttl=65    dl_type=0x0800

ovs_match_00016
    [Documentation]    *set pass rule match nw_ttl to stream*
    [Tags]    IPV6
    验证三层流量    fwd    ipv6    udp    nw_ttl=65    dl_type=0x86dd

ovs_match_00017
    [Documentation]    *set pass rule match nw_frag to stream*
    验证三层流量    fwd    ipv4    udp    nw_frag=first    dl_type=0x0800

ovs_match_00019
    [Documentation]    *set pass rule match nw_tos to stream*
    验证三层流量    fwd    ipv4    udp    nw_tos=16    dl_type=0x0800

ovs_match_00020
    [Documentation]    *set pass rule match nw_tos to stream*
    验证三层流量    fwd    ipv6    udp    nw_tos=16    dl_type=0x86dd

ovs_match_00021
    [Documentation]    *set pass rule match ip_dscp to stream*
    验证三层流量    fwd    ipv4    udp    ip_dscp=16    dl_type=0x0800

ovs_match_00022
    [Documentation]    *set pass rule match ip_dscp to stream*
    [Tags]    IPV6
    验证三层流量    fwd    ipv6    udp    ip_dscp=32    dl_type=0x86dd

ovs_match_00023
    [Documentation]    *set pass rule match nw_ecn to stream*
    验证三层流量    fwd    ipv4    udp    nw_ecn=1    dl_type=0x0800

ovs_match_00024
    [Documentation]    *set pass rule match nw_ecn to stream*
    [Tags]    IPV6
    验证三层流量    fwd    ipv6    udp    nw_ecn=2    dl_type=0x86dd

ovs_match_00025
    [Documentation]    *set pass rule match arp_op to stream*
    [Tags]    RAT    OVS    ARP
    验证三层流量    fwd    arp    udp    dl_type=0x0806    arp_op=1    arp_spa=1.1.1.1    arp_tpa=2.2.2.2    arp_sha=00:11:11:22:22:33    arp_tha=00:11:11:22:22:44

ovs_match_00026
    [Documentation]    *set pass rule match tcp_src and tcp_dst to stream*
    [Tags]    TCP
    验证三层流量    fwd    ipv4    tcp    tcp_src=1025    tcp_dst=1026    tcp_flags=syn    nw_proto=6    dl_type=0x0800

ovs_match_00027
    [Documentation]    *set pass rule match tcp_src and tcp_dst with mask to stream*
    [Tags]    TCP
    验证三层流量    fwd    ipv4    tcp    tcp_src=0x100/0xff00    tcp_dst=0x1/0xff    tcp_flags=0x1/0xff    nw_proto=6    dl_type=0x0800

ovs_match_00028
    [Documentation]    *set pass rule match udp_src and udp_dst to stream*
    [Tags]    UDP
    验证三层流量    fwd    ipv4    udp    udp_src=2025    udp_dst=2026    nw_proto=17    dl_type=0x0800

ovs_match_00029
    [Documentation]    *set pass rule match udp_src and udp_dst with mask to stream*
    [Tags]    UDP
    验证三层流量    fwd    ipv4    udp    udp_src=0x100/0xff00    udp_dst=0x100/0xff00    nw_proto=17    dl_type=0x0800

ovs_match_00030
    [Documentation]    *set pass rule match sctp_src and sctp_dst to stream*
    [Tags]    SCTP
    验证三层流量    fwd    ipv4    sctp    sctp_src=2025    sctp_dst=2026    nw_proto=132    dl_type=0x0800

ovs_match_00031
    [Documentation]    *set pass rule match sctp_src and sctp_dst with mask to stream*
    [Tags]    SCTP
    验证三层流量    fwd    ipv4    sctp    sctp_src=0x100/0xff00    sctp_dst=0x100/0xff00    nw_proto=132    dl_type=0x0800

ovs_match_00032
    [Documentation]    *set pass rule match icmp_type and icmp_code to stream*
    [Tags]    ICMP
    验证三层流量    fwd    ipv4    icmp    icmp_type=0    icmp_code=100    nw_proto=1    dl_type=0x0800

*** Keywords ***
