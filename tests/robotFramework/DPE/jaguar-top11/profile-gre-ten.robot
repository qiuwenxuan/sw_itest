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
COSSW-11691_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre-tencent.v4

COSSW-11692_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre-tencent.ipv4-frag(flags=0x1,frag=0x200)

COSSW-11693_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre-tencent.ipv4-frag(frag=0x200)

COSSW-11694_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre-tencent.v4.tcp

COSSW-11695_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre-tencent.v4.udp

COSSW-11696_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre-tencent.v4.icmp

COSSW-11697_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre-tencent.v4(proto=2).igmp

COSSW-11698_Proflie
    [Documentation]    *验证*
    [Tags]    ok    
    验证Profile    eth.v4.gre-tencent.v4.sctp

COSSW-11699_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre-tencent.ipv4-frag(flags=0x1,proto=6)

COSSW-11700_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre-tencent.ipv4-frag(flags=0x1,proto=17)

COSSW-11701_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre-tencent.ipv4-frag(flags=0x1).udp(dport=4791)

COSSW-11702_Proflie
    [Documentation]    *验证*
    [Tags]    ok    
    验证Profile    eth.v4.gre-tencent.ipv4-option.udp

COSSW-11703_Proflie
    [Documentation]    *验证*
    [Tags]    ok    
    验证Profile    eth.v4.gre-tencent.ipv4-option.tcp

COSSW-11704_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre-tencent.v6.tcp

COSSW-11705_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre-tencent.v6.udp

COSSW-11706_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.gre-tencent.v6.icmp6

COSSW-11707_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre-tencent.v6

COSSW-11708_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre-tencent.v6-ext

COSSW-11709_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre-tencent.v4

COSSW-11710_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre-tencent.ipv4-frag(flags=0x1,frag=0x200)

COSSW-11711_Proflie
    [Documentation]    *验证*
    [Tags]    ok    
    验证Profile    eth.v6.gre-tencent.ipv4-option

COSSW-11712_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre-tencent.v6.tcp

COSSW-11713_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre-tencent.v6.udp

COSSW-11714_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre-tencent.v6.udp(dport=4791)

COSSW-11715_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre-tencent.v6.icmp6

COSSW-11716_Proflie
    [Documentation]    *验证*
    [Tags]    ok    
    验证Profile    eth.v6.gre-tencent.v6.sctp

COSSW-11717_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre-tencent.ipv6-ext.tcp

COSSW-11718_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre-tencent.ipv6-ext.udp

COSSW-11719_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre-tencent.v4.tcp

COSSW-11720_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre-tencent.v4.udp

COSSW-11721_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.gre-tencent.v4.icmp

COSSW-11832_Proflie
    [Documentation]    *验证*
    [Tags]    ok    
    验证Profile    eth.qinq.v4.gre-tencent.v4.gre-tencent.v6.sctp

COSSW-11833_Proflie
    [Documentation]    *验证*
    [Tags]    ok    
    验证Profile    eth.qinq.v6.gre-tencent.v6.udp.geneve.v6.udp(dport=8585)

*** Keywords ***
组配置初始化
    ${config}    ipv4Config.getGreTencentProfileSuiteConfig
    jaguarRunConfig    ${A}    ${config}
    清理测试仪

组配置清理
    ${config}    ipv4Config.getGreTencentProfileSuiteConfig
    jaguarClearConfig    ${A}    ${config}
    清理测试仪

验证Profile
    [Arguments]    ${arg1}
    ${configResult}    ipv4Config.getProfileValue    ${arg1}
    验证RESTFUL流量    ${configResult}
