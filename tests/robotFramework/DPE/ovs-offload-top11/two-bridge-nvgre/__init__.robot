*** Settings ***
Suite Setup       创建OVS-DOUBLE环境    ${A}    -tun_type=nvgre
Suite Teardown    清除OVS环境    ${A}
Test Teardown
Resource          ../../testlib/testlib.robot
