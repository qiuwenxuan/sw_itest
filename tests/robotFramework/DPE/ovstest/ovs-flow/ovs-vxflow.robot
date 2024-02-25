*** Settings ***
Suite Setup       创建VXLAN环境    ${A}
Suite Teardown    清除VXLAN环境    ${A}
Test Teardown     Clean Test Environment
Resource          ../../testlib/testlib.robot
Resource          ../../testlib/features/ovs.robot
Library           SSHLibrary

*** Variables ***

*** Test Cases ***
ovs_vxflow_00001
    [Documentation]    *set pass rule match mac to stream*
    [Tags]    RAT    OVS    VXLAN
    ${list1}    create list
    ${config}    Create Dictionary    flowtype=ipv4    protocol=udp    tunlType=vxlan    flowRule=${list1}
    testOvsFlow    config=${config}

*** Keywords ***
Clean Test Environment
    run_sys_command    rm -f /home/jaguar/test/vxlan_test/vxlan_ovs_appctl_inbound.log
