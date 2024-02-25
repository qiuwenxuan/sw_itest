*** Settings ***
Documentation     网桥、端口配置已经完成，指定测试仪和端口dpdk端口的对应关系
...               dpdk0 ------ 101/0
...               dpdk1 ------ 101/1
Suite Setup       初始化拓扑TOP11-TOPO
Suite Teardown    清理测试仪
Force Tags        OVS    INLINE
Resource          ../testlib/testlib.robot

*** Keywords ***
