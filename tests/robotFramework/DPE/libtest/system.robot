*** Settings ***
Library           SSHLibrary
Resource          ../testlib/config/configsystem.robot

*** Variables ***

*** Test Cases ***
connet
    Open Connection    ${dut1ip}    alias=linux1
    Login    ${dut1user}    ${dut1password}    alias=linux1
    ${output}=    Execute Command    uname -r
    Close All Connections
