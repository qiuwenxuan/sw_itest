*** Settings ***
Suite Setup       组配置初始化
Suite Teardown    组配置清理
Test Setup        清理测试仪
Test Teardown     清理测试仪
Resource          ../testlib/testlib.robot
Resource          ../testlib/features/jaguar.robot
Library           SSHLibrary
Library           creteconfig.py

*** Variables ***

*** Test Cases ***
COSSW-8590_ClassifyIpv4Value
    [Documentation]    *验证*
    [Tags]    ok    基础通路
    验证classify    eth.ipv4    ot     0

COSSW-8592_ClassifyIpv4Value
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.ipv4.udp     ot    0
    验证classify    eth.ipv4.udp     ot    1
    验证classify    eth.ipv4.udp     ot    2
    验证classify    eth.ipv4.udp     ot    3  
    验证classify    eth.ipv4.udp     ot    4
    验证classify    eth.ipv4.udp     ot    5
    验证classify    eth.ipv4.udp     ot    6
    验证classify    eth.ipv4.udp     ot    7
    验证classify    eth.ipv4.udp     ot    8
    验证classify    eth.ipv4.udp     ot    9

COSSW-8593_ClassifyIpv6Value
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.ipv6     ot   5

COSSW-8594_ClassifyIpv6Value
    [Documentation]    *验证*
    [Tags]    ok    
    验证classify    eth.ipv6     ot    0

COSSW-8595_ClassifyIpv6Value
    [Documentation]    *验证*
    [Tags]    ok    版本问题
    验证classify    eth.ipv6     ot    3

COSSW-8596_ClassifyIpv6Value
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.ipv6     ot    8

COSSW-8597_ClassifyIpv6Value
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.ipv6     ot    9

COSSW-8604_ClassifyIpv4Value
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.2vlan.ipv4    ot    -1    OT_OUT_VLAN_ID

COSSW-8605_ClassifyIpv4Value
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.2vlan.ipv4    ot    -1    OT_OUT_VLAN_TPID

COSSW-8606_ClassifyIpv4Value
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.2vlan.ipv4    ot    -1    OT_OUT_VLAN_ID,OT_OUT_VLAN_TPID

COSSW-8607_ClassifyIpv4Value
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.2vlan.ipv4    ot    -1    OT_INNER_VLAN_VALID

COSSW-8608_ClassifyIpv4Value
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.2vlan.ipv4    ot    -1    OT_INNER_VLAN_TPID

COSSW-8609_ClassifyIpv4Value
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.2vlan.ipv4    ot    -1    OT_INNER_VLAN_ID,OT_INNER_VLAN_TPID

COSSW-8610_ClassifyIpv4Value
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.2vlan.ipv4    ot    -1    OT_OUT_VLAN_ID,OT_OUT_VLAN_TPID,OT_INNER_VLAN_ID,OT_INNER_VLAN_TPID

COSSW-8611_ClassifyArpValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.arp    ot    8

COSSW-8612_ClassifyArpValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.arp    ot    9

COSSW-8613_ClassifyArpValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.arp    ot    5

COSSW-8614_ClassifyArpValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.arp    ot    0

COSSW-8615_ClassifyArpValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.arp    ot    1

COSSW-8616_ClassifyIpv4Value
    [Documentation]    *验证ipv4报文， classify的key从最外层报文提取Ethernet Type 作为key*
    [Tags]    ok
    验证classify    eth.ipv4    ot    -1    OT_ETH_TYPE

COSSW-8617_ClassifyIpv6Value
    [Documentation]    *验证ipv6报文， classify的key从最外层报文提取Ethernet Type 作为key*
    [Tags]    ok
    验证classify    eth.ipv6    ot    -1    OT_ETH_TYPE

COSSW-8618_ClassifyIpv4VxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.tcp   tl    0

COSSW-8619_ClassifyIpv4VxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.tcp   tl    1

COSSW-8620_ClassifyIpv4VxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.tcp   tl    2

COSSW-8621_ClassifyIpv4VxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.tcp   tl    3

COSSW-8622_ClassifyIpv4VxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.tcp   tl    4

COSSW-8623_ClassifyIpv4VxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.tcp   tl    5

COSSW-8624_ClassifyIpv4VxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.tcp   tl    6

COSSW-8625_ClassifyIpv4VxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.tcp   tl    7

COSSW-8626_ClassifyIpv4VxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.tcp   tl    8

COSSW-8627_ClassifyIpv4VxlanValue
    [Documentation]    *验证 次外层*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.tcp   tl    9

COSSW-8628_ClassifyIpv6VxlanValue
    [Documentation]    *验证*
    [Tags]    ok    
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v6.tcp    tl    0

COSSW-8629_ClassifyIpv6VxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v6.tcp    tl    3

COSSW-8630_ClassifyIpv6VxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v6.tcp    tl    5

COSSW-8631_ClassifyIpv6VxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v6.tcp    tl    8

COSSW-8632_ClassifyIpv6VxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v6.tcp    tl    9

COSSW-8640_ClassifyIpv4VxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.udp     tl    -1    TL_OUT_VLAN_ID

COSSW-8641_ClassifyIpv4VxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.udp    tl    -1    TL_OUT_VLAN_TPID

COSSW-8642_ClassifyIpv4VxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.udp    tl    -1    TL_OUT_VLAN_ID,TL_OUT_VLAN_TPID

COSSW-8643_ClassifyIpv4VxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.udp    tl    -1    TL_INNER_VLAN_VALID

COSSW-8644_ClassifyIpv4VxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.udp    tl    -1    TL_INNER_VLAN_TPID

COSSW-8645_ClassifyIpv4VxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.udp    tl    -1    TL_INNER_VLAN_ID,TL_INNER_VLAN_TPID

COSSW-8646_ClassifyIpv4VxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.udp    tl    -1    TL_OUT_VLAN_ID,TL_OUT_VLAN_TPID,TL_INNER_VLAN_ID,TL_INNER_VLAN_TPID

COSSW-8647_ClassifyArpVxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.arp    tl    8

COSSW-8648_ClassifyArpVxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.arp    tl    9

COSSW-8649_ClassifyArpVxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.arp    tl    5

COSSW-8650_ClassifyArpVxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.arp    tl    0

COSSW-8651_ClassifyArpVxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.arp    tl    1  

COSSW-8652_ClassifyIpv4VxlanValue
    [Documentation]    *验证*
    [Tags]    ok    版本问题
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.tcp    tl    -1    TL_ETH_TYPE

COSSW-8653_ClassifyIpv6VxlanValue
    [Documentation]    *验证*
    [Tags]    ok    版本问题
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v6.tcp    tl    -1    TL_ETH_TYPE

COSSW-8654_ClassifyIpv4VxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.tcp    tl    -1    OT_TUNNEL_ID

COSSW-8655_ClassifyIpv4VxlanValue
    [Documentation]    *验证*
    [Tags]    nok    context测试需要设置寄存器
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.tcp    tl    -1    ???

COSSW-8656_ClassifyIpv4VxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.gre.eth.2vlan.v4.udp    tl    -1    OUT_TUNNEL_TYPE

COSSW-8657_ClassifyIpv4GreValue
    [Documentation]    *验证*
    [Tags]    ok    gre隧道tunnelid计算
    验证classify    eth.vlan.v4.gre.eth.2vlan.v4.udp    tl    -1    OT_TUNNEL_ID

COSSW-8658_ClassifyIpv4GreValue
    [Documentation]    *验证*
    [Tags]    nok    context测试需要设置寄存器
    验证classify    eth.vlan.v4.gre.eth.2vlan.v4.udp    tl    -1    ???

COSSW-8659_ClassifyIpv4GreValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.gre.eth.2vlan.v4.udp    tl    -1    OUT_TUNNEL_TYPE

COSSW-8660_ClassifyIpv4GeneveValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.geneve.eth.2vlan.v4.tcp    tl    -1    OT_TUNNEL_ID

COSSW-8661_ClassifyIpv4GeneveValue
    [Documentation]    *验证*
    [Tags]    nok    context测试需要设置寄存器
    验证classify    eth.vlan.v4.udp.geneve.eth.2vlan.v4.tcp    tl    -1    ???

COSSW-8662_ClassifyIpv4GeneveValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.geneve.eth.2vlan.v4.tcp    tl    -1    OUT_TUNNEL_TYPE

COSSW-8666_ClassifyIpv4VxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.tcp    tl    -1    OT_TUNNEL_ID

COSSW-8667_ClassifyIpv4VxlanValue
    [Documentation]    *验证*
    [Tags]    nok    context测试需要设置寄存器
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.tcp    tl    -1    ???

COSSW-8668_ClassifyIpv4VxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.tcp    tl    -1    OUT_TUNNEL_TYPE

COSSW-8672_ClassifyIpv4AliVxlanValue
    [Documentation]    *验证*
    [Tags]    ok
    验证classify    eth.vlan.v4.udp.vxlan-ali.eth.2vlan.v4.udp    tl    -1    OT_TUNNEL_ID

COSSW-8673_ClassifyIpv4AliVxlanValue
    [Documentation]    *验证*
    [Tags]    nok    context测试需要设置寄存器
    验证classify    eth.vlan.v4.udp.vxlan-ali.eth.2vlan.v4.udp    tl    -1    ???

COSSW-8674_ClassifyIpv4AliVxlanValue
    [Documentation]    *验证*
    [Tags]    ok    
    验证classify    eth.vlan.v4.udp.vxlan-ali.eth.2vlan.v4.udp    tl    -1    OUT_TUNNEL_TYPE

COSSW-8675_ClassifyIpv4VxlanVxlanValue
    [Documentation]    *验证 最内层*
    [Tags]    ok    
    验证classify    eth.vlan.v4.udp.vxlan.eth.vlan.v4.udp.vxlan.eth.2vlan.v4.tcp    in    0    ETH_TYPE

COSSW-8676_ClassifyIpv4VxlanVxlanValue
    [Documentation]    *验证*
    [Tags]    ok    
    验证classify    eth.vlan.v4.udp.vxlan.eth.vlan.v4.udp.vxlan.eth.2vlan.v4.tcp    in    5    TL_ETH_TYPE

COSSW-8677_ClassifyIpv4VxlanVxlanValue
    [Documentation]    入向是两层隧道报文，最内层是IPV6报文，classify match项指定从最内层提取
    ...    ADDR0:SIP
    ...    ADDR1:DMAC
    ...    ETHER TYPE
    ...    从最内层提取IPV6 SIP作为key
    ...    VLANID/TPID从最内层提取
    ...    TUNNEL ID从最外层提取
    [Tags]    ok    
    验证classify    eth.vlan.v4.udp.vxlan.eth.vlan.v4.udp.vxlan.eth.2vlan.v6.tcp    in    3    IN_ETH_TYPE,IN_INNER_VLAN_ID,IN_INNER_VLAN_TPID,OT_TUNNEL_ID

COSSW-8678_ClassifyIpv6VxlanVxlanValue
    [Documentation]    *验证*
    [Tags]    ok    
    验证classify    eth.vlan.v4.udp.vxlan.eth.vlan.v4.udp.vxlan.eth.2vlan.v6.tcp    in    3    TL_ETH_TYPE,OT_OUT_VLAN_ID,OT_OUT_VLAN_TPID,TL_TUNNEL_ID

COSSW-8679_ClassifyIpv6VxlanVxlanValue
    [Documentation]    *验证 ？？*
    [Tags]    ok    
    验证classify    eth.vlan.v4.udp.vxlan.eth.vlan.v4.udp.vxlan.eth.2vlan.v6.tcp    in    0    TL_ETH_TYPE,TL_OUT_VLAN_ID,TL_OUT_VLAN_TPID

*** Keywords ***
组配置初始化
    ${config}    creteconfig.getClassifySuiteConfig
    jaguarRunConfig    ${A}    ${config}
    清理测试仪

组配置清理
    ${config}    creteconfig.getClassifySuiteConfig
    jaguarClearConfig    ${A}    ${config}
    清理测试仪

验证classify
    [Arguments]    ${pkt}    ${layer}    ${mode}=5    ${ilist}=None
    ${configResult}    creteconfig.getClassifyValue    ${pkt}    ${layer}    ${mode}    ${ilist}
    验证RESTFUL流量    ${configResult}    
