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
COSSW-11888_em
    [Documentation]    *验证 匹配一层gre隧道sqence id，seqence_number == 0x12345678来区分使用seq id作为tunid*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.gre-tencent(seqence_number=0x12345678).ipv4.udp    OT_TUNNEL_TYPE,OT_TUNNEL_ID,UDF0_EN
    
COSSW-11900_em
    [Documentation]    *验证 匹配两层gre隧道sqence id，seqence_number == 0x12345678来区分使用seq id作为tunid*
    [Tags]    ok    
    验证EM    eth.2vlan.ipv4.udp.geneve.eth.2vlan.ipv4.gre-tencent(seqence_number=0x12345678).eth.ipv4.udp    TL_TUNNEL_TYPE,TL_TUNNEL_ID

*** Keywords ***
组配置初始化
    ${config}    ipv4Config.getGreTencentSeqIdEmSuiteConfig
    jaguarRunConfig    ${A}    ${config}
    清理测试仪

组配置清理
    ${config}    ipv4Config.getGreTencentSeqIdEmSuiteConfig
    jaguarClearConfig    ${A}    ${config}
    清理测试仪

验证EM
    [Arguments]    ${pkt}    ${keys}=${None}    ${keylen}=${None}    ${action}=${None}
    ${configResult}    ipv4Config.getEmValue    ${pkt}    ${keys}    ${keylen}    ${action}
    验证RESTFUL流量    ${configResult}
