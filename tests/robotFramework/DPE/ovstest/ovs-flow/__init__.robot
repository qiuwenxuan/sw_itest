*** Settings ***
Suite Setup       初始化拓扑TOP11
Suite Teardown    清理测试仪
Force Tags        route
Resource          ../../testlib/testlib.robot

*** Keywords ***
清理测试仪及TOP11
    清理测试仪
