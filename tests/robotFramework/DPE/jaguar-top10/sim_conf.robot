*** Settings ***
Suite Setup       
Suite Teardown    
Test Setup        
Test Teardown     
Resource          ../testlib/testlib.robot
Resource          ../testlib/features/jaguar.robot
Library           SSHLibrary
Library           rxPortConfig.py
Library           meter.py
Library           meterProfile.py
Library           mirrorPolicy.py
Library           outputMeter.py
Library           destMirror.py
Library           inputPortRx.py
Library           inputPortTx.py
Library           classify.py
Library           profile.py
Library           keyTemplate.py
Library           keyMask.py
Library           mcGroupRx.py
Library           mcGroupTx.py
Library           mcLeafRx.py
Library           mcLeafTx.py
Library           leafActionRx.py
Library           leafActionTx.py

*** Variables ***

*** Test Cases ***
jaguar_sim_meter_00001
    [Documentation]    *验证*
    ${config}    meter.getMeterValue1
    验证配置  ${config}

jaguar_sim_meter_00002
    [Documentation]    *验证*
    ${config}    meter.getMeterValue2
    验证配置  ${config}

jaguar_sim_meterProfile_00001
    [Documentation]    *验证*
    ${config}    meterProfile.getMeterProfileValue1
    验证配置  ${config}

jaguar_sim_meterProfile_00002
    [Documentation]    *验证*
    ${config}    meterProfile.getMeterProfileValue2
    验证配置  ${config}

jaguar_sim_destMirror_00001
    [Documentation]    *验证*
    ${config}    destMirror.getDestMirrorValue1
    验证配置  ${config}

jaguar_sim_destMirror_00002
    [Documentation]    *验证*
    ${config}    destMirror.getDestMirrorValue2
    验证配置  ${config}

jaguar_sim_outputMeter_00001
    [Documentation]    *验证*
    ${config}    outputMeter.getOutputMeterValue1
    验证配置  ${config}

jaguar_sim_outputMeter_00002
    [Documentation]    *验证*
    ${config}    outputMeter.getOutputMeterValue2
    验证配置  ${config}

jaguar_sim_mirrorPolicy_00001
    [Documentation]    *验证*
    ${config}    mirrorPolicy.getMirrorPolicyValue1
    验证配置  ${config}

jaguar_sim_mirrorPolicy_00002
    [Documentation]    *验证*
    ${config}    mirrorPolicy.getMirrorPolicyValue2
    验证配置  ${config}

jnet_sim_inputPortRx
    [Documentation]    *验证*
    ${config}    inputPortRx.getData
    验证配置  ${config}

jnet_sim_inputPortTx
    [Documentation]    *验证*
    ${config}    inputPortTx.getData
    验证配置  ${config}

jnet_sim_classify
    [Documentation]    *验证*
    ${config}    classify.getData
    验证配置  ${config}

jnet_sim_profile
    [Documentation]    *验证*
    ${config}    profile.getData
    验证配置  ${config}

jnet_sim_keyTemplate
    [Documentation]    *验证*
    ${config}    keyTemplate.getData
    验证配置  ${config}

jnet_sim_keyMask
    [Documentation]    *验证*
    ${config}    keyMask.getData
    验证配置  ${config}

jnet_sim_mcGroupRx
    [Documentation]    *验证*
    ${config}    mcGroupRx.getData
    验证配置  ${config}

jnet_sim_mcGroupTx
    [Documentation]    *验证*
    ${config}    mcGroupTx.getData
    验证配置  ${config}

jnet_sim_mcLeafRx
    [Documentation]    *验证*
    ${config}    mcLeafRx.getData
    验证配置  ${config}

jnet_sim_mcLeafTx
    [Documentation]    *验证*
    ${config}    mcLeafTx.getData
    验证配置  ${config}

jnet_sim_leafActionRx
    [Documentation]    *验证*
    ${config}    leafActionRx.getData
    验证配置  ${config}

jnet_sim_leafActionTx
    [Documentation]    *验证*
    ${config}    leafActionRx.getData
    验证配置  ${config}
*** Keywords ***
