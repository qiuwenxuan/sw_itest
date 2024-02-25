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
COSSW-8814_em
    [Documentation]    *验证 EM表中： destination valid置位， action type为单播， 从指定目的地单播发送*
    [Tags]    ok
    验证EM-ACTION    eth.ipv4.udp    action    ACTION_TYPE

COSSW-8815_em
    [Documentation]    *验证 EM表中： destination valid置位， action type为组播， 查组播成员表， 发送给多个成员*
    [Tags]    unknow
    验证EM-ACTION    eth.ipv4.udp    ACTION_TYPE(v=1)

COSSW-8816_em
    [Documentation]    *验证 EM表中： destination valid置位， action type为单播， 指定发送的queue id， 从指定目的地queue单播发送*
    [Tags]    unknow
    验证EM-ACTION    eth.ipv4.udp    CMD_QUEUE_ID(id=1)

COSSW-8817_em
    [Documentation]    *验证 EM表中： destination valid置位， action type为单播， 从指定目的地 RSS queue单播发送*
    [Tags]    test
    验证EM-ACTION    eth.ipv4.udp    DESTINATION()

COSSW-8818_em
    [Documentation]    *验证 RX方向， EM表中： destination valid置位， action type为单播，目的地是vnic， 需要经过RPE， destination中RPE标记置位*
    [Tags]    unknow
    验证EM-ACTION    [Net][DPE][PIPE]指定目的地-5

COSSW-8819_em
    [Documentation]    *验证 RX方向，EM表中： destination valid置位， action type为单播，目的地是vnet， 需要经过RPE， destination中RPE标记置位*
    [Tags]    unknow
    验证EM-ACTION    [Net][DPE][PIPE]指定目的地-6

COSSW-8820_em
    [Documentation]    *验证 EM表中： destination valid置位， action type为单播， 从指定目的地单播发送*
    [Tags]    ok
    验证EM-ACTION    eth.2vlan.ipv6.udp    action    ACTION_TYPE

COSSW-8821_em
    [Documentation]    *验证 使用高性能统计（容量默认支持8K， 可以与源表共享， 最大支持15K）*
    [Tags]    unknow
    验证EM-ACTION    [Net][DPE][PIPE]指定目的地-8

COSSW-8822_em
    [Documentation]    *验证 EM表中： destination valid置位， action type为单播， 从指定目的地单播发送
    ...    使用高性能统计（容量默认支持8K， 可以与源表共享， 最大支持15K）*
    [Tags]    unknow
    验证EM-ACTION    [Net][DPE][PIPE]指定目的地-9

COSSW-8823_em
    [Documentation]    *验证 EM表action ：
    ...    decap直到最外层L3
    ...    encap L3和L2
    ...    从指定的目的地发送（IP IN IP隧道场景）*
    [Tags]    ok
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    DECAPSULATION(layer='ot_l3'),TUNNEL_ENCAP_TYPE(type='v4inv4'),L3_ENCAP_TYPE(type='ipv4'),L2_FLAG
    验证EM-ACTION    eth.2vlan.ipv6.udp    action    DECAPSULATION(layer='ot_l3'),TUNNEL_ENCAP_TYPE(type='v6inv4'),L3_ENCAP_TYPE(type='ipv4'),L2_FLAG
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    DECAPSULATION(layer='ot_l3'),TUNNEL_ENCAP_TYPE(type='v4inv6'),L3_ENCAP_TYPE(type='ipv6'),L2_FLAG
    验证EM-ACTION    eth.2vlan.ipv6.udp    action    DECAPSULATION(layer='ot_l3'),TUNNEL_ENCAP_TYPE(type='v6inv6'),L3_ENCAP_TYPE(type='ipv6'),L2_FLAG

COSSW-8824_em
    [Documentation]    *验证 EM表action ：
    ...    decap直到最外层L4
    ...    encap L3和L2
    ...    从指定的目的地发送（NAT64场景）*
    [Tags]    ok
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    DECAPSULATION(layer='ot_l4'),L3_ENCAP_TYPE(type='ipv6'),L2_FLAG

COSSW-8825_em
    [Documentation]    *验证 EM表action ：
    ...    decap直到最外层最外层隧道头
    ...    opcode: NORMAL_FLOW lookup subpipe 2
    ...    下一级pipe使用隧道信息组key查EM表， decap到最外层L2， 从指定的目的转发*
    [Tags]    test    基础通路
    验证EM-ACTION    [Net][DPE][PIPE]decap action-3

COSSW-8826_em
    [Documentation]    *验证 EM表action ：
    ...    decap直到次外层L2
    ...    从指定的目的地发送（decap一层隧道转发）*
    [Tags]    ok    基础通路
    验证EM-ACTION    eth.vlan.v4.udp.vxlan.eth.2vlan.v6.udp    action    DECAPSULATION(layer='tl_l2')
    验证EM-ACTION    eth.vlan.v4.udp.vxlan.eth.2vlan.v4.udp    action    DECAPSULATION(layer='tl_l2')

COSSW-8827_em
    [Documentation]    *验证 EM表action ：
    ...    decap直到次外层L3
    ...    encap L2
    ...    从指定的目的地发送*
    [Tags]    ok    基础通路
    验证EM-ACTION    eth.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    action    DECAPSULATION(layer='tl_l3'),L2_FLAG
    验证EM-ACTION    eth.ipv4.udp.geneve.eth.2vlan.ipv6.udp    action    DECAPSULATION(layer='tl_l3'),L2_FLAG

COSSW-8828_em
    [Documentation]    *验证 EM表action ：
    ...    decap直到次外层L4
    ...    encap L3和L2
    ...    从指定的目的地发送（NAT64场景）*
    [Tags]    ok
    验证EM-ACTION    eth.ipv4.udp.vxlan.eth.2vlan.ipv6.udp    action    DECAPSULATION(layer='tl_l4'),L3_ENCAP_TYPE(type='ipv6'),L2_FLAG

COSSW-8829_em
    [Documentation]    *验证 EM表action ：
    ...    decap直到次外层隧道头
    ...    opcode: NORMAL_FLOW lookup subpipe 2
    ...    下一级pipe使用隧道信息组key查EM表， decap到最外层L2， 从指定的目的转发*
    [Tags]    test    基础通路
    验证EM-ACTION    eth.2vlan.ipv4.udp.geneve.eth.vlan.ipv4.udp    action    DECAPSULATION(layer='tl_tun')

COSSW-8830_em
    [Documentation]    *验证 EM表action ：
    ...    decap直到最内层L2
    ...    从指定的目的地发送（decap两层隧道转发）*
    [Tags]    ok    基础通路
    验证EM-ACTION    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.v4   action    DECAPSULATION(layer='l2')
    验证EM-ACTION    eth.2vlan.ipv4.udp.geneve.eth.2vlan.ipv4.udp.geneve.eth.2vlan.v4   action    DECAPSULATION(layer='l2')
    验证EM-ACTION    eth.2vlan.ipv4.gre.eth.2vlan.ipv4.gre.eth.2vlan.v4   action    DECAPSULATION(layer='l2')

COSSW-8831_em
    [Documentation]    *验证 EM表action ：
    ...    decap直到最内层L3
    ...    encap L2
    ...    从指定的目的地发送*
    [Tags]    ok
    验证EM-ACTION    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.v4.udp   action    DECAPSULATION(layer='l3'),L2_FLAG
    验证EM-ACTION    eth.2vlan.ipv4.udp.geneve.eth.2vlan.ipv4.udp.geneve.eth.2vlan.v4.udp   action    DECAPSULATION(layer='l3'),L2_FLAG
    验证EM-ACTION    eth.2vlan.ipv4.gre.eth.ipv4.gre.eth.2vlan.v4.udp   action    DECAPSULATION(layer='l3'),L2_FLAG

COSSW-8832_em
    [Documentation]    *验证 EM表action ：
    ...    decap直到最内层L4
    ...    encap L3和L2
    ...    从指定的目的地发送（NAT64场景）*
    [Tags]    ok
    验证EM-ACTION    eth.2vlan.ipv4.gre.eth.ipv4.gre.eth.2vlan.v4.udp   action    DECAPSULATION(layer='l4'),L3_ENCAP_TYPE(type='ipv6'),L2_FLAG

COSSW-8833_em
    [Documentation]    *验证 EM opcode为NORMAL_FLOW lookup subpipe 2
    ...    本EM action为decap一层隧道， 根据metadata更新mask，修改metainfo中的metadata, 指定下一级pipe的profile
    ...    下一级查profile表、EM表从指定的出接口转发, EM表的key包含上一级pipe更新的metadata
    ...    metadata更新的mask模板支持16个， 通过寄存器配置32bit的mask值*
    [Tags]    unknow
    验证EM-ACTION    [Net][DPE][PIPE]modify metadata

COSSW-8834_em
    [Documentation]    *验证 remove outer vlan置位当前层为0层vlan， 不操作*
    [Tags]    ok    基础通路
    验证EM-ACTION    eth.ipv4.udp    action    REMOVE_OUTER_VLAN

COSSW-8835_em
    [Documentation]    *验证 remove outer vlan置位当前层为1层vlan， 删除vlan*
    [Tags]    ok    基础通路
    验证EM-ACTION    eth.vlan.ipv4.udp    action    REMOVE_OUTER_VLAN

COSSW-8836_em
    [Documentation]    *验证 remove outer vlan置位当前层为2层vlan， 删除外层vlan*
    [Tags]    ok
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    REMOVE_OUTER_VLAN

COSSW-8837_em
    [Documentation]    *验证 remove inner vlan置位当前层为0层vlan， 不操作*
    [Tags]    ok
    验证EM-ACTION    eth.ipv4.udp    action    REMOVE_INNER_VLAN

COSSW-8838_em
    [Documentation]    *验证 remove inner vlan置位当前层为1层vlan， 删除vlan*
    [Tags]    ok
    验证EM-ACTION    eth.vlan.ipv4.udp    action    REMOVE_INNER_VLAN

COSSW-8839_em
    [Documentation]    *验证 remove inner vlan置位当前层为2层vlan， 删除内层vlan， 外层vlan移至内层*
    [Tags]    ok    
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    REMOVE_INNER_VLAN

COSSW-8840_em
    [Documentation]    *验证 Replace/Add Inner VLAN 置位
    ...    0层vlan：添加一层vlan
    ...    a) inherit为0/1/2时， 使用封装表中的pri
    ...    b) inherit为3， 内层是IP报文， 使用dscp映射表中的优先级(配置寄存器)
    ...    c) inherit为3， 内层非IP报文， 使用封装表中的pri*
    [Tags]    ok
    #验证EM-ACTION    eth.ipv4.udp    action    REPLACE_INNER_VLAN(tpid=0x9100,inherit=1,vid=200)
    验证EM-ACTION    eth.ipv4.udp    action    REPLACE_INNER_VLAN

COSSW-8841_em
    [Documentation]    *验证 Replace/Add Inner VLAN 置位
    ...    1层vlan：替换vlan
    ...    a) inherit为0/1/2时， 使用封装表中的pri
    ...    b) inherit为3， 内层是IP报文， 使用dscp映射表中的优先级
    ...    c) inherit为3， 内层非IP报文， 使用封装表中的pri*
    [Tags]    ok
    验证EM-ACTION    eth.vlan.ipv4.udp    action    REPLACE_INNER_VLAN(inherit=0)
    验证EM-ACTION    eth.vlan.ipv4.udp    action    REPLACE_INNER_VLAN(inherit=1)
    验证EM-ACTION    eth.vlan.ipv4.udp    action    REPLACE_INNER_VLAN(inherit=2)
    验证EM-ACTION    eth.vlan.ipv4(tos=0xcc).udp    action    REPLACE_INNER_VLAN(inherit=3)
    验证EM-ACTION    eth.vlan.arp    action    REPLACE_INNER_VLAN(inherit=3)

COSSW-8842_em
    [Documentation]    *验证 Replace/Add Inner VLAN 置位
    ...    1层vlan：替换vlan
    ...    通过mask设置，只修改TPID/PRI/VLANID*
    [Tags]    ok
    验证EM-ACTION    eth.vlan.ipv4.udp    action    REPLACE_INNER_VLAN(tpid=0x9100,inherit=2,cfi=1,mask=0x01)
    验证EM-ACTION    eth.vlan.ipv4.udp    action    REPLACE_INNER_VLAN(tpid=0x9100,inherit=2,cfi=1,mask=0x03)
    #验证EM-ACTION    eth.vlan.ipv4.udp    action    REPLACE_INNER_VLAN(tpid=0x9100,inherit=2,cfi=1,mask=0x05)

COSSW-8843_em
    [Documentation]    *验证 Replace/Add Inner VLAN 置位
    ...    2层vlan：替换内层vlan
    ...    a) inherit为0/1时， 使用封装表中的pri
    ...    b) inherit为2时， 使用内层vlan的pri
    ...    c) inherit为3， 内层是IP报文， 使用dscp映射表中的优先级
    ...    d) inherit为3， 内层非IP报文， 使用封装表中的pri*
    [Tags]    ok
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    REPLACE_INNER_VLAN(inherit=0)
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    REPLACE_INNER_VLAN(inherit=1)
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    REPLACE_INNER_VLAN(inherit=2)
    验证EM-ACTION    eth.2vlan.ipv4(tos=0x0c).udp    action    REPLACE_INNER_VLAN(inherit=3)
    验证EM-ACTION    eth.2vlan.arp    action    REPLACE_INNER_VLAN(inherit=3)

COSSW-8844_em
    [Documentation]    *验证 Replace/Add outer VLAN 置位
    ...    0层vlan：添加一层vlan*
    [Tags]    ok
    验证EM-ACTION    eth.ipv4.udp    action    REPLACE_OUTER_VLAN
    验证EM-ACTION    eth.ipv4.udp    action    REPLACE_OUTER_VLAN(inherit=1)
    验证EM-ACTION    eth.ipv4(tos=0x0c).udp    action    REPLACE_OUTER_VLAN(inherit=2)  
    验证EM-ACTION    eth.arp    action    REPLACE_OUTER_VLAN(inherit=2)    
    验证EM-ACTION    eth.ipv4(tos=0x0c).udp    action    REPLACE_OUTER_VLAN(inherit=3)  
    验证EM-ACTION    eth.icmp    action    REPLACE_OUTER_VLAN(inherit=3)
    #验证EM-ACTION    eth.ipv4.udp    action    REPLACE_OUTER_VLAN(tpid=0x9100,inherit=1)

COSSW-8845_em
    [Documentation]    *验证 Replace/Add outer VLAN 置位
    ...    1层vlan：添加 一层vlan
    ...    a) inherit为0/1时， 使用封装表中的pri
    ...    b) inherit为2时， 使用内层vlan的pri
    ...    c) inherit为3， 内层是IP报文， 使用dscp映射表中的优先级
    ...    d) inherit为3， 内层非IP报文， 使用封装表中的pri*
    [Tags]    ok
    验证EM-ACTION    eth.vlan.ipv4.udp    action    REPLACE_OUTER_VLAN
    验证EM-ACTION    eth.vlan.ipv4.udp    action    REPLACE_OUTER_VLAN(inherit=1)
    验证EM-ACTION    eth.vlan(prio=4).ipv4.udp    action    REPLACE_OUTER_VLAN(inherit=2)
    验证EM-ACTION    eth.vlan.ipv4(tos=0x0b).udp    action    REPLACE_OUTER_VLAN(inherit=3)   
    验证EM-ACTION    eth.vlan.arp    action    REPLACE_OUTER_VLAN(inherit=3)   

COSSW-8846_em
    [Documentation]    *验证 Replace/Add outer VLAN 置位
    ...    2层vlan：替换外层vlan
    ...    a) inherit为0/1时， 0不修改，使用封装表中的pri
    ...    b) inherit为2时， 使用内层vlan的pri
    ...    c) inherit为3， 内层是IP报文， 使用dscp映射表中的优先级
    ...    d) inherit为3， 内层非IP报文， 使用封装表中的pri*
    [Tags]    ok 
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    REPLACE_OUTER_VLAN(inherit=0)
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    REPLACE_OUTER_VLAN(inherit=1)
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    REPLACE_OUTER_VLAN(inherit=2)
    验证EM-ACTION    eth.2vlan.ipv4(tos=0x80).udp    action    REPLACE_OUTER_VLAN(inherit=3)
    验证EM-ACTION    eth.2vlan.arp    action    REPLACE_OUTER_VLAN(inherit=3)
    #验证EM-ACTION    eth.2vlan.ipv4.udp    action    REPLACE_OUTER_VLAN(tpid=0x9100,inherit=0)
    #验证EM-ACTION    eth.2vlan.ipv4.udp    action    REPLACE_OUTER_VLAN(tpid=0x9200,inherit=1)
    #验证EM-ACTION    eth.2vlan.ipv4.udp    action    REPLACE_OUTER_VLAN(tpid=0x9300,inherit=2)

COSSW-8847_em
    [Documentation]    *验证 Replace/Add outer VLAN 置位
    ...    2层vlan：替换外层vlan
    ...    通过mask设置，只修改TPID/PRI/VLANID
    ...    3bits bitmap表示mask，在modify vlan的时候，依次表示可修改vlan的TPID，CFI, VLAN ID;在add vlan时不看mask。*
    [Tags]    ok
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    REPLACE_OUTER_VLAN(inherit=0,mask=0x01)
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    REPLACE_OUTER_VLAN(inherit=1,cfi=1,mask=0x02)
    #验证EM-ACTION    eth.2vlan.ipv4.udp    action    REPLACE_OUTER_VLAN(tpid=0x9100,inherit=2,mask=0x04)
    #验证EM-ACTION    eth.2vlan.ipv4.udp    action    REPLACE_OUTER_VLAN(tpid=0x9200,inherit=3,mask=0x05)

COSSW-8848_em
    [Documentation]    *验证opcode=1 ttl>1的报文， TTL-1， 并修改checksum  ttl <=1 不操作，opcode =2 ,set ttl *
    [Tags]    ok
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    TTL_UPDATE(opcode=0)
    验证EM-ACTION    eth.2vlan.ipv6.udp    action    TTL_UPDATE(opcode=0)
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    TTL_UPDATE(opcode=1)
    验证EM-ACTION    eth.2vlan.ipv6.udp    action    TTL_UPDATE(opcode=1)
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    TTL_UPDATE(opcode=2,ttl=127)
    验证EM-ACTION    eth.2vlan.ipv6.udp    action    TTL_UPDATE(opcode=2,hlim=127)

COSSW-8849_em
    [Documentation]    *验证 ttl<=1的报文， TTL不修改， 送到指定的目的地处理 opcode = 0  
    ...    ttl减1，如果ttl<=0,dst重定向到6口 
    ...    TX/RX方向支持送MAC PORT和VNET
    ...    TX方向：指定SPD的话， 送VPE带过来的spd queue*
    [Tags]    ok    测试不全
    验证EM-ACTION    eth.2vlan.ipv4(ttl=1).udp    action    TTL_UPDATE(opcode=1)
    验证EM-ACTION    eth.2vlan.ipv6(hlim=1).udp    action    TTL_UPDATE(opcode=1)
    #验证EM-ACTION    eth.2vlan.ipv4(ttl=1).udp    action    TTL_UPDATE(opcode=0)
    #验证EM-ACTION    eth.2vlan.ipv6(hlim=1).udp    action    TTL_UPDATE(opcode=0)

COSSW-8850_em
    [Documentation]    *验证 通过指定的mask进行tos的更新 #mask:0xfc  setvalue=0xb0*
    [Tags]    ok
    验证EM-ACTION    eth.2vlan.ipv4.udp    action   TOS_UPDATE(mask=0xfc,tos=0xb0)
    #验证EM-ACTION    eth.2vlan.ipv4.udp    action   TOS_UPDATE

COSSW-8851_em
    [Documentation]    *验证 指定offset和size， size小于等于32bit， 不使用mask
    ...    a)? 直接使用data值set
    ...    b)? 从指定的offset位置进行set
    ...    c)?? 使用指定的data ADD
    ...    d）使用指定的offset处的值进行ADD
    ...    e)?? 使用指定的data SUB
    ...    f）使用指定的offset处的值进行SUB
    ...    更改IPV4/L4的内容，需要更新checksum
    ...    UPDATE_FIELD 支持的格式有限，满足条件才能下发成功 
    ...    参数 src dst opcode必须填值，其中src需要指定是立即数还是从报文的字段中获取*
    [Tags]    硬件不支持
    验证EM-ACTION    eth.2vlan.ipv4.udp    action   UPDATE_FIELD(src ="src_mode=data", dst="layer=ot_l3,field=dst,offset=0",opcode='add')
    #验证EM-ACTION    eth.2vlan.ipv4.udp    action   UPDATE_FIELD(src ="src_mode=seg,layer=ot_l3,field=src,offset=1,width=10", dst="layer=ot_l3,field=dst,offset=0,width=10",opcode='set')
    #验证EM-ACTION    eth.2vlan.ipv4.udp    action   UPDATE_FIELD(src ="src_mode=data", dst="layer=ot_l3,field=dst,offset=0",opcode='add')
    #验证EM-ACTION    eth.2vlan.ipv4.udp    action   UPDATE_FIELD(layer='ot_l3',field='src',offset=0,opcode='sub')
    #验证EM-ACTION    eth.2vlan.ipv4.udp    action   UPDATE_FIELD(layer='ot_l4',field='sport',offset=0,opcode='set')
    #验证EM-ACTION    eth.2vlan.ipv4.udp    action   UPDATE_FIELD(layer='ot_l4',field='sport',offset=0,opcode='add')
    #验证EM-ACTION    eth.2vlan.ipv4.udp    action   UPDATE_FIELD(layer='ot_l4',field='sport',offset=0,opcode='sub')    

COSSW-8852_em
    [Documentation]    *验证 指定offset和size， size小于等于32bit，
    ...    a）使用mask，进行data值set
    ...    b)? 使用mask， 从指定的offset位置进行set
    ...    支持16个mask模板
    ...    更改IPV4/L4的内容，需要更新checksum*
    [Tags]    硬件不支持
    验证EM-ACTION    [Net][DPE][PIPE]modify udf field-2

COSSW-8853_em
    [Documentation]    *验证 指定offset和size， size大于32bit，使用data值set
    ...    更改IPV4/L4的内容，需要更新checksum*
    [Tags]    硬件不支持
    验证EM-ACTION    [Net][DPE][PIPE]modify udf field-3

COSSW-8854_em
    [Documentation]    *验证 替换当前L2头中的DMAC*
    [Tags]    ok    基础通路
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    REPLACE_DMAC

COSSW-8855_em
    [Documentation]    *验证 替换当前L2头中的SMAC*
    [Tags]    ok    基础通路
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    REPLACE_SMAC

COSSW-8856_em
    [Documentation]    *验证 替换当前L3头中的IPV6 SIP*
    [Tags]    ok    基础通路
    验证EM-ACTION    eth.2vlan.ipv6.udp    action    REPLACE_SIPV6

COSSW-8857_em
    [Documentation]    *验证 替换当前L3头中的IPV6 DIP*
    [Tags]    ok    基础通路
    验证EM-ACTION    eth.2vlan.ipv6.udp    action    REPLACE_DIPV6

COSSW-8858_em
    [Documentation]    *验证 替换当前L3头中的IPV4 SIP,? 需要更新checksum*
    [Tags]    ok    基础通路
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    REPLACE_SIPV4

COSSW-8859_em
    [Documentation]    *验证 替换当前L3头中的IPV4 DIP,? 需要更新checksum*
    [Tags]    ok    基础通路
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    REPLACE_DIPV4

COSSW-8860_em
    [Documentation]    *验证 替换当前L4头中的源PORT,?
    ...    a)TCP报文需要更新checksum
    ...    b)UDP checksum !=0 需要更新checksum
    ...    c)UDP checksum==0, 不更新checksum*
    [Tags]    ok    基础通路
    验证EM-ACTION    eth.2vlan.ipv4.tcp(sport=0x1234)    action    REPLACE_L4_SPORT
    验证EM-ACTION    eth.2vlan.ipv4.udp(sport=0x2345)    action    REPLACE_L4_SPORT
    #验证EM-ACTION    eth.2vlan.ipv4.sctp(sport=0x2345)    action    REPLACE_L4_SPORT
    验证EM-ACTION    eth.2vlan.ipv6.tcp(sport=0x1234)    action    REPLACE_L4_SPORT
    验证EM-ACTION    eth.2vlan.ipv6.udp(sport=0x2345)    action    REPLACE_L4_SPORT
    #验证EM-ACTION    eth.2vlan.ipv6.sctp(sport=0x2345)    action    REPLACE_L4_SPORT

COSSW-8861_em
    [Documentation]    *验证 替换当前L4头中的目的PORT
    ...    a)TCP报文需要更新checksum
    ...    b)UDP checksum !=0 需要更新checksum
    ...    c)UDP checksum==0, 不更新checksum*
    [Tags]    ok    基础通路
    验证EM-ACTION    eth.2vlan.ipv4.tcp(dport=0x1234)    action    REPLACE_L4_DPORT
    验证EM-ACTION    eth.2vlan.ipv4.udp(dport=0x2345)    action    REPLACE_L4_DPORT
    #验证EM-ACTION    eth.2vlan.ipv4.sctp(dport=0x2345)    action    REPLACE_L4_DPORT
    验证EM-ACTION    eth.2vlan.ipv6.tcp(dport=0x1234)    action    REPLACE_L4_DPORT
    验证EM-ACTION    eth.2vlan.ipv6.udp(dport=0x2345)    action    REPLACE_L4_DPORT
    #验证EM-ACTION    eth.2vlan.ipv6.sctp(dport=0x2345)    action    REPLACE_L4_DPORT

COSSW-8862_em
    [Documentation]    *验证 封装通用隧道信息， 使用RAW数据封装在当前层外面--通用隧道无法解析，使用vxlan测试
    ...    a）L3 encap IPV4，使用隧道的封装配置表，封装IPv4 ID/TTL/TOS
    ...    b)? L3 encap IPv6， 使用隧道的封装配置， 封装IPV6 HOP LIMIT/ TOS
    ...    c)?? L4 encap,?? 源port、目的PORT使用封装表中的固定值，L4的checksum=0
    ...    d）L4 encap,?? 源port、目的PORT使用封装表中的固定值，L4的checksum需要计算
    ...    e)?? L4 encap,?? 目的PORT使用封装表中的固定值，L4的checksum=0,? 源PORT需要计算，端口范围使用TUNNEL TYPE配置的mask指定---nok 寄存器配置
    ...    f） L4 encap,?? 目的PORT使用封装表中的固定值，L4的checksum需要计算，源PORT需要计算，端口范围使用TUNNEL TYPE配置的mask指定---nok 寄存器配置
    ...    g)?? 封装配置表中vlan继承为0，添加一层vlan, PRI使用encap表中的值
    ...    h)?? 封装配置表中vlan继承为0，添加一层vlan, PRI继承内层VLAN (隧道封装需要配置寄存器)
    ...    i)??? 封装配置表中vlan继承为0，添加一层vlan, PRI为DSCP映射的优先级
    ...    j)??? 封装配置表中vlan继承为0，添加两层vlan， PRI使用encap表中的值
    ...    k)?? 封装配置表中vlan继承为0，添加两层vlan，PRI为DSCP映射的优先级
    ...    l)??? 封装配置表中vlan继承为1，从内层拷贝vlan， 有几层拷贝几层
    ...    m)? 封装L2, 源MAC从源表中提取， 目的MAC从encap字段提取
    ...    n)?? 封装L2, 封装配置表配置源MAC继承， 封装前的最外层为L2报文，源MAC从封装前的最外层L2头中提取
    ...    o)?? 封装L2, 封装配置表配置源MAC继承， 内层非L2报文，源MAC从源表中提取
    ...    p)?? 封装L2, 封装配置表配置目的MAC继承， 封装前的最外层为L2报文，目的MAC从封装前的最外层L2头中提取
    ...    q)?? 封装L2, 封装配置表配置目的MAC继承， 内层非L2报文，目的MAC从encap字段 中提取*
    [Tags]    ok    基础通路    通用隧道无法解析，使用vxlan测试
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    TUNNEL_ENCAP_TYPE(type='vxlan'),L4_ENCAP_TYPE(type=4,dport=4789),L3_ENCAP_TYPE(type='ipv4',inherit=1),L2_FLAG
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    TUNNEL_ENCAP_TYPE(type='vxlan'),L4_ENCAP_TYPE(type=5,dport=4789),L3_ENCAP_TYPE(type='ipv6',inherit=1),L2_FLAG
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    TUNNEL_ENCAP_TYPE(type='vxlan'),L4_ENCAP_TYPE(type=6,sport=0,dport=4789),L3_ENCAP_TYPE(type='ipv4',inherit=1),L2_FLAG
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    TUNNEL_ENCAP_TYPE(type='vxlan'),L4_ENCAP_TYPE(type=7,sport=0,dport=4789),L3_ENCAP_TYPE(type='ipv6',inherit=1),L2_FLAG
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    TUNNEL_ENCAP_TYPE(type='vxlan'),L4_ENCAP_TYPE(type=4,dport=4789),L3_ENCAP_TYPE(type='ipv4'),VTAG_TYPE(type=1),L2_FLAG   
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    TUNNEL_ENCAP_TYPE(type='vxlan'),L4_ENCAP_TYPE(type=4,dport=4789),L3_ENCAP_TYPE(type='ipv4'),VTAG_TYPE(type=2),L2_FLAG
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    TUNNEL_ENCAP_TYPE(type='vxlan'),L4_ENCAP_TYPE(type=4,dport=4789),L3_ENCAP_TYPE(type='ipv4'),VTAG_TYPE(type=3),L2_FLAG
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    TUNNEL_ENCAP_TYPE(type='vxlan'),L4_ENCAP_TYPE(type=4,dport=4789),L3_ENCAP_TYPE(type='ipv4'),VTAG_TYPE(type=4),L2_FLAG
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    TUNNEL_ENCAP_TYPE(type='vxlan'),L4_ENCAP_TYPE(type=4,dport=4789),L3_ENCAP_TYPE(type='ipv4'),VTAG_TYPE(type=5),L2_FLAG
    验证EM-ACTION    eth.vlan.ipv4.udp    action    TUNNEL_ENCAP_TYPE(type='vxlan'),L4_ENCAP_TYPE(type=4,dport=4789),L3_ENCAP_TYPE(type='ipv4'),VTAG_TYPE(type=0,inherit=1),L2_FLAG
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    TUNNEL_ENCAP_TYPE(type='vxlan'),L4_ENCAP_TYPE(type=4,dport=4789),L3_ENCAP_TYPE(type='ipv4'),VTAG_TYPE(type=0,inherit=1),L2_FLAG
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    TUNNEL_ENCAP_TYPE(type='vxlan'),L4_ENCAP_TYPE(type=4,dport=4789),L3_ENCAP_TYPE(type='ipv4'),VTAG_TYPE(type=0,inherit=1),L2_FLAG(inherit=1)
    验证EM-ACTION    ipv4.udp    action    DECAPSULATION(layer='ot_l3'),TUNNEL_ENCAP_TYPE(type='vxlan-gpe'),L4_ENCAP_TYPE(type=4,dport=4790),L3_ENCAP_TYPE(type='ipv6'),L2_FLAG(inherit=1)

COSSW-8863_em
    [Documentation]    *验证 封装VXLAN隧道
    ...    a）L3 encap IPV4，使用隧道的封装配置表，封装IPv4 ID/TTL/TOS
    ...    b)? L3 encap IPv6， 使用隧道的封装配置， 封装IPV6 HOP LIMIT/ TOS*
    [Tags]    ok
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    TUNNEL_ENCAP_TYPE(type='vxlan'),L4_ENCAP_TYPE(type=4,dport=4789),L3_ENCAP_TYPE(type='ipv4',inherit=1),L2_FLAG
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    TUNNEL_ENCAP_TYPE(type='vxlan'),L4_ENCAP_TYPE(type=5,dport=4789),L3_ENCAP_TYPE(type='ipv6',inherit=1),L2_FLAG 

COSSW-8864_em
    [Documentation]    *验证 封装GENEVE隧道
    ...    a) 当前内层为L2， 隧道头中的next protocol为Ethernet
    ...    b) 当前内层为IPV4， 隧道头中的next protocol为IPV4
    ...    c) 当前内层为IPV6， 隧道头中的next protocol为IPV6
    ...    e）L3 encap IPV4，使用隧道的封装配置表，封装IPv4 ID/TTL/TOS
    ...    f)? L3 encap IPv6， 使用隧道的封装配置， 封装IPV6 HOP LIMIT/ TOS*
    [Tags]    ok
    验证EM-ACTION    eth    action    TUNNEL_ENCAP_TYPE(type='geneve'),L4_ENCAP_TYPE(type=4,dport=6081),L3_ENCAP_TYPE(type='ipv4'),L2_FLAG
    验证EM-ACTION    ipv4    action    DECAPSULATION(layer='ot_l3'),TUNNEL_ENCAP_TYPE(type='geneve'),L4_ENCAP_TYPE(type=5,dport=6081),L3_ENCAP_TYPE(type='ipv4'),L2_FLAG
    验证EM-ACTION    ipv6    action    DECAPSULATION(layer='ot_l3'),TUNNEL_ENCAP_TYPE(type='geneve'),L4_ENCAP_TYPE(type=4,dport=6081),L3_ENCAP_TYPE(type='ipv6'),L2_FLAG
    验证EM-ACTION    eth    action    TUNNEL_ENCAP_TYPE(type='geneve',optlen=5),L4_ENCAP_TYPE(type=5,dport=6081),L3_ENCAP_TYPE(type='ipv4'),L2_FLAG
    验证EM-ACTION    eth.2vlan.ipv4    action    TUNNEL_ENCAP_TYPE(type='geneve'),L4_ENCAP_TYPE(type=4,dport=6081),L3_ENCAP_TYPE(type='ipv4',inherit=1),L2_FLAG
    验证EM-ACTION    eth.2vlan.ipv6    action    TUNNEL_ENCAP_TYPE(type='geneve'),L4_ENCAP_TYPE(type=4,dport=6081),L3_ENCAP_TYPE(type='ipv6',inherit=1),L2_FLAG
    验证EM-ACTION    eth.2vlan.ipv4    action    TUNNEL_ENCAP_TYPE(type='geneve',optlen=6),L4_ENCAP_TYPE(type=4,dport=6081),L3_ENCAP_TYPE(type='ipv4'),L2_FLAG

COSSW-8865_em
    [Documentation]    *验证 封装NVGRE隧道
    ...    a）L3 encap IPV4，使用隧道的封装配置表，封装IPv4 ID/TTL/TOS
    ...    b) L3 encap IPv6， 使用隧道的封装配置， 封装IPV6 HOP LIMIT/ TOS*
    [Tags]    ok
    验证EM-ACTION    eth.ipv4    action    TUNNEL_ENCAP_TYPE(type='nvgre'),L3_ENCAP_TYPE(type='ipv4',inherit=1),L2_FLAG
    验证EM-ACTION    eth.ipv4    action    TUNNEL_ENCAP_TYPE(type='nvgre'),L3_ENCAP_TYPE(type='ipv6',inherit=1),L2_FLAG

COSSW-8866_em
    [Documentation]    *验证 封装GRE隧道
    ...    a) 当前内层为L2， 隧道头中的next protocol为Ethernet
    ...    b) 当前内层为IPV4， 隧道头中的next protocol为IPV4
    ...    c) 当前内层为IPV6， 隧道头中的next protocol为IPV6
    ...    e）L3 encap IPV4，使用隧道的封装配置表，封装IPv4 ID/TTL/TOS
    ...    f)? L3 encap IPv6， 使用隧道的封装配置， 封装IPV6 HOP LIMIT/ TOS*
    [Tags]    ok
    验证EM-ACTION    eth    action    TUNNEL_ENCAP_TYPE(type='gre'),L3_ENCAP_TYPE(type='ipv4'),L2_FLAG
    验证EM-ACTION    ipv4    action    DECAPSULATION(layer='ot_l3'),TUNNEL_ENCAP_TYPE(type='gre'),L3_ENCAP_TYPE(type='ipv4'),L2_FLAG
    验证EM-ACTION    ipv6    action    DECAPSULATION(layer='ot_l3'),TUNNEL_ENCAP_TYPE(type='gre'),L3_ENCAP_TYPE(type='ipv4'),L2_FLAG
    验证EM-ACTION    eth.2vlan.ipv4    action    TUNNEL_ENCAP_TYPE(type='gre'),L3_ENCAP_TYPE(type='ipv4',inherit=1),L2_FLAG
    验证EM-ACTION    eth.2vlan.ipv6    action    TUNNEL_ENCAP_TYPE(type='gre'),L3_ENCAP_TYPE(type='ipv6',inherit=1),L2_FLAG

COSSW-8867_em
    [Documentation]    *验证 封装VXLAN-GPE隧道
    ...    a) 当前内层为L2， 隧道头中的next protocol为Ethernet
    ...    b) 当前内层为IPV4， 隧道头中的next protocol为IPV4
    ...    c) 当前内层为IPV6， 隧道头中的next protocol为IPV6
    ...    e）L3 encap IPV4，使用隧道的封装配置表，封装IPv4 ID/TTL/TOS
    ...    f)? L3 encap IPv6， 使用隧道的封装配置， 封装IPV6 HOP LIMIT/ TOS*
    [Tags]    ok
    验证EM-ACTION    eth    action    TUNNEL_ENCAP_TYPE(type='vxlan-gpe'),L4_ENCAP_TYPE(type=4,dport=4790),L3_ENCAP_TYPE(type='ipv4'),L2_FLAG
    验证EM-ACTION    ipv4    action    DECAPSULATION(layer='ot_l3'),TUNNEL_ENCAP_TYPE(type='vxlan-gpe'),L4_ENCAP_TYPE(type=5,dport=4790),L3_ENCAP_TYPE(type='ipv4'),L2_FLAG
    验证EM-ACTION    ipv6    action    DECAPSULATION(layer='ot_l3'),TUNNEL_ENCAP_TYPE(type='vxlan-gpe'),L4_ENCAP_TYPE(type=4,dport=4790),L3_ENCAP_TYPE(type='ipv4'),L2_FLAG
    验证EM-ACTION    eth.2vlan.ipv4    action    TUNNEL_ENCAP_TYPE(type='vxlan-gpe'),L4_ENCAP_TYPE(type=4,dport=4790),L3_ENCAP_TYPE(type='ipv4',inherit=1),L2_FLAG
    验证EM-ACTION    eth.2vlan.ipv6    action    TUNNEL_ENCAP_TYPE(type='vxlan-gpe'),L4_ENCAP_TYPE(type=4,dport=4790),L3_ENCAP_TYPE(type='ipv6',inherit=1),L2_FLAG

COSSW-8869_em
    [Documentation]    *验证 IPV4-in-IPV4, 没有隧道信息， 使用tunnel type查封装配置表
    ...    a）L3 encap IPV4，使用隧道的封装配置表，封装IPv4 ID/TTL/TOS
    ...    b)? L3 encap IPv6， 使用隧道的封装配置， 封装IPV6 HOP LIMIT/ TOS*
    [Tags]    ok
    验证EM-ACTION    eth.ipv4.udp    action   DECAPSULATION(layer='ot_l3'),TUNNEL_ENCAP_TYPE(type='v4inv4'),L3_ENCAP_TYPE(type='ipv4',inherit=1),L2_FLAG

COSSW-8870_em
    [Documentation]    *验证 IPV4-in-IPV6, 没有隧道信息， 使用tunnel type查封装配置表
    ...    a）L3 encap IPV4，使用隧道的封装配置表，封装IPv4 ID/TTL/TOS
    ...    b)? L3 encap IPv6， 使用隧道的封装配置， 封装IPV6 HOP LIMIT/ TOS*
    [Tags]    ok
   验证EM-ACTION    ipv4.udp    action   DECAPSULATION(layer='ot_l3'),TUNNEL_ENCAP_TYPE(type='v4inv6'),L3_ENCAP_TYPE(type='ipv6',inherit=1),L2_FLAG

COSSW-8871_em
    [Documentation]    *验证 IPV6-in-IPV4, 没有隧道信息， 使用tunnel type查封装配置表
    ...    a）L3 encap IPV4，使用隧道的封装配置表，封装IPv4 ID/TTL/TOS
    ...    b)? L3 encap IPv6， 使用隧道的封装配置， 封装IPV6 HOP LIMIT/ TOS*
    [Tags]    ok
    验证EM-ACTION    ipv6.udp    action   DECAPSULATION(layer='ot_l3'),TUNNEL_ENCAP_TYPE(type='v6inv4'),L3_ENCAP_TYPE(type='ipv4',inherit=1),L2_FLAG

COSSW-8872_em
    [Documentation]    *验证 IPV6-in-IPV6, 没有隧道信息， 使用tunnel type查封装配置表
    ...    a）L3 encap IPV4，使用隧道的封装配置表，封装IPv4 ID/TTL/TOS
    ...    b)? L3 encap IPv6， 使用隧道的封装配置， 封装IPV6 HOP LIMIT/ TOS*
    [Tags]    ok
    验证EM-ACTION    ipv6.udp    action    DECAPSULATION(layer='ot_l3'),TUNNEL_ENCAP_TYPE(type='v6inv6'),L3_ENCAP_TYPE(type='ipv6',inherit=1),L2_FLAG

COSSW-10016_em
    [Documentation]    *验证 EM表配置4个version group, version group中的version全部匹配， 报文按照EM表的action转发*
    [Tags]    unknow
    验证EM-ACTION    [Net][DPE][EM]EM version检查全部通过

COSSW-10017_em
    [Documentation]    *验证 EM表配置4个version group, version group中的version其中有一个以上不匹配， 报文按照前级的有效destination转发*
    [Tags]    unknow
    验证EM-ACTION    [Net][DPE][EM]EM version检查不通过

EM_ACTION_EX_01
    [Documentation]    *验证 EM action 叠加*
    [Tags]    ok
    验证EM-ACTION    eth.2vlan.ipv4.udp    action    REPLACE_L4_DPORT,REPLACE_L4_SPORT,REPLACE_DIPV4,REPLACE_SIPV4,TTL_UPDATE(opcode=2,ttl=127),TOS_UPDATE(mask=0xfc,tos=0xb0),REMOVE_OUTER_VLAN,REMOVE_INNER_VLAN,REPLACE_SMAC,REPLACE_DMAC
    验证EM-ACTION    eth.2vlan.ipv6.udp    action    REPLACE_L4_DPORT,REPLACE_L4_SPORT,REPLACE_DIPV6,REPLACE_SIPV6,TTL_UPDATE(opcode=2,ttl=127),TOS_UPDATE(mask=0xfc,tos=0xb0),REMOVE_OUTER_VLAN,REMOVE_INNER_VLAN,REPLACE_SMAC,REPLACE_DMAC

EM_ACTION_EX_02
    [Documentation]    *验证 EM action 叠加*
    [Tags]    ok
    验证EM-ACTION    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.v4.udp   action    DECAPSULATION(layer='l3'),REPLACE_L4_DPORT,REPLACE_DIPV4,REPLACE_SIPV4,TTL_UPDATE(opcode=2,ttl=127),TOS_UPDATE(mask=0xfc,tos=0xb0),REMOVE_OUTER_VLAN,REMOVE_INNER_VLAN,REPLACE_SMAC,REPLACE_DMAC,L2_FLAG
    验证EM-ACTION    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.v6.udp    action    DECAPSULATION(layer='l3'),REPLACE_L4_DPORT,REPLACE_L4_SPORT,REPLACE_DIPV6,TTL_UPDATE(opcode=2,ttl=127),TOS_UPDATE(mask=0xfc,tos=0xb0),REMOVE_OUTER_VLAN,REMOVE_INNER_VLAN,REPLACE_SMAC,REPLACE_DMAC,L2_FLAG

COSSW-8756_em
    [Documentation]    *验证 key_template中key enable SIP+DIP+PROTOCOL,
    ...    range_check使能最外层SPORT和最外层DPORT
    ...    EM使用SIP+DIP+PROTOCOL可以命中， 但是range_check是失败的， 报文MISS上送*
    [Tags]    unknow
    验证EM-ACTION    eth.vlan.ipv4.udp.vxlan.eth.vlan.udp    OT_L4_SPORT,OT_L4_DPORT,OT_L3_PROT,RANGE_CHECK_TYPE0(type=14),RANGE_CHECK_TYPE1(type=15)    ${None}    miss

COSSW-11945_em
    [Documentation]    *验证 *
    [Tags]    unknow
    验证EM    [Net][DPE][EM]em表异常decap动作处理

COSSW-11947_em
    [Documentation]    *验证 对于overlay报文，如果decap掉隧道的l2/l3/l4信息，仅保留隧道头，不能支持ecn从外层继承到内层（如果后面有encap l3，配置ecn_inh2inner && ecn_inh2outer可以将decap掉的外层ecn信息继承到encap的l3中）*
    [Tags]    unknow
    验证EM    [Net][DPE][EM]EM ecn继承验证-1

COSSW-11948_em
    [Documentation]    *验证 ecn的继承只能在同一级pipe中配置，不支持在某一级pipe配置copy到内层，在另一级又配置copy到外层*
    [Tags]    unknow
    验证EM    [Net][DPE][EM]EM ecn继承验证-2

COSSW-11949_em
    [Documentation]    *验证 ecn的继承只能在同一级pipe中配置，不支持在某一级pipe配置copy到内层，在另一级又配置copy到外层*
    [Tags]    unknow
    验证EM    [Net][DPE][EM]EM ecn继承验证-2

COSSW-11950_em
    [Documentation]    *验证 *
    [Tags]    unknow
    验证EM    [Net][DPE][Mirror]配置镜像出口的报文， 对于drop的报文， 不做镜像

COSSW-11951_em
    [Documentation]    *验证 *
    [Tags]    unknow
    验证EM    [Net][DPE][RSS]IPV6带扩展头, 不支持L4信息参与RSS

COSSW-11952_em
    [Documentation]    *验证 TX 组播既往MAC口发， 又往VM发。 如果往MAC侧发送需要封装GRE隧道， 则L2头在EM表中需要decap掉， 环回到RX的报文无L2头。 待确认是否可以在action中封装一层L2*
    [Tags]    unknow
    验证EM    [Net][DPE][MC]TX组播， EM表decap L2的场景

*** Keywords ***
组配置初始化
    ${config}    ipv4Config.getEmActionSuiteConfig
    jaguarRunConfig    ${A}    ${config}
    清理测试仪

组配置清理
    ${config}    ipv4Config.getEmActionSuiteConfig
    jaguarClearConfig    ${A}    ${config}
    清理测试仪

验证EM-ACTION
    [Arguments]    ${pkt}    ${atype}=${None}    ${action}=${None}
    ${configResult}    ipv4Config.getEmActionValue    ${pkt}    OT_L2_SMAC,OT_L2_DMAC    ${None}    ${atype}    ${action}
    验证RESTFUL流量    ${configResult}
