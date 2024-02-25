*** Settings ***
Documentation     验证模拟设备表项下发的正确性
Resource          public.robot
*** Variables ***
${self}    self

*** Keywords ***
验证配置
    [Arguments]    ${config}
    testSimDevConf    ${config}

 验证通道
    [Arguments]    ${config}   
    testSimDevConf    ${config}    ${2}       

验证批量配置
    [Arguments]    ${config}
    testSimDevConf    ${config}    true

验证流量
    [Arguments]    ${config}    ${flow}
    testSimDevFlow    ${config}    ${flow}

验证RESTFUL流量
    [Arguments]    ${config}
    testSimDevFlow    ${config}    true

清除所有配置
    [Arguments]    ${A}
    jaguar.jaguarClearConfigAll    ${A}