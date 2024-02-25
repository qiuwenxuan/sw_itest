*** Settings ***
Suite Setup       清理测试仪
Suite Teardown    清理测试仪
Test Setup        清理测试仪
Test Teardown     清理测试仪
Force Tags        MOD    FWD
Resource          ../../testlib/testlib.robot
Resource          ../../testlib/features/ovs.robot

*** Variables ***

*** Test Cases ***
COSSW-16240 验证modify项eth_001 
    [Documentation]    *set l2 src mac match icmp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    -mod_dl_src=\

COSSW-16241 验证modify项eth_002
    [Documentation]    *set l2 src mac match ipv4 to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    -mod_dl_src=\    

COSSW-16242 验证modify项eth_003
    [Documentation]    *set  l2 dst mac match icmp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    -mod_dl_dst=\

COSSW-16243 验证modify项eth_004
    [Documentation]    *set  l2 dst mac match ipv4 to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    -mod_dl_dst=\    

COSSW-16244 验证modify项eth_005
    [Documentation]    *set l2 src and dst mac match icmp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    -mod_dl_src=\    -mod_dl_dst=\    

COSSW-16245 验证modify项eth_006
    [Documentation]    *set l2 src and dst mac match ipv4 to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    -mod_dl_src=\    -mod_dl_dst=\       

COSSW-16246 验证modify项ipv4_001
    [Documentation]    *set l3 src ip match ipv4 to stream*
    [Tags]    ok    decap_nok    COSSW-15832
    验证ovs-hw-offload流量    fwd    ipv4    0    nw_proto=17    dl_type=\    -mod_nw_src=\

COSSW-16247 验证modify项ipv4_002
    [Documentation]    *set  l3 dst ip match ipv4 to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    nw_proto=17    dl_type=\    -mod_nw_dst=\

COSSW-16248 验证modify项ipv4_003
    [Documentation]    *set l3 src and dst ip match ipv4 to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    0    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\

COSSW-16249 验证modify项ipv4_004
    [Documentation]    *set l3 src ip match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\

COSSW-16250 验证modify项ipv4_005
    [Documentation]    *set  l3 dst ip match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_dst=\

COSSW-16251 验证modify项ipv4_006
    [Documentation]    *set l3 src and dst ip match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\

COSSW-16252 验证modify项eth+ipv4_001
    [Documentation]    *set l2 src mac and l3 src ip match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_dl_src=\

COSSW-16253 验证modify项eth+ipv4_002
    [Documentation]    *set l2 dst mac and l3 src ip match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_dl_dst=\

COSSW-16254 验证modify项eth+ipv4_003
    [Documentation]    *set l2 src mac and l3 dst ip match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_dst=\    -mod_dl_src=\

COSSW-16255 验证modify项eth+ipv4_004
    [Documentation]    *set l2 dst mac and l3 dst ip match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_dst=\    -mod_dl_dst=\

COSSW-16256 验证modify项eth+ipv4_005
    [Documentation]    *set l3_src l2_src dl_dst match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_dl_src=\    -mod_dl_dst=\    -mod_nw_src=\

COSSW-16257 验证modify项eth+ipv4_006
    [Documentation]    *set l2_src l3_dst l2_dst match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_dl_src=\    -mod_dl_dst=\    -mod_nw_dst=\

COSSW-16258 验证modify项eth+ipv4_007
    [Documentation]    *set l3_src l2_src l3_dst match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_src=\

COSSW-16259 验证modify项eth+ipv4_008
    [Documentation]    *set l3_src l3_dst l2_dst nw_dst match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_dst=\

COSSW-16260 验证modify项eth+ipv4_009
    [Documentation]    *set l3_src l2_src l3_dst l2_dst nw_dst match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_dl_src=\    -mod_dl_dst=\    -mod_nw_src=\    -mod_nw_dst=\

COSSW-16261 验证modify项tp_001
    [Documentation]    *set udp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_tp_src=\

COSSW-16262 验证modify项tp_002
    [Documentation]    *set udp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_tp_dst=\  

COSSW-16263 验证modify项tp_003
    [Documentation]    *set udp_src udp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_tp_src=\    -mod_tp_dst=\      

COSSW-16264 验证modify项tp_004
    [Documentation]    *set tcp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    dl_type=\    nw_proto=6    -mod_tp_src=\   

COSSW-16265 验证modify项tp_005
    [Documentation]    *set tcp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    dl_type=\    nw_proto=6    -mod_tp_dst=\

COSSW-16266 验证modify项tp_006
    [Documentation]    *set tcp_src tcp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    dl_type=\    nw_proto=6    -mod_tp_src=\    -mod_tp_dst=\   

COSSW-16267 验证modify项tp_007
    [Documentation]    *set sctp_src to stream*
    [Tags]    nok    ovs not support
    验证ovs-hw-offload流量    fwd    ipv4    sctp    dl_type=\    nw_proto=132    -mod_tp_dst=\     

COSSW-16268 验证modify项tp_008
    [Documentation]    *set sctp_dst to stream*
    [Tags]    nok    ovs not support
    验证ovs-hw-offload流量    fwd    ipv4    sctp    dl_type=\    nw_proto=132    -mod_tp_dst=\

COSSW-16269 验证modify项tp_009
    [Documentation]    *set sctp_src sctp_dst to stream*
    [Tags]    nok    ovs not support
    验证ovs-hw-offload流量    fwd    ipv4    sctp    dl_type=\    nw_proto=132    -mod_tp_src=\    -mod_tp_dst=\ 

COSSW-16270 验证modify项tp+eth_001
    [Documentation]    *set l2_src and udp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_dl_src=\    -mod_tp_dst=\

COSSW-16271 验证modify项tp+eth_002
    [Documentation]    *set l2_dst and udp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_dl_dst=\    -mod_tp_dst=\

COSSW-16272 验证modify项tp+eth_003
    [Documentation]    *set l2_src and udp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_dl_src=\    -mod_tp_src=\

COSSW-16273 验证modify项tp+eth_004
    [Documentation]    *set l2_src and udp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_dl_dst=\    -mod_tp_src=\ 

COSSW-16274 验证modify项tp+eth_005
    [Documentation]    *set l2_src and udp_src and udp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_dl_src=\    -mod_dl_dst=\    -mod_tp_src=\

COSSW-16275 验证modify项tp+eth_006
    [Documentation]    *set l2_src and l2_dst and udp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_dl_src=\    -mod_dl_dst=\    -mod_tp_dst=\

COSSW-16276 验证modify项tp+eth_007
    [Documentation]    *set l2_src and l2_dst and udp_src and udp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_dl_src=\    -mod_dl_dst=\    -mod_tp_src=\    -mod_tp_dst=\

COSSW-16277 验证modify项tp+eth_008
    [Documentation]    *set l2_src and tcp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_dl_src=\    -mod_tp_dst=\

COSSW-16278 验证modify项tp+eth_009
    [Documentation]    *set l2_dst and tcp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_dl_dst=\    -mod_tp_dst=\

COSSW-16279 验证modify项tp+eth_010
    [Documentation]    *set l2_src and tcp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_dl_src=\    -mod_tp_src=\

COSSW-16280 验证modify项tp+eth_011
    [Documentation]    *set l2_dst and tcp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_dl_dst=\    -mod_tp_src=\ 

COSSW-16281 验证modify项tp+eth_012
    [Documentation]    *set l2_src l2_dst and tcp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp   nw_proto=6    dl_type=\    -mod_dl_src=\    -mod_dl_dst=\    -mod_tp_src=\

COSSW-16282 验证modify项tp+eth_013
    [Documentation]    *set l2_src l2_dst and tcp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_dl_src=\    -mod_dl_dst=\    -mod_tp_dst=\

COSSW-16283 验证modify项tp+eth_014
    [Documentation]    *set l2_src l2_dst tcp_src and tcp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_dl_src=\    -mod_dl_dst=\    -mod_tp_src=\    -mod_tp_dst=\
    
COSSW-16284 验证modify项tp+ipv4_001
    [Documentation]    *set l3_src and udp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_tp_src=\          

COSSW-16285 验证modify项tp+ipv4_002
    [Documentation]    *set l3_dst and udp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_dst=\    -mod_tp_src=\ 

COSSW-16286 验证modify项tp+ipv4_003
    [Documentation]    *set l3_src and udp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_tp_dst=\          

COSSW-16287 验证modify项tp+ipv4_004
    [Documentation]    *set l3_dst and udp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_dst=\    -mod_tp_dst=\ 

COSSW-16288 验证modify项tp+ipv4_005
    [Documentation]    *set l3_src l3_dst and udp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\     -mod_tp_src=\ 

COSSW-16289 验证modify项tp+ipv4_006
    [Documentation]    *set l3_src l3_dst and udp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\     -mod_tp_dst=\    

COSSW-16290 验证modify项tp+ipv4_007
    [Documentation]    *set l3_src l3_dst udp_src and udp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\     -mod_tp_src=\    -mod_tp_dst=\        

COSSW-16291 验证modify项tp+ipv4_008
    [Documentation]    *set l3_src and tcp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_tp_src=\          

COSSW-16292 验证modify项tp+ipv4_009
    [Documentation]    *set l3_dst and tcp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_dst=\    -mod_tp_src=\ 

COSSW-16293 验证modify项tp+ipv4_010
    [Documentation]    *set l3_src and tcp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_tp_dst=\          

COSSW-16294 验证modify项tp+ipv4_011
    [Documentation]    *set l3_dst and tcp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_dst=\    -mod_tp_dst=\ 

COSSW-16295 验证modify项tp+ipv4_012
    [Documentation]    *set l3_src l3_dst and tcp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\     -mod_tp_src=\ 

COSSW-16296 验证modify项tp+ipv4_013
    [Documentation]    *set l3_src l3_dst and tcp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\     -mod_tp_dst=\    

COSSW-16297 验证modify项tp+ipv4_014
    [Documentation]    *set l3_src l3_dst tcp_src and tcp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\     -mod_tp_src=\    -mod_tp_dst=\ 

COSSW-16298 验证modify项tp+eth+ipv4_001 
    [Documentation]    *set l2_src l3_src and udp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_dl_src=\    -mod_tp_src=\

COSSW-16299 验证modify项tp+eth+ipv4_002
    [Documentation]    *set l2_dst l3_src and udp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_dl_dst=\    -mod_tp_src=\

COSSW-16300 验证modify项tp+eth+ipv4_003
    [Documentation]    *set l2_src l3_dst and udp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_dst=\    -mod_dl_src=\    -mod_tp_src=\

COSSW-16301 验证modify项tp+eth+ipv4_004
    [Documentation]    *set l2_dst l3_dst and udp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_dst=\    -mod_dl_dst=\    -mod_tp_src=\

COSSW-16302 验证modify项tp+eth+ipv4_005
    [Documentation]    *set l2_src l3_dst and udp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_dl_src=\    -mod_tp_dst=\

COSSW-16303 验证modify项tp+eth+ipv4_006
    [Documentation]    *set l2_dst l3_src and udp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_dl_dst=\    -mod_tp_dst=\

COSSW-16304 验证modify项tp+eth+ipv4_007
    [Documentation]    *set l2_src l3_dst and udp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_dst=\    -mod_dl_src=\    -mod_tp_dst=\

COSSW-16305 验证modify项tp+eth+ipv4_008
    [Documentation]    *set l2_dst l3_dst and udp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_dst=\    -mod_dl_dst=\    -mod_tp_dst=\

COSSW-16306 验证modify项tp+eth+ipv4_009
    [Documentation]    *set l2_src l3_src l3_dst and udp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_src=\    -mod_tp_src=\

COSSW-16307 验证modify项tp+eth+ipv4_010
    [Documentation]    *set l2_dst l3_src l3_dst and udp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_dst=\    -mod_tp_src=\

COSSW-16308 验证modify项tp+eth+ipv4_011
    [Documentation]    *set l2_src l3_src l3_dst and udp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_src=\    -mod_tp_dst=\

COSSW-16309 验证modify项tp+eth+ipv4_012
    [Documentation]    *set l2_dst l3_src l3_dst and udp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_dst=\    -mod_tp_dst=\

COSSW-16310 验证modify项tp+eth+ipv4_013
    [Documentation]    *set l2_dst l3_src l3_dst udp_src and udp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_dst=\    -mod_tp_src=\    -mod_tp_dst=\

COSSW-16311 验证modify项tp+eth+ipv4_014
    [Documentation]    *set l2_src l3_src and tcp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_dl_src=\    -mod_tp_src=\

COSSW-16312 验证modify项tp+eth+ipv4_015
    [Documentation]    *set l2_dst l3_src and tcp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_dl_dst=\    -mod_tp_src=\

COSSW-16313 验证modify项tp+eth+ipv4_016
    [Documentation]    *set l2_src l3_dst and tcp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_dst=\    -mod_dl_src=\    -mod_tp_src=\

COSSW-16314 验证modify项tp+eth+ipv4_017
    [Documentation]    *set l2_dst l3_dst and tcp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_dst=\    -mod_dl_dst=\    -mod_tp_src=\

COSSW-16315 验证modify项tp+eth+ipv4_018
    [Documentation]    *set l2_src l3_src and tcp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_dl_src=\    -mod_tp_dst=\

COSSW-16316 验证modify项tp+eth+ipv4_019
    [Documentation]    *set l2_dst l3_src and tcp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_dl_dst=\    -mod_tp_dst=\

COSSW-16317 验证modify项tp+eth+ipv4_020
    [Documentation]    *set l2_src l3_dst and tcp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_dst=\    -mod_dl_src=\    -mod_tp_dst=\

COSSW-16318 验证modify项tp+eth+ipv4_021
    [Documentation]    *set l2_dst l3_dst and tcp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_dst=\    -mod_dl_dst=\    -mod_tp_dst=\

COSSW-16319 验证modify项tp+eth+ipv4_022
    [Documentation]    *set l2_src l3_src l3_dst and tcp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_src=\    -mod_tp_src=\

COSSW-16320 验证modify项tp+eth+ipv4_023
    [Documentation]    *set l2_dst l3_src l3_dst and tcp_src to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_dst=\    -mod_tp_src=\

COSSW-16321 验证modify项tp+eth+ipv4_024
    [Documentation]    *set l2_src l3_src l3_dst and tcp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_src=\    -mod_tp_dst=\

COSSW-16322 验证modify项tp+eth+ipv4_025
    [Documentation]    *set l2_dst l3_src l3_dst and tcp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_dst=\    -mod_tp_dst=\

COSSW-16323 验证modify项tp+eth+ipv4_026
    [Documentation]    *set l2_dst l3_src l3_dst tcp_src and tcp_dst to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_dst=\    -mod_tp_src=\    -mod_tp_dst=\

COSSW-16324 验证modify项ttl_001
    [Documentation]    *set ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\    nw_proto=17    -mod_nw_ttl=\

COSSW-16325 验证modify项ttl_003
    [Documentation]    *dec ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\    nw_proto=17    -dec_ttl=\    

COSSW-16326 验证modify项ttl_006
    [Documentation]    *set and dec ipv4_ttl match udp to stream*
    [Tags]    nok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\    nw_proto=17    -mod_nw_ttl=\    -dec_ttl=\ 

COSSW-16327 验证modify项ttl+eth_001
    [Documentation]    *set l2_src and ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\    nw_proto=17    -mod_dl_src=\    -mod_nw_ttl=\

COSSW-16328 验证modify项ttl+eth_002
    [Documentation]    *set l2_src and dec ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\    nw_proto=17    -mod_dl_src=\    -dec_ttl=\

COSSW-16329 验证modify项ttl+eth_003
    [Documentation]    *set l2_dst and ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\    nw_proto=17    -mod_dl_dst=\    -mod_nw_ttl=\

COSSW-16330 验证modify项ttl+eth_004
    [Documentation]    *set l2_dst and dec ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\    nw_proto=17    -mod_dl_dst=\    -dec_ttl=\   

COSSW-16331 验证modify项ttl+eth_005
    [Documentation]    *set l2_src l2_dst and ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\    nw_proto=17    -mod_dl_src=\    -mod_dl_dst=\    -mod_nw_ttl=\  

COSSW-16332 验证modify项ttl+eth_006
    [Documentation]    *set l2_src l2_dst and dec ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\    nw_proto=17    -mod_dl_src=\    -mod_dl_dst=\    -dec_ttl=\  

COSSW-16333 验证modify项ttl+eth_015
    [Documentation]    *set l2_src l2_dst ipv4_ttl and dec ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\    nw_proto=17    -mod_dl_src=\    -mod_dl_dst=\    -mod_nw_ttl=\    -dec_ttl=\

COSSW-16334 验证modify项ttl+ipv4_001
    [Documentation]    *set l3_src and ipv4_ttl match udp to stream*
    [Tags]    ok  
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\    nw_proto=17    -mod_nw_src=\    -mod_nw_ttl=\

COSSW-16335 验证modify项ttl+ipv4_002
    [Documentation]    *set l3_src and dec ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\    nw_proto=17    -mod_nw_src=\    -dec_ttl=\

COSSW-16336 验证modify项ttl+ipv4_003
    [Documentation]    *set l3_dst and ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\    nw_proto=17    -mod_nw_dst=\    -mod_nw_ttl=\

COSSW-16337 验证modify项ttl+ipv4_004
    [Documentation]    *set l3_dst and dec ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\    nw_proto=17    -mod_nw_dst=\    -dec_ttl=\   

COSSW-16338 验证modify项ttl+ipv4_005
    [Documentation]    *set l3_src l3_dst and ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\    nw_proto=17    -mod_nw_src=\    -mod_nw_dst=\    -mod_nw_ttl=\  

COSSW-16339 验证modify项ttl+ipv4_006
    [Documentation]    *set l3_src l3_dst and dec ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\    nw_proto=17    -mod_nw_src=\    -mod_nw_dst=\    -dec_ttl=\  

COSSW-16340 验证modify项ttl+ipv4_007
    [Documentation]    *set l3_src l3_dst ipv4_ttl and dec ipv4_ttl match udp to stream*
    [Tags]    ok   
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\    nw_proto=17    -mod_nw_src=\    -mod_nw_dst=\    -mod_nw_ttl=\    -dec_ttl=\

COSSW-16341 验证modify项ttl+tp_001
    [Documentation]    *set tp_src and ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\    nw_proto=17    -mod_tp_src=\    -mod_nw_ttl=\ 

COSSW-16342 验证modify项ttl+tp_002
    [Documentation]    *set tp_src and dec ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\    nw_proto=17    -mod_tp_src=\    -dec_ttl=\

COSSW-16343 验证modify项ttl+tp_003
    [Documentation]    *set tp_dst and ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\    nw_proto=17    -mod_tp_dst=\    -mod_nw_ttl=\ 

COSSW-16344 验证modify项ttl+tp_004
    [Documentation]    *set tp_dst and dec ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\    nw_proto=17    -mod_tp_dst=\    -dec_ttl=\

COSSW-16345 验证modify项ttl+tp_005
    [Documentation]    *set tp_src tp_dst and ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\    nw_proto=17    -mod_tp_src=\    -mod_tp_dst=\    -mod_nw_ttl=\ 

COSSW-16346 验证modify项ttl+tp_006
    [Documentation]    *set tp_src tp_dst and dec ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\    nw_proto=17    -mod_tp_src=\    -mod_tp_dst=\    -dec_ttl=\

COSSW-16347 验证modify项ttl+eth+ipv4_001
    [Documentation]    *set l2_src l3_src and ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_dl_src=\    -mod_nw_ttl=\

COSSW-16348 验证modify项ttl+eth+ipv4_002
    [Documentation]    *set l2_dst l3_src and ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_dl_dst=\    -mod_nw_ttl=\

COSSW-16349 验证modify项ttl+eth+ipv4_003
    [Documentation]    *set l2_src l3_dst and ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_dst=\    -mod_dl_src=\    -mod_nw_ttl=\

COSSW-16350 验证modify项ttl+eth+ipv4_004
    [Documentation]    *set l2_dst l3_dst and ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_dst=\    -mod_dl_dst=\    -mod_nw_ttl=\

COSSW-16351 验证modify项ttl+eth+ipv4_005
    [Documentation]    *set l2_src l3_src and dec ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_dl_src=\    -dec_ttl=\

COSSW-16352 验证modify项ttl+eth+ipv4_006
    [Documentation]    *set l2_dst l3_src and dec ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_dl_dst=\    -dec_ttl=\

COSSW-16353 验证modify项ttl+eth+ipv4_007
    [Documentation]    *set l2_src l3_src and dec ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_dst=\    -mod_dl_src=\    -dec_ttl=\

COSSW-16354 验证modify项ttl+eth+ipv4_008
    [Documentation]    *set l2_dst l3_dst and dec ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_dst=\    -mod_dl_dst=\    -dec_ttl=\

COSSW-16355 验证modify项ttl+eth+ipv4_009
    [Documentation]    *set l2_src l3_src l3_dst and ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_src=\    -mod_nw_ttl=\

COSSW-16356 验证modify项ttl+eth+ipv4_010
    [Documentation]    *set l2_dst l3_src l3_dst and ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_dst=\    -mod_nw_ttl=\

COSSW-16357 验证modify项ttl+eth+ipv4_011
    [Documentation]    *set l2_src l3_src l3_dst and dec ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_src=\    -dec_ttl=\

COSSW-16358 验证modify项ttl+eth+ipv4_012
    [Documentation]    *set l2_dst l3_src l3_dst and dec ipv4_ttl match udp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_dst=\    -dec_ttl=\

COSSW-16359 验证modify项ttl+eth+ipv4_013
    [Documentation]    *set l2_dst l3_src l3_dst ipv4_ttl and dec ipv4_ttl match udp to stream*
    [Tags]    ok    
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_dst=\    -mod_nw_ttl=\    -dec_ttl=\

COSSW-16360 验证modify项ttl+eth+ipv4_0131
    [Documentation]    *set l2_src l3_src l3_dst ipv4_ttl and dec ipv4_ttl match udp to stream*
    [Tags]    ok    
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_src=\    -mod_nw_ttl=\    -dec_ttl=\

COSSW-16361 验证modify项ttl+eth+ipv4_0132
    [Documentation]    *set l2_src l2_dst l3_src l3_dst ipv4_ttl and dec ipv4_ttl match udp to stream*
    [Tags]    ok    
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_src=\    -mod_dl_dst=\    -mod_nw_ttl=\    -dec_ttl=\          

COSSW-16362 验证modify项ttl+eth+ipv4_014
    [Documentation]    *set l2_src l3_src and ipv4_ttl match tcp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_dl_src=\    -mod_nw_ttl=\

COSSW-16363 验证modify项ttl+eth+ipv4_015
    [Documentation]    *set l2_dst l3_src and ipv4_ttl match tcp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_dl_dst=\    -mod_nw_ttl=\

COSSW-16364 验证modify项ttl+eth+ipv4_016
    [Documentation]    *set l2_src l3_dst and ipv4_ttl match tcp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_dst=\    -mod_dl_src=\    -mod_nw_ttl=\

COSSW-16365 验证modify项ttl+eth+ipv4_017
    [Documentation]    *set l2_dst l3_dst and ipv4_ttl match tcp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_dst=\    -mod_dl_dst=\    -mod_nw_ttl=\

COSSW-16366 验证modify项ttl+eth+ipv4_018
    [Documentation]    *set l2_src l3_src and dec ipv4_ttl match tcp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_dl_src=\    -dec_ttl=\

COSSW-16367 验证modify项ttl+eth+ipv4_019
    [Documentation]    *set l2_dst l3_src and dec ipv4_ttl match tcp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_dl_dst=\    -dec_ttl=\

COSSW-16368 验证modify项ttl+eth+ipv4_020
    [Documentation]    *set l2_src l3_dst and dec ipv4_ttl match tcp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_dst=\    -mod_dl_src=\    -dec_ttl=\

COSSW-16369 验证modify项ttl+eth+ipv4_021
    [Documentation]    *set l2_dst l3_dst and dec ipv4_ttl match tcp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_dst=\    -mod_dl_dst=\    -dec_ttl=\

COSSW-16370 验证modify项ttl+eth+ipv4_022
    [Documentation]    *set l2_dst l3_src l3_dst and ipv4_ttl match tcp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_src=\    -mod_nw_ttl=\

COSSW-16371 验证modify项ttl+eth+ipv4_023
    [Documentation]    *set l2_dst l3_src l3_dst and ipv4_ttl match tcp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_dst=\    -mod_nw_ttl=\

COSSW-16372 验证modify项ttl+eth+ipv4_024
    [Documentation]    *set l2_dst l3_src l3_dst and dec ipv4_ttl match tcp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_src=\    -dec_ttl=\

COSSW-16373 验证modify项ttl+eth+ipv4_025
    [Documentation]    *set l2_dst l3_src l3_dst ipv4_ttl and dec ipv4_ttl match tcp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_dst=\    -dec_ttl=\

COSSW-16374 验证modify项ttl+eth+ipv4_026
    [Documentation]    *set l2_dst l3_src l3_dst ipv4_ttl and dec ipv4_ttl match tcp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_dst=\    -mod_nw_ttl=\    -dec_ttl=\

COSSW-16375 验证modify项ttl+eth+ipv4_027
    [Documentation]    *set l2_src l2_dst l3_src l3_dst ipv4_ttl and dec ipv4_ttl match tcp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_src=\    -mod_dl_dst=\    -mod_nw_ttl=\    -dec_ttl=\

COSSW-16376 验证modify项ttl+eth+ipv4_028
    [Documentation]    *set l2_src l2_dst l3_src l3_dst ipv4_ttl and dec ipv4_ttl match tcp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_nw_src=\    -mod_nw_dst=\    -mod_dl_src=\    -mod_dl_dst=\    -mod_nw_ttl=\    -dec_ttl=\

COSSW-16377 验证modify项ttl+eth+tp_001
    [Documentation]    *set l2_src udp_src and ipv4_ttl to stream*
    [Tags]    ok    
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_tp_src=\    -mod_dl_src=\    -mod_nw_ttl=\

COSSW-16378 验证modify项ttl+eth+tp_002
    [Documentation]    *set l2_dst udp_src and ipv4_ttl to stream*
    [Tags]    ok 
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_tp_src=\    -mod_dl_dst=\    -mod_nw_ttl=\

COSSW-16379 验证modify项ttl+eth+tp_003
    [Documentation]    *set l2_src udp_dst and ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_tp_dst=\    -mod_dl_src=\    -mod_nw_ttl=\

COSSW-16380 验证modify项ttl+eth+tp_004
    [Documentation]    *set l2_dst udp_dst and ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_tp_dst=\    -mod_dl_dst=\    -mod_nw_ttl=\

COSSW-16381 验证modify项ttl+eth+tp_005
    [Documentation]    *set l2_src udp_src and dec ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_tp_src=\    -mod_dl_src=\    -dec_ttl=\

COSSW-16382 验证modify项ttl+eth+tp_006
    [Documentation]    *set l2_dst udp_src and dec ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_tp_src=\    -mod_dl_dst=\    -dec_ttl=\

COSSW-16383 验证modify项ttl+eth+tp_007
    [Documentation]    *set l2_src udp_dst and dec ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_tp_dst=\    -mod_dl_src=\    -dec_ttl=\

COSSW-16384 验证modify项ttl+eth+tp_008
    [Documentation]    *set l2_dst udp_dst and dec ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_tp_dst=\    -mod_dl_dst=\    -dec_ttl=\

COSSW-16385 验证modify项ttl+eth+tp_009
    [Documentation]    *set l2_src udp_src udp_dst and ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_tp_src=\    -mod_tp_dst=\    -mod_dl_src=\    -mod_nw_ttl=\

COSSW-16386 验证modify项ttl+eth+tp_010
    [Documentation]    *set l2_dst udp_src udp_dst and ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_tp_src=\    -mod_tp_dst=\    -mod_dl_dst=\    -mod_nw_ttl=\

COSSW-16387 验证modify项ttl+eth+tp_011
    [Documentation]    *set l2_src udp_src udp_dst and dec ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_tp_src=\    -mod_tp_dst=\    -mod_dl_src=\    -dec_ttl=\

COSSW-16388 验证modify项ttl+eth+tp_012
    [Documentation]    *set l2_dst udp_src udp_dst and dec ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_tp_src=\    -mod_tp_dst=\    -mod_dl_dst=\    -dec_ttl=\

COSSW-16389 验证modify项ttl+eth+tp_0133
    [Documentation]    *set l2_dst udp_src udp_dst ipv4_ttl and dec ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_tp_src=\    -mod_tp_dst=\    -mod_dl_dst=\    -mod_nw_ttl=\    -dec_ttl=\

COSSW-16390 验证modify项ttl+eth+tp_0131
    [Documentation]    *set l2_dst udp_src udp_dst ipv4_ttl and dec ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_tp_src=\    -mod_tp_dst=\    -mod_dl_src=\   -mod_dl_dst=\    -mod_nw_ttl=\    -dec_ttl=\    

COSSW-16391 验证modify项ttl+eth+tp_014
    [Documentation]    *set l2_src tcp_src and ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_tp_src=\    -mod_dl_src=\    -mod_nw_ttl=\

COSSW-16392 验证modify项ttl+eth+tp_015
    [Documentation]    *set l2_dst tcp_src and ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_tp_src=\    -mod_dl_dst=\    -mod_nw_ttl=\

COSSW-16393 验证modify项ttl+eth+tp_016 
    [Documentation]    *set l2_src tcp_dst and ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_tp_dst=\    -mod_dl_src=\    -mod_nw_ttl=\

COSSW-16394 验证modify项ttl+eth+tp_017
    [Documentation]    *set l2_dst tcp_dst and ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_tp_dst=\    -mod_dl_dst=\    -mod_nw_ttl=\

COSSW-16395 验证modify项ttl+eth+tp_018
    [Documentation]    *set l2_src tcp_src and dec ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_tp_src=\    -mod_dl_src=\    -dec_ttl=\

COSSW-16396 验证modify项ttl+eth+tp_019
    [Documentation]    *set l2_dst tcp_src and dec ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_tp_src=\    -mod_dl_dst=\    -dec_ttl=\

COSSW-16397 验证modify项ttl+eth+tp_020
    [Documentation]    *set l2_src tcp_dst and dec ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_tp_dst=\    -mod_dl_src=\    -dec_ttl=\

COSSW-16398 验证modify项ttl+eth+tp_021
    [Documentation]    *set l2_dst tcp_dst and dec ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_tp_dst=\    -mod_dl_dst=\    -dec_ttl=\

COSSW-16399 验证modify项ttl+eth+tp_022
    [Documentation]    *set l2_src tcp_src tcp_dst and ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_tp_src=\    -mod_tp_dst=\    -mod_dl_src=\    -mod_nw_ttl=\

COSSW-16400 验证modify项ttl+eth+tp_023
    [Documentation]    *set l2_dst tcp_src tcp_dst and ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_tp_src=\    -mod_tp_dst=\    -mod_dl_dst=\    -mod_nw_ttl=\

COSSW-16401 验证modify项ttl+eth+tp_024
    [Documentation]    *set l2_src tcp_src tcp_dst and dec ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_tp_src=\    -mod_tp_dst=\    -mod_dl_src=\    -dec_ttl=\

COSSW-16402 验证modify项ttl+eth+tp_025
    [Documentation]    *set l2_dst tcp_src tcp_dst and dec ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_tp_src=\    -mod_tp_dst=\    -mod_dl_dst=\    -dec_ttl=\

COSSW-16403 验证modify项ttl+eth+tp_026
    [Documentation]    *set l2_src tcp_src tcp_dst ipv4_ttl and dec ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_tp_src=\    -mod_tp_dst=\    -mod_dl_dst=\    -mod_nw_ttl=\    -dec_ttl=\

COSSW-16404 验证modify项ttl+eth+tp_027
    [Documentation]    *set l2_src tcp_src tcp_dst ipv4_ttl and dec ipv4_ttl to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    tcp    nw_proto=6    dl_type=\    -mod_tp_src=\    -mod_tp_dst=\    -mod_dl_src=\    -mod_dl_dst=\    -mod_nw_ttl=\    -dec_ttl=\

COSSW-16405 验证modify项dscp_001
    [Documentation]    *set ipv4 dscp to stream*
    [Tags]    nok    ovs not support offload
    验证ovs-hw-offload流量    fwd    ipv4    0    dl_type=\    -set_field=16-\\>ip_dscp

COSSW-16406 验证modify项tos_001
    [Documentation]    *set ipv4 tos to stream*
    [Tags]    nok    ovs not support offload
    验证ovs-hw-offload流量    fwd    ipv4    0    dl_type=\    -mod_nw_tos=\  

COSSW-16407 验证modify项tos_002
    [Documentation]    *set ipv4 dscp match udp to stream*
    [Tags]    nok    ovs not support offload
    验证ovs-hw-offload流量    fwd    ipv4    udp    dl_type=\    nw_proto=17    -mod_nw_tos=\     

COSSW-16408 验证modify项vlan_001
    [Documentation]    *set vlan id to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_vlan_vid=\

COSSW-16409 验证modify项vlan_002
    [Documentation]    *set vlan pcp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_vlan_pcp=\

COSSW-16410 验证modify项vlan_003
    [Documentation]    *set vlan id and vlan pcp to stream*
    [Tags]    ok
    验证ovs-hw-offload流量    fwd    ipv4    udp    nw_proto=17    dl_type=\    -mod_vlan_vid=\    -mod_vlan_pcp=\   

*** Keywords ***
