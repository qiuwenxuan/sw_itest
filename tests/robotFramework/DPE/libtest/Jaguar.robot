*** Settings ***
Suite Setup       连接设备1
Resource          ../testlib/testlib.robot

*** Test Cases ***
POST
    ${info}    getTable    ${A}    meter_table
    log    ${info}
