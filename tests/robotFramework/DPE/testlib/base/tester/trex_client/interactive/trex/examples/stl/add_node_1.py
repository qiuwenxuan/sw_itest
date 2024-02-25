import stl_path
from trex.stl.api import *
import pprint


#verbose_level = 'debug'
c = STLClient(server = "csi-kiwi-02")
c.connect()

my_ports=[0,1]
c.acquire(ports=my_ports, force=True)
pkt = STLPktBuilder(pkt = Ether()/IP(src="16.0.0.1",dst="48.0.0.1")/UDP(dport=12,sport=1025)/IP()/'a_payload_example')
total_pkts = 100
s1 = STLStream(name = 'rx',
                packet = pkt,
                flow_stats = STLFlowStats(pg_id = 5),
                mode = STLTXSingleBurst(total_pkts = total_pkts,
                                        percentage = 1))

# connect to server
c.connect()

tx_port =0
rx_port = 1
# prepare our ports
c.reset(ports = [tx_port, rx_port])

# add stream to port
c.add_streams(s1, ports = [tx_port])
c.start(ports=tx_port, duration=10)
print("after start")
c.wait_on_traffic(ports=[tx_port], rx_delay_ms=10000)
print("DONE!")
pprint.pprint(c.get_stats(sync_now=True))

c.disconnect()

# print the results
