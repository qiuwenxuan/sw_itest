*** Settings ***
Documentation     静态路由环境的创建：包含拓扑信息的报文，各个设备间IP的配置，不包含路由配置，路由在各个案例中配置
Resource          public.robot

*** Keywords ***
创建静态路由环境
    [Arguments]    ${A}    ${B}    ${line}=1
    topoRouteInit    ${A}    ${B}    ${line}

清除静态路由环境
    log    ===${A},${B}
    topoPortDel    ${A}<->${B}
    topoPortDel    ${A}<->cha
    topoPortDel    ${B}<->cha

创建静态路由frr环境
    log    ===${A},${B}
    log    frr环境配置开始
    TopoPortSet    ${A}.1<->${B}.1
    TopoPortSet    ${A}.2<->${B}.2
    TopoPortSet    ${A}<->cha
    TopoPortSet    ${B}<->cha
    log    frr环境设置结束

路由环境清配置
    去除配置    ${A}
    去除配置    ${B}
    清理测试仪
