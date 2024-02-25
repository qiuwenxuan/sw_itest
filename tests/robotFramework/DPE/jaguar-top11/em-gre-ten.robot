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
COSSW-8868_em
    [Documentation]    *验证 封装GRE-TENCENT隧道
    ...    a）L3 encap IPV4，使用隧道的封装配置表，封装IPv4 ID/TTL/TOS
    ...    b)? L3 encap IPv6， 使用隧道的封装配置， 封装IPV6 HOP LIMIT/ TOS*
    [Tags]    unknow
    验证EM    [Net][DPE][PIPE]tunnel encap-7

COSSW-11894_em
    [Documentation]    *验证 匹配一层gre-ten隧道sqence id*
    [Tags]    ok    gre-tencent
    验证EM    eth.2vlan.ipv4.gre-tencent.eth.ipv4.udp    OT_TUNNEL_TYPE,OT_TUNNEL_ID,UDF1_EN

COSSW-11895_em
    [Documentation]    *验证 匹配一层gre-ten隧道key id*
    [Tags]    ok    gre-tencent
    验证EM    eth.2vlan.ipv4.gre-tencent.ipv4.udp    OT_TUNNEL_TYPE,OT_TUNNEL_ID

COSSW-11906_em
    [Documentation]    *验证 匹配两层gre-ten隧道sqence id*
    [Tags]    ok    gre-tencent
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.gre-tencent.eth.ipv4.udp    TL_TUNNEL_TYPE,TL_TUNNEL_ID,UDF0_EN

COSSW-11907_em
    [Documentation]    *验证 匹配两层gre-ten隧道key id*
    [Tags]    ok    gre-tencent
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.gre-tencent.eth.ipv4.udp    TL_TUNNEL_TYPE,TL_TUNNEL_ID

*** Keywords ***
组配置初始化
    ${config}    ipv4Config.getGreTencentEmSuiteConfig
    jaguarRunConfig    ${A}    ${config}
    清理测试仪

组配置清理
    ${config}    ipv4Config.getGreTencentEmSuiteConfig
    jaguarClearConfig    ${A}    ${config}
    清理测试仪

验证EM
    [Arguments]    ${pkt}    ${keys}=${None}    ${keylen}=${None}    ${action}=${None}
    ${configResult}    ipv4Config.getEmValue    ${pkt}    ${keys}    ${keylen}    ${action}
    验证RESTFUL流量    ${configResult}
