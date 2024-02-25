# !!! Auto-generated code !!!
from trex.stl.api import *

class STLS1(object):
    def get_streams(self, direction = 0, **kwargs):
        streams = []
        packet = (Ether(type=34525,dst='00:00:aa:aa:aa:aa',src='00:00:bb:bb:bb:bb') / 
                  IPv6(src='2002:aaaa::1',dst='2002:aaaa::2',plen=6) / 
                  Raw(load=b'!' * 6))
        vm = STLVM()
        stream = STLStream(packet = STLPktBuilder(pkt = packet, vm = vm),
                           flow_stats = STLFlowStats(88),
                           mac_src_override_by_pkt = True,
                           mac_dst_override_mode = 1,
                           mode = STLTXCont(percentage = 0.16384306732055284))
        streams.append(stream)
        packet = (Ether(type=34525,dst='00:00:aa:aa:aa:aa',src='00:00:bb:bb:bb:bb') / 
                  IPv6(src='2002:aaaa::1',dst='2002:aaaa::2',plen=512) / 
                  Raw(load=b'!' * 512))
        vm = STLVM()
        stream = STLStream(packet = STLPktBuilder(pkt = packet, vm = vm),
                           flow_stats = STLFlowStats(88),
                           mac_src_override_by_pkt = True,
                           mac_dst_override_mode = 1,
                           mode = STLTXCont(percentage = 0.6576014266607223))
        streams.append(stream)
        packet = (Ether(type=34525,dst='00:00:aa:aa:aa:aa',src='00:00:bb:bb:bb:bb') / 
                  IPv6(src='2002:aaaa::1',dst='2002:aaaa::2',plen=1460) / 
                  Raw(load=b'!' * 1460))
        vm = STLVM()
        stream = STLStream(packet = STLPktBuilder(pkt = packet, vm = vm),
                           flow_stats = STLFlowStats(88),
                           mac_src_override_by_pkt = True,
                           mac_dst_override_mode = 1,
                           mode = STLTXCont(percentage = 0.42855550601872494))
        streams.append(stream)

        return streams

def register():
    return STLS1()

