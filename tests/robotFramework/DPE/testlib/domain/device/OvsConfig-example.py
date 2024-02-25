#!/usr/bin/python
# -*- coding: utf-8 -*-
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger

class OvsConfigExample(object):
    '''
    | 随机字符串（需要在领域层支持）：
    | *31*ins1     -- 随机字符串最大长度为31
    | *dm1         -- 随机字符串，默认最大31
    | $2000$ins1   -- 随机数，最大为2000
    | $poolid1     -- 随机数, 默认最大63
    
    | 名称        | 默认值 | 值  | 说明 |
    | vrf         | 无     | vrf        | vrf名称  |
    
    '''
    def __init__(self):
        pass
    def __openswitch(self):
        self.value = {
            'Open_vSwitch' : {
                'other_config' : {
                    'init'  : True,
                    'dpdk-init'  : True
                    },
                },
                'interface' : {
                        
                }
            }
        
    def __syslog(self):
        self.value = {
            #配置syslog
            'syslog' : {'31.1.1.2':{}},
            }
        
    def __logging(self):
        self.value = {
            #配置logging
            'logging' : {
                'logging' : 'on',
                #alerts/critical/debugging/emergencies/
                #errors/informational/notifications/warnings
                'console-level' : 'debugging',
                'file-default-almlog'  : {
                        'level' : 'debugging'
                    }
                },
            }
        
    def __intf(self):
        self.value = {
            #配置接口 
            'int' : {
                self.int11 : {
                    'vrf'    : 'zte',
                    'ipv6'   : '5000::1',
                    'masklen': '96',
                    'ipv4'   : '31.1.1.1',
                    'maskv4' : '255.255.255.0'
                    },
                self.int12 : {
                    'ipv4'    : '132.1.1.1',
                    'maskv4'  : '255.255.255.0',
                    },
                'loopback1' : {
                    'ipv4'    : '11.19.19.19',
                    'maskv4'  : '255.255.255.0',
                    },
                'te_tunnel1': {
                    'ip-unumber' : 'loopback1',
                    },
                'l3vi1'     : {
                    'nni-gateway': '30.1.1.1',
                    },
                'l3vi1.1'   : {
                    'bind-interface':'fei-0/1/0/1.1',
                    },
                },
            }

        





