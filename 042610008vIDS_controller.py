# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.dpid import str_to_dpid
from ryu.lib.packet import ipv4
from ryu.lib.packet import tcp
from ryu.lib.packet import ipv6
from ryu.lib.packet import icmpv6
from ryu.lib.packet import arp
from ryu.lib import hub


from sklearn import tree
import pydotplus
import time
import socket

VFW1_DPID_FIELD = 0
VFW1_IPV6_BROADCAST_ADDRESS_FIELD = 1 
VFW1_INPORT_FIELD = 2 
VFW1_IPV6_SRC_ADDRESS_FIELD =  3

#(Step 3) only use IPv4 for co-brain with v4+v6_vIDS(client) send alert to v4_vIDS(server)
HOST = '192.168.0.12'#(ipv4.server's IP)
#HOST = '192.168.146.47'#(openstack.server's I[)
#HOST = 'fd17:625c:f037:2:9100:4aa2:4037:c34'
#HOST = '10.0.2.7'
PORT = 9876
ADDR = (HOST,PORT)
BUFSIZE = 4096
global timestart
timestart=1
global datapathv4
global ddos_buf
ddos_buf=500
####for RA START(Step 4) change to each tanent
str_ipv6_0 = {}
str_ipv6_0[1] = "fe80::f816:3eff:febe:181f" #vRouter's ipv6 link layer address
str_ipv6_0[2] = 60 #time slot ever RA send 
str_ipv6_0[3] = 6 #vRouter's port number coneect to vSwitch(static) 
str_ipv6_0[4] = "fa:16:3e:be:18:1f" #vRouter's MAC address(static)

str_ipv6_0[51] = "fe80::f816:3eff:fe6e:dfdf" #VM_1's ipv6 link later address
str_ipv6_0[52] = 5 #!!!!need to catch pre packet and compute the time slot by new one(default:5)!!!
str_ipv6_0[53] = 10 #VM_1's port number connect to vSwitch
str_ipv6_0[54] = "d2:0f:a0:09:83:4a" #VM_1's MAC address

str_ipv6_0[100]= "test:me"
str_ipv6_0[1000] = "default:random:ip:addr"
"""
!!!if time<30 goto str_ipv6_0[52],elif time>30 goto str_ipv6_0[2]


"""
mac_table = {}
mac_table[6]="fa:16:3e:be:18:1f"
mac_table[10]="d2:0f:a0:09:83:4a"
mac_table[14]="46:bf:dd:b1:ec:4b"#Step 15(for v4 net host)

listme=['ip_buf','time_buf','port_buf','mac_buf']
listname=['MITM','Router','fake','flood','flood_1','flood_2']

X = [ [1,2,3,4],
        [1,2,3,4],
        [1,2,3,4],
        [1,2,3,4],
        [1,2,3,4],

        [51,2,53,4],
        [51,52,53,4],
        [1,2,53,4],
        [1,52,53,4],
        [51,52,53,54],

        [51,2,53,4],
        [51,52,53,4],
        [1,2,53,4],
        [1,52,53,4],
        [51,52,53,54],

        [1,2,53,54],
        [1,2,53,54],
        [1,2,53,54],
        [1,2,53,54],
        [1,2,53,54],

        [1,2,53,1000],#default for random spoof RA
        [1,2,53,1000],
        [1000,2,53,1000],#static port other with random
        [1000,52,53,1000],
                ]

Y = ['Router','Router','Router','Router','Router',
        'fake','flood_1','fake','flood_2','flood',
        'fake','flood_1','fake','flood_2','flood',
        'MITM','MITM','MITM','MITM','MITM',
        'fake','fake','fake','fake',
        ]

list_array = [[1,2,3,4]]

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X,Y)

#prediction = clf.predict(list_array)


####for RA END


##tcp start(syn-flood,port scan) Step 18.0
str_ipv6_tcp = {}
str_ipv6_tcp[21] =  "fd49:6c67:8764:0:f816:3eff:fe6e:dfdf" #srcip
#str_ipv6_tcp[21] =  "fd17:625c:f037:2:a00:27ff:fedc:d3ca" #delete me test for vm

str_ipv6_tcp[20] =  20 #payload length
str_ipv6_tcp[23] =  10 #VM_1's port number coneect to vSwitch(static) 
str_ipv6_tcp[24] =   1#count for other ip
str_ipv6_tcp[50] =   1#count for 21

JY = [ [21,20,23,ddos_buf],#static src_ip for port scanning
        [21,20,23,ddos_buf],
        [21,20,23,ddos_buf],
        [21,20,23,ddos_buf],
        [21,20,23,ddos_buf],

        [600,20,23,ddos_buf],#random src for syn-flood
        [600,20,23,ddos_buf],
        [600,20,23,ddos_buf],
        [600,20,23,ddos_buf],
        [600,20,23,ddos_buf],

        [21,600,23,1],#normal length
        [21,600,23,2],
        [21,600,23,3],
        [21,600,23,2],
        [21,600,23,2],

	[600,20,600,5],
        [600,600,600,ddos_buf],
	[600,20,600,4],
        [600,600,600,ddos_buf],

	[21,20,23,2],
        [21,20,23,2],
        [21,20,23,1],
        [21,20,23,1],

                ]

EN = ['flood','flood','flood','flood','flood',
        'flood','flood','flood','flood','flood',
        'normal','normal','normal','normal','normal',
	'suspenious_tcp','suspenious_tcp','suspenious_tcp','suspenious_tcp',
        'normal','normal','normal','normal',
        ]

list_array = [[1,2,3,4]]

global clf_tcp
clf_tcp = tree.DecisionTreeClassifier()
clf_tcp = clf_tcp.fit(JY,EN)
##tcp end


####for RS STARTT(Step 6)
str_ipv6_1 = {}
str_ipv6_1[21] =  "fe80::f816:3eff:fe6e:dfdf" #VM_1's ipv6 link layer address
str_ipv6_1[22] =  1 #RS count(interface ip count) by VM_1 
str_ipv6_1[23] =  10 #VM_1's port number coneect to vSwitch(static) 
str_ipv6_1[24] =  "d2:0f:a0:09:83:4a" #vm_1's MAC address(static)

str_ipv6_1[51] = "fe80::f816:3eff:feed:52fb" #VM_2's ipv6 link later address
str_ipv6_1[52] = 1 #RS count(interface ip count) by VM_2
str_ipv6_1[53] = 9 #VM_2's port number connect to vSwitch
str_ipv6_1[54] = "fa:16:3e:ed:52:fb" #VM_2's MAC address

mac_table[9]="fa:16:3e:ed:52:fb"

A = [ [21,22,23,24],
        [21,22,23,24],
        [21,22,23,24],
        [21,22,23,24],
        [51,52,53,54],

        [51,52,53,54],
        [51,52,53,54],
        [51,52,53,54],
        [51,52,53,54],
        [51,52,53,54],

        [51,52,23,54],#vm1 spoof vm2(ful)
        [51,52,23,54],
        [21,22,53,24],#vm2 spoog vm1(ful)
        [21,22,53,24],
        [21,22,53,24],

        [51,52,23,24],#vm1 spoof vm2(ip spoof)
        [51,22,23,24],
        [21,22,53,54],#vm2 spoog vm1(ip spoof)
        [21,22,53,54],
        [51,52,53,500],#default spoof for random mac

        [21,22,23,500],#default spoof for random mac
        [500,22,23,500],
        [500,52,53,500],
	[500,52,53,54]
                ]

B = ['VM_1','VM_1','VM_1','VM_1','VM_2',
        'VM_2','VM_2','VM_2','VM_2','VM_2',
        'fake','fake','fake','fake','fake',
        'fake','fake','fake','fake','fake',
        'fake','fake','fake','fake',
        ]

clf_rs = tree.DecisionTreeClassifier()
clf_rs = clf_rs.fit(A,B)


####for RS END

####for NA START(Step 11 )
str_ipv6_2 = {}
str_ipv6_2[21] =  "fd49:6c67:8764:0:f816:3eff:fe6e:dfdf" #src_ipv6 for VM_1(target)
#str_ipv6_2[21] =  "fd17:625c:f037:2:89f4:606c:3280:756d" #delete me test for vm
str_ipv6_2[22] =  1# time dif -->NORMAL(less then 1 per 1s)
str_ipv6_2[23] =  10 #port for VM_1 at vSwitch 
str_ipv6_2[24] =  "d2:0f:a0:09:83:4a" #mac for VM_1
str_ipv6_2[25] =  "fe80::f816:3eff:fe6e:dfdf" #other ip2 accessable ipv6 for VM_1(target)
str_ipv6_2[26] =  "fd49:6c67:8764:0:9cd8:ba06:e941:eaf4"#other ip3
str_ipv6_2[27] =  0#pre packet count for VM_1(27 not mean anything)

str_ipv6_2[51] =  "fd49:6c67:8764:0:f816:3eff:feed:52fb" #src_ipv6 for 46_vIDS
str_ipv6_2[52] = 10 #" time dif for pre NS by each VM send"(need to setup each buffer to store time dif)-->MALWARE(more 10 packet per 1s)
str_ipv6_2[53] = 9 #46_vIDS's port number connect to vSwitch(static)
str_ipv6_2[54] =  "fa:16:3e:ed:52:fb" #mac for 46_vIDS
str_ipv6_2[55] = "fe80::f816:3eff:feed:52fb" #other ip2 accessable for VM_2(target)
str_ipv6_2[56] = 0#pre packet count for VM_2(56 not mean anything)

str_ipv6_2[101] =  "fe80::f816:3eff:febe:181f" #src_ipv6 for vRouter
str_ipv6_2[102] = 1 #" time dif for pre NS by each VM send"(need to setup each buffer to store time dif)-->MALWARE(more 10 packet per 1s)
str_ipv6_2[103] = 6 #vRouter's port number connect to vSwitch(static)
str_ipv6_2[104] =  "fa:16:3e:be:18:1f" #mac for router
str_ipv6_2[105] = 0#pre packet count for vRouter(105 not mean anything)

str_ipv6_2[100] =  "fd36:9a58:c865:0:f816:3eff:fea3:4bbb" #dest_ipv6 for VM_3
str_ipv6_2[150] =  "fd36:9a58:c865:0:f816:3eff:feb5:7895" #dest_ipv6 for VM_4
str_ipv6_2[200] =  "fd36:9a58:c865:0:f816:3eff:fea6:bba1" #dest_ipv6 for VM_5
str_ipv6_2[250] =  "fd36:9a58:c865:0:f816:3eff:fec1:56ff" #dest_ipv6 for VM_6
str_ipv6_2[350] =  "fd36:9a58:c865:0:f816:3eff:fea8:127b" #dest_ipv6 for VM_7

C = [ [21,23,24,21,1],#IP1 for VM_1
        [21,23,24,21,2],
        [21,23,24,21,3],
        [25,23,24,25,1],#IP2 for VM_1
        [25,23,24,25,2],

        [25,23,24,25,3],
        [26,23,24,26,1],#IP3 for VM_1
        [26,23,24,26,2],
        [26,23,24,26,3],
        [26,23,24,26,1],

        [51,53,54,51,1],#IP1 for VM_2
        [51,53,54,51,2],
        [51,53,54,51,3],
        [55,53,54,55,1],#IP2 for VM_2
        [55,53,54,55,2],

        [51,23,24,51,3],#VM_1 spoof ip1 by VM_2(Man-in-the-middle~)
        [51,23,24,51,2],
        [55,23,24,55,1],#VM_1 spoof ip2 by VM_2
        [55,23,24,55,2],
        [55,23,24,55,1],

        [21,53,54,21,3],#VM_2 spoof ip1 by VM_1
        [25,53,54,25,2],#VM_2 spoof ip2 by VM_1
        [26,53,54,26,1],#VM_2 spoof ip3 by VM_1
        [25,53,54,25,3],#VM_2 spoof ip2 by VM_1
        [26,53,54,26,3],

        [21,23,54,21,1],#VM_1 spoof  mac by VM_2(neighbor mac spoof attack~)
        [21,23,54,21,2],
        [51,53,24,51,2],#VM_2 spoof  mac by VM_1
        [51,53,24,51,2],

        [21,23,24,21,ddos_buf],#flood without spoof_mac  by VM_1(flood NA~)
        [21,23,24,21,ddos_buf],
        [25,23,24,25,ddos_buf],
        [25,23,24,25,ddos_buf],

        [26,23,24,26,ddos_buf],
        [26,23,24,26,ddos_buf],
        [51,53,54,51,ddos_buf],#flood without spoof_mac by VM_2
        [51,53,54,51,ddos_buf],

        [55,53,54,55,ddos_buf],
        [55,53,54,55,ddos_buf],
        [55,53,54,55,ddos_buf],
        [55,53,54,55,ddos_buf],

        [21,23,24,51,3],#target spoof by VM_1(NA target spoof~)
        [21,23,24,55,2],
        [26,23,24,51,1],
        [26,23,24,55,1],

        [25,23,24,51,1],
        [25,23,24,55,2],
        [25,23,24,51,1],
        [25,23,24,55,3],

        [21,23,24,51,2],
        [21,23,24,55,1],
        [26,23,24,51,1],
        [26,23,24,55,3],

        [51,53,54,21,1],#target spoof by VM_2
        [51,53,54,25,2],
        [51,53,54,26,3],

        [55,53,54,21,1],
        [55,53,54,25,2],
        [55,53,54,26,3],

        [51,53,54,21,2],
        [51,53,54,25,3],
        [51,53,54,26,4],

        [55,53,54,21,1],
        [55,53,54,25,2],
        [55,53,54,26,2],

        [1000,23,1000,1000,1],#random field only static match(port,time_dif)
        [1000,53,1000,1000,1000],
	[600,53,54,600,2],
	[600,23,24,600,3],

	[101,103,104,51,1],#router to inside(if vm want to talk to internet riseup)
	[101,103,104,55,1],
	[101,103,104,25,2],
	[101,103,104,25,2],

        [101,103,104,51,1],#router to inside(if vm want to talk to internet riseup)
        [101,103,104,55,1],
        [101,103,104,25,2],
        [101,103,104,25,2],	
                ]

D = ['VM_1','VM_1','VM_1','VM_1','VM_1',
        'VM_1','VM_1','VM_1','VM_1','VM_1',
        'VM_2','VM_2','VM_2','VM_2','VM_2',
        'spoof_srcIP_field','spoof_srcIP_field','spoof_srcIP_field','spoof_srcIP_field','spoof_srcIP_field',
        'spoof_srcIP_field','spoof_srcIP_field','spoof_srcIP_field','spoof_srcIP_field','spoof_srcIP_field',
        'spoof_mac_field','spoof_mac_field','spoof_mac_field','spoof_mac_field',
        'flood','flood','flood','flood',
        'flood','flood','flood','flood',
        'flood','flood','flood','flood',
        'spoof_target_field','spoof_target_field','spoof_target_field','spoof_target_field',
        'spoof_target_field','spoof_target_field','spoof_target_field','spoof_target_field',
        'spoof_target_field','spoof_target_field','spoof_target_field','spoof_target_field',
        'spoof_target_field','spoof_target_field','spoof_target_field',
        'spoof_target_field','spoof_target_field','spoof_target_field',
        'spoof_target_field','spoof_target_field','spoof_target_field',
        'spoof_target_field','spoof_target_field','spoof_target_field',
        'random_field_attack','random_field_attack',
	'random_field_attack','random_field_attack',
	'Router','Router','Router','Router',
        'Router','Router','Router','Router',

        ]

global clf_na
clf_na = tree.DecisionTreeClassifier()
clf_na = clf_na.fit(C,D)


####for NA END

####for NS START!!!!!!!watch me>>>>>>>>>because no specific port and no mac, NS this time is not correct!!!!!!!!!(Step 13)
str_ipv6_3 = {}
str_ipv6_3[21] =  "fd49:6c67:8764:0:f816:3eff:fe6e:dfdf" #src_ipv6 for VM_1
str_ipv6_3[22] =  1 #" time dif for pre NS by each VM send"(need to setup each buffer to store time dif)-->NORMAL
str_ipv6_3[23] =  10 #VM_1's port number coneect to vSwitch(static) 
#str_ipv6_3[24] =  "fd17:625c:f037:2:9cd2:a5c9:cd1:d66e" #dest_ipv6 for VM_2
str_ipv6_3[25] = "fe80::f816:3eff:fe6e:dfdf"#other access ip for vm_1(not dst)


str_ipv6_3[51] =  "fd49:6c67:8764:0:f816:3eff:feed:52fb" #src_ipv6 for VM_2
str_ipv6_3[52] = 10 #" time dif for pre NS by each VM send"(need to setup each buffer to store time dif)-->MALWARE(more 10 packet per 1s)
str_ipv6_3[53] = 9 #VM_2's port number connect to vSwitch(static)
#str_ipv6_3[54] =  "fd17:625c:f037:2:a00:27ff:fe2c:e664" #dest_ipv6 for VM_1
str_ipv6_3[55] = "fe80::f816:3eff:feed:52fb"#oher access ip for vm_2(not dst)


str_ipv6_3[101] =  "fe80::f816:3eff:febe:181f" #src_ipv6 for vRouter(if someone want to talk to internet)
str_ipv6_3[102] = 1 #" time dif for pre NS by each VM send"(need to setup each buffer to store time dif)-->MALWARE(more 10 packet per 1s)
str_ipv6_3[103] = 6 #VM_2's port number connect to vSwitch(static)
#str_ipv6_3[54] =  "fd17:625c:f037:2:a00:27ff:fe2c:e664" #dest_ipv6 for VM_1
str_ipv6_3[105] = "fd49:6c67:8764::1"

str_ipv6_3[0] = "::"

M = [ [21,22,23,51],
        [21,22,23,51],
        [21,22,23,51],
        [51,22,53,21],
        [51,22,53,21],

        [21,52,23,51],
        [51,52,53,21],
        [21,52,23,51],
        [51,52,53,21],
        [21,52,23,51],

        [51,22,23,51], #vm1 spoof vm2 with src_ip
        [21,22,53,21], #vm2 spoof vm1 with src_ip
        [600,22,23,51],#vm1 spoof random with src_ip
        [600,22,53,51],#vm2 spoof random with src_ip
        [600,22,23,51],

        [51,22,23,200], #vm1 spoof vm2 with src_ip
        [51,22,23,250], #vm2 spoof vm1 with src_ip
        [600,22,23,150],#vm1 spoof random with src_ip
        [600,22,53,250],#vm2 spoof random with src_ip
        [600,22,53,350],


        [21,22,23,100], #vm1 to inside with dst_ip
        [21,22,23,150],
        [21,22,23,200],
        [21,22,23,250],
        [21,22,23,350],

        [51,22,53,100], #vm2 to inside with dst_ip
        [51,22,53,150],
        [51,22,53,200],
        [51,22,53,250],
        [51,22,53,350],

        [21,22,23,3000], #black list for dst_ip from vm1
        [21,22,23,3000],
        [51,22,53,3000], #black list for dst_ip from vm2
        [51,22,53,3000],

        [21,22,23,2000], #default valid ip for  vm1
        [51,22,53,2000], #default valid ip for  vm2
        [0,22,23,21],#DAD check for vm1
        [0,22,53,51],#DAD check for vm2
        [0,22,23,21],
        [0,22,53,51],

        [0,22,23,21],
        [0,22,53,51],

	[25,22,23,55],
        [21,22,23,55],
        [25,22,23,55],
        [51,22,53,25],
        [55,22,53,25],

        [25,52,23,55],
        [55,52,53,25],
        [25,52,23,55],
        [55,52,53,25],
        [25,52,23,55],

        [55,22,23,600], #vm1 spoof vm2 with src_ip
        [25,22,53,600], #vm2 spoof vm1 with src_ip
	[51,22,23,600],
	[21,22,53,600],

	[101,22,103,21],
        [101,22,103,51],
        [101,22,103,55],
        [101,22,103,25],
        [101,22,103,21],

	[101,22,53,21],
	[101,22,53,25],
	[101,22,23,51],
	[101,22,23,55],
                ]

N = ['VM_1','VM_1','VM_1','VM_2','VM_2',
        'flood_attack','flood_attack','flood_attack','flood_attack','flood_attack',
        'spoofing','spoofing','spoofing','spoofing','spoofing',
        'spoofing','spoofing','spoofing','spoofing','spoofing',
        'VM_1','VM_1','VM_1','VM_1','VM_1',
        'VM_2','VM_2','VM_2','VM_2','VM_2',
        'black_list','black_list','black_list','black_list',
        'VM_1','VM_2','VM_1','VM_2','VM_1','VM_2',
        'VM_1','VM_2',
	'VM_1','VM_1','VM_1','VM_2','VM_2',
        'flood_attack','flood_attack','flood_attack','flood_attack','flood_attack',
        'spoofing','spoofing','spoofing','spoofing',
	'Router','Router','Router','Router','Router',
        'spoofing','spoofing','spoofing','spoofing',

        ]

clf_ns = tree.DecisionTreeClassifier()
clf_ns = clf_ns.fit(M,N)
####for NS END


####
buffer_pkt_ipv6 = {}
buffer_pkt_ipv6[20] = "fd17:a:suspicious:ipv6:discovery:20"
buffer_pkt_ipv6[11] = "fd17:a:suspicious:ipv6:discovery:11"






class SimpleSwitch13(app_manager.RyuApp):
	OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

	def __init__(self, *args, **kwargs):
		super(SimpleSwitch13, self).__init__(*args, **kwargs)
		self.mac_to_port = {}
		self.vfw1_table = {}
        	self.monitor_thread = hub.spawn(self._monitor)
		self.timer = hub.spawn(self._timer)
		self.check=True


####When VM reboot,its IPv6 link local addr and ipv6 addr maybe change
 

#		self.vfw1_table[VFW1_DPID_FIELD]=8796760270169
		self.vfw1_table[VFW1_DPID_FIELD]=8796761805770
		self.vfw1_table[VFW1_IPV6_BROADCAST_ADDRESS_FIELD]="fe80::f048:f9ff:fe16:c432"
		self.vfw1_table[VFW1_INPORT_FIELD]=1
		self.vfw1_table[VFW1_IPV6_SRC_ADDRESS_FIELD]="fd17:625c:f037:2:603d:a187:cf45:e56"
####



#######send START
##(Step 2) change for AF_INET6 for IPv6(AF_INET for IPv4)
        def _alert_features(self,in_port,src,attack_type,icmpv6,PV):

		f = open('alert.txt','a')


#		learn=[1,2,3,4]
#		type_learn="VM_1"


		learn=[in_port,src,icmpv6,PV]
		type_learn=str(attack_type)

		f.write(type_learn)
		f.write('\t')

		for i in range(0,len(learn)):
        		f.write(str(learn[i]))
	      		f.write(',')


		f.close()


		bytes = open("alert.txt").read()

		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		client.connect(ADDR)
		client.send(bytes)#bytes
		
		
		client.close()
		print ""
#		self._re_trainning(f_list,f_type)

#######send END

###self learning tcp START Step 18.1
        def _self_learning_tcp(self,datapath,srcip6,in_port,payload_len,tcp_port_count):
                self.logger.info("TCP ML Detect Now!!!!")
                print "srcip:",srcip6,", port:",in_port,", payload_len:",payload_len,", tcp_port_count",tcp_port_count
		ofproto = datapath.ofproto
                parser = datapath.ofproto_parser
                ipbuf = 0
                in_portbuf = 0
                payload_lenbuf = 0
		tcp_port_countbuf = 0
                if srcip6 == str_ipv6_tcp[21]:
                        ipbuf=21
                else:
                        ipbuf=600

		if in_port == str_ipv6_tcp[23]:
			in_portbuf=23
		else:
			in_portbuf=600

		if payload_len == str_ipv6_tcp[20]:
			payload_lenbuf=20
		else:
			payload_lenbuf=600

#		if tcp_port_count == 24:
#			tcp_port_countbuf=24
#		else:
#			tcp_port_countbuf =50

		print ipbuf,payload_lenbuf,in_portbuf,tcp_port_count
                list_array=[[ipbuf,payload_lenbuf,in_portbuf,tcp_port_count]]####feed me test(Step 6) stay normal

                print list_array

                prediction = clf_tcp.predict(list_array)
		print prediction

                for i in range(0,len(list_array)): #len is 5
                        if prediction[i:i+1] == 'normal':
                        	print "stat[1]: normal TCP catch:",srcip6
			else:
				match = parser.OFPMatch(eth_type=0x086dd,ip_proto=6)
                                actions = []
                                inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
                                self.add_flow(datapath, 100, match, actions, inst)

                                while(self.check):
					global timestart
					timestart=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())	
                                        self._alert_features(in_port,mac_table[in_port],prediction,3,6)
					self._re_trainning(list_array,prediction[i:i+1],6)
					self.check=False
###self learning tcp end


###self learning ra START(Step 5) continue Step 4.
	def _self_learning_ra(self,datapath,srcip6,in_port,src):
		self.logger.info("RA ML Detect Now!!!!")
		print "srcip:",srcip6,", port:",in_port,", mac:",src

		ofproto = datapath.ofproto
                parser = datapath.ofproto_parser
		ipbuf = 0
		in_portbuf = 0
		srcbuf = 0
		if srcip6 == str_ipv6_0[1]:
			ipbuf=1
		else:
			ipbuf=51
		if in_port == str_ipv6_0[3]:
			in_portbuf = 3
		else:
			in_portbuf=53		
		if src == str_ipv6_0[4]:
			srcbuf=4
		elif src == str_ipv6_0[54]:
			srcbuf=54
		else:
			str_ipv6_0[1000]=src
			srcbuf=1000
		print "number",ipbuf,"2",in_portbuf,srcbuf
		list_array=[[ipbuf,2,in_portbuf,srcbuf]]####feed me test(Step 6) stay normal

		print list_array

		prediction = clf.predict(list_array)

#test1start
#		prediction[0:1] = 'flood_2'
#test2end
		for i in range(0,len(list_array)): #len is 5
        		print ""
        		print "input(ipv6,time,port,mac) : ",',ipv6:',srcip6,',time:',',port:',in_port,',mac:',src

        		point = int(list_array[i][0])
        		point_2=int(list_array[i][2])
        		if prediction[i:i+1] == 'Router':
                        	print "stat[1]: normal RA catch:",srcip6
        		elif prediction[i:i+1] == 'fake':##normal ra stay here
                        	print "stat[1]: ipv6 [kill_router6] attack, [suspenseful] alert:",mac_table[in_port]
                        	print "at port:",in_port

#hit                        	match = parser.OFPMatch(in_port=in_port)
#hit                       		actions = []
#hit                        	inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
#hit                        	self.add_flow(datapath, 50, match, actions, inst)

#disable me if on openstack env(start)
                                match = parser.OFPMatch(eth_type=0x086dd,ip_proto=58,icmpv6_type=134)
                                actions = []
                                inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
                                self.add_flow(datapath, 100, match, actions, inst)
#disable me if on openstack env(en)


				while(self.check):#(Step 9) add co-brain function
                                        self._alert_features(in_port,mac_table[in_port],prediction,3,134)
                                        self.check=False

        		elif prediction[i:i+1] == 'flood_1':
                        	print "stat[2]: ipv6 [bad prefix length] attack: spoofing random RA with flooding attack,[attack] alert:",mac_table[in_port]
                        	print "at port:",in_port

                                match = parser.OFPMatch(eth_type=0x086dd,ip_proto=58,icmpv6_type=134)
                                actions = []
                                inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
                                self.add_flow(datapath, 100, match, actions, inst)


				while(self.check):
                                        self._alert_features(in_port,mac_table[in_port],prediction,3,134)
                                        self.check=False

        		elif prediction[i:i+1] == 'flood_2':
                        	print "stat[3]: spoofing router's RA with flooding attack:",mac_table[in_port]
                        	print "at port:",in_port
#test2start
				match = parser.OFPMatch(eth_type=0x086dd,ip_proto=58,icmpv6_type=134)
				actions = []
				inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
				self.add_flow(datapath, 100, match, actions, inst)
#test2end

				while(self.check):
                                        self._alert_features(in_port,mac_table[in_port],prediction,3,134)
                                        self.check=False

        		elif prediction[i:i+1] == 'MITM':
                        	print "stat[4]: ipv6 man in the middle attack,[suspenseful] alert:",mac_table[in_port]
                        	print "at port:",in_port
		                match = parser.OFPMatch(eth_type=0x086dd,ip_proto=58,icmpv6_type=134)
		                actions = []
		                inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]

		                self.add_flow(datapath, 100, match, actions,inst)

				while(self.check):
                                        self._alert_features(in_port,mac_table[in_port],prediction,3,134)
                                        self.check=False
#                                match = parser.OFPMatch(eth_src=mac_table[int(in_port)])
#                                actions = []
#                                inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
#                                self.add_flow(datapath, 50, match, actions, inst)

        		else: #flood status
                		print "stat[5]: suspense packet discovery:",list_array[i]
                                match = parser.OFPMatch(eth_type=0x086dd,ip_proto=58,icmpv6_type=134)
                                actions = []
                                inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
                                self.add_flow(datapath, 100, match, actions, inst)

				while(self.check):
                                        self._alert_features(in_port,mac_table[in_port],prediction,3,134)
                                        self.check=False
				print "\nResult:======================== "

				print prediction
				print "END============================"

###self_learn_ra END

###self_learn_rs START(Step 7) continue Step 6.
	def _self_learning_rs(self,datapath,srcip6,in_port,src):
                self.logger.info("RS ML Detect now!!!!")
                print "srcip:",srcip6,", port:",in_port,", mac:",src

                ofproto = datapath.ofproto
                parser = datapath.ofproto_parser
                ipbuf = 0
                in_portbuf = 0
                srcbuf = 0

		if srcip6 == str_ipv6_1[21]:
                	ipbuf=21
		elif srcip6 == str_ipv6_1[51]:
			ipbuf=51
                else:
                        ipbuf=1000
                if in_port == str_ipv6_1[23]:
                        in_portbuf = 23
		elif in_port == str_ipv6_1[53]:
			in_portbuf=53
                else:
                        in_portbuf=500
                if src == str_ipv6_1[24]:
                        srcbuf=24
                elif src == str_ipv6_1[54]:
                        srcbuf=54
                else:
                        str_ipv6_1[1000]=src
                        srcbuf=1000
                print "number",ipbuf,"22",in_portbuf,srcbuf
                list_array=[[ipbuf,22,in_portbuf,srcbuf]]####feed me test for ubuntu VM(Step 8.)

                print list_array

                prediction = clf_rs.predict(list_array)
		print prediction

		

		for i in range(0,len(list_array)): #len is 5

        		point = int(list_array[i][0])
        		point_2=int(list_array[i][2])

        		if prediction[i:i+1] == 'fake':
                        	print "stat[2]: ipv6 RS spoof attack, [suspenseful] alert:",mac_table[in_port]
                        	print "at port:",in_port

				match = parser.OFPMatch(eth_type=0x086dd,ip_proto=58,icmpv6_type=133)
                                actions = []
                                inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
                                self.add_flow(datapath, 100, match, actions, inst)

				while(self.check):
                                        self._alert_features(in_port,mac_table[in_port],prediction,3,134)
                                        self.check=False

        		else: #flood status

                		if int(str_ipv6_1[int(list_array[i][1])])>3:
                        		print "stat[3]: ipv6 RS flood overflow attack, [suspenseful] alert:",mac_table[in_port]
                        		print "at port:",in_port,str_ipv6_1[int(list_array[i][1])]
					match = parser.OFPMatch(eth_type=0x086dd,ip_proto=58,icmpv6_type=133)
                                	actions = []
                                	inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
                                	self.add_flow(datapath, 100, match, actions, inst)

					str_ipv6_1[int(list_array[i][1])]=0
					while(self.check):
                                        	self._alert_features(in_port,mac_table[in_port],prediction,3,134)
                                        	self.check=False

                		else:
                        		print "stat[1]: NORMAL RS detection:",prediction[i:i+1]
                        		str_ipv6_1[int(list_array[i][1])]+=1
                        

###self_learn_rs END

###self_learn_na START(Step 12.)
	def _self_learning_na(self,datapath,srcip6,in_port,src,target,countpkt):
                self.logger.info("NA ML Detect now!!!!")
                print "srcip:",srcip6,",time" ,", port:",in_port,", mac:",src,', target:',target,"count/s:",countpkt


		global datapathv4
                ofproto = datapath.ofproto
                parser = datapath.ofproto_parser
                ipbuf = 0
                in_portbuf = 0
                srcbuf = 0
		targetbuf=0
		
                if srcip6 == str_ipv6_2[21]:
                        ipbuf=21
		elif srcip6 == str_ipv6_2[25]:
                        ipbuf=25
                elif srcip6 == str_ipv6_2[26]:
                        ipbuf=26
                elif srcip6 == str_ipv6_2[51]:
                        ipbuf=51
                elif srcip6 == str_ipv6_2[55]:
                        ipbuf=55
                elif srcip6 == str_ipv6_2[101]:
                        ipbuf=101
                else:
                        ipbuf=600

                if in_port == str_ipv6_2[23]:
                        in_portbuf = 23
                else:
                        in_portbuf=53
                if src == str_ipv6_2[24]:
                        srcbuf=24
                elif src == str_ipv6_2[54]:
                        srcbuf=54
                elif src == str_ipv6_2[104]:
                        srcbuf=104
                else:
                        str_ipv6_0[1000]=src
                        srcbuf=1000

		if target == str_ipv6_2[21]:
                        targetbuf=21
                elif target == str_ipv6_2[25]:
                        targetbuf=25
                elif target == str_ipv6_2[26]:
                        targetbuf=26
                elif target == str_ipv6_2[51]:
                        targetbuf=51
                elif target == str_ipv6_2[55]:
                        targetbuf=55
                elif target == str_ipv6_2[101]:
                        targetbuf=101
                else:
                        targetbuf=600

#		if countpkt replace with 22/55
		print "number",ipbuf,in_portbuf,srcbuf,targetbuf,countpkt
                list_array=[[ipbuf,in_portbuf,srcbuf,targetbuf,int(countpkt)]]####feed me test

                print list_array

                prediction = clf_na.predict(list_array)
		print prediction

		for i in range(0,len(list_array)): #len is 5


	        	if prediction[i:i+1] == 'VM_1' or prediction[i:i+1] == 'VM_2' or prediction[i:i+1]=='Router':

                        	if int(list_array[i][4])>599:
                                	print "stat[2]: NORMAL NA to outside INTERNET detection:",prediction[i:i+1]

                        	else:
                                	print "stat[1]: NORMAL NA to inside vNET detection:",prediction[i:i+1]
			else:
				match = parser.OFPMatch(eth_type=0x086dd,ip_proto=58,icmpv6_type=136)
                                actions = []
                                inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
                                self.add_flow(datapath, 100, match, actions, inst)


	
				while(self.check):
					global timestart
                                        timestart=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

					self._alert_features(in_port,mac_table[in_port],prediction,3,136)
					self._re_trainning(list_array,prediction[i:i+1],136)
					self.check=False
##co-brain
				match = parser.OFPMatch(eth_type=0x086dd,ip_proto=58,icmpv6_type=136)
                                actions = []
                                inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
                                self.add_flow(datapathv4, 100, match, actions, inst)

##co-brain

###self_learn_na END

###self_learn_ns START(Step 14)
        def _self_learning_ns(self,datapath,srcip6,in_port,dstipv6):
                self.logger.info("I am learning now!!!!")
                print "srcip:",srcip6,",time" ,", port:",in_port,', dst:',dstipv6

                ofproto = datapath.ofproto
                parser = datapath.ofproto_parser
                ipbuf = 0
                in_portbuf = 0
		dstipv6buf = 0

                if srcip6 == str_ipv6_3[21]:
                        ipbuf=21
                elif srcip6 == str_ipv6_3[25]:
                        ipbuf=25
		elif srcip6 == str_ipv6_3[51]:
                        ipbuf=51
		elif srcip6 == str_ipv6_3[55]:
                        ipbuf=55
                elif srcip6 == str_ipv6_3[101]:
                        ipbuf=101
                else:
			str_ipv6_3[600]=srcip6
                        ipbuf=600
                if in_port == str_ipv6_1[23]:
                        in_portbuf = 23
                elif in_port == str_ipv6_1[53]:
                        in_portbuf=53
                else:
                        in_portbuf=500

                if dstipv6 == str_ipv6_3[21]:
                        dstipv6buf=21
                elif dstipv6 == str_ipv6_3[25]:
                        dstipv6buf=25
                elif dstipv6 == str_ipv6_3[51]:
                        dstipv6buf=51
                elif dstipv6 == str_ipv6_3[55]:
                        dstipv6buf=55
                elif dstipv6 == str_ipv6_3[101]:
                        dstipv6buf=101
                else:
                        str_ipv6_3[600]=dstipv6
                        dstipv6buf=600
                print "number",ipbuf,"22(normal)",in_portbuf,dstipv6buf
                list_array=[[ipbuf,22,in_portbuf,dstipv6buf]]####feed me test

                print list_array

                prediction = clf_ns.predict(list_array)
                print prediction


		
###self_learn_ns END


	def _monitor(self):
		global ddos_buf

        	while True:
			global timestart
			self.check=True
            		print ('\n\n')
            		self.logger.info('----------table-------------------------------------')
			print "ddos_threshold: "+str(ddos_buf)
			self.logger.info('----Alert----|------FEATURES------|------CLASSIFY---')
			
#			while(self.check):
#				self._alert_features(srcip6,in_port,src,target,prediction)
#				self.check=False

			myfile = open("alert.txt").read()

			print "\t\t",myfile	
##pre 1s pkt count for na
#			print C+D
#			print "------"
#			print JY+EN
#			self._alert_features(1,2,3,4,"vm")					
            		print ('\n\n')
			print timestart
            		hub.sleep(5)

	def _timer(self):
		while True:
			str_ipv6_2[27]=0
                	str_ipv6_2[56]=0
                	str_ipv6_2[105]=0
			str_ipv6_tcp[50]=0
			str_ipv6_tcp[24]=0
			hub.sleep(1)

	def _re_trainning(self,feature_list,feature_type,pkt_type):
		hub.sleep()
		global clf_na
		global ckf_tcp
		global ddos_buf
		print "re_training"
		print feature_list
		print feature_type


		if pkt_type==6:
			if int(feature_list[0][3])<ddos_buf:
                                ddos_buf=ddos_buf/3
		elif pkt_type==136:
			if int(feature_list[0][4])<ddos_buf:
				ddos_buf=ddos_buf/3
		else:
			self.logger.debug("bugme")

		if ddos_buf<50:
			ddos_buf=50
		for i in range(0,3):	
			C.append([int(feature_list[0][0]),int(feature_list[0][1]),int(feature_list[0][2]),int(feature_list[0][3]),ddos_buf])
			D.append(str(feature_type[0]))

		clf_na = tree.DecisionTreeClassifier()
		clf_na = clf_na.fit(C,D)

##testme
                for j in range(0,3):
                        JY.append([600,20,23,ddos_buf])
                        EN.append('flood')

                clf_tcp = tree.DecisionTreeClassifier()
                clf_tcp = clf_tcp.fit(JY,EN)
##testme


	@set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
	def switch_features_handler(self, ev):
		datapath = ev.msg.datapath
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser
		
		# install table-miss flow entry
		#
		# We specify NO BUFFER to max_len of the output action due to
		# OVS bug. At this moment, if we specify a lesser number, e.g.,
		# 128, OVS will send Packet-In with invalid buffer_id and
		# truncated packet data. In that case, we cannot output packets
		# correctly.  The bug has been fixed in OVS v2.1.0.
		
        	match = parser.OFPMatch()
        	actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER),parser.OFPActionOutput(ofproto.OFPP_NORMAL, ofproto.OFPCML_NO_BUFFER)]
		inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]

		self.add_flow(datapath, 10, match, actions,inst)
	
#for icmpv6 start
                match = parser.OFPMatch(eth_type=0x086dd,ip_proto=58,icmpv6_type=134)
                actions = []
                inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]

                self.add_flow(datapath, 100, match, actions,inst)
#for icmpv6 end

		print "Switches connects to Controller OK!!!"
		print "OpenFlow entries initialization are done"


    	@set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    	def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        	if ev.msg.msg_len < ev.msg.total_len:
            		self.logger.debug("packet truncated: only %s of %s bytes",
                        	      ev.msg.msg_len, ev.msg.total_len)
        	msg = ev.msg
        	datapath = msg.datapath
        	ofproto = datapath.ofproto
        	parser = datapath.ofproto_parser
        	in_port = msg.match['in_port']

        	pkt = packet.Packet(msg.data)
        	eth = pkt.get_protocols(ethernet.ethernet)[0]

		co_check=True
        	if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            		return
        	dst = eth.dst
        	src = eth.src
		srcip6 =""
        	dpid = datapath.id
        	self.mac_to_port.setdefault(dpid, {})

#		print hex(dpid)
		self.logger.info("================Packet_in Start=============")

#(Step 1)port table to vSwitch(each VM have one vFW under tanent's vIDS)
		if hex(dpid) == "0xd20fa009834a":
			in_port=10 ###match dpid to specific port(if not a router)
       			self.logger.info("vFirewall id: %s , its in_port: %s", hex(dpid), in_port)
		elif hex(dpid) == "0x46bfddb1ec4b":
                        in_port=14 ###match dpid to specific port(if not a router)
                        self.logger.info("vFirewall id: %s , its in_port: %s", hex(dpid), in_port)
			global datapathv4
			datapathv4 = datapath
		else:
                	in_port=6#6
#                        global datapathv4
#                        datapathv4 = datapath

		pkt_ipv4= pkt.get_protocol(ipv4.ipv4)
		if pkt_ipv4:
#v4			dstip4 = pkt_ipv4.dst 
#			print "v4in"
			co_check=False
			self.logger.debug("Match IPv4")

#v4		pkt_arp = pkt.get_protocol(arp.arp)
#v4		if pkt_arp:
#v4                        self.dstip = pkt_arp.dst_ip 

		pkt_ipv6 = pkt.get_protocol(ipv6.ipv6)
		if pkt_ipv6:
			dstip6 = pkt_ipv6.dst
			srcip6 = pkt_ipv6.src
			co_check=True
#	    		self.logger.info("IPv6 src : %s , IPv6 dst %s", srcip6, dstip6)
#			print pkt_ipv6
	
		pkt_tcp = pkt.get_protocol(tcp.tcp)
		if pkt_tcp and pkt_tcp.bits==2 and co_check==True:#Step 19
#		if pkt_tcp:
#			print pkt_tcp
			if srcip6==str_ipv6_tcp[21]:
				self._self_learning_tcp(datapath,srcip6,in_port,pkt_ipv6.payload_length,str_ipv6_tcp[50])
				str_ipv6_tcp[50]+=1
				print "1-"
			else:
				self._self_learning_tcp(datapath,srcip6,in_port,pkt_ipv6.payload_length,str_ipv6_tcp[24])
				str_ipv6_tcp[24]+=1
				print "2-"
		if co_check==False:
			self.logger.debug("tcp but ipv4")
#		else:
#                        self._self_learning_tcp(datapath,srcip6,in_port,pkt_ipv6.payload_length,24)
		



		pkt_icmpv6 = pkt.get_protocol(icmpv6.icmpv6)
		if pkt_icmpv6:
#			self.logger.info("icmpv6in")			
#disable	    		self.logger.info("My ICMPv6 type is %s", pkt_icmpv6.type_)	
#disable			self.logger.info("Packet msg:  %r ", pkt)
			
			if pkt_icmpv6.type_ == 134:#128,echo req;134,ra
				print "\ncatch value:",pkt_icmpv6.type_,srcip6," , time, ",in_port,", ",src
				self._self_learning_ra(datapath,srcip6,in_port,src)##ra
			elif pkt_icmpv6.type_ == 133:#133,rs
				print "\ncatch value:",pkt_icmpv6.type_,srcip6," , count, ",in_port,", ",src
				self._self_learning_rs(datapath,srcip6,in_port,src)##rs
			elif pkt_icmpv6.type_ == 136:#136,na
				if srcip6 == str_ipv6_2[21] or srcip6 == str_ipv6_2[25] or srcip6 == str_ipv6_2[26] :
					str_ipv6_2[27]+=1
					target=pkt_icmpv6.data.dst
                                	print "\ncatch value:",pkt_icmpv6.type_,srcip6," , time, ",in_port,", ",src,", ",target,", ",str_ipv6_2[27]
                                	self._self_learning_na(datapath,srcip6,in_port,src,target,str_ipv6_2[27])##na
				else:
					str_ipv6_2[27]+=1
					target=pkt_icmpv6.data.dst
					print "\ncatch value:",pkt_icmpv6.type_,srcip6," , time, ",in_port,", ",src,", ",target,", ",str_ipv6_2[27]
                                        self._self_learning_na(datapath,srcip6,in_port,src,target,str_ipv6_2[27])
##8888888

#Step 16(enable me if nessary)			elif pkt_icmpv6.type_ == 135:#135,ns
#                                dstipv6=pkt_icmpv6.data.dst
#                                print "\ncatch value:",pkt_icmpv6.type_,srcip6," , time, ",in_port,", ",dstipv6
#                                self._self_learning_ns(datapath,srcip6,in_port,dstipv6)


		self.logger.info("================Packet_in End=============")
		
		
                

        	# learn a mac address to avoid FLOOD next time.
        	self.mac_to_port[dpid][src] = in_port

		actions=[]


                    
        	data = None
        	if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            		data = msg.data

        	out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        	datapath.send_msg(out)                
		
	def add_flow(self, datapath, priority, match, actions, inst, buffer_id=None):
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser
		mod = parser.OFPFlowMod(datapath=datapath, priority=priority,match=match, instructions=inst)
		datapath.send_msg(mod)

