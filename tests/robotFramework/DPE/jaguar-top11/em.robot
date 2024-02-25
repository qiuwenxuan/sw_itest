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
COSSW-8739_em_kt1
    [Documentation]    *验证 EM表定长128bit key查找 tbid=4*
    [Tags]    ok    基础通路
    验证EM    eth.vlan.ipv4.udp    OT_L3_SIP    128bits(type='fix')

COSSW-8740_em_kt2
    [Documentation]    *验证 EM表定长256bit key查找 tbid=3*
    [Tags]    ok    基础通路
    验证EM    eth.vlan.ipv4.udp    OT_L3_SIP    256bits(type='fix')

COSSW-8741_em_kt3
    [Documentation]    *验证 RX收到报文后， 依次查rx_inport、classify、profile、key_template、EM发送EM表定长512bit key查找 tbid=2*
    [Tags]    ok    基础通路
    验证EM    eth.vlan.ipv4.udp    OT_L3_SIP    512bits(type='fix')

COSSW-8742_em
    [Documentation]    *验证 RX收到报文后， 依次查rx_inport、classify、profile、key_template、EM发送EM表定长768bit key查找 tbid= 1*
    [Tags]    ok    基础通路
    验证EM    eth.vlan.ipv4.udp    OT_L3_SIP    768bits(type='fix')

COSSW-8743_em
    [Documentation]    *验证 RX收到报文后， 依次查rx_inport、classify、profile、key_template、EM发送
    ...    EM表变长128bit key查找*
    [Tags]    ok    基础通路
    验证EM    eth.vlan.ipv6.udp    OT_L3_SIP   128bits(type='change')

COSSW-8744_em
    [Documentation]    *验证 RX收到报文后， 依次查rx_inport、classify、profile、key_template、EM发送
    ...    EM表变长256bit key查找*
    [Tags]    ok    基础通路
    验证EM   eth.vlan.ipv6.udp    OT_L3_SIP,OT_L3_DIP  256bits(type='change')

COSSW-8745_em
    [Documentation]    *验证 EM表变长512bit key查找*
    [Tags]    ok
    验证EM    eth.vlan.ipv6.udp    OT_L3_SIP,OT_L3_DIP    512bits(type='change')

COSSW-8746_em
    [Documentation]    *验证 h1. RX收到报文后， 依次查rx_inport、classify、profile、key_template、EM发送
    ...    EM表变长768bit key查找*
    [Tags]    ok    基础通路
     验证EM    eth.vlan.ipv6.udp    OT_L3_SIP,OT_L3_DIP    768bits(type='change')

COSSW-8747_em
    [Documentation]    *验证 其中Em的key为六元组：tunnel id(24bit)+SIP(24bit掩码)+DIP(24bit)+PROTOCOL+SPORT(10bit)+DPORT(10bit)
    ...    使用key_template_mask配置域段的掩码
    ...    EM表key为定长128bit*
    [Tags]    test    基础通路
    验证EM    eth.vlan.ipv4.udp.vxlan.eth.ip.udp    OT_TUNNEL_ID(mask=24),TL_L3_SIP(mask=24),TL_L3_DIP(mask=24),TL_L3_PROT,TL_L4_SPORT(mask=10),TL_L4_DPORT(mask=10)    128bits(type='fix')

COSSW-8748_em
    [Documentation]    *验证 使用key_template_mask配置域段的掩码*
    [Tags]    unknow
    验证EM    [Net][DPE][KT]RX EM查找 -10

COSSW-8749_em
    [Documentation]    *验证 使用key_template_mask配置域段的掩码*
    [Tags]    unknow
    验证EM    [Net][DPE][KT]RX EM查找 -11

COSSW-8751_em
    [Documentation]    *验证 使用key_template_mask配置域段的掩码*
    [Tags]    unknow
    验证EM    [Net][DPE][KT]RX EM查找 -13

COSSW-8752_em
    [Documentation]    *验证 使能五元组和1个L4的UDF域段*
    [Tags]    unknow
    验证EM    [Net][DPE][KT]RX EM查找 -14

COSSW-8753_em
    [Documentation]    *验证 RX收到报文后， 依次查rx_inport、classify、profile、key_template、EM发送key_template使能UDF域段-2
    ...    使用7个UDF域段， 包括最外层、次外层和最内层的域段提取*
    [Tags]    unknow
    验证EM    [Net][DPE][KT]RX EM查找 -15

COSSW-8754_em
    [Documentation]    *验证 key使能L4 sport、dport域段， 但非TCP/UDP/ICMP， 域段填0*
    [Tags]    ok
    验证EM    eth.vlan.ipv4.igmp    OT_L4_SPORT,OT_L4_DPORT

COSSW-8755_em
    [Documentation]    *验证 key使能内层L2的MAC域段， 但内层l2 valid为0， 域段填0*
    [Tags]    ok
    验证EM    eth.vlan.ipv4.ipinip.ipv4.udp    TL_L2_SMAC,TL_L4_SPORT

COSSW-8757_em
    [Documentation]    *验证 key_template中key enable SIP+DIP+PROTOCOL,
    ...    range_check使能最外层SPORT和最外层DPORT
    ...    EM使用SIP+DIP+PROTOCOL可以命中，并且range_check可以命中， 报文使用EM指定的目的转发*
    [Tags]    test
    验证EM    eth.vlan.ipv4.udp.vxlan.eth.vlan.udp    OT_L3_SIP,OT_L3_DIP,OT_L3_PROT,RANGE_CHECK_TYPE0(type='ot_l4_sport'),RANGE_CHECK_TYPE1(type='ot_l4_dport')

COSSW-8758_em
    [Documentation]    *验证 key_template中key enable SIP+DIP+PROTOCOL,
    ...    range_check使能最外层的外层VLANID和内层VLANID
    ...    EM使用SIP+DIP+PROTOCOL可以命中，并且range_check可以命中， 报文使用EM指定的目的转发*
    [Tags]    test
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.udp    OT_L3_SIP,OT_L3_SIP,OT_L3_PROT,RANGE_CHECK_TYPE0(type=0),RANGE_CHECK_TYPE1(type=1)

COSSW-8759_em
    [Documentation]    *验证 key_template中key enable SIP+DIP+PROTOCOL,
    ...    range_check使能次外层的外层VLANID和内层VLANID
    ...    EM使用SIP+DIP+PROTOCOL可以命中，并且range_check可以命中， 报文使用EM指定的目的转发*
    [Tags]    test
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.udp    OT_L3_SIP,OT_L3_SIP,OT_L3_PROT,RANGE_CHECK_TYPE0(type=2),RANGE_CHECK_TYPE1(type=3)

COSSW-8760_em
    [Documentation]    *验证 key_template中key enable SIP+DIP+PROTOCOL,
    ...    range_check使能内层的外层VLANID和内层VLANID
    ...    EM使用SIP+DIP+PROTOCOL可以命中，并且range_check可以命中， 报文使用EM指定的目的转发*
    [Tags]    test
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4    OT_L3_SIP,OT_L3_SIP,OT_L3_PROT,RANGE_CHECK_TYPE0(4),RANGE_CHECK_TYPE1(type=5)

COSSW-8761_em
    [Documentation]    *验证 key_template中key enable SIP+DIP+PROTOCOL,
    ...    range_check使能次外层SPORT和次外层DPORT
    ...    EM使用SIP+DIP+PROTOCOL可以命中，并且range_check可以命中， 报文使用EM指定的目的转发*
    [Tags]    test
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4    OT_L3_SIP,OT_L3_SIP,OT_L3_PROT,RANGE_CHECK_TYPE0(type=4),RANGE_CHECK_TYPE1(type=5)

COSSW-8762_em
    [Documentation]    *验证 key_template中key enable SIP+DIP+PROTOCOL,
    ...    range_check使能最内层SPORT和最内层层DPORT
    ...    EM使用SIP+DIP+PROTOCOL可以命中，并且range_check可以命中， 报文使用EM指定的目的转发*
    [Tags]    unknow
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4    OT_L3_SIP,OT_L3_SIP,OT_L3_PROT,RANGE_CHECK_TYPE0(type=4),RANGE_CHECK_TYPE1(type=5)

COSSW-8763_em
    [Documentation]    *验证 key_template中key enable SIP+DIP+PROTOCOL,
    ...    range_check使能udf0和udf1域段
    ...    EM使用SIP+DIP+PROTOCOL可以命中，并且range_check可以命中， 报文使用EM指定的目的转发*
    [Tags]    unknow
    验证EM    [Net][DPE][KT]RX EM查找 -25

COSSW-8764_em
    [Documentation]    *验证 匹配Key profile id*
    [Tags]    ok    内部写死
    验证EM    eth.ipv4.udp    OT_L2_DMAC

COSSW-8765_em
    [Documentation]    *验证 匹配Group index*
    [Tags]    ok    内部写死
    验证EM    eth.ipv4.udp    OT_L2_DMAC

COSSW-8766_em
    [Documentation]    *验证 匹配Vnic ID*
    [Tags]    test
    验证EM    eth.ipv4.udp    VNIC_ID

COSSW-8767_em
    [Documentation]    *验证 匹配Meta Data*
    [Tags]    unknow
    验证EM    eth.ipv4.udp    META_DATA

COSSW-8768_em
    [Documentation]    *验证 匹配mac port enable*
    [Tags]    unknow
    验证EM    eth.ipv4.udp    MAC_PORT_ENABLE

COSSW-8769_em
    [Documentation]    *验证 匹配最外层DMAC*
    [Tags]    ok
    验证EM    eth.ipv4.udp    OT_L2_DMACOT_L2_DMAC

COSSW-8770_em
    [Documentation]    *验证 匹配最外层SMAC*
    [Tags]    ok
    验证EM    eth.ipv4.udp    OT_L2_SMAC

COSSW-8771_em
    [Documentation]    *验证 匹配最外层outer vlan tpid*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp    OT_L2_OUT_VLAN_TPID

COSSW-8772_em
    [Documentation]    *验证 匹配最外层outer vlan pri*
    [Tags]    ok
    验证EM    eth.vlan(prio=5).vlan.ipv4.udp    OT_L2_OUT_VLAN_PRI

COSSW-8773_em
    [Documentation]    *验证 匹配最外层outer vlan de*
    [Tags]    ok
    验证EM    eth.vlan(id=1).vlan.ipv4.udp    OT_L2_OUT_VLAN_DE

COSSW-8774_em
    [Documentation]    *验证 匹配最外层outer vlan vid*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp    OT_L2_OUT_VLAN_VID

COSSW-8775_em
    [Documentation]    *验证 匹配最外层inner vlan tpid*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp    OT_L2_INNER_VLAN_TPID

COSSW-8776_em
    [Documentation]    *验证 匹配最外层inner vlan pri*
    [Tags]    ok
    验证EM    eth.vlan.vlan(prio=2).ipv4.udp    OT_L2_INNER_VLAN_PRI

COSSW-8777_em
    [Documentation]    *验证 匹配最外层inner vlan de*
    [Tags]    ok
    验证EM    eth.vlan.vlan(id=1).ipv4.udp    OT_L2_INNER_VLAN_DE

COSSW-8778_em
    [Documentation]    *验证 匹配最外层inner vlan vid*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp    OT_L2_INNER_VLAN_VID

COSSW-8779_em
    [Documentation]    *验证 匹配最外层L3 type*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp    OT_L3_TYPE

COSSW-8780_em
    [Documentation]    *验证 匹配最外层IPv6_SIP[127:0]/IPv4_SIP[31:0]*
    [Tags]    ok
    验证EM    eth.2vlan.ipv6.udp.vxlan.eth.2vlan.ipv4    OT_L3_SIP
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6    OT_L3_SIP

COSSW-8781_em
    [Documentation]    *验证 匹配最外层IPv6_DIP[127:0]/IPv4_DIP[31:0]*
    [Tags]    ok
    验证EM    eth.2vlan.ipv6.udp.vxlan.eth.2vlan.ipv4    OT_L3_DIP
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6    OT_L3_DIP

COSSW-8782_em
    [Documentation]    *验证 匹配最外层Protocol*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4    OT_L3_PROT

COSSW-8783_em
    [Documentation]    *验证 匹配最外层TTL*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4(ttl=12).udp.vxlan.eth.2vlan.ipv4

COSSW-8784_em
    [Documentation]    *验证 匹配最外层TOS*
    [Tags]    ok
    验证EM    eth.2vlan.ipv6(tc=12).udp.vxlan.eth.2vlan.ipv4

COSSW-8785_em
    [Documentation]    *验证 匹配最外层Flow*
    [Tags]    ok
    验证EM    eth.2vlan.ipv6(fl=1234).udp.vxlan.eth.2vlan.ipv4

COSSW-8786_em
    [Documentation]    *验证 匹配最外层fragment*
    [Tags]    ok    重跑
    验证EM    eth.2vlan.ipv4-frag(flags=1,proto=17)

COSSW-8787_em
    [Documentation]    *验证 匹配最外层Extension header valid*
    [Tags]    ok    重跑
    验证EM    eth.2vlan.ipv6-ext.udp.vxlan.eth.2vlan.ipv4    OT_L3_EXT_HD_VALID

COSSW-8788_em
    [Documentation]    *验证 匹配最外层SPORT[7:0]/ICMP_Code*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.tcp(sport=0x1234)    OT_L4_SPORT1
    验证EM    eth.2vlan.ipv4.udp(sport=0x1234)    OT_L4_SPORT1
    验证EM    eth.2vlan.ipv4.icmp    OT_L4_SPORT1

COSSW-8789_em
    [Documentation]    *验证 匹配最外层SPORT[15:8]/ICMP_Type*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.tcp(sport=0x1234)    OT_L4_SPORT2
    验证EM    eth.2vlan.ipv4.udp(sport=0x1234)    OT_L4_SPORT2
    验证EM    eth.2vlan.ipv4.icmp    OT_L4_SPORT2

COSSW-8790_em
    [Documentation]    *验证 匹配最外层DPORT[15:0]/ICMP_Identifier*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.tcp(dport=0x1234)    OT_L4_DPORT
    验证EM    eth.2vlan.ipv4.udp(dport=0x2345)    OT_L4_DPORT
    验证EM    eth.2vlan.ipv4.icmp    OT_L4_dPORT

COSSW-8791_em
    [Documentation]    *验证 匹配最外层Flags*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.tcp    OT_L4_FLAGS

COSSW-8792_em
    [Documentation]    *验证 EM opcode为bypass PIPE
    ...    使用EM中的action_type和Destination发送
    ...    destionation valid,
    [Tags]    unknow
    action type为单播， destination为目的， 使用EM表中的目的转发*
    验证EM    [Net][DPE][KT]RX EM查找 -54

COSSW-8793_em
    [Documentation]    *验证 EM opcode为bypass PIPE
    ...    使用EM中的action_type和Destination发送
    ...    destionation valid,
    [Tags]    unknow
    action type为组播， destination为group id， 使用groupid查组播表， 将报文发到多个目的*
    验证EM    [Net][DPE][KT]RX EM查找 -125

COSSW-8794_em
    [Documentation]    *验证 EM opcode为bypass PIPE
    ...    使用EM中的action_type和Destination发送
    ...    destionation invalid,
    [Tags]    unknow
    profile表中的destionation有效， 使用profile中的目的转发*
    验证EM    [Net][DPE][KT]RX EM查找 -126

COSSW-8795_em
    [Documentation]    *验证 EM opcode为bypass PIPE
    ...    使用EM中的action_type和Destination发送
    ...    destionation invalid,
    [Tags]    unknow
    profile表中的destionation无效， classify表中的destination有效， 使用classify表中的目的转发*
    验证EM    [Net][DPE][KT]RX EM查找 -127

COSSW-8796_em
    [Documentation]    *验证 EM opcode为bypass PIPE
    ...    使用EM中的action_type和Destination发送
    ...    destionation invalid,
    [Tags]    unknow
    profile表、classify表中的destionation无效，使用port表中的目的转发*
    验证EM    [Net][DPE][KT]RX EM查找 -128

COSSW-8797_em
    [Documentation]    *验证 叠加EM表中set tc为7， 配置转发时高优先级上送*
    [Tags]    unknow
    验证EM    [Net][DPE][KT]RX EM查找 -129

COSSW-8798_em
    [Documentation]    *验证 叠加mirror使能， 将mirror优先级和index写入metainfo传给POL*
    [Tags]    unknow
    验证EM    [Net][DPE][KT]RX EM查找 -130

COSSW-8799_em
    [Documentation]    *验证 叠加meter使能4级， 将meter index写入meta info 传给POL*
    [Tags]    unknow
    验证EM    [Net][DPE][KT]RX EM查找 -131

COSSW-8800_em
    [Documentation]    *验证 EM opcode为：Send to MEP with action
    ...    decap动作剥掉一层隧道， 将EM中mep reason、profile id、KT index写入meta info中发送给MEP*
    [Tags]    unknow
    验证EM    [Net][DPE][PIPE]完成本EM的action后， 再送MEP

COSSW-8801_em
    [Documentation]    *验证 EM opcode为：Send to MEP without action
    ...    不关心EM表中的action动作， 将EM中mep reason、profile id、KT index写入meta info中发送给MEP*
    [Tags]    unknow
    验证EM    [Net][DPE][PIPE]本EM的action不处理， 直接送MEP

COSSW-8802_em
    [Documentation]    *验证 EM opcode为: drop
    ...    报文丢弃， flow表中的mirror enable和index提取到meta info中传给POL*
    [Tags]    unknow
    验证EM    [Net][DPE][PIPE]action动作为drop

COSSW-8805_em
    [Documentation]    *验证 EM key为128bit， key+result 大于1024bit，? （896bit-160bit）<pipe_result<=1024bit的场景， 由于TSE进行扩展读*
    [Tags]    unknow
    验证EM    [Net][DPE][PIPE]EM扩展表-1

COSSW-8806_em
    [Documentation]    *验证 EM key为128bit，pipe_result>1024bit， TSE不读扩展表， 由PIPE进行扩展读*
    [Tags]    unknow
    验证EM    [Net][DPE][PIPE]EM扩展表-2

COSSW-8807_em
    [Documentation]    *验证 EM key为128bit， key+result 大于1024bit，? （768bit-160bit）<pipe_result<=1024bit的场景， 由于TSE进行扩展读512bit*
    [Tags]    unknow
    验证EM    [Net][DPE][PIPE]EM扩展表-3

COSSW-8808_em
    [Documentation]    *验证 EM key为256bit，pipe_result>1024bit， TSE不读扩展表， 由PIPE进行扩展读*
    [Tags]    unknow
    验证EM    [Net][DPE][PIPE]EM扩展表-4

COSSW-8809_em
    [Documentation]    *验证 EM key为512bit， key+result 大于1024bit，? （512bit-160bit）<pipe_result<=1024bit的场景， 由于TSE进行扩展读1Kbit*
    [Tags]    unknow
    验证EM    [Net][DPE][PIPE]EM扩展表-5

COSSW-8810_em
    [Documentation]    *验证 EM key为512bit，pipe_result>1024bit， TSE读512bit的扩展表， 其余的由PIPE进行扩展读*
    [Tags]    unknow
    验证EM    [Net][DPE][PIPE]EM扩展表-6

COSSW-8811_em
    [Documentation]    *验证 EM key为768bit， key+result 大于1024bit，? （256bit-160bit）<pipe_result<=1024bit的场景， 由于TSE进行扩展读1Kbit*
    [Tags]    unknow
    验证EM    [Net][DPE][PIPE]EM扩展表-7

COSSW-8812_em
    [Documentation]    *验证 EM key为768bit，pipe_result>1024bit， TSE读1kbit的扩展表， 其余的由PIPE进行扩展读*
    [Tags]    unknow
    验证EM    [Net][DPE][PIPE]EM扩展表-8

COSSW-8813_em
    [Documentation]    *验证 EM表中：
    ...    storage_read为1
    ...    mirror_meter_index: 存放存储读的索引， PIPE存放在vblk_index位置传递给VPE
    ...    destination中指定vnic信息*
    [Tags]    unknow
    验证EM    [Net][DPE][PIPE]自定义存储读

COSSW-11865_em
    [Documentation]    *验证 匹配一层隧道的内层DMAC*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    TL_L2_DMAC

COSSW-11866_em
    [Documentation]    *验证 匹配一层隧道的内层SMAC*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    TL_L2_SMAC

COSSW-11867_em
    [Documentation]    *验证 匹配一层隧道的内层outer vlan tpid*
    [Tags]    ok    重跑
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    TL_L2_OUT_VLAN_TPID

COSSW-11868_em
    [Documentation]    *验证 匹配一层隧道的内层outer vlan pri*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan(prio=1).ipv4.udp    TL_L2_OUT_VLAN_PRI

COSSW-11869_em
    [Documentation]    *验证 匹配一层隧道的内层outer vlan de*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    TL_L2_OUT_VLAN_DE

COSSW-11870_em
    [Documentation]    *验证 匹配一层隧道的内层outer vlan vid*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    TL_L2_OUT_VLAN_VID

COSSW-11871_em
    [Documentation]    *验证 匹配一层隧道的内层inner vlan tpid*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    TL_L2_INNER_VLAN_TPID

COSSW-11872_em
    [Documentation]    *验证 匹配一层隧道的内层inner vlan pri*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan(prio=2).ipv4.udp    TL_L2_INNER_VLAN_PRI

COSSW-11873_em
    [Documentation]    *验证 匹配一层隧道的内层inner vlan de*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    TL_L2_INNER_VLAN_DE

COSSW-11874_em
    [Documentation]    *验证 匹配一层隧道的内层inner vlan vid*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    TL_L2_INNER_VLAN_VID

COSSW-11875_em
    [Documentation]    *验证 匹配一层隧道的内层L3 type*
    [Tags]    ok    重跑
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    TL_L3_TYPE

COSSW-11876_em
    [Documentation]    *验证 匹配一层隧道的内层IPv6_SIP[127:0]/IPv4_SIP[31:0]*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.udp    TL_L3_SIP
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    TL_L3_SIP

COSSW-11877_em
    [Documentation]    *验证 匹配一层隧道的内层IPv6_DIP[127:0]/IPv4_DIP[31:0]*
    [Tags]    ok   
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.udp    TL_L3_DIP
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    TL_L3_DIP

COSSW-11878_em
    [Documentation]    *验证 匹配一层隧道的内层Protocol*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    TL_L3_PROT

COSSW-11879_em
    [Documentation]    *验证 匹配一层隧道的内层TTL*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    TL_L3_TTL

COSSW-11880_em
    [Documentation]    *验证 匹配一层隧道的内层TOS*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.udp    TL_L3_TOS

COSSW-11881_em
    [Documentation]    *验证 匹配一层隧道的内层Flow*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.udp    TL_L3_FLOW
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    TL_L3_FLOW   

COSSW-11882_em
    [Documentation]    *验证 匹配一层隧道的内层fragment*
    [Tags]    ok    
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.udp    TL_L3_FRAG
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4-frag(flags=0x01,frag=0x200,proto=17)    TL_L3_FRAG

COSSW-11883_em
    [Documentation]    *验证 匹配一层隧道的内层Extension header valid*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6-ext.udp    TL_L3_EXT_HD_VALID

COSSW-11884_em
    [Documentation]    *验证 匹配一层隧道的内层SPORT[7:0]/ICMP_Code*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.icmp    TL_L4_SPORT1
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.tcp(sport=0x1234)    TL_L4_SPORT1
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp(sport=0x2345)    TL_L4_SPORT1
    
COSSW-11885_em
    [Documentation]    *验证 匹配一层隧道的内层SPORT[15:8]/ICMP_Type*
    [Tags]    ok    
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.tcp(sport=0x1234)    TL_L4_SPORT2
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp(sport=0x2345)    TL_L4_SPORT2
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.icmp    TL_L4_SPORT2

COSSW-11886_em
    [Documentation]    *验证 匹配一层隧道的内层DPORT[15:0]/ICMP_Identifier*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.icmp    TL_L4_DPORT
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.tcp(dport=0x1234)    TL_L4_DPORT
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp(dport=0x2345)    TL_L4_DPORT

COSSW-11887_em
    [Documentation]    *验证 匹配一层隧道的内层Flags*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.ipv4.tcp    TL_L4_FLAGS

COSSW-11889_em
    [Documentation]    *验证 匹配一层gre隧道key id*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.gre.ipv4.udp    OT_TUNNEL_TYPE,OT_TUNNEL_ID

COSSW-11890_em
    [Documentation]    *验证 匹配一层geneve隧道vni id*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.geneve.eth.ipv4.udp    OT_TUNNEL_TYPE,OT_TUNNEL_ID

COSSW-11891_em
    [Documentation]    *验证 匹配一层vxlan隧道vni id*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.ipv4.udp    OT_TUNNEL_TYPE,OT_TUNNEL_ID

COSSW-11892_em
    [Documentation]    *验证 匹配一层vxlan-gpre隧道vni id*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan-gpe.eth.ipv4.udp    OT_TUNNEL_TYPE,OT_TUNNEL_ID

COSSW-11896_em
    [Documentation]    *验证 匹配一层ipv4-ipv4隧道类型*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.ipinip.ipv4.udp    OT_TUNNEL_TYPE

COSSW-11897_em
    [Documentation]    *验证 匹配一层ipv4-ipv6隧道类型*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.ipinip.ipv6.udp    OT_TUNNEL_TYPE

COSSW-11898_em
    [Documentation]    *验证 匹配一层ipv6-ipv4隧道类型*
    [Tags]    ok
    验证EM    eth.2vlan.ipv6.ipinip.ipv4.udp    OT_TUNNEL_TYPE

COSSW-11899_em
    [Documentation]    *验证 匹配一层ipv6-ipv6隧道类型*
    [Tags]    ok
    验证EM    eth.2vlan.ipv6.ipinip.ipv6.udp    OT_TUNNEL_TYPE

COSSW-11901_em
    [Documentation]    *验证 匹配两层gre隧道key id*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.gre.eth.2vlan.ipv4.gre.eth.ipv4.udp    TL_TUNNEL_TYPE,TL_TUNNEL_ID

COSSW-11902_em
    [Documentation]    *验证 匹配两层geneve隧道vni id*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.geneve.eth.2vlan.ipv4.udp.geneve.eth.ipv4.udp    TL_TUNNEL_TYPE,TL_TUNNEL_ID

COSSW-11903_em
    [Documentation]    *验证 匹配两层vxlan隧道vni id*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.ipv4.udp    TL_TUNNEL_TYPE,TL_TUNNEL_ID

COSSW-11904_em
    [Documentation]    *验证 匹配两层vxlan-gpre隧道vni id*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan-gpe.eth.2vlan.ipv4.udp.vxlan-gpe.eth.ipv4.udp    TL_TUNNEL_TYPE,TL_TUNNEL_ID

COSSW-11908_em
    [Documentation]    *验证 匹配两层ipv4-ipv4隧道类型*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.ipinip.ipv4.udp    TL_TUNNEL_TYPE

COSSW-11909_em
    [Documentation]    *验证 匹配两层ipv4-ipv6隧道类型*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.ipinip.ipv6.udp    TL_TUNNEL_TYPE

COSSW-11910_em
    [Documentation]    *验证 匹配两层ipv6-ipv4隧道类型*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.ipinip.ipv4.udp    TL_TUNNEL_TYPE

COSSW-11911_em
    [Documentation]    *验证 匹配两层ipv6-ipv6隧道类型*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.ipinip.ipv6.udp    TL_TUNNEL_TYPE

COSSW-11912_em
    [Documentation]    *验证 匹配两层隧道的最内层DMAC*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    L2_DMAC

COSSW-11913_em
    [Documentation]    *验证 匹配两层隧道的最内层SMAC*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    L2_SMAC

COSSW-11914_em
    [Documentation]    *验证 匹配两层隧道的最内层outer vlan tpid*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    L2_OUT_VLAN_TPID

COSSW-11915_em
    [Documentation]    *验证 匹配两层隧道的最内层outer vlan pri*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.vlan(prio=3).vlan(prio=2).ipv4.udp    L2_OUT_VLAN_PRI

COSSW-11916_em
    [Documentation]    *验证 匹配两层隧道的最内层outer vlan de*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    L2_OUT_VLAN_DE

COSSW-11917_em
    [Documentation]    *验证 匹配两层隧道的最内层outer vlan vid*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    L2_OUT_VLAN_VID

COSSW-11918_em
    [Documentation]    *验证 匹配两层隧道的最内层inner vlan tpid*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    L2_INNER_VLAN_TPID

COSSW-11919_em
    [Documentation]    *验证 匹配两层隧道的最内层inner vlan pri*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan(prio=1).ipv4.udp    L2_INNER_VLAN_PRI

COSSW-11920_em
    [Documentation]    *验证 匹配两层隧道的最内层inner vlan de*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    INNER_VLAN_DE

COSSW-11921_em
    [Documentation]    *验证 RX EM查找 匹配两层隧道的最内层inner vlan vid*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan(vlan=103).ipv4.udp    INNER_VLAN_VID

COSSW-11922_em
    [Documentation]    *验证 匹配两层隧道的最内层L3 type*
    [Tags]    ok    
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    L3_TYPE

COSSW-11923_em
    [Documentation]    *验证 匹配两层隧道的最内层IPv6_SIP[127:0]/IPv4_SIP[31:0]*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    L3_SIP
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.udp    L3_SIP

COSSW-11924_em
    [Documentation]    *验证 匹配两层隧道的最内层IPv6_DIP[127:0]/IPv4_DIP[31:0]*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp    L3_DIP
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.udp    L3_DIP

COSSW-11925_em
    [Documentation]    *验证 匹配两层隧道的最内层Protocol*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.udp    L3_PROT

COSSW-11926_em
    [Documentation]    *验证 匹配两层隧道的最内层TTL*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.udp    L3_TTL

COSSW-11927_em
    [Documentation]    *验证 匹配两层隧道的最内层TOS*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.udp    L3_TOS

COSSW-11928_em
    [Documentation]    *验证 匹配两层隧道的最内层Flow*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.udp    L3_FLOW

COSSW-11929_em
    [Documentation]    *验证 匹配两层隧道的最内层fragment*
    [Tags]    ok    
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.udp    L3_FRAG
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4-frag(flags=0x01,proto=17)    L3_FRAG

COSSW-11930_em
    [Documentation]    *验证 匹配两层隧道的最内层Extension header valid*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6-ext.udp    L3_EXT_HD_VALID

COSSW-11931_em
    [Documentation]    *验证 匹配两层隧道的最内层SPORT[7:0]/ICMP_Code*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.tcp(sport=0x1234)    L4_SPORT1
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.udp(sport=0x2345)    L4_SPORT1
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.icmp6    L4_SPORT1

COSSW-11932_em
    [Documentation]    *验证 匹配两层隧道的最内层SPORT[15:8]/ICMP_Type*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.tcp(sport=0x1234)    L4_SPORT2
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.udp(sport=0x2345)    L4_SPORT2
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.icmp6    L4_SPORT2

COSSW-11933_em
    [Documentation]    *验证 匹配两层隧道的最内层DPORT[15:0]/ICMP_Identifier*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.tcp(dport=0x2143)    L4_DPORT
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.udp(dport=0x3254)    L4_DPORT
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.icmp6    L4_DPORT

COSSW-11934_em
    [Documentation]    *验证 匹配两层隧道的最内层Flags*
    [Tags]    ok
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv6.tcp    L4_FLAGS
    验证EM    eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.udp.vxlan.eth.2vlan.ipv4.tcp    L4_FLAGS

COSSW-11938_em
    [Documentation]    *验证 *
    [Tags]    unknow
    #验证EM    [Net][DPE][EM]上行PIPE编辑报文超过110字节- 不带扩展头
    验证EM    eth.ipv4(len=120)

COSSW-11939_em
    [Documentation]    *验证 *
    [Tags]    unknow
    验证EM    [Net][DPE][EM]上行PIPE编辑报文超过110字节- 带V4扩展头

COSSW-11940_em
    [Documentation]    *验证 *
    [Tags]    unknow
    验证EM    [Net][DPE][EM]上行PIPE编辑报文超过110字节- 带V6扩展头

COSSW-11941_em
    [Documentation]    *验证 *
    [Tags]    unknow
    验证EM    [Net][DPE][EM]下行PIPE编辑报文超过256字节- 不带扩展头

COSSW-11942_em
    [Documentation]    *验证 *
    [Tags]    unknow
    验证EM    [Net][DPE][EM]下行PIPE编辑报文超过256字节- 带V4扩展头

COSSW-11943_em
    [Documentation]    *验证 *
    [Tags]    unknow
    验证EM    [Net][DPE][EM]下行PIPE编辑报文超过256字节- 带V6扩展头

COSSW-11944_em
    [Documentation]    *验证 *
    [Tags]    unknow
    验证EM    [Net][DPE][EM]EM表key udf域段在256byte之外

COSSW-11946_em
    [Documentation]    *验证 *
    [Tags]    unknow
    验证EM    [Net][DPE][WC]WC表项SIZE验证

*** Keywords ***
组配置初始化
    ${config}    ipv4Config.getEmSuiteConfig
    jaguarRunConfig    ${A}    ${config}
    清理测试仪

组配置清理
    ${config}    ipv4Config.getEmSuiteConfig
    jaguarClearConfig    ${A}    ${config}
    清理测试仪

验证EM
    [Arguments]    ${pkt}    ${keys}=${None}    ${keylen}=${None}    ${action}=${None}
    ${configResult}    ipv4Config.getEmValue    ${pkt}    ${keys}    ${keylen}    ${action}
    验证RESTFUL流量    ${configResult}
