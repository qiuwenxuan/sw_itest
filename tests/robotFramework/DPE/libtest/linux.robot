*** Settings ***
Suite Setup       连接设备1
Resource          ../testlib/testlib.robot

*** Test Cases ***
获取接口MAC
    ${mac}    Linux.Get Interface Mac    ${A}    virbr0
    ${info}    Process    ${A}    ip link show
    ${info}    arpShow    ${A}
    log    ${info}

获取目录
    ${info}    Process    ${A}    ls
    log    ${info}
    appRunKeywordError    2    AppDut.Process    ${A}    ls jfie

