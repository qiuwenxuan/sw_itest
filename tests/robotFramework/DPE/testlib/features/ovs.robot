*** Settings ***
Documentation     静态路由环境的创建：包含拓扑信息的报文，各个设备间IP的配置，不包含路由配置，路由在各个案例中配置
Resource          public.robot

*** Variables ***
${Bridge_Name}    br-ext
${Bridge_Internal}    br-int
${Bridge_Tun}     br-tun
${datapath_type}    netdev
${failmode}       standalone
${dpdk-devargs0}    0000:ec:01.1
${dpdk-devargs1}    0000:ec:09.1
${port0}          dpdk0
${port1}          dpdk1
${interface_type}    dpdk
${n_rxq_desc}     256
${n_txq_desc}     256
${ofport_request}    ${1}
${dl_dst}         52:54:00:44:e8:3b

*** Keywords ***
创建OVS环境
    [Arguments]    ${A}    @{rest}
    sceneOvsInlineInit    ${A}    @{rest}

创建OVS-ONE环境
    [Arguments]    ${A}    @{rest}
    sceneOvsSigleBridgeInit    ${A}    @{rest}

创建OVS-DOUBLE环境
    [Arguments]    ${A}    @{rest}
    sceneOvsDoubleBridgeInit    ${A}    @{rest}

创建OVS-THREE环境
    [Arguments]    ${A}    @{rest}
    sceneOvsThreeBridgeInit    ${A}    @{rest}

清除OVS环境
    [Arguments]    ${A}
    sceneOvsDeinit    ${A}
    清理测试仪

创建TESTPMD环境
    [Arguments]    ${A}    @{rest}
    sceneTestpmdInlineInit    ${A}    @{rest}

清除TESTPMD环境
    [Arguments]    ${A}    @{rest}
    sceneTestpmdDeinit    ${A}
    清理测试仪

创建OVS单桥环境
    [Arguments]    ${A}
    ${config}    Create Dictionary    type=${datapath_type}
    Ovs.gotoBridge    ${A}    ${Bridge_Name}    ${config}
    ${options}    Create Dictionary    dpdk-devargs=${dpdk-devargs0}    n_rxq_desc=${n_rxq_desc}    n_txq_desc=${n_txq_desc}
    ${config}    Create Dictionary    type=${interface_type}    options=${options}    ofport_request=${ofport_request}
    Ovs.gotoPort    ${A}    ${Bridge_Name}    ${port0}    ${config}
    ${options}    Create Dictionary    dpdk-devargs=${dpdk-devargs1}    n_rxq_desc=${n_rxq_desc}    n_txq_desc=${n_txq_desc}
    ${config}    Create Dictionary    type=${interface_type}    options=${options}    ofport_request=${ofport_request}
    Ovs.gotoPort    ${A}    ${Bridge_Name}    ${port1}    ${config}

清除OVS单桥环境
    [Arguments]    ${A}
    Ovs.delBridge    ${A}    ${Bridge_Name}

创建VXLAN环境
    [Arguments]    ${A}
    ${vxlanconfig}    chaipv4config.getVxlanConfig
    ovsRunConfig    ${A}    ${vxlanconfig}

创建VXLAN环境AC
    [Arguments]    ${A}
    ${vxlanconfig}    chaipv4config.getVxlanConfigAc
    ovsRunConfig    ${A}    ${vxlanconfig}

清除VXLAN环境
    [Arguments]    ${A}
    Ovs.delBridge    ${A}    ${Bridge_Name}
    Ovs.delBridge    ${A}    ${Bridge_Internal}
    Ovs.delBridge    ${A}    ${Bridge_Tun}

清除VXLAN环境AC
    [Arguments]    ${A}
    Ovs.delBridge    ${A}    ${Bridge_Name}
    Ovs.delBridge    ${A}    ${Bridge_Internal}
    Ovs.delBridge    ${A}    ${Bridge_Tun}

创建GENEVE环境
    [Arguments]    ${A}
    ${geneveconfig}    chaipv4config.getGeneveConfig
    ovsRunConfig    ${A}    ${geneveconfig}

清除GENEVE环境
    [Arguments]    ${A}
    Ovs.delBridge    ${A}    ${Bridge_Name}
    Ovs.delBridge    ${A}    ${Bridge_Internal}
    Ovs.delBridge    ${A}    ${Bridge_Tun}

验证三层流量
    [Arguments]    @{args}    &{match}
    ${action}    appTransformToDict    type=${args}[0]
    ${flow1}    Create Dictionary    match=${match}    action=${action}
    ${flow}    create list    ${flow1}
    ${config}    Create Dictionary    flowtype=${args}[1]    protocol=${args}[2]    flowRule=${flow}
    testOvsFlow    ${config}

验证OVS流量
    [Arguments]    @{args}    &{argsd}
    ${flow1}    Ovs.flowTransArgToDict    &{argsd}
    ${flow}    create list    ${flow1}
    ${config}    Create Dictionary    flowtype=${args}[1]    protocol=${args}[2]    flowRule=${flow}
    testOvsFlow    ${config}

验证ovs-hw-offload流量
    [Arguments]    @{args}    &{argsd}
    ${flow1}    Ovs.flowTransArgToDict    &{argsd}
    ${flow}    create list    ${flow1}
    ${config}    Create Dictionary    flowtype=${args}[1]    protocol=${args}[2]    flowRule=${flow}    hw_offload=true
    testOvsFlow    ${config}

验证ovs-vxlan-encap-hw-offload流量
    [Arguments]    @{args}    &{argsd}
    ${flow1}    Ovs.flowTransArgToDict    &{argsd}
    ${flow}    create list    ${flow1}
    ${config}    Create Dictionary    flowtype=${args}[1]    protocol=${args}[2]    flowRule=${flow}    hw_offload=true    tunnel_encap=true    tunnel_type=vxlan
    testOvsFlow    ${config}

验证ovs-tunnel-hw-offload流量
    [Arguments]    @{args}    &{argsd}
    ${flow1}    Ovs.flowTransArgToDict    &{argsd}
    ${flow}    create list    ${flow1}
    ${config}    Create Dictionary    flowtype=${args}[1]    protocol=${args}[2]    tun_type=${args}[3]    flowRule=${flow}    hw_offload=true
    testOvsFlow    ${config}

验证三层流量-多流
    [Arguments]    ${action}    ${flowtype}    ${protocol}    @{args}
    @{flow}    Create List
    FOR    ${item}    IN    @{args}
        ${matchitem}    appTransformToDict    ${item}
        ${flowitem}    Create Dictionary    match=${matchitem}    action=${action}
        Append To List    ${flow}    ${flowitem}
    END
    ${config}    Create Dictionary    flowtype=${flowtype}    protocol=${protocol}    flowrule=${flow}
    testOvsFlow    ${config}

验证二层流量
    [Arguments]    ${output}    ${dstmac}=${dl_dst}    ${protocol}=udp    ${dltype}=0x0806
    ${match}    Create Dictionary    in_port=${port0}    dl_dst=${dstmac}    dl_type=${dltype}
    ${action}    Create Dictionary    output=${output}
    ${rule}    Create Dictionary    match=${match}    action=${action}
    @{list}    Create List    ${rule}
    ${locconfig}    Create Dictionary    flowtype=ipv4    protocol=${protocol}    flowRule=${list}
    Set Global Variable    ${config}    ${locconfig}

验证TESTPMD流量
    [Arguments]    @{args}    &{argsd}
    ${flow1}    Ovs.flowTransArgToDict    &{argsd}
    ${flow}    create list    ${flow1}
    ${config}    Create Dictionary    flowtype=${args}[1]    protocol=${args}[2]    flowRule=${flow}    hw_offload=true
    testPmdFlow    ${config}
