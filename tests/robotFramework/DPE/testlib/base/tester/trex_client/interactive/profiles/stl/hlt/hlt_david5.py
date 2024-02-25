##### hltapi that can pass on 2.71 but fails on 2.82:
from trex.stl.trex_stl_hltapi import STLHltStream


class STLS1(object):

    '''
    Example number 1 of using HLTAPI from David
    Creates 3 streams (imix) Eth/802.1Q/IP/TCP without VM
    '''


    def get_streams (self, direction = 0, **kwargs):
        #'''
        return STLHltStream(
                #enable_auto_detect_instrumentation = '1', # not supported yet
                flow_stats_id = 88,
                ip_ttl =  255,
                ipv6_dst_addr = '2002:aaaa::2',
                ipv6_dst_count = 1,
                ipv6_dst_mode = 'increment',
                ipv6_dst_step = '0::1',
                ipv6_src_addr = '2002:aaaa::1',
                ipv6_src_count = '1',
                ipv6_src_mode = 'increment',
                ipv6_src_step = '0::1',
                l3_length = 110,
                l3_protocol = 'ipv6',
                #length_mode = 'fixed',
                length_mode = 'imix',
                mac_dst = '0000.aaaa.aaaa',
                mac_dst_mode = 'fixed',
                mac_src = '0000.bbbb.bbbb',
                mac_src_mode = 'fixed',
                pkts_per_burst = 200000,
                rate_percent = 1.25,
                transmit_mode = 'continuous',
                direction = direction,
                )

        '''
        return STLHltStream(
                frame_size = 1000,
                length_mode = 'fixed',
                rate_percent = 0.001,
                transmit_mode = 'continuous',
                l3_protocol = 'ipv4',
                l4_protocol = 'udp',
                )
        '''

# dynamic load - used for trex console or simulator

def register():
    return STLS1()