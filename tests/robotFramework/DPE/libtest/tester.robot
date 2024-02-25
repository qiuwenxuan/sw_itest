*** Settings ***
Suite Setup       Tester Connect    ${cha1ip}
Suite Teardown    清理测试仪
Test Teardown
Resource          ../testlib/testlib.robot

*** Test Cases ***
IPV4测试包
    ${chaconfig}    chaipv4config.Get Config
    Cha Config    ${chaconfig}
    Send Arp Request    host1

复制host
    ${chaconfig}    chaipv4config.Get Config
    Cha Config    ${chaconfig}
    Clone Host    host1    2

清理测试仪
    Reset Session
