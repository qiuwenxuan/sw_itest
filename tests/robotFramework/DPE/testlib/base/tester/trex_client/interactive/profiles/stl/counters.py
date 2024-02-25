from  scapy.all import *
from scapy.contrib.mpls import * # import from contrib folder of scapy 
from trex.stl.trex_stl_streams import STLStream, STLTXSingleBurst, STLFlowStats
from trex.stl.trex_stl_packet_builder_scapy import STLPktBuilder

class STLS1(object):

    def get_streams (self, tunables=None, port_id=None, direction = 0):

        src_mac = "44:01:00:6b:00:04"
        dst_mac = "44:04:00:6b:00:04"
        src_ip = "10.80.169.24"
        dst_ip = "10.80.169.54"
        src_mac_mpls = "44:01:00:6b:00:04"
        dst_mac_mpls = "FF:04:00:6b:00:04"

        vlan=107

        if direction == 0:
            base_pkt = Ether(src=src_mac, dst=dst_mac)/Dot1Q(vlan=vlan)/IP(src=src_ip,dst=dst_ip)

            pkt_1 = base_pkt/UDP(dport=5001,sport=5000)
            pkt_2 = base_pkt/UDP(dport=5002,sport=5000)
            pkt_3 = Ether(src=src_mac_mpls,dst=dst_mac_mpls)/MPLS(label=17,cos=1,s=0,ttl=255)/MPLS(label=12,cos=1,s=1,ttl=12)/('x'*20)


            return [STLStream(packet = STLPktBuilder(pkt = pkt_1),
                              mode = STLTXSingleBurst( pps = 1000, total_pkts = 10),
                              flow_stats = STLFlowStats(pg_id = 1)),

                    STLStream(packet = STLPktBuilder(pkt = pkt_2),
                              mode = STLTXSingleBurst( pps = 1000, total_pkts = 10),
                              flow_stats = STLFlowStats(pg_id = 2)),

                    STLStream(packet = STLPktBuilder(pkt = pkt_3),
                              mode = STLTXSingleBurst( pps = 1000, total_pkts = 20),
                              )

                   ]
        else:
            base_pkt = Ether(src=dst_mac, dst=src_mac)/Dot1Q( vlan=vlan)/IP(src=dst_ip,dst=src_ip)

            pkt_1 = base_pkt/UDP(dport=5003,sport=5000)
            pkt_2 = base_pkt/UDP(dport=5004,sport=5000)

            return [STLStream(packet = STLPktBuilder(pkt = pkt_1),
                              mode = STLTXSingleBurst( pps = 1000, total_pkts = 10),
                              flow_stats = STLFlowStats(pg_id = 3)),

                    STLStream(packet = STLPktBuilder(pkt = pkt_2),
                              mode = STLTXSingleBurst( pps = 1000, total_pkts = 10),
                              flow_stats = STLFlowStats(pg_id = 4)),
                    
                    STLStream(packet = STLPktBuilder(pkt = pkt_3),
                              mode = STLTXSingleBurst( pps = 1000, total_pkts = 20))
                   ]
# dynamic load - used for trex console or simulator
def register():
    return STLS1()