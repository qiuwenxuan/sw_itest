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
COSSW-8507_Proflie
    [Documentation]    *验证*
    [Tags]    ok    基础通路
    验证Profile    eth.v4.nvgre.eth

COSSW-8508_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.nvgre.eth.vlan.arp

COSSW-8509_Proflie
    [Documentation]    *验证*
    [Tags]    unknown
    验证Profile    eth.v4.nvgre.eth.vlan.rocev1

COSSW-8510_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.nvgre.eth.vlan.v4

COSSW-8511_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.nvgre.eth.vlan.ipv4-frag(flags=0x1,frag=0x200)

COSSW-8512_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.nvgre.eth.vlan.ipv4-frag(frag=0x200)

COSSW-8513_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.nvgre.eth.qinq.v4.tcp

COSSW-8514_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.nvgre.eth.qinq.v4.udp

COSSW-8515_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.nvgre.eth.qinq.v4.icmp

COSSW-8516_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.nvgre.eth.qinq.v4.igmp

COSSW-8517_Proflie
    [Documentation]    *验证*
    [Tags]    ok    
    验证Profile    eth.v4.nvgre.eth.qinq.v4.sctp

COSSW-8518_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.nvgre.eth.qinq.ipv4-frag(flags=0x1,frag=0x200,proto=6)

COSSW-8519_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.nvgre.eth.qinq.ipv4-frag(flags=0x1,frag=0x200,proto=17)

COSSW-8520_Proflie
    [Documentation]    *验证*
    [Tags]    ok    
    验证Profile    eth.v4.nvgre.eth.qinq.ipv4-frag(flags=0x1,frag=0x200,proto=17)

COSSW-8521_Proflie
    [Documentation]    *验证*
    [Tags]    ok    
    验证Profile    eth.v4.nvgre.eth.qinq.ipv4-option.tcp

COSSW-8522_Proflie
    [Documentation]    *验证*
    [Tags]    ok    
    验证Profile    eth.v4.nvgre.eth.qinq.ipv4-option.udp

COSSW-8523_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.nvgre.eth.qinq.v6.tcp

COSSW-8524_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.nvgre.eth.qinq.v6.udp

COSSW-8525_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v4.nvgre.eth.qinq.v6.icmp6

COSSW-8526_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.nvgre.eth

COSSW-8527_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.nvgre.eth.vlan.arp

COSSW-8528_Proflie
    [Documentation]    *验证*
    [Tags]    unknown
    验证Profile    eth.v6.nvgre.eth.vlan.rocev1

COSSW-8529_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.nvgre.eth.vlan.v6

COSSW-8530_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.nvgre.eth.vlan.v6-ext

COSSW-8531_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.nvgre.eth.vlan.v4

COSSW-8532_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.nvgre.eth.vlan.ipv4-frag(flags=0x1,frag=0x200)

COSSW-8533_Proflie
    [Documentation]    *验证*
    [Tags]    ok    
    验证Profile    eth.v6.nvgre.eth.vlan.ipv4-option(flags=0x2)

COSSW-8534_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.nvgre.eth.qinq.v6.tcp

COSSW-8535_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.nvgre.eth.qinq.v6.udp

COSSW-8536_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.nvgre.eth.qinq.v6.udp(dport=4791)

COSSW-8537_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.nvgre.eth.qinq.v6.icmp6

COSSW-8538_Proflie
    [Documentation]    *验证*
    [Tags]    ok    
    验证Profile    eth.v6.nvgre.eth.qinq.v6.sctp

COSSW-8539_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.nvgre.eth.qinq.v6-ext.tcp

COSSW-8540_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.nvgre.eth.qinq.v6-ext.udp

COSSW-8541_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.nvgre.eth.qinq.v4.tcp

COSSW-8542_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.nvgre.eth.qinq.v4.udp

COSSW-8543_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.v6.nvgre.eth.qinq.v4.icmp

COSSW-11826_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.qinq.v4.nvgre.eth.qinq.v4.nvgre.eth.qinq.v6.icmp6

COSSW-11830_Proflie
    [Documentation]    *验证*
    [Tags]    ok
    验证Profile    eth.qinq.v6.nvgre.eth.v6.udp.geneve.v6.tcp(dport=8686)

*** Keywords ***
组配置初始化
    ${config}    ipv4Config.getNvgreProfileSuiteConfig
    jaguarRunConfig    ${A}    ${config}
    清理测试仪

组配置清理
    ${config}    ipv4Config.getNvgreProfileSuiteConfig
    jaguarClearConfig    ${A}    ${config}
    清理测试仪

验证Profile
    [Arguments]    ${arg1}
    ${configResult}    ipv4Config.getProfileValue    ${arg1}
    验证RESTFUL流量    ${configResult}
