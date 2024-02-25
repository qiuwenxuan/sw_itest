#!/usr/bin/python
# -*- coding: utf-8 -*-
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from scapy.all import *
from scapy.contrib.geneve import GENEVE
'''
CreateTestPort -PortLocation 101/4 -PortName ::CHASSIS1/1/4 -PortType ETHERNET -object CHASSIS1

CreateTestPort -PortLocation 101/1 -PortName ::CHASSISMY -PortType ETHERNET -object CHASSIS1
CreateHost -HostName myhost11 -MacAddr 00:01:00:00:00:01 -Ipv4Addr 31.1.1.2 -Ipv4Mask 24 -Ipv4sutAddr 31.1.1.1 -Arpd enable -FlagPing enable -Ipv6Addr 6000::2 -Ipv6Mask 96 -Ipv6sutAddr 6000::1 -object CHASSISMY
CreateHost -HostName myhost12 -MacAddr 00:01:00:00:00:10 -Ipv4Addr 31.1.1.3 -Ipv4Mask 24 -Ipv4sutAddr 31.1.1.1 -Arpd enable -FlagPing enable -Ipv6Addr 6000::3 -Ipv6Mask 96 -Ipv6sutAddr 6000::1 -object CHASSISMY
CreateSubInt -SubIntName cha1Vlan -object CHASSISMY
ConfigPort -VlanTag 0x8100 -VlanId 10 -object cha1Vlan
CreateHost -HostName myhost21 -MacAddr 00:01:00:00:00:03 -Ipv4Addr 132.1.1.2 -Ipv4Mask 24 -Ipv4sutAddr 132.1.1.1 -Arpd enable -FlagPing enable -object cha1Vlan
SendArpRequest -object myhost11
SendArpRequest -object myhost12
SendArpRequest -object myhost21

'''
class chaipv4config(object):
    def __init__(self):
        pass

    def getConfig(self):
        loc1 = str(BuiltIn().get_variable_value('${cha1port1}'))
        loc2 = str(BuiltIn().get_variable_value('${cha1port2}'))
        self.value = {
            'cha' :{
                'port' : {
                    'port1' : {
                        'PortLocation' :  str(loc1),
                        'PortType'     : 'ETHERNET',
                        },
                    'port2' : {
                        'PortLocation' :  str(loc2),
                        'PortType'     : 'ETHERNET',
                        }
                    },
                'host' : {
                    'host11': {
                        'object' : 'port1',
                        'MacAddr'  : 'auto',
                        'Ipv4Addr' : 'auto.101', #@ip4.24@inprefix1.inipv42
                        'Ipv4Mask' : 'auto',
                        'Ipv4sutAddr' :'auto',#@ip4.24@inprefix1.inipv41
                        'Arpd' : 'enable',
                        'FlagPing' :'enable',
                        'Ipv6Addr' :'auto',
                        'Ipv6Mask' :'64',
                        'Ipv6sutAddr' : 'auto'
                        },
                    'host12': {
                        'object' : 'port1',
                        'MacAddr'  : '00:01:00:00:00:12',
                        'Ipv4Addr' : 'auto.102',
                        'Ipv4Mask' : '24',
                        'Ipv4sutAddr' :'auto',
                        'Arpd' : 'enable',
                        'FlagPing' :'enable',
                        'Ipv6Addr' :'6000::3',
                        'Ipv6Mask' :'64',
                        'Ipv6sutAddr' : '6000::1'
                        },
                    'host13': {
                        'object' : 'port1',
                        'MacAddr'  : '00:01:00:00:00:20',
                        'Ipv4Addr' : '177.0.0.4',
                        'Ipv4Mask' : '24',
                        'Ipv4sutAddr' :'177.0.0.1',
                        'Arpd' : 'enable',
                        'FlagPing' :'enable',
                        'Ipv6Addr' :'6000::4',
                        'Ipv6Mask' :'64',
                        'Ipv6sutAddr' : '6000::1'
                        },
                    'host21': {
                        'object' : 'port2',
                        'MacAddr'  : '00:02:00:00:00:03',
                        'Ipv4Addr' : '178.0.0.2', 
                        'Ipv4Mask' : '24',
                        'Ipv4sutAddr' :'178.0.0.1',
                        'Arpd' : 'enable',
                        'FlagPing' :'enable',
                        },
                    'host22': {
                        'object' : 'port2',
                        'MacAddr'  : '00:02:00:00:00:04',
                        'Ipv4Addr' : '178.0.0.3', 
                        'Ipv4Mask' : '24',
                        'Ipv4sutAddr' :'178.0.0.1',
                        'Arpd' : 'enable',
                        'FlagPing' :'enable',
                        }
                    },
                'traffic' : {
                    'port1Traffic' : {
                        'object' : 'port1',
                        },
                    'port2Traffic' : {
                        'object' : 'port2',
                        }
                    },
                'staEngine' : {
                    'port1Sta' : {
                        'engtype': 'Statistics',
                        'object' : 'port1',
                        },
                    'port1Ana' : {
                        'engtype': 'Analysis',
                        'object' : 'port1',
                        },
                    'port2Sta' : {
                        'engtype': 'Statistics',
                        'object' : 'port2',
                        },
                    'port2Ana' : {
                        'engtype': 'Analysis',
                        'object' : 'port2',
                        },
                    },
                }
            }
        return self.value

    def getProfile(self):
        self.value = {
            'cha' :{
                'profile' : {
                    'profile1' :{
                        'config' :{
                            'object' : 'port1Traffic',
                            'Type' : 'Constant',
                            },
                        'stream' : {
                            'stream1' : {
                                    'flowType' : 'ipv4',
                                    'hostsrc'  : 'host11',
                                    'hostdst'  : 'host21',
                                    'UdpSrcPort' : '1000',
                                    'UdpDstPort' : '1000',
                                    'UdpSrcPortMode' : 'increment',
                                    'UdpSrcPortStep' : '1',
                                    'UdpSrcPortCount' : '10',
                                    'L2' : 'Ethernet',
                                    'L3' : 'IPV4',
                                    'EthDst' : '08:00:27:a2:42:de',
                                    'framelen' : '100',
                                    'StreamLoad':'10',
                                    'StreamLoadUnit':'fps'
                                },
                            }
                        },
                    'profile2' :{
                        'config' :{
                            'object' : 'port2Traffic',
                            'Type' : 'Constant',
                            },
                        'stream' : {
                            'stream1' : {
                                    'flowType' : 'ipv4',
                                    'hostsrc'  : 'host11',
                                    'hostdst'  : 'host21',
                                    'TcpSrcPort' : '1020',
                                    'TcpDstPort' : '1020',
                                    'TcpSrcPortMode' : 'increment',
                                    'TcpSrcPortStep' : '1',
                                    'TcpSrcPortCount' : '10',
                                    'L2' : 'Ethernet',
                                    'L3' : 'IPV4',
                                    'EthDst' : '08:00:27:a2:42:de',
                                    'framelen' : '100',
                                    'StreamLoad':'10',
                                    'StreamLoadUnit':'fps'
                                },
                            }
                        }
                    }
                }
            }
        return self.value

    def getOneConfig(self):
        loc1 = str(BuiltIn().get_variable_value('${cha1port1}'))
        self.value = {
            'cha' :{
                'port' : {
                    'port1' : {
                        'PortLocation' :  str(loc1),
                        'PortType'     : 'ETHERNET',
                        },
                    },
                'host' : {
                    'host11': {
                        'object' : 'port1',
                        'MacAddr'  : '00:01:00:00:00:20',
                        'Ipv4Addr' : '177.0.0.4',
                        'Ipv4Mask' : '24',
                        'Ipv4sutAddr' :'177.0.0.1',
                        'Arpd' : 'enable',
                        'FlagPing' :'enable',
                        'Ipv6Addr' :'6000::4',
                        'Ipv6Mask' :'64',
                        'Ipv6sutAddr' : '6000::1'
                        },
                    },
                'traffic' : {
                    'port1Traffic' : {
                        'object' : 'port1',
                        },
                    },
                'staEngine' : {
                    'port1Sta' : {
                        'engtype': 'Statistics',
                        'object' : 'port1',
                        },
                    'port1Ana' : {
                        'engtype': 'Analysis',
                        'object' : 'port1',
                        },
                    }
                }
            }
        return self.value
        
    def getOneProfile(self):
        self.value = {
            'cha' :{
                'profile' : {
                    'profile1' :{
                        'config' :{
                            'object' : 'port1Traffic',
                            'Type' : 'Constant',
                            },
                        'stream' : {
                            'stream1' : {
                                    'flowType' : 'ipv4',
                                    'hostsrc'  : 'host11',
                                    'hostdst'  : 'host21',
                                    'UdpSrcPort' : '1000',
                                    'UdpDstPort' : '1000',
                                    'UdpSrcPortMode' : 'increment',
                                    'UdpSrcPortStep' : '1',
                                    'UdpSrcPortCount' : '10',
                                    'L2' : 'Ethernet',
                                    'L3' : 'IPV4',
                                    'EthDst' : '08:00:27:a2:42:de',
                                    'framelen' : '100',
                                    'StreamLoad':'10',
                                    'StreamLoadUnit':'fps'
                                },
                            }
                        },
                    'profile2' :{
                        'config' :{
                            'object' : 'port1Traffic',
                            'Type' : 'Constant',
                            },
                        'stream' : {
                            'stream1' : {
                                    'pkt' : Ether(dst='00:01:00:00:01:01',src='00:01:00:00:01:02')/IP(src='172.0.1.1',dst='172.0.1.2')/UDP(),
                                    'framelen' : '100',
                                    'StreamLoad':'10',
                                    'StreamLoadUnit':'fps'
                                },
                            }
                        }
                    }
                }
            }
        return self.value

    def getVxlanConfig(self):
        self.value = {
            'bridge' : {
                'br-ext': {
                    'type': 'netdev',
                    'failmode': 'standalone'
                },
                'br-int': {
                    'type': 'netdev',
                    'failmode': 'standalone'
                },
                'br-tun': {
                    'type': 'netdev',
                    'failmode': 'standalone'
                },
            },
            'port' : {
                'br-ext': {
                    'dpdk0': {
                        'type': 'dpdk',
                        'options': {
                            'dpdk-devargs': '0000:ec:01.1',
                            'n_rxq_desc': '1024',
                            'n_txq_desc': '1024',
                        },
                        'ofport_request': 1,
                    }
                },
                'br-tun': {
                    'vxlan0': {
                         'type': 'vxlan',
                         'options': {
                             'remote_ip': "192.168.2.10",
                             'local_ip': "192.168.2.55",
                             'in_key': '100',
                             'out_key': '100',
                         },
                   },
                    'patch-int': {
                         'type': 'patch',
                         'options': {
                             'peer': 'patch-tun'
                        },
                    }
                },
                'br-int': {
                    'dpdk1': {
                        'type': 'dpdk',
                        'options': {
                            'dpdk-devargs': '0000:ec:09.1',
                            'n_rxq_desc': '1024',
                            'n_txq_desc': '1024',
                        },
                        'ofport_request': 1,
                    },
                    'patch-tun': {
                         'type': 'patch',
                         'options': {
                             'peer': 'patch-int'
                         },
                         'ofport_request': 2,
                    },
                    'net_jmnd0': {
                         'type': 'dpdk',
                         'options': {
                             'dpdk-devargs': 'eth_jmnd0,iface=/tmp/sock0,client=1,queues=4'
                         },
                         'ofport_request': 3,
                    },
                    'net_jmnd1': {
                         'type': 'dpdk',
                         'options': {
                             'dpdk-devargs': 'eth_jmnd1,iface=/tmp/sock1,client=1,queues=4'
                         },
                         'ofport_request': 4,
                    },
                    'net_jmnd2': {
                         'type': 'dpdk',
                         'options': {
                             'dpdk-devargs': 'eth_jmnd2,iface=/tmp/sock2,client=1,queues=4'
                         },
                         'ofport_request': 5,
                    },
                    'net_jmnd3': {
                         'type': 'dpdk',
                         'options': {
                             'dpdk-devargs': 'eth_jmnd3,iface=/tmp/sock3,client=1,queues=4'
                         },
                         'ofport_request': 6,
                    }

                }
            },
            'interface': {
                'dpdk0': {
                     'options': {
                         'n_rxq': '4'
                     },
                     'other_config': {
                         'pmd-rxq-affinity': "0:4,1:5,2:6,3:7"
                     }
                },
                'dpdk1': {
                     'options': {
                         'n_rxq': '4'
                     },
                     'other_config': {
                         'pmd-rxq-affinity': "0:4,1:5,2:6,3:7"
                     }
                },
                 'net_jmnd0': {
                     'options': {
                         'n_rxq': '4'
                     },
                     'other_config': {
                         'pmd-rxq-affinity': "0:4,1:5,2:6,3:7"
                     }
                 },
                 'net_jmnd1': {
                     'options': {
                         'n_rxq': '4'
                     },
                     'other_config': {
                         'pmd-rxq-affinity': "0:4,1:5,2:6,3:7"
                     }
                 },
                 'net_jmnd2': {
                     'options': {
                         'n_rxq': '4'
                     },
                     'other_config': {
                         'pmd-rxq-affinity': "0:4,1:5,2:6,3:7"
                     }
                 },
                 'net_jmnd3': {
                      'options': {
                         'n_rxq': '4'
                     },
                     'other_config': {
                         'pmd-rxq-affinity': "0:4,1:5,2:6,3:7"
                     }
                 }
            },
            'flow': {
                'br-tun': {
                    '1': {
                        'match': {
                            'in_port': '2'
                        }, 
                        'action': {
                            'type': 'fwd',
                            'output': '1'
                        }
                    },
                    '2': {
                        'match': {
                            'in_port': '1'
                        }, 
                        'action': {
                            'type': 'fwd',
                            'output': '2'
                        }
                    }
                },
                'br-int': {
                    '1': {
                        'match': {
                            'in_port': '2'
                        }, 
                        'action': {
                            'type': 'fwd',
                            'output': '1'
                        }
                    },
                    '2': {
                        'match': {
                            'in_port': '1'
                        }, 
                        'action': {
                            'type': 'fwd',
                            'output': '2'
                        }
                    }
                }
            }
        }
        return self.value 

    def getVxlanConfigAc(self):
        self.value = {
            'bridge' : {
                'br-ext': {
                    'type': 'netdev',
                    'failmode': 'standalone'
                },
                'br-int': {
                    'type': 'netdev',
                    'failmode': 'standalone'
                },
                'br-tun': {
                    'type': 'netdev',
                    'failmode': 'standalone'
                },
            },
            'port' : {
                'br-tun': {
                    'vxlan0': {
                         'type': 'vxlan',
                         'options': {
                             'remote_ip': "192.168.2.10",
                             'local_ip': "192.168.2.55",
                             'in_key': '100',
                             'out_key': '100',
                         },
                   },
                    'patch-int': {
                         'type': 'patch',
                         'options': {
                             'peer': 'patch-tun'
                        },
                    }
                },
                'br-int': {
                    'dpdk0': {
                        'type': 'dpdk',
                        'options': {
                            'dpdk-devargs': '0000:ec:01.1',
                            'n_rxq_desc': '1024',
                            'n_txq_desc': '1024',
                        },
                        'ofport_request': 1,
                    },
                    'dpdk1': {
                        'type': 'dpdk',
                        'options': {
                            'dpdk-devargs': '0000:ec:09.1',
                            'n_rxq_desc': '1024',
                            'n_txq_desc': '1024',
                        },
                        'ofport_request': 1,
                    },
                    'patch-tun': {
                         'type': 'patch',
                         'options': {
                             'peer': 'patch-int'
                         },
                         'ofport_request': 2,
                    },
                    'net_jmnd0': {
                         'type': 'dpdk',
                         'options': {
                             'dpdk-devargs': 'eth_jmnd0,iface=/tmp/sock0,client=1,queues=4'
                         },
                         'ofport_request': 3,
                    },
                    'net_jmnd1': {
                         'type': 'dpdk',
                         'options': {
                             'dpdk-devargs': 'eth_jmnd1,iface=/tmp/sock1,client=1,queues=4'
                         },
                         'ofport_request': 4,
                    },
                    'net_jmnd2': {
                         'type': 'dpdk',
                         'options': {
                             'dpdk-devargs': 'eth_jmnd2,iface=/tmp/sock2,client=1,queues=4'
                         },
                         'ofport_request': 5,
                    },
                    'net_jmnd3': {
                         'type': 'dpdk',
                         'options': {
                             'dpdk-devargs': 'eth_jmnd3,iface=/tmp/sock3,client=1,queues=4'
                         },
                         'ofport_request': 6,
                    }

                }
            },
            'interface': {
                'dpdk0': {
                     'options': {
                         'n_rxq': '4'
                     },
                     'other_config': {
                         'pmd-rxq-affinity': "0:4,1:5,2:6,3:7"
                     }
                },
                'dpdk1': {
                     'options': {
                         'n_rxq': '4'
                     },
                     'other_config': {
                         'pmd-rxq-affinity': "0:4,1:5,2:6,3:7"
                     }
                },
                 'net_jmnd0': {
                     'options': {
                         'n_rxq': '4'
                     },
                     'other_config': {
                         'pmd-rxq-affinity': "0:4,1:5,2:6,3:7"
                     }
                 },
                 'net_jmnd1': {
                     'options': {
                         'n_rxq': '4'
                     },
                     'other_config': {
                         'pmd-rxq-affinity': "0:4,1:5,2:6,3:7"
                     }
                 },
                 'net_jmnd2': {
                     'options': {
                         'n_rxq': '4'
                     },
                     'other_config': {
                         'pmd-rxq-affinity': "0:4,1:5,2:6,3:7"
                     }
                 },
                 'net_jmnd3': {
                      'options': {
                         'n_rxq': '4'
                     },
                     'other_config': {
                         'pmd-rxq-affinity': "0:4,1:5,2:6,3:7"
                     }
                 }
            },
            'flow': {
                'br-tun': {
                    '1': {
                        'match': {
                            'in_port': '2'
                        }, 
                        'action': {
                            'type': 'fwd',
                            'output': '1'
                        }
                    },
                    '2': {
                        'match': {
                            'in_port': '1'
                        }, 
                        'action': {
                            'type': 'fwd',
                            'output': '2'
                        }
                    }
                },
                'br-int': {
                    '1': {
                        'match': {
                            'in_port': '8'
                        }, 
                        'action': {
                            'type': 'fwd',
                            'output': '2'
                        }
                    },
                    '2': {
                        'match': {
                            'in_port': '2'
                        }, 
                        'action': {
                            'type': 'fwd',
                            'output': '8'
                        }
                    }
                }
            }
        }
        return self.value 

    def getGeneveConfig(self):
        self.value = {
            'bridge' : {
                'br-ext': {
                    'type': 'netdev',
                    'failmode': 'standalone'
                },
                'br-int': {
                    'type': 'netdev',
                    'failmode': 'standalone'
                },
                'br-tun': {
                    'type': 'netdev',
                    'failmode': 'standalone'
                },
            },
            'port' : {
                'br-ext': {
                    'dpdk0': {
                        'type': 'dpdk',
                        'options': {
                            'dpdk-devargs': '0000:ec:01.0',
                            'n_rxq_desc': '1024',
                            'n_txq_desc': '1024',
                        },
                        'ofport_request': 1,
                    }
                },
                'br-tun': {
                    'gen0': {
                         'type': 'geneve',
                         'options': {
                             'remote_ip': "192.168.2.10",
                             'local_ip': "192.168.2.55",
                             'in_key': '100',
                             'out_key': '100',
                         },
                   },
                    'patch-int': {
                         'type': 'patch',
                         'options': {
                             'peer': 'patch-tun'
                        },
                    }
                },
                'br-int': {
                    'dpdk1': {
                        'type': 'dpdk',
                        'options': {
                            'dpdk-devargs': '0000:ec:09.0',
                            'n_rxq_desc': '1024',
                            'n_txq_desc': '1024',
                        },
                        'ofport_request': 1,
                    },
                    'patch-tun': {
                         'type': 'patch',
                         'options': {
                             'peer': 'patch-int'
                         },
                         'ofport_request': 2,
                    },
                    'net_jmnd0': {
                         'type': 'dpdk',
                         'options': {
                             'dpdk-devargs': 'eth_jmnd0,iface=/tmp/sock0,client=1,queues=4'
                         },
                         'ofport_request': 3,
                    },
                    'net_jmnd1': {
                         'type': 'dpdk',
                         'options': {
                             'dpdk-devargs': 'eth_jmnd1,iface=/tmp/sock1,client=1,queues=4'
                         },
                         'ofport_request': 4,
                    },
                    'net_jmnd2': {
                         'type': 'dpdk',
                         'options': {
                             'dpdk-devargs': 'eth_jmnd2,iface=/tmp/sock2,client=1,queues=4'
                         },
                         'ofport_request': 5,
                    },
                    'net_jmnd3': {
                         'type': 'dpdk',
                         'options': {
                             'dpdk-devargs': 'eth_jmnd3,iface=/tmp/sock3,client=1,queues=4'
                         },
                         'ofport_request': 6,
                    }

                }
            },
            'interface': {
                'dpdk0': {
                     'options': {
                         'n_rxq': '4'
                     },
                     'other_config': {
                         'pmd-rxq-affinity': "0:4,1:5,2:6,3:7"
                     }
                },
                'dpdk1': {
                     'options': {
                         'n_rxq': '4'
                     },
                     'other_config': {
                         'pmd-rxq-affinity': "0:4,1:5,2:6,3:7"
                     }
                },
                 'net_jmnd0': {
                     'options': {
                         'n_rxq': '4'
                     },
                     'other_config': {
                         'pmd-rxq-affinity': "0:4,1:5,2:6,3:7"
                     }
                 },
                 'net_jmnd1': {
                     'options': {
                         'n_rxq': '4'
                     },
                     'other_config': {
                         'pmd-rxq-affinity': "0:4,1:5,2:6,3:7"
                     }
                 },
                 'net_jmnd2': {
                     'options': {
                         'n_rxq': '4'
                     },
                     'other_config': {
                         'pmd-rxq-affinity': "0:4,1:5,2:6,3:7"
                     }
                 },
                 'net_jmnd3': {
                      'options': {
                         'n_rxq': '4'
                     },
                     'other_config': {
                         'pmd-rxq-affinity': "0:4,1:5,2:6,3:7"
                     }
                 }
            },
            'flow': {
                'br-tun': {
                    '1': {
                        'match': {
                            'in_port': '2'
                        }, 
                        'action': {
                            'type': 'fwd',
                            'output': '1'
                        }
                    },
                    '2': {
                        'match': {
                            'in_port': '1'
                        }, 
                        'action': {
                            'type': 'fwd',
                            'output': '2'
                        }
                    }
                },
                'br-int': {
                    '1': {
                        'match': {
                            'in_port': '2'
                        }, 
                        'action': {
                            'type': 'fwd',
                            'output': '1'
                        }
                    },
                    '2': {
                        'match': {
                            'in_port': '1'
                        }, 
                        'action': {
                            'type': 'fwd',
                            'output': '2'
                        }
                    }
                }
            }
        }
        return self.value 
    




