*** Settings ***
Documentation     静态路由环境的创建：包含拓扑信息的报文，各个设备间IP的配置，不包含路由配置，路由在各个案例中配置
Resource          public.robot

*** Variables ***

*** Keywords ***
创建TESTPMD环境
    [Arguments]    ${A}    @{rest}
    sceneOvsInlineInit    ${A}    @{rest}

清除TESTPMD环境
    [Arguments]    ${A}    @{rest}
    sceneOvsDeinit    ${A}
    清理测试仪
