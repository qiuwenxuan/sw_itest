*** Settings ***
Suite Setup       创建GENEVE环境    ${A}
Resource          ../../testlib/testlib.robot    #Suite Teardown    清除GENEVE环境    ${A}    #Test Teardown    Clean Test Environment
Resource          ../../testlib/features/ovs.robot
Library           SSHLibrary

*** Variables ***

*** Test Cases ***
ovs_geneflow_00001
    [Documentation]    *set pass rule match mac to stream*
    [Tags]    RAT    OVS    GENEVE
    ${list1}    create list
    ${config}    Create Dictionary    flowtype=ipv4    protocol=udp    tun_type=geneve    flowRule=${list1}
    testOvsFlow

*** Keywords ***
Clean Test Environment
    run_sys_command    rm -f /home/jaguar/test/vxlan_test/vxlan_ovs_appctl_inbound.log
