*** Settings ***
Suite Setup       清理测试仪
Suite Teardown    清理测试仪
Test Setup        清理测试仪
Test Teardown     清理测试仪
Force Tags        MOD    FWD
Resource          ../../testlib/testlib.robot

*** Variables ***

*** Test Cases ***
ovs_mod_00001
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证OVS流量    fwd    ipv4    udp    -mod_dl_src=\

ovs_mod_00002
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证OVS流量    fwd    ipv4    udp    -mod_dl_dst=\

ovs_mod_00003
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证OVS流量    fwd    ipv4    udp    -mod_nw_src=\

ovs_mod_00004
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证OVS流量    fwd    ipv4    udp    -mod_nw_dst=\

*** Keywords ***
