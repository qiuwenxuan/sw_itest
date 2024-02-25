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
COSSW-8394_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.ipv4(chksum=1).udp
    验证Profile    ipv4(version=1)
    验证Profile    ipv4(len=20000)
    验证Profile    ipv4(len=1)

COSSW-8395_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    ipv4(chksum=1).UDP

COSSW-8396_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    ipv4(chksum=1).ICMP

COSSW-8407_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    IPv6(version=1)

COSSW-8408_Proflie
    [Documentation]    *验证*
    [tags]    nok    error不会配
    验证Profile    IPV6.TCP(chksum=1)

COSSW-8409_Proflie
    [Documentation]    *验证*
    [tags]    nok    error不会配
    验证Profile    IPV6.UDP(chksum=1)

COSSW-8410_Proflie
    [Documentation]    *验证*
    [tags]    nok    error不会配
    验证Profile    IPV6.ICMP(chksum=1)

COSSW-8564_Proflie
    [Documentation]    *验证*
    [tags]    nok    用例构造问题
    验证Profile    eth.qinq.v6.udp.geneve.v6.udp.vxlan.IPv6(version=1).TCP(chksum=1)

*** Keywords ***
组配置初始化
    ${config}    ipv4Config.getErrorPktProfileSuiteConfig
    jaguarRunConfig    ${A}    ${config}
    清理测试仪

组配置清理
    ${config}    ipv4Config.getErrorPktProfileSuiteConfig
    jaguarClearConfig    ${A}    ${config}
    清理测试仪

验证Profile
    [Arguments]    ${arg1}
    ${configResult}    ipv4Config.getErrorPktProfileValue    ${arg1}
    验证RESTFUL流量    ${configResult}
