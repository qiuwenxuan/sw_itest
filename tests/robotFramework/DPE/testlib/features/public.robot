*** Settings ***
Resource          ../config/config.robot
Resource          ../domain/domain.robot
Resource          ../base/base.robot

*** Keywords ***
连接拓扑所有设备
    Topo Dev Connect All

清理测试仪
    Reset Session

清配置
    [Arguments]    ${dut}    ${config}=${None}    # 设备名称
    [Documentation]    清除设备上影响测试的配置
    ...
    ...    根据show run进行删除
    App Clear All    ${dut}    ${config}

去除配置
    [Arguments]    ${dut}    # 设备名称
    [Documentation]    去除已有配置
    ...
    ...    根据配置的内容删除
    sceneOvsDeinit    ${dut}

初始化拓扑TOP20
    TopoLoad    top21
    连接拓扑所有设备
    ${locA}    ${locB}=    TopoGetTop2Type1
    Set Global Variable    ${A}    ${locA}
    Set Global Variable    ${B}    ${locB}

初始化拓扑TOP11-TOPO
    TopoLoad    top11
    连接拓扑所有设备
    ${locA}=    TopoGetTop1Type1
    Set Global Variable    ${A}    ${locA}

初始化拓扑TOP11
    #TopoLoad    top11
    #连接拓扑所有设备
    #${locA}=    TopoGetTop1Type1
    #Set Global Variable    ${A}    ${locA}
    连接设备1
    Tester Connect    ${cha1ip}
    TopoPortSet    cha.1->${A}.1
    TopoPortSet    cha.2->${A}.2

连接设备1
    Import Resource    ../config/configsystem.robot
    TopoLoad    top11
    #${locA}    ${locB}=    TopoGetTop2Type1
    ${locA}=    TopoGetTop1Type1
    Set Global Variable    ${A}    ${locA}
    topoDevConnect    ${A}

初始化仿真拓扑TOP10
    #TopoLoad    top10
    #连接拓扑所有设备
    #${locA}=    TopoGetTop1Type1
    #Set Global Variable    ${A}    ${locA}
    连接设备1

初始化仿真拓扑TOP11
    #TopoLoad    top11
    #连接拓扑所有设备
    #${locA}=    TopoGetTop1Type1
    #Set Global Variable    ${A}    ${locA}
    连接设备1
    Tester Connect    ${cha1ip}
    TopoPortCreate    cha.1->${A}.1
    TopoPortCreate    cha.2->${A}.2