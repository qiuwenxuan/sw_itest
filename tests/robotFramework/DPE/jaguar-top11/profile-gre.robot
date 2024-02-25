*** Settings ***
Suite Setup       组配置初始化
Suite Teardown    组配置清理
Test Setup        清理测试仪
Test Teardown     清理测试仪
Resource          ../testlib/testlib.robot
Resource          ../testlib/features/jaguar.robot
Library           SSHLibrary
Library           ipv4config.py

*** Variables ***

*** Test Cases ***
COSSW-8544_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    GRE(c=0,k=0,s=0,proto=0x0800).IPV4

COSSW-8545_Proflie
    [Documentation]    *验证*
    [Tags]    nok    GRE隧道带R，不支持
    验证Profile    GRE(proto=0x0800).IPV4

COSSW-8546_Proflie
    [Documentation]    *验证*
    [Tags]    ok    
    验证Profile    GRE(c=0,k=1,s=1,proto=0x0800).IPV4

COSSW-8547_Proflie
    [Documentation]    *验证*
    [Tags]    ok    
    验证Profile    GRE(c=1,k=1,s=1,proto=0x0800).IPV4

COSSW-8548_Proflie
    [Documentation]    *验证*
    [Tags]    nok        GRE隧道带R，不支持
    验证Profile    GRE(proto=0x0800).IPV4

COSSW-8549_Proflie
    [Documentation]    *验证*
    [Tags]    ok    
    验证Profile    GRE(c=1,k=1,s=1).IPV6

COSSW-8550_Proflie
    [Documentation]    *验证*
    [Tags]    ok    
    验证Profile    GRE(c=1,k=1,s=1).eth.ARP

COSSW-8551_Proflie
    [Documentation]    *验证*
    [Tags]    nok    rocev1
    验证Profile    GRE(c=1,k=1,s=1).rocev1

COSSW-8552_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    IPV4.GRE.ETH.2VLAN.IPV4.UDP

COSSW-8553_Proflie
    [Documentation]    *验证*
    [Tags]    nok    ROCEv2
    验证Profile    IPV6.GRE.ETH.2VLAN.IPV4.ROCEv2

COSSW-8554_Proflie
    [Documentation]    *验证*
    [Tags]    nok    unknown
    验证Profile    GRE(c=1,k=1,s=1).unknown

COSSW-8709_Proflie
    [Documentation]    *验证*
    [Tags]    ok    基础通路
    验证Profile    eth.v4.gre.eth

COSSW-8710_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.eth.vlan.arp

COSSW-8711_Proflie
    [Documentation]    *验证*
    [Tags]    nok
    验证Profile    eth.v4.gre.eth.vlan.rocev1

COSSW-8712_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.eth.vlan.v4

COSSW-8713_Proflie
    [Documentation]    *验证*
    [Tags]    ok    re
    验证Profile    eth.v4.gre.eth.vlan.ipv4-option

COSSW-8714_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.eth.vlan.ipv4-frag(flags=1,frag=0x200)

COSSW-8715_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.eth.vlan.ipv4-frag(frag=0x200)

COSSW-8716_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.eth.vlan.v6

COSSW-8717_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.eth.vlan.v6-ext

COSSW-8718_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.eth.qinq.v4.tcp

COSSW-8719_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.eth.qinq.v4.udp

COSSW-8720_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.eth.qinq.v4.icmp

COSSW-8721_Proflie
    [Documentation]    *验证*
    [Tags]    ok   
    验证Profile    eth.v4.gre.eth.qinq.v4.igmp

COSSW-8722_Proflie
    [Documentation]    *验证*
    [Tags]    ok    
    验证Profile    eth.v4.gre.eth.qinq.v4.sctp

COSSW-8723_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.eth.qinq.ipv4-frag(flags=1,frag=0).tcp

COSSW-8951_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.eth.qinq.ipv4-frag(flags=1,frag=0).udp

COSSW-11642_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.eth.qinq.v6.tcp

COSSW-11643_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.eth.qinq.v6.tcp

COSSW-11644_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.eth.qinq.v6.udp

COSSW-11645_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.eth.qinq.v6.icmp6

COSSW-11646_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.v4

COSSW-11647_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.ipv4-frag(flags=1,frag=0x200)

COSSW-11648_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.ipv4-frag(frag=0x200)

COSSW-11649_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.v6

COSSW-11650_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.v6-ext

COSSW-11651_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.v4.tcp

COSSW-11652_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.v4.udp

COSSW-11653_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.v4.udp(dport=4791)

COSSW-11654_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.v4.icmp

COSSW-11655_Proflie
    [Documentation]    *验证*
    [Tags]    ok    
    验证Profile    eth.v4.gre.v4.igmp

COSSW-11656_Proflie
    [Documentation]    *验证*
    [Tags]    ok   
    验证Profile    eth.v4.gre.v4.sctp

COSSW-11657_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.v6.tcp

COSSW-11658_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.v6.udp

COSSW-11659_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.v6.udp(dport=4791)

COSSW-11660_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre.v6.icmp6

COSSW-11661_Proflie
    [Documentation]    *验证*
    [Tags]    ok    
    验证Profile    eth.v4.gre.v6.sctp

COSSW-11662_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.eth

COSSW-11663_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.eth.vlan.arp

COSSW-11664_Proflie
    [Documentation]    *验证*
    [Tags]    nok    rocev1
    验证Profile    eth.v6.gre.eth.vlan.rocev1

COSSW-11665_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.eth.vlan.v6

COSSW-11666_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.eth.vlan.v6-ext

COSSW-11667_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.eth.vlan.v4

COSSW-11668_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.eth.qinq.v6.tcp

COSSW-11669_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.eth.qinq.v6.udp

COSSW-11670_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.eth.qinq.v6.icmp6

COSSW-11671_Proflie
    [Documentation]    *验证*
    [Tags]    ok    
    验证Profile    eth.v6.gre.eth.qinq.v6.sctp

COSSW-11672_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.eth.qinq.v6-ext.tcp

COSSW-11673_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.eth.qinq.v6-ext.udp

COSSW-11674_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.eth.qinq.v4.tcp

COSSW-11675_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.eth.qinq.v4.udp

COSSW-11676_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.eth.qinq.v4.icmp

COSSW-11677_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.v4

COSSW-11678_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.ipv4-frag(flags=0x1,frag=0x200)

COSSW-11679_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.ipv4-frag(frag=0x200)

COSSW-11680_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.v4.tcp

COSSW-11681_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.v4.udp

COSSW-11682_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.v4.udp(dport=4791)

COSSW-11683_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.v4.icmp

COSSW-11684_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.v4(proto=2).igmp

COSSW-11685_Proflie
    [Documentation]    *验证*
    [Tags]    ok    
    验证Profile    eth.v6.gre.v4.sctp

COSSW-11686_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.v6

COSSW-11687_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.v6-ext

COSSW-11688_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.v6.tcp

COSSW-11689_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.v6.udp

COSSW-11690_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre.v6.udp(dport=4791)

COSSW-11818_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.qinq.v4.udp.vxlan.eth.qinq.v4.gre.eth.qinq.v4.tcp

COSSW-11820_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.qinq.v4.gre.v6.ipinip.v4.icmp

COSSW-11825_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.qinq.v4.gre.eth.qinq.v4.gre.eth.qinq.v6.icmp6

COSSW-11829_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.qinq.v6.gre.v6.udp.geneve.v6.tcp(dport=8484)

COSSW-11831_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.qinq.v6.gre.v4.udp.vxlan-gpe.eth.qinq.v4.udp(dport=8181)

*** Keywords ***
组配置初始化
    ${config}    ipv4Config.getProfileSuiteConfig
    jaguarRunConfig    ${A}    ${config}
    清理测试仪

组配置清理
    ${config}    ipv4Config.getProfileSuiteConfig
    jaguarClearConfig    ${A}    ${config}
    清理测试仪

验证Profile
    [Arguments]    ${arg1}
    ${configResult}    ipv4Config.getProfileValue    ${arg1}
    验证RESTFUL流量    ${configResult}
