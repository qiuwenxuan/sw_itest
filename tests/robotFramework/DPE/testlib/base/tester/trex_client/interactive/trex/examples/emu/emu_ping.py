#!/usr/bin/python
import emu_path

from trex.emu.api import *

import argparse
import pprint
import time

EMU_SERVER = "localhost"

c = EMUClient(server=EMU_SERVER,
                sync_port=4510,
                verbose_level= "error",
                logger=None,
                sync_timeout=None)

# load profile
parser = argparse.ArgumentParser(description='Simple script to run EMU profile.')
parser.add_argument("-f", "--file", required = True, dest="file", help="Python file with a valid EMU profile.")
args = parser.parse_args()

c.connect()
print("connect")

print("loading profile from: %s" % args.file)

# start the emu profile using tunables
cl=80000
c.load_profile(profile = args.file, tunables = ["--clients={}".format(cl), "--ns=2"])

# print tables of namespaces and clients
print("Current ns and clients:")

ns_key = EMUNamespaceKey(vport  = 0,
                         tci     = [0, 0],
                        tpid    = [0x00, 0x00])
mac = Mac('00:00:00:70:00:03')
c_key=EMUClientKey(ns_key, mac[0].V())

#time.sleep(2)
#c.print_all_ns_clients(max_ns_show = 1, max_c_show = 10)
time.sleep(2)
iter=0
while True:
    print(" inter {} \n".format(iter))   
    iter=iter+1
    for i in range (0,cl):
        c_key=EMUClientKey(ns_key, mac[i].V())
        #dst=Ipv4("2.2.2.3")[i].V()
        success, err = c.icmp.start_ping(c_key=c_key, amount=2000, payload_size=1300, pace=12000.0)
        print(i)
    time.sleep(1)
    for i in range (0,min(10,cl)):
        c_key=EMUClientKey(ns_key, mac[i].V())
        r = c.icmp.get_ping_stats(c_key=c_key,zero=True)
        if i==0:
           pprint.pprint(r)
    time.sleep(5)

while True: 
    time.sleep(1)


# removing profile
print("Removing profile..")
c.remove_all_clients_and_ns()

# print tables of namespaces and clients after removal
print("After removal ns and clients:")
#c.print_all_ns_clients(max_ns_show = 1, max_c_show = 10)
