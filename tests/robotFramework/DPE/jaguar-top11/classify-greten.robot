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
COSSW-8669_ClassifyIpv4TencentGreValue
    [Documentation]    *验证*
    [tags]    nok    自动化需要配置寄存器
    验证classify    eth.v6.gre-tencent.ipv4.udp    tl    -1    OT_TUNNEL_ID

COSSW-8670_ClassifyIpv4TencentGreValue
    [Documentation]    *验证*
    验证classify    eth.v6.gre-tencent.ipv4.udp    tl    -1    ???

COSSW-8671_ClassifyIpv4TencentGreValue
    [Documentation]    *验证*
    [tags]    ok
    验证classify    eth.v6.gre-tencent.ipv4.udp    tl    -1    OUT_TUNNEL_TYPE

*** Keywords ***
组配置初始化
    ${config}    ipv4Config.getClassifySuiteConfig
    ${registerconfig}    ipv4Config.getGreTencentRegConfig
    jaguarRunConfig    ${A}    ${config}
    jaguarRunConfig    ${A}    ${registerconfig}
    清理测试仪

组配置清理
    ${config}    ipv4Config.getClassifySuiteConfig
    ${registerconfig}    ipv4Config.getGreTencentRegConfig
    jaguarClearConfig    ${A}    ${config}
    jaguarClearConfig    ${A}    ${registerconfig}
    清理测试仪

验证classify
    [Arguments]    ${pkt}    ${layer}    ${mode}=5    ${ilist}=None
    ${configResult}    ipv4Config.getClassifyValue    ${pkt}    ${layer}    ${mode}    ${ilist}
    验证RESTFUL流量    ${configResult}    
