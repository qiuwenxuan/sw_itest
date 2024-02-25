*** Settings ***
Suite Setup       清理测试仪
Suite Teardown    清理测试仪
Test Setup        清理测试仪
Test Teardown     清理测试仪
Force Tags        MATCH    FWD
Resource          ../../testlib/testlib.robot
Resource          ../../testlib/features/ovs.robot

*** Variables ***

*** Test Cases ***
ovs_set_00001
    [Documentation]    *set l2 src mac to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_src=\

ovs_set_00002
    [Documentation]    *set  l2 dst mac to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_dst=\

ovs_set_00003
    [Documentation]    *set l3 src ip to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\

ovs_set_00004
    [Documentation]    *set  l3 dst ip to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_dst=\

ovs_set_00005
    [Documentation]    *set l3 src and dst ip to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_nw_dst=\

ovs_set_00006
    [Documentation]    *set l2 src and dst mac to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_src=\    -mod_dl_dst=\

ovs_set_00007
    [Documentation]    *set l2 src mac and l3 src ip to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_dl_src=\

ovs_set_00008
    [Documentation]    *set l2 dst mac and l3 src ip to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_dl_dst=\

ovs_set_00009
    [Documentation]    *set l2 src mac and l3 dst ip to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_dst=\    -mod_dl_src=\

ovs_set_00010
    [Documentation]    *set l2 dst mac and l3 dst ip to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_dst=\    -mod_dl_dst=\

ovs_mod_00011
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_src=\    -mod_dl_dst=\    -mod_nw_src=\

ovs_mod_00012
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_src=\    -mod_dl_dst=\    -mod_nw_dst=\

ovs_mod_00013
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_src=\

ovs_mod_00014
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_dst=\

ovs_mod_00015
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_src=\    -mod_dl_dst=\    -mod_nw_src=\    -mod_nw_dst=\

ovs_mod_00032
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_src=\    -mod_tp_dst=\

ovs_mod_00033
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_dst=\    -mod_tp_dst=\

ovs_mod_00034
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_tp_dst=\

ovs_mod_00035
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_dst=\    -mod_tp_dst=\

ovs_mod_00036
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_nw_dst=\    -mod_tp_dst=\

ovs_mod_00037
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_src=\    -mod_dl_dst=\    -mod_tp_dst=\

ovs_mod_00038
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_dl_src=\    -mod_tp_dst=\

ovs_mod_00039
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_dl_dst=\    -mod_tp_dst=\

ovs_mod_00040
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_dst=\    -mod_dl_src=\    -mod_tp_dst=\

ovs_mod_00041
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_dst=\    -mod_dl_dst=\    -mod_tp_dst=\

ovs_mod_00042
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_src=\    -mod_tp_src=\

ovs_mod_00043
    [Documentation]    *set l2 dst mac and l4 src port to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_dst=\    -mod_tp_src=\

ovs_mod_00044
    [Documentation]    *set l3 src ip and l4 src port to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_tp_src=\

ovs_mod_00045
    [Documentation]    *set l3 dst ip and l4 src port to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_dst=\    -mod_tp_src=\

ovs_mod_00046
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_nw_dst=\    -mod_tp_src=\

ovs_mod_00047
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_src=\    -mod_dl_dst=\    -mod_tp_src=\

ovs_mod_00048
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_dl_src=\    -mod_tp_src=\

ovs_mod_00049
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_dl_dst=\    -mod_tp_src=\

ovs_mod_00050
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_dst=\    -mod_dl_src=\    -mod_tp_src=\

ovs_mod_00051
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_dst=\    -mod_dl_dst=\    -mod_tp_src=\

ovs_mod_00052
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_src=\    -mod_tp_src=\    -mod_tp_dst=\

ovs_mod_00053
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_dst=\    -mod_tp_src=\    -mod_tp_dst=\

ovs_mod_00054
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_tp_src=\    -mod_tp_dst=\

ovs_mod_00055
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_dst=\    -mod_tp_src=\    -mod_tp_dst=\

ovs_mod_00056
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_nw_dst=\    -mod_tp_src=\    -mod_tp_dst=\

ovs_mod_00057
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_dl_src=\    -mod_dl_dst=\    -mod_tp_src=\    -mod_tp_dst=\

ovs_mod_00058
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_dl_src=\    -mod_tp_src=\    -mod_tp_dst=\

ovs_mod_00059
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_src=\    -mod_dl_dst=\    -mod_tp_src=\    -mod_tp_dst=\

ovs_mod_00060
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_dst=\    -mod_dl_src=\    -mod_tp_src=\    -mod_tp_dst=\

ovs_mod_00061
    [Documentation]    *set pass rule match nw_src dl_src nw_dst dl_dst to stream*
    验证ovs-hw-offload流量    fwd    ipv4    udp    -mod_nw_dst=\    -mod_dl_dst=\    -mod_tp_src=\    -mod_tp_dst=\

*** Keywords ***
