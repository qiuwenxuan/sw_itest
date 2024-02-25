*** Settings ***
Suite Setup       组配置初始化
Suite Teardown    组配置清理
Test Setup        清理测试仪
Test Teardown     清理测试仪
Resource          ../testlib/testlib.robot
Resource          ../testlib/features/jaguar.robot
Library           SSHLibrary
Library           ipv4config.py

*** Variables ***

*** Test Cases ***
COSSW-8364_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.ipv4

COSSW-8367_Proflie
    [Documentation]    *验证*
    [tags]    unknown
    验证Profile    MAC.VLAN.unknown

COSSW-8368_Proflie
    [Documentation]    *验证*
    [tags]    ROCEv1
    验证Profile    ETH.VLAN.ROCEv1

COSSW-8369_Proflie
    [Documentation]    *验证 tpid遍历*
    [tags]    ok
    验证Profile    ETH.VLAN.ARP
    验证Profile    ETH.2VLAN.ARP

COSSW-8373_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    ipv4.tcp
    验证Profile    ipv4-frag(flags=0x1,frag=0x01).tcp
    验证Profile    ipv4-frag(flags=0x1).tcp     
    验证Profile    ipv4-option.tcp

COSSW-8375_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    ETH.IPV4.UDP

COSSW-8382_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    ETH.2VLAN.IPV4

COSSW-8389_Proflie
    [Documentation]    *验证*
    [tags]    ok    基础通路
    验证Profile    IPV4.UDP

COSSW-8390_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    IPV4.ICMP

COSSW-8391_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    IPV4(proto=2).IGMP

COSSW-8392_Proflie
    [Documentation]    *验证* 
    [tags]    ok    
    验证Profile    IPV4.SCTP

COSSW-8393_Proflie
    [Documentation]    *验证*
    [tags]    nok    ROCEv2
    验证Profile    IPV4.ROCEv2

COSSW-8397_Proflie
    [Documentation]    *验证*
    [tags]    ok    基础通路
    验证Profile    ipv6.tcp

COSSW-8398_Proflie
    [Documentation]    *验证*
    [tags]    ok    报文比较问题,先不比较options
    验证Profile    ipv6-ext.tcp

COSSW-8399_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    IPV6.TCP

COSSW-8403_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    IPV6.UDP

COSSW-8404_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    IPV6.ICMP6

COSSW-8405_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    IPV6.SCTP

COSSW-8406_Proflie
    [Documentation]    *验证*
    [tags]    nok    rocev2
    验证Profile    IPV6.ROCEv2

COSSW-8411_Proflie
    [Documentation]    *验证*
    [tags]    ok    基础通路
    验证Profile    eth.v4.udp.vxlan.eth

COSSW-8412_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.vxlan.eth.vlan.arp

COSSW-8413_Proflie
    [Documentation]    *验证*
    [tags]    nok    rocev1
    验证Profile    eth.v4.udp.vxlan.eth.2vlan.rocev1

COSSW-8414_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.vlan.v4.udp.vxlan.eth.vlan.v4

COSSW-8415_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.tcp

COSSW-8416_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.udp

COSSW-8417_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.icmp

COSSW-8418_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.vlan.v4.udp.vxlan.eth.2vlan.v4(proto=2).igmp

COSSW-8419_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.sctp

COSSW-8420_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.qinq.v4.udp.vxlan.eth.vlan.ipv4-frag(flags=1,frag=0).tcp

COSSW-8421_Proflie
    [Documentation]    *验证 首片*
    [tags]    ok
    验证Profile    eth.qinq.v4.udp.vxlan.eth.vlan.ipv4-frag(flags=1,frag=0).udp

COSSW-8422_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.qinq.v4.udp.vxlan.eth.vlan.ipv4-frag(flags=1,frag=0x200)

COSSW-8423_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.qinq.v4.udp.vxlan.eth.vlan.ipv4-frag(frag=0x200)

COSSW-8424_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.vlan.v4.udp.vxlan.eth.2vlan.v6.tcp

COSSW-8425_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.vlan.v4.udp.vxlan.eth.2vlan.v6.udp

COSSW-8426_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.vlan.v4.udp.vxlan.eth.2vlan.v6.icmp6

COSSW-8427_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan.eth

COSSW-8428_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan.eth.vlan.arp

COSSW-8429_Proflie
    [Documentation]    *验证*
    [tags]    nok    rocev1
    验证Profile    eth.v6.udp.vxlan.eth.qinq.rocev1

COSSW-8430_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.vlan.v6.udp.vxlan.eth.vlan.v6

COSSW-8431_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.vlan.v6.udp.vxlan.eth.2vlan.v6.tcp

COSSW-8432_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.vlan.v6.udp.vxlan.eth.2vlan.v6.udp

COSSW-8433_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.vlan.v6.udp.vxlan.eth.2vlan.v6.icmp6

COSSW-8434_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.vlan.v6.udp.vxlan.eth.2vlan.v6.sctp

COSSW-8435_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.qinq.v6.udp.vxlan.eth.vlan.v6-ext.tcp

COSSW-8436_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.qinq.v6.udp.vxlan.eth.vlan.v6-ext.udp

COSSW-8437_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.qinq.v6.udp.vxlan.eth.vlan.v6-ext

COSSW-8438_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.vlan.v6.udp.vxlan.eth.2vlan.v4.tcp

COSSW-8439_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.vlan.v6.udp.vxlan.eth.2vlan.v4.udp

COSSW-8440_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.vlan.v6.udp.vxlan.eth.2vlan.v4.icmp

COSSW-8441_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.eth

COSSW-8442_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.eth.vlan.arp

COSSW-8443_Proflie
    [Documentation]    *验证*
    [tags]    nok    rocev1
    验证Profile    eth.v4.udp.geneve.eth.vlan.rocev1

COSSW-8444_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.eth.vlan.v4

COSSW-8445_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.eth.vlan.ipv4-frag(flags=1,frag=0x200)

COSSW-8446_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.eth.vlan.ipv4-frag(frag=0x200)

COSSW-8447_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.eth.vlan.v6

COSSW-8448_Proflie
    [Documentation]    *验证*
    [tags]    ok   检查报文
    验证Profile    eth.v4.udp.geneve.eth.vlan.v6-ext

COSSW-8449_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.eth.2vlan.v4.tcp

COSSW-8450_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.eth.2vlan.v4.udp

COSSW-8451_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.eth.2vlan.v4.icmp

COSSW-8452_Proflie
    [Documentation]    *验证*
    [tags]    ok        
    验证Profile    eth.v4.udp.geneve.eth.2vlan.v4(proto=2).igmp

COSSW-8453_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v4.udp.geneve.eth.2vlan.v4.sctp

COSSW-8454_Proflie
    [Documentation]    *验证  首片*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.eth.2vlan.ipv4-frag(flags=1,frag=0).tcp

COSSW-8455_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.eth.2vlan.ipv4-frag(flags=1,frag=0).udp

COSSW-8456_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.eth.2vlan.v6.tcp

COSSW-8457_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.eth.2vlan.v6.udp

COSSW-8458_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.eth.2vlan.v6.icmp6

COSSW-8459_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.v4

COSSW-8460_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.ipv4-frag(flags=1,frag=0x200)

COSSW-8461_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.ipv4-frag(frag=0x200)

COSSW-8462_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.v6

COSSW-8463_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.v6-ext

COSSW-8464_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.v4.tcp

COSSW-8465_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.v4.udp

COSSW-8466_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.v4.udp(dport=4791)

COSSW-8467_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.v4.icmp

COSSW-8468_Proflie
    [Documentation]    *验证*
    [tags]    ok        
    验证Profile    eth.v4.udp.geneve.v4(proto=2).igmp

COSSW-8469_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.v4.sctp

COSSW-8470_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.v6.tcp

COSSW-8471_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.v6.udp

COSSW-8472_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.ip.udp.geneve.ipv6.udp(dport=4791)

COSSW-8473_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.geneve.v6.icmp6

COSSW-8474_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v4.udp.geneve.v6.sctp

COSSW-8475_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.geneve.eth

COSSW-8476_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.geneve.eth.vlan.arp

COSSW-8477_Proflie
    [Documentation]    *验证*
    [tags]    nok    rocev1
    验证Profile    eth.v6.udp.geneve.eth.vlan.rocev1

COSSW-8478_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.geneve.eth.vlan.v6

COSSW-8479_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.geneve.eth.vlan.v6-ext

COSSW-8480_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.geneve.eth.vlan.v4

COSSW-8481_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.geneve.eth.2vlan.v6.tcp

COSSW-8482_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.geneve.eth.2vlan.v6.udp

COSSW-8483_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.geneve.eth.2vlan.v6.icmp6

COSSW-8484_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v6.udp.geneve.eth.2vlan.v6.sctp

COSSW-8485_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.geneve.eth.2vlan.v6-ext.tcp

COSSW-8486_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.geneve.eth.2vlan.v6-ext.udp

COSSW-8487_Proflie
    [Documentation]    *验证*
    [tags]    ok   
    验证Profile    eth.v6.udp.geneve.eth.2vlan.v4.tcp

COSSW-8488_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.geneve.eth.2vlan.v4.udp

COSSW-8489_Proflie
    [Documentation]    *验证*
    [tags]    ok    基础通路
    验证Profile    eth.v6.udp.geneve.eth.2vlan.v4.icmp

COSSW-8490_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.geneve.v4

COSSW-8491_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.geneve.ipv4-frag(flags=0x1,frag=0x200)

COSSW-8492_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.geneve.ipv4-frag(frag=0x200)

COSSW-8493_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.geneve.v4.tcp

COSSW-8494_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.geneve.v4.udp

COSSW-8495_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.geneve.v4.udp(dport=4791)

COSSW-8496_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.geneve.v4.icmp

COSSW-8497_Proflie
    [Documentation]    *验证*
    [tags]    ok        
    验证Profile    eth.v6.udp.geneve.v4(proto=2).igmp

COSSW-8498_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v6.udp.geneve.v4.sctp

COSSW-8499_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.geneve.v6

COSSW-8500_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.geneve.v6-ext

COSSW-8501_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.geneve.v6.tcp

COSSW-8502_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.geneve.v6.udp

COSSW-8503_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.geneve.v6.udp(dport=4791)

COSSW-8504_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.geneve.v6.icmp6

COSSW-8505_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v6.udp.geneve.v6.sctp

COSSW-8506_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    Geneve.IPV4.UDP

COSSW-8555_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    v4.ipinip.v4

COSSW-8556_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    ipv4-frag(flags=0x1,frag=0x01).ipinip.v4

COSSW-8557_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    v4.ipinip.v6

COSSW-8558_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    v6.ipinip.v4

COSSW-8559_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    v6.ipinip.v6

COSSW-8560_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    VXLAN-GPE.IPV4

COSSW-8561_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    VXLAN-GPE.IPV6

COSSW-8562_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    VXLAN-GPE.ETH.2VLAN.IPV4

COSSW-8563_Proflie
    [Documentation]    *验证*
    [tags]    ok   
    验证Profile    IPV6.UDP.VXLAN-GPE.ETH.2VLAN.IPV6.UDP

COSSW-8564_Proflie
    [Documentation]    *验证*
    [tags]    ok    reexe    用例构造问题
    验证Profile    eth.qinq.v4.udp.geneve.v6.udp.vxlan.eth.v4.udp
    验证Profile    eth.qinq.v6.udp.geneve.v6.udp.vxlan.eth.v4.udp
    验证Profile    eth.qinq.v4-frag(frag=1).udp.geneve.v4-frag(frag=1).udp.vxlan.eth.v4.udp

COSSW-8685_Proflie
    [Documentation]    *RX收到报文后，使用profile的目的地发送*
    [tags]    ok    基础通路
    验证Profile    ETH.IPV4.UDP  
    验证Profile    IPV6.UDP.VXLAN-GPE.ETH.2VLAN.IPV6.UDP

COSSW-11722_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.ipinip.v4

COSSW-11723_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.ipinip.ipv4-frag(flags=0x1,frag=0x200)

COSSW-11724_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.ipinip.ipv4-frag(frag=0x200)

COSSW-11725_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.ipinip.v4.tcp

COSSW-11726_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.ipinip.v4.udp

COSSW-11727_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v4.ipinip.v4.icmp

COSSW-11728_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v4.ipinip.v4(proto=2).igmp

COSSW-11729_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v4.ipinip.v4.sctp

COSSW-11730_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.ipinip.ipv4-frag(flags=0x1).tcp

COSSW-11731_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.ipinip.ipv4-frag(flags=0x1).udp

COSSW-11732_Proflie
    [Documentation]    *验证*
    [tags]    ok   
    验证Profile    eth.v4.ipinip.ipv4-frag(flags=0x1).udp(dport=4791)

COSSW-11733_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.ipinip.ipv4-option.tcp

COSSW-11734_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.ipinip.ipv4-option.udp

COSSW-11735_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v4.ipinip.v6.tcp

COSSW-11736_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v4.ipinip.v6.udp

COSSW-11737_Proflie
    [Documentation]    *验证*
    [tags]    ok   
    验证Profile    eth.v4.ipinip.v6.icmp6

COSSW-11738_Proflie
    [Documentation]    *验证*
    [tags]    ok 
    验证Profile    eth.v6.ipinip.v6

COSSW-11739_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v6.ipinip.v6-ext

COSSW-11740_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v6.ipinip.v4

COSSW-11741_Proflie
    [Documentation]    *验证*
    [tags]    ok 
    验证Profile    eth.v6.ipinip.ipv4-frag(flags=0x1)

COSSW-11742_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.ipinip.ipv4-option

COSSW-11743_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v6.ipinip.v6.tcp

COSSW-11744_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v6.ipinip.v6.udp

COSSW-11745_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v6.ipinip.v6.udp(dport=4791)

COSSW-11746_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v6.ipinip.v6.icmp6

COSSW-11747_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v6.ipinip.v6.sctp

COSSW-11748_Proflie
    [Documentation]    *验证*
    [tags]    ok   
    验证Profile    eth.v6.ipinip.v6-ext.tcp

COSSW-11749_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v6.ipinip.v6-ext.udp

COSSW-11750_Proflie
    [Documentation]    *验证*
    [tags]    ok   
    验证Profile    eth.v6.ipinip.v4.tcp

COSSW-11751_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v6.ipinip.v4.udp

COSSW-11752_Proflie
    [Documentation]    *验证*
    [tags]    ok   
    验证Profile    eth.v6.ipinip.v4.icmp

COSSW-11753_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v4.udp.vxlan-gpe.eth

COSSW-11754_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v4.udp.vxlan-gpe.eth.vlan.arp

COSSW-11755_Proflie
    [Documentation]    *验证*
    [tags]    nok    rocev1
    验证Profile    eth.v4.udp.vxlan-gpe.eth.vlan.rocev1

COSSW-11756_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v4.udp.vxlan-gpe.eth.vlan.v4

COSSW-11757_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.vxlan-gpe.eth.vlan.ipv4-frag(flags=0x1,frag=0x200)

COSSW-11758_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.vxlan-gpe.eth.vlan.ipv4-frag(frag=0x200)

COSSW-11759_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v4.udp.vxlan-gpe.eth.vlan.v6

COSSW-11760_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v4.udp.vxlan-gpe.eth.vlan.v6-ext

COSSW-11761_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.vxlan-gpe.eth.qinq.v4.tcp

COSSW-11762_Proflie
    [Documentation]    *验证*
    [tags]    ok   
    验证Profile    eth.v4.udp.vxlan-gpe.eth.qinq.v4.udp

COSSW-11763_Proflie
    [Documentation]    *验证*
    [tags]    ok   
    验证Profile    eth.v4.udp.vxlan-gpe.eth.qinq.v4.icmp

COSSW-11764_Proflie
    [Documentation]    *验证*
    [tags]    ok        
    验证Profile    eth.v4.udp.vxlan-gpe.eth.qinq.v4.igmp

COSSW-11765_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v4.udp.vxlan-gpe.eth.qinq.v4.sctp

COSSW-11766_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v4.udp.vxlan-gpe.eth.qinq.ipv4-frag(flags=0x1).tcp

COSSW-11767_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v4.udp.vxlan-gpe.eth.qinq.ipv4-frag(flags=0x1).udp

COSSW-11768_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.vxlan-gpe.eth.qinq.v6.tcp

COSSW-11769_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.vxlan-gpe.eth.qinq.v6.udp

COSSW-11770_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.vxlan-gpe.eth.qinq.v6.icmp6

COSSW-11771_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.vxlan-gpe.v4

COSSW-11772_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.vxlan-gpe.ipv4-frag(flags=0x1,frag=0x200)

COSSW-11773_Proflie
    [Documentation]    *验证*
    [tags]    ok 
    验证Profile    eth.v4.udp.vxlan-gpe.ipv4-frag(frag=0x200)

COSSW-11774_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.vxlan-gpe.v6

COSSW-11775_Proflie
    [Documentation]    *验证*
    [tags]    ok   
    验证Profile    eth.v4.udp.vxlan-gpe.v6-ext

COSSW-11776_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.vxlan-gpe.v4.tcp

COSSW-11777_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.vxlan-gpe.v4.udp

COSSW-11778_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.vxlan-gpe.v4.udp(dport=4791)

COSSW-11779_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.vxlan-gpe.v4.icmp

COSSW-11780_Proflie
    [Documentation]    *验证*
    [tags]    ok        
    验证Profile    eth.v4.udp.vxlan-gpe.v4(proto=2).igmp

COSSW-11781_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v4.udp.vxlan-gpe.v4.sctp

COSSW-11782_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.vxlan-gpe.v6.tcp

COSSW-11783_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.vxlan-gpe.v6.udp

COSSW-11784_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.vxlan-gpe.v6.udp(dport=4791)

COSSW-11785_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v4.udp.vxlan-gpe.v6.icmp6

COSSW-11786_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v4.udp.vxlan-gpe.v6.sctp

COSSW-11787_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.eth

COSSW-11788_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.eth.vlan.arp

COSSW-11789_Proflie
    [Documentation]    *验证*
    [tags]    nok    rocev1
    验证Profile    eth.v6.udp.vxlan-gpe.eth.vlan.rocev1

COSSW-11790_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.eth.vlan.v6

COSSW-11791_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.eth.vlan.v6-ext

COSSW-11792_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.eth.vlan.v4

COSSW-11793_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.eth.qinq.v6.tcp

COSSW-11794_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.eth.qinq.v6.udp

COSSW-11795_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.eth.qinq.v6.icmp6

COSSW-11796_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v6.udp.vxlan-gpe.eth.qinq.v6.sctp

COSSW-11797_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.eth.qinq.v6-ext.tcp

COSSW-11798_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.eth.qinq.v6-ext.udp

COSSW-11799_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.eth.qinq.v4.tcp

COSSW-11800_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.eth.qinq.v4.udp

COSSW-11801_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.eth.qinq.v4.icmp

COSSW-11802_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.v4

COSSW-11803_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.ipv4-frag(flags=0x1,frag=0x200)

COSSW-11804_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.ipv4-frag(frag=0x200)

COSSW-11805_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.v4.tcp

COSSW-11806_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.v4.udp

COSSW-11807_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.v4.udp(dport=4791)

COSSW-11808_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.v4.icmp

COSSW-11809_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.v4(proto=2).igmp

COSSW-11810_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v6.udp.vxlan-gpe.v4.sctp

COSSW-11811_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.v6

COSSW-11812_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.v6-ext

COSSW-11813_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.v6.tcp

COSSW-11814_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.v6.udp

COSSW-11815_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.v6.udp(dport=4791)

COSSW-11816_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.v6.udp.vxlan-gpe.v6.icmp6

COSSW-11817_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.v6.udp.vxlan-gpe.v6.sctp

COSSW-11819_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.qinq.v4.udp.geneve.v6.udp.vxlan.eth.qinq.v6.sctp

COSSW-11821_Proflie
    [Documentation]    *验证*
    [tags]    ok    
    验证Profile    eth.qinq.v4.udp.vxlan.eth.vlan.v4.udp.vxlan.eth.vlan.v4(proto=2).igmp

COSSW-11822_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.qinq.v4.udp.vxlan-gpe.eth.vlan.v4.udp.vxlan-gpe.eth.vlan.v4.udp

COSSW-11823_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.qinq.v4.ipinip.v4.ipinip.v4.tcp(dport=8000)

COSSW-11824_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.qinq.v4.udp.geneve.eth.qinq.v4.udp.geneve.eth.qinq.v6.tcp

COSSW-11827_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.qinq.v6.udp.vxlan.eth.qinq.v6.udp.vxlan-gpe.v6.tcp(dport=8282)

COSSW-11828_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.qinq.v6.udp.vxlan.eth.qinq.v6.udp.geneve.v6.udp(dport=8383)

COSSW-11861_Proflie
    [Documentation]    *验证*
    [tags]    ok
    验证Profile    eth.qinq.v6.udp.vxlan.eth.qinq.v6.udp.geneve.eth.qinq.v4

*** Keywords ***
组配置初始化
    ${config}    ipv4Config.getProfileSuiteConfig
    jaguarRunConfig    ${A}    ${config}
    清理测试仪

组配置清理
    ${config}    ipv4Config.getProfileSuiteConfig
    jaguarClearConfig    ${A}    ${config}
    清理测试仪

验证Profile
    [Arguments]    ${arg1}
    ${configResult}    ipv4Config.getProfileValue    ${arg1}
    验证RESTFUL流量    ${configResult}
