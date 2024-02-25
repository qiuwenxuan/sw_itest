*** Settings ***
Suite Setup       创建OVS单桥环境    ${A}
Suite Teardown    清除OVS单桥环境    ${A}
Resource          ../../testlib/testlib.robot
Resource          ../../testlib/features/ovs.robot
Library           SSHLibrary

*** Variables ***

*** Test Cases ***
ovs_match_00001
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    RAT    OVS    UDP
    验证三层流量    fwd    ipv4    udp    nw_src=1.1.1.1    dl_src=22:22:22:22:22:22    nw_dst=2.2.2.2    dl_dst=00:0B:C4:A8:22:B0    dl_type=0x0800

ovs_match_00002
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst with mask to stream*
    [Tags]    RAT    OVS    UDP
    验证三层流量    fwd    ipv4    udp    nw_src=1.1.1.0/24    dl_src=00:0B:C4:A8:22:B0/ff:ff:ff:ff:ff:ff    nw_dst=2.2.2.0/24    dl_dst=00:0B:C4:A8:22:B0/ff:ff:ff:ff:ff:ff    dl_type=0x0800

ovs_match_00003
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst with mask to stream*
    [Tags]    RAT    OVS    UDP    IPV6
    验证三层流量    fwd    ipv6    udp    ipv6_src=11::1    ipv6_dst=22::1    dl_type=0x86dd

ovs_match_00004
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst with mask to stream*
    [Tags]    RAT    OVS    UDP    IPV6
    验证三层流量    fwd    ipv6    udp    ipv6_src=1::1/64    ipv6_dst=2::2/64    dl_type=0x86dd

ovs_match_00005
    [Documentation]    *set pass rule match dl_type to stream*
    [Tags]    RAT    OVS    UDP
    验证三层流量    fwd    ipv6    udp    dl_type=0x86dd

ovs_match_00006
    [Documentation]    *set pass rule match dl_vlan to stream*
    [Tags]    RAT    OVS    UDP
    验证三层流量    fwd    ipv4    udp    dl_vlan=101

ovs_match_00007
    [Documentation]    *set pass rule match dl_vlan_pcp to stream*
    [Tags]    RAT    OVS    UDP
    验证三层流量    fwd    ipv4    udp    dl_vlan_pcp=7

ovs_match_00008
    [Documentation]    *set pass rule match vlan_tci to stream*
    [Tags]    RAT    OVS    UDP
    验证三层流量    fwd    ipv4    udp    vlan_tci=0x1123/0x1fff

ovs_match_00009
    [Documentation]    *set pass rule match mpls_label to stream*
    [Tags]    RAT    OVS    UDP
    验证三层流量    fwd    ipv4    udp    mpls_label=222    dl_type=0x8847

ovs_match_00010
    [Documentation]    *set pass rule match mpls_tc to stream*
    [Tags]    RAT    OVS    UDP
    验证三层流量    fwd    ipv4    udp    mpls_tc=1    dl_type=0x8847

ovs_match_00011
    [Documentation]    *set pass rule match mpls_bos to stream*
    [Tags]    RAT    OVS    UDP
    验证三层流量    fwd    ipv4    udp    mpls_bos=1    dl_type=0x8847

ovs_match_00012
    [Documentation]    *set pass rule match mpls_ttl to stream*
    [Tags]    RAT    OVS    UDP
    验证三层流量    fwd    ipv4    udp    mpls_ttl=55    dl_type=0x8847

ovs_match_00013
    [Documentation]    *set pass rule match nw_proto to stream*
    [Tags]    RAT    OVS    DCN-MEAS
    验证三层流量    fwd    ipv4    DCN-MEAS    nw_proto=19    dl_type=0x0800

ovs_match_00014
    [Documentation]    *set pass rule match nw_proto to stream*
    [Tags]    RAT    OVS    HMP    IPV6
    验证三层流量    fwd    ipv6    HMP    nw_proto=20    dl_type=0x86dd

ovs_match_00015
    [Documentation]    *set pass rule match nw_ttl to stream*
    [Tags]    RAT    OVS    UDP
    验证三层流量    fwd    ipv4    udp    nw_ttl=65    dl_type=0x0800

ovs_match_00016
    [Documentation]    *set pass rule match nw_ttl to stream*
    [Tags]    RAT    OVS    UDP    IPV6
    验证三层流量    fwd    ipv6    udp    nw_ttl=65    dl_type=0x86dd

ovs_match_00017
    [Documentation]    *set pass rule match nw_frag to stream*
    [Tags]    RAT    OVS    UDP
    验证三层流量    fwd    ipv4    udp    nw_frag=first    dl_type=0x0800

ovs_match_00018
    [Documentation]    *set pass rule match nw_frag to stream*
    [Tags]    RAT    OVS    UDP    IPV6
    验证三层流量    fwd    ipv6    udp    nw_frag=first    dl_type=0x86dd

ovs_match_00019
    [Documentation]    *set pass rule match nw_tos to stream*
    [Tags]    RAT    OVS    UDP
    验证三层流量    fwd    ipv4    udp    nw_tos=16    dl_type=0x0800

ovs_match_00020
    [Documentation]    *set pass rule match nw_tos to stream*
    [Tags]    RAT    OVS    UDP    IPV6
    验证三层流量    fwd    ipv6    udp    nw_tos=16    dl_type=0x86dd

ovs_match_00021
    [Documentation]    *set pass rule match ip_dscp to stream*
    [Tags]    RAT    OVS    UDP
    验证三层流量    fwd    ipv4    udp    ip_dscp=16    dl_type=0x0800

ovs_match_00022
    [Documentation]    *set pass rule match ip_dscp to stream*
    [Tags]    RAT    OVS    UDP    IPV6
    验证三层流量    fwd    ipv6    udp    ip_dscp=32    dl_type=0x86dd

ovs_match_00023
    [Documentation]    *set pass rule match nw_ecn to stream*
    [Tags]    RAT    OVS    UDP
    验证三层流量    fwd    ipv4    udp    nw_ecn=1    dl_type=0x0800

ovs_match_00024
    [Documentation]    *set pass rule match nw_ecn to stream*
    [Tags]    RAT    OVS    UDP    IPV6
    验证三层流量    fwd    ipv6    udp    nw_ecn=2    dl_type=0x86dd

ovs_match_00025
    [Documentation]    *set pass rule match arp_op to stream*
    [Tags]    RAT    OVS    ARP
    验证三层流量    fwd    arp    udp    dl_type=0x0806    arp_op=1    arp_spa=1.1.1.1    arp_tpa=2.2.2.2    arp_sha=00:11:11:22:22:33    arp_tha=00:11:11:22:22:44

ovs_match_00026
    [Documentation]    *set pass rule match tcp_src and tcp_dst to stream*
    [Tags]    RAT    OVS    TCP
    验证三层流量    fwd    ipv4    tcp    tcp_src=1025    tcp_dst=1026    tcp_flags=syn    nw_proto=6    dl_type=0x0800

ovs_match_00027
    [Documentation]    *set pass rule match tcp_src and tcp_dst with mask to stream*
    [Tags]    RAT    OVS    TCP
    验证三层流量    fwd    ipv4    tcp    tcp_src=0x100/0xff00    tcp_dst=0x1/0xff    tcp_flags=0x1/0xff    nw_proto=6    dl_type=0x0800

ovs_match_00028
    [Documentation]    *set pass rule match udp_src and udp_dst to stream*
    [Tags]    RAT    OVS    UDP
    验证三层流量    fwd    ipv4    udp    udp_src=2025    udp_dst=2026    nw_proto=17    dl_type=0x0800

ovs_match_00029
    [Documentation]    *set pass rule match udp_src and udp_dst with mask to stream*
    [Tags]    RAT    OVS    UDP
    验证三层流量    fwd    ipv4    udp    udp_src=0x100/0xff00    udp_dst=0x100/0xff00    nw_proto=17    dl_type=0x0800

ovs_match_00030
    [Documentation]    *set pass rule match sctp_src and sctp_dst to stream*
    [Tags]    RAT    OVS    SCTP
    验证三层流量    fwd    ipv4    sctp    sctp_src=2025    sctp_dst=2026    nw_proto=132    dl_type=0x0800

ovs_match_00031
    [Documentation]    *set pass rule match sctp_src and sctp_dst with mask to stream*
    [Tags]    RAT    OVS    SCTP
    验证三层流量    fwd    ipv4    sctp    sctp_src=0x100/0xff00    sctp_dst=0x100/0xff00    nw_proto=132    dl_type=0x0800

ovs_match_00032
    [Documentation]    *set pass rule match icmp_type and icmp_code to stream*
    [Tags]    RAT    OVS    ICMP
    验证三层流量    fwd    ipv4    icmp    icmp_type=0    icmp_code=100

ovs_match_00033
    [Documentation]    *set pass rule match icmpv6_type icmpv6_code and nd_target to stream*
    [Tags]    RAT    OVS    ICMPV6
    验证三层流量    fwd    ipv4    icmpv6    icmpv6_type=135    icmpv6_code=100    nd_target=1::1

ovs_match_00034
    [Documentation]    *set pass rule match icmpv6_type icmpv6_code and nd_target to stream*
    [Tags]    RAT    OVS    ICMPV6
    验证三层流量    fwd    ipv4    icmpv6    icmpv6_type=136    icmpv6_code=100    nd_target=2::/64

ovs_match_00035
    [Documentation]    *set pass rule match icmpv6_type nd_sll and nd_tll to stream*
    [Tags]    RAT    OVS    ICMPV6
    验证三层流量    fwd    ipv4    icmpv6    icmpv6_type=135    nd_sll=00:11:22:33:44:55    nd_tll=00:11:ad:33:cb:55

ovs_match_00036
    [Documentation]    *set pass rule match icmpv6_type and nd_reserved to stream*
    [Tags]    RAT    OVS    ICMPV6
    验证三层流量    fwd    ipv4    icmpv6    icmpv6_type=135    nd_reserved=1

ovs_match_00037
    [Documentation]    *set pass rule match icmpv6_type and nd_options_type to stream*
    [Tags]    RAT    OVS    ICMPV6
    验证三层流量    fwd    ipv4    icmpv6    icmpv6_type=135    nd_options_type=1

ovs_match_00038
    [Documentation]    *set pass rule match vxlan protocol to stream*
    [Tags]    RAT    OVS    VXLAN
    验证三层流量    fwd    ipv4    udp    udp_dst=4789

ovs_match_00039
    [Documentation]    *set pass rule match gre protocol to stream*
    [Tags]    RAT    OVS    GRE
    验证三层流量    fwd    ipv4    udp    nw_proto=47

ovs_match_00040
    [Documentation]    *set pass rule match NSH protocol and nsh_flags to stream*
    [Tags]    RAT    OVS    NSH
    验证三层流量    fwd    ipv4    NSH    dl_type=0x894f    nsh_flags=0

ovs_match_00041
    [Documentation]    *set pass rule match NSH protocol and nsh_ttl to stream*
    [Tags]    RAT    OVS    NSH
    验证三层流量    fwd    ipv4    NSH    dl_type=0x894f    nsh_ttl=14

ovs_match_00042
    [Documentation]    *set pass rule match NSH protocol and nsh_mdtype to stream*
    [Tags]    RAT    OVS    NSH
    验证三层流量    fwd    ipv4    NSH    dl_type=0x894f    nsh_mdtype=0x1

ovs_match_00043
    [Documentation]    *set pass rule match NSH protocol and nsh_np to stream*
    [Tags]    RAT    OVS    NSH
    验证三层流量    fwd    ipv4    NSH    dl_type=0x894f    nsh_np=0x3

ovs_match_00044
    [Documentation]    *set pass rule match NSH protocol and nsh_spi to stream*
    [Tags]    RAT    OVS    NSH
    验证三层流量    fwd    ipv4    NSH    dl_type=0x894f    nsh_spi=0x1

ovs_match_00045
    [Documentation]    *set pass rule match NSH protocol and nsh_si to stream*
    [Tags]    RAT    OVS    NSH
    验证三层流量    fwd    ipv4    NSH    dl_type=0x894f    nsh_si=1

ovs_match_00046
    [Documentation]    *set pass rule match NSH protocol and nsh_c1 to stream*
    [Tags]    RAT    OVS    NSH
    验证三层流量    fwd    ipv4    NSH    dl_type=0x894f    nsh_c1=0x1123

ovs_match_00047
    [Documentation]    *set pass rule match NSH protocol and nsh_c2 to stream*
    [Tags]    RAT    OVS    NSH
    验证三层流量    fwd    ipv4    NSH    dl_type=0x894f    nsh_c2=1234

ovs_match_00048
    [Documentation]    *set pass rule match NSH protocol and nsh_c3 to stream*
    [Tags]    RAT    OVS    NSH
    验证三层流量    fwd    ipv4    NSH    dl_type=0x894f    nsh_c3=1345

ovs_match_00049
    [Documentation]    *set pass rule match NSH protocol and nsh_c4 to stream*
    [Tags]    RAT    OVS    NSH
    验证三层流量    fwd    ipv4    NSH    dl_type=0x894f    nsh_c4=1456

ovs_match_00050
    [Documentation]    *set pass rule match table to stream*
    [Tags]    RAT    OVS    table
    验证三层流量    fwd    ipv4    udp    table=0    ip_src=2.2.2.2

ovs_match_00051
    [Documentation]    *set pass rule match tun_id to stream*
    [Tags]    RAT    OVS    tunnel
    验证三层流量    fwd    ipv4    udp    tun_id=0x7/0xf

ovs_match_00052
    [Documentation]    *set pass rule match tun_src and tun_dst to stream*
    [Tags]    RAT    OVS    tunnel
    验证三层流量    fwd    ipv4    udp    tun_src=192.168.1.0/24    tun_dst=192.168.2.0/24

ovs_match_00053
    [Documentation]    *set pass rule match tun_ipv6_src and tun_ipv6_dst to stream*
    [Tags]    RAT    OVS    tunnel    IPV6
    验证三层流量    fwd    ipv6    udp    tun_ipv6_src=1::0/64    tun_ipv6_dst=1::0/64

ovs_match_00054
    [Documentation]    *set pass rule match tun_gbp_id and tun_gbp_flags to stream*
    [Tags]    RAT    OVS    tunnel
    验证三层流量    fwd    ipv4    udp    tun_gbp_id=1    tun_gbp_flags=0x48

ovs_match_00055
    [Documentation]    *set pass rule match tun_erspan_ver tun_erspan_idx tun_erspan_dir and tun_erspan_hwid to stream*
    [Tags]    RAT    OVS    tunnel
    验证三层流量    fwd    ipv4    udp    tun_erspan_ver=1    tun_erspan_idx=1024    tun_erspan_dir=0    tun_erspan_hwid=12

ovs_match_00056
    [Documentation]    *set pass rule match tun_gtpu_flags and tun_gtpu_msgtype to stream*
    [Tags]    RAT    OVS    tunnel
    验证三层流量    fwd    ipv4    udp    tun_gtpu_flags=0x30    tun_gtpu_msgtype=1

ovs_match_00057
    [Documentation]    *set pass rule match tun_metadata0 to stream*
    [Tags]    RAT    OVS    tunnel
    验证三层流量    fwd    ipv4    udp    tun_metadata0=1234

ovs_match_00058
    [Documentation]    *set pass rule match tun_flags to stream*
    [Tags]    RAT    OVS    tunnel
    验证三层流量    fwd    ipv4    udp    tun_flags=+oam

ovs_match_00059
    [Documentation]    *set pass rule match in_port_oxm to stream*
    [Tags]    RAT    OVS    metadata
    验证三层流量    fwd    ipv4    udp    in_port_oxm=12345

ovs_match_00060
    [Documentation]    *set pass rule match skb_priority to stream*
    [Tags]    RAT    OVS    metadata
    验证三层流量    fwd    ipv4    udp    skb_priority=0x3

ovs_match_00061
    [Documentation]    *set pass rule match pkt_mark to stream*
    [Tags]    RAT    OVS    metadata
    验证三层流量    fwd    ipv4    udp    pkt_mark=0x55

ovs_match_00062
    [Documentation]    *set pass rule match actset_output to stream*
    [Tags]    RAT    OVS    metadata
    验证三层流量    fwd    ipv4    udp    actset_output=12345

ovs_match_00063
    [Documentation]    *set pass rule match packet_type to stream*
    [Tags]    RAT    OVS    metadata
    验证三层流量    fwd    ipv4    udp    packet_type=0x0800

ovs_match_00064
    [Documentation]    *set pass rule match ct_state to stream*
    [Tags]    RAT    OVS    conntrack
    验证三层流量    fwd    ipv4    udp    ct_state=+trk+est

ovs_match_00065
    [Documentation]    *set pass rule match ct_zone to stream*
    [Tags]    RAT    OVS    conntrack
    验证三层流量    fwd    ipv4    udp    ct_zone=-100

ovs_match_00066
    [Documentation]    *set pass rule match ct_mark to stream*
    [Tags]    RAT    OVS    conntrack
    验证三层流量    fwd    ipv4    udp    ct_mark=15

ovs_match_00067
    [Documentation]    *set pass rule match ct_label to stream*
    [Tags]    RAT    OVS    conntrack
    验证三层流量    fwd    ipv4    udp    ct_label=16

ovs_match_00068
    [Documentation]    *set pass rule match ct_nw_src to stream*
    [Tags]    RAT    OVS    conntrack
    验证三层流量    fwd    ipv4    udp    ct_nw_src=1.1.1.1

ovs_match_00069
    [Documentation]    *set pass rule match ct_nw_dst to stream*
    [Tags]    RAT    OVS    conntrack
    验证三层流量    fwd    ipv4    udp    ct_nw_dst=2.2.2.2

ovs_match_00070
    [Documentation]    *set pass rule match ct_ipv6_src to stream*
    [Tags]    RAT    OVS    conntrack
    验证三层流量    fwd    ipv4    udp    ct_ipv6_src=1::1

ovs_match_00071
    [Documentation]    *set pass rule match ct_ipv6_dst to stream*
    [Tags]    RAT    OVS    conntrack
    验证三层流量    fwd    ipv4    udp    ct_ipv6_dst=2::1

ovs_match_00072
    [Documentation]    *set pass rule match ct_nw_proto to stream*
    [Tags]    RAT    OVS    conntrack
    验证三层流量    fwd    ipv4    udp    ct_nw_proto=6

ovs_match_00073
    [Documentation]    *set pass rule match ct_tp_src to stream*
    [Tags]    RAT    OVS    conntrack
    验证三层流量    fwd    ipv4    udp    ct_tp_src=1024

ovs_match_00074
    [Documentation]    *set pass rule match ct_tp_dst to stream*
    [Tags]    RAT    OVS    conntrack
    验证三层流量    fwd    ipv4    udp    ct_tp_dst=1024

ovs_match_00075
    [Documentation]    *set pass rule match ip to stream*
    [Tags]    RAT    OVS    UDP
    验证三层流量-多流    fwd    ipv4    udp    nw_src=1.1.1.1    nw_src=2.2.2.2

*** Keywords ***
