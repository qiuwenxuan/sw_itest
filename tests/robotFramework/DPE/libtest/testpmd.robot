*** Settings ***
Suite Setup       连接设备1
Resource          ../testlib/testlib.robot

*** Test Cases ***
TESTPMD
    pmdConnect    ${A}
    ${info}    pmdProcess    ${A}    show port info all
    log    ${info}
    ${info}    pmdProcess    ${A}    show port stats all
    log    ${info}
    ${info}    Testpmd.getPortInfo    ${A}
    log    ${info}
    ${info}    Testpmd.getPortStats    ${A}
    log    ${info}
