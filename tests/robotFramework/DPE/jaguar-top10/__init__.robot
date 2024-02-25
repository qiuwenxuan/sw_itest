*** Settings ***
Suite Setup       初始化仿真拓扑TOP10
Suite Teardown    
Force Tags        route
Resource          ../testlib/testlib.robot
Resource          ../testlib/features/jaguar.robot 
*** Keywords ***