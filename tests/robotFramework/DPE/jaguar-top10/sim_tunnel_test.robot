*** Settings ***
Suite Setup       
Suite Teardown    
Test Setup        
Test Teardown     
Resource          ../testlib/testlib.robot
Resource          ../testlib/features/jaguar.robot
Library           SSHLibrary
Library           tunneltest.py

*** Variables ***

*** Test Cases ***
jaguar_sim_tunnel_test_00001
    [Documentation]    *验证*
    FOR    ${i}    IN RANGE     2
        ${config}    tunneltest.getData
        验证通道  ${config}    
    END



*** Keywords ***
