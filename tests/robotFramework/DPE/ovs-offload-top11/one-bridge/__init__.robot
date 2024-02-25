*** Settings ***
Suite Setup       创建OVS-ONE环境    ${A}
Suite Teardown    清除OVS环境    ${A}
Test Teardown     清理测试仪
Resource          ../../testlib/testlib.robot
