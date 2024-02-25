*** Settings ***
Suite Setup       初始化拓扑TOP11
Suite Teardown    清理测试仪  
Test Teardown     清理测试仪    
Force Tags        route
Resource          ../testlib/testlib.robot

*** Keywords ***