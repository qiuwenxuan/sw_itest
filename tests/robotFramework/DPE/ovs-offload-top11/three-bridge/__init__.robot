*** Settings ***
Suite Setup       创建OVS-THREE环境    ${A}    -tun_type=vxlan
Suite Teardown    清除OVS环境    ${A}
Test Teardown
Resource          ../../testlib/testlib.robot
