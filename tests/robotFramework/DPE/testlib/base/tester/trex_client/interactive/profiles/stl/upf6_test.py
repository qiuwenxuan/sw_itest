import scapy.utils
from trex_stl_lib.api import *

class STLS1(object):

    def create_stream (self):
        raw = (Ether(src='00:25:90:eb:e8:ec', dst='0c:c4:7a:59:ab:7c', type=0x86dd) /
                IPv6(src="2001:420:380:dead:beef:d06:f001:2", dst="2001:420:380:dead:beef:d06:f002:2", tc=0, fl=0, nh=17) /
                UDP(sport=61, dport=2152) /
                Raw(b'\x24\xFF\x00\x04\x00\x00\x00\x9F') /
                Raw(b'\x00\x00\x00\x00\x01\x00\x84\x00') /
                IPv6(src="2002::1", dst="2002::2")/UDP() /
                Raw(10*'x')/Raw('1111111'))

#        print(scapy.utils.hexdump(raw))

        return STLStream( 
           packet = 
                    STLPktBuilder(
                        pkt = raw
                    ),
             mode = STLTXCont())

    def get_streams (self, direction = 0, **kwargs):
        # create 1 stream 
        return [ self.create_stream() ]


# dynamic load - used for trex console or simulator
def register():
    return STLS1()


