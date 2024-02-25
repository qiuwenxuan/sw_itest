*** Settings ***
Suite Setup       Tester Connect    ${cha1ip}
Resource          ../testlib/testlib.robot

*** Test Cases ***
加载测试仪
    ${chaconfig}    chaipv4config.Get Config
    Cha Config    ${chaconfig}

测试仪发流
    ${chaconfig}    chaipv4config.Get Config
    Cha Config    ${chaconfig}
    ${chaconfig}    chaipv4config.Get Profile
    Cha Config    ${chaconfig}
    SendArpRequest
    startProfile    profile1
    Sleep    3s
    stopProfile    profile1
    profileShouldRXeqZero    profile1

清理测试仪
    清理测试仪
