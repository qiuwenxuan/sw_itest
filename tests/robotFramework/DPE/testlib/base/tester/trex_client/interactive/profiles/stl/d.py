from trex.stl.api import *

class STLS1(object):
    def get_streams(self, direction = 0, **kwargs):
        streams = []
        packet = (Ether(dst='00:00:aa:aa:aa:aa',src='00:00:bb:bb:bb:bb',type=34525) / 
                  IPv6(plen=70,src='2002:aaaa::1',dst='2002:aaaa::2') / 
                  Raw(load=b'!' * 70))
        packet.show()
        hexdump(packet)
        vm = STLVM()
        stream = STLStream(packet = STLPktBuilder(pkt = packet, vm = vm),
                           flow_stats = STLFlowStats(88),
                           mac_src_override_by_pkt = True,
                           mac_dst_override_mode = 1,
                           mode = STLTXCont(percentage = 1.25))
        streams.append(stream)

        return streams

def register():
    return STLS1()
