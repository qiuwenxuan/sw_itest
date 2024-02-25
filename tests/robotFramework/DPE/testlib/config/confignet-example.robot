*** Settings ***
Documentation     网络特殊配置

*** Variables ***
${ovs}            test
${ovslocal1}      jmnd0    # HOST环回ovs port1
${ovslocal2}      jmnd1    # HOST环回ovs port2
${bridge_tun}     False
${failmode}       standalone
${n_rxq_desc}     256
${n_txq_desc}     256
${ofport_request}    ${1}

