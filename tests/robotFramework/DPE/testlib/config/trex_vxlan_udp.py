from trex_stl_lib.api import *
import argparse

class STLS1(object):

    def __init__ (self):
        pass;
    
    def create_stream (self, packet_len, stream_count):
        base_pkt = Ether()/IP(src="16.0.0.1",dst="48.0.0.1")/UDP(sport=1337,dport=4789)/VXLAN(vni=42)/Ether()/IP()/('x'*20)
        base_pkt_len = len(base_pkt)
        base_pkt /= 'x' * max(0, packet_len - base_pkt_len)
        packets = []
        for i in range(stream_count):
            packets.append(STLStream(
                packet = STLPktBuilder(pkt = base_pkt),
                mode = STLTXCont()
                ))
        return packets


    def get_streams (self, tunables, **kwargs):
        parser = argparse.ArgumentParser(description='Argparser for {}'.format(os.path.basename(__file__)), 
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument('--packet_len',
                            type=int,
                            default=128,
                            help="The packets length in the stream")
        parser.add_argument('--stream_count',
                            type=int,
                            default=1,
                            help="The number of streams")
        args = parser.parse_args(tunables)
        # create 1 stream 
        return self.create_stream(args.packet_len - 4, args.stream_count)

def register():
    return STLS1()



