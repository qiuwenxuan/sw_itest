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
COSSW-8565_InportAction
    [Documentation]    *验证 input表：
    ...    opcode：0，action type: 0
    ...    default destination: 直接发送的目的地
    [Tags]    ok    基础通路    
    验证INPORT-ACTION    eth.ipv4.tcp    drop    

COSSW-8569_InportAction1
    [Documentation]    *RX 收到报文后， 使用默认的Action转发*
    [Tags]    ok    基础通路
    验证INPORT-ACTION    eth.ipv4.tcp    action    REPLACE_L4_DPORT

COSSW-8589_InportAction1
    [Documentation]    *Tx loopback报文 对于环回的报文，开启Antispoof功能（TPID检查，VLAN优先级检查，SMAC检查）报文不做Antispoof*
    [Tags]    test    基础通路
    验证INPORT-ACTION    eth.ipv4.tcp    action    REPLACE_L4_DPORT

*** Keywords ***
组配置初始化
    ${config}    ipv4Config.getInportActionSuiteConfig
    jaguarRunConfig    ${A}    ${config}
    清理测试仪

组配置清理
    ${config}    ipv4Config.getInportActionSuiteConfig
    jaguarClearConfig    ${A}    ${config}
    清理测试仪

验证INPORT-ACTION
    [Arguments]    ${pkt}    ${atype}=${None}    ${action}=${None}
    ${configResult}    ipv4Config.getInportActionValue    ${pkt}    ${atype}    ${action}
    验证RESTFUL流量    ${configResult}