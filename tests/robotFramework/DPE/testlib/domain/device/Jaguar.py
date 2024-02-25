#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
日期 :  2015-8-21
作者 ： APP RF小组
'''
from ast import Break, operator
import copy , re, random, time, os, subprocess, sys
from pickle import BUILD, FALSE, TRUE
from pprint import pprint
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
import requests , json, operator
from scapy.layers.inet6 import IPv6
from operator import itemgetter

from scapy.contrib.mpls import * # import from contrib folder of scapy 
from scapy.layers.inet6 import *
from scapy.contrib.geneve import GENEVE

import time

__path = os.path.realpath(os.path.join(__file__,'..','..','..','base'))
if __path not in sys.path:sys.path.append(__path)

from corsica import corsica_dpe
from register import *
import AppBaseLib as _baselib

class Jaguar(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    zxins = dict()
    zxinsbk = dict()
    dutlib = None
    headers = {'Content-Type': 'application/json'}
    name = "Jaguar"

    def __init__(self):
        pass

    def __getJsonNew(self):
        now = time.strftime("%m%d%H%M%S")
        filename = "jaguar_json_"+now+str(random.randint(100,999))
        file = os.path.join(os.getenv('TEMP'),filename+".json")
        return filename+".json",file

    def __getObj(self, name):
        try:
            return BuiltIn().get_library_instance(name)
        except Exception:
            pass
        return None

    def __initlib(self,dut = None):
        if self.dutlib == None:
            self.dutlib   = BuiltIn().get_library_instance('AppDut')
            self.ovslib   = BuiltIn().get_library_instance('Ovs')  #使用ovs的流表公共库
        if dut != None:
            if dut not in self.zxins:
                self.zxins[dut] = dict()
                self.zxins[dut]['tables'] = dict()
                self.zxins[dut]['info'] = {'base':self.__getBaseUrl(dut)}
        return True

    def __getBaseUrl(self,dut):
        config = self.dutlib.dutGetConfig(dut)
        logger.info(config)
        port = config.get('port',None)
        port1 = config.get('restful',None)
        if port1 != None :
            port = port1
        ip = config['ip']
        if self.__isCurl():
            ip = '127.0.0.1'
        return "http://%s:%s/jmndapi/v2/ovsconfig"%(ip,port)

    def __createUrl(self,dut,table,params=dict()):
        '''获取url
        '''
        url = self.zxins[dut]['info']['base']
        if table != None:
            url += '/' + table + '?token=jmnd_001'
        return url

    def __isCurl(self):
        iscurl = BuiltIn().get_variable_value("${curl}",True)
        if iscurl == 'False':
            iscurl = False
        return  iscurl

    def __urlSleep(self):
        sleep = BuiltIn().get_variable_value("${restful_sleep}",1)
        tt = int(sleep)
        if tt > 0:
            time.sleep(tt)

    def __putFile(self,dut,config):
        filename,file_local = self.__getJsonNew()
        with open(file_local,"w") as f:
            json.dump(config,f)
        logger.info('[FileLocal]'+file_local)
        conn = self.dutlib.getConnet(dut)
        conn.put_file(file_local,"/share/home/emu1/json_restful_tmp/")
        file_remote = "/share/home/emu1/json_restful_tmp/"+filename
        logger.info('[FileLocal]'+file_remote)
        return file_remote

    def postTable(self,dut,table,name,config):
        self.__initlib(dut)
        url = self.__createUrl(dut,table,name)
        data = config
        retSucNum = 0
        if self.__isCurl():
            file = self.__putFile(dut,config)
            #self.dutlib.process(dut,"curl --help")
            logger.debug("------------------------------------")
            logger.debug(config)
            logger.debug("------------------------------------")
            #logger.warn(corsica_dpe.corsica_config_check(copy.deepcopy(config),True))
            logger.debug("curl -H \"Content-Type: application/json\"  -XPOST \"%s\" -d@%s"%(url,file))
            ret = self.dutlib.process(dut,"curl -H \"Content-Type: application/json\"  -XPOST \"%s\" -d@%s"%(url,file))
            logger.debug(ret)
            logger.debug("------------------------------------")
            retSucNum = ret.count('success!')
            return retSucNum
        r = requests.post(url=url,
                          headers=self.headers,
                          data=json.dumps(data))
        if not r.ok :
            raise AssertionError("Post error!")
        retdata = r.json()
        ret = retdata.get('data',"")
        logger.debug(ret)
        if 'appret' in ret:
            appret =  ret['appret']
            retSucNum = appret.count('success!')
        return retSucNum

    def getTable(self,dut,table=None,name=None, data=None, params=None):
        self.__initlib(dut)
        url = self.__createUrl(dut,table,name)
        if data != None:
            data=json.dumps(data)
        if params != None:
            params=json.dumps(params)
        if self.__isCurl():
            if params != None:
                file = self.__putFile(dut,params)
                ret = self.dutlib.process(dut,"curl -H \"Content-Type: application/json\"  -XGET \"%s\" -d@%s"%(url,file))
            else:
                ret = self.dutlib.process(dut,"curl -H \"Content-Type: application/json\"  -XGET \"%s\""%(url))
            return
        r = requests.get(url=url, headers=self.headers, data=data, params=params)
        if not r.ok :
            raise AssertionError("Get error!")
        return r.json()

    def putTable(self,dut,table,name=None):
        self.__initlib(dut)
        url = self.__createUrl(dut,table,name)
        if self.__isCurl():
            raise AssertionError("Not support")
            return
        r = requests.put(url=url, headers=self.headers)
        if not r.ok :
            raise AssertionError("Put error!")
        return r.json()

    def deleteTable(self,dut,table=None,name=None):
        self.__initlib(dut)
        url = self.__createUrl(dut,table,name)
        retSucNum = 0
        if self.__isCurl():
            file = self.__putFile(dut,name)
            ret = self.dutlib.process(dut,"curl --help")
            logger.warn("------------------------------------")
            logger.warn(name)
            logger.warn("------------------------------------")
            logger.warn(corsica_dpe.corsica_config_check(copy.deepcopy(name),True))
            logger.warn("curl -H \"Content-Type: application/json\"  -XDELETE \"%s\" -d@%s"%(url,file))
            ret = self.dutlib.process(dut,"curl -H \"Content-Type: application/json\"  -XDELETE \"%s\" -d@%s"%(url,file))
            logger.warn(ret)
            logger.warn("------------------------------------")
            retSucNum = ret.count('success!')
            return retSucNum
        r = requests.delete(url=url, headers=self.headers,
                          data=json.dumps(name))
        if not r.ok :
            raise AssertionError("Delete error!")
        retdata = r.json()
        ret = retdata.get('data',"")
        logger.debug(ret)
        if 'appret' in ret:
            appret =  ret['appret']
            retSucNum = appret.count('success!')
        return retSucNum

    def deal_json_invaild(self, text):
        if type(text) != str:
            raise Exception("参数接受的是字符串类型")
        # text = re.search(r"\{.*\}", text).group()
        text = re.sub(r"\n|\t|\r|\r\n|\n\r|\x08|\\", "", text)
        try:
            json.loads(text)
        except json.decoder.JSONDecodeError as err:
            temp_pos = int(re.search(r"\(char (\d+)\)", str(err)).group(1))
            temp_list = list(text)
            while True:
                if temp_list[temp_pos] == "\"" or "}":
                    if temp_list[temp_pos - 1] == "{":
                        break
                    elif temp_list[temp_pos - 1] == (":" or "{") and temp_list[temp_pos - 2] == ("\"" or ":" or "["):
                        break
                    elif temp_list[temp_pos] == "|\n|\t|\r|\r\n|\n\r| ":
                        temp_list[temp_pos] = re.sub(temp_list[temp_pos], "", temp_list[temp_pos])
                        text = "".join(temp_list)
                    elif temp_list[temp_pos] == "\"":
                        temp_list[temp_pos] = re.sub(temp_list[temp_pos], "“", temp_list[temp_pos])
                        text = "".join(temp_list)
                    elif temp_list[temp_pos] == "}":
                        temp_list[temp_pos - 1] = re.sub(temp_list[temp_pos], "\"", temp_list[temp_pos])
                        text = "".join(temp_list)
                        temp_pos -= 1
                temp_pos -= 1
            return self.deal_json_invaild(text)
        else:
            return text


    def transJsonToDict(self,dut,jsondata):
        self.__initlib(dut)
        data = jsondata.get('data', None)
        #data = self.deal_json_invaild(data)
        #logger.debug("get %s table: %s"%(k, data))
        if data == None:
            return False
        #data = data.replace('\n', '')
        data = re.sub(r"\n|\t|\r|\r\n|\n\r|\x08|\\", "", data)
        try:
            data = json.loads(data)
        except json.decoder.JSONDecodeError as err:
            logger.debug("get table error: %s"%(err))
            logger.debug("get table data: %s"%(data))
            return None

        return data
    
    def jaguarGetTableList(self,dut,data):
        self.__initlib(dut)
        '''
        获取出来的data是列表形式
        '''
        if data == None:
            logger.error("jaguarGetTableList is None!")
            return None
        for groupData in data:
            if 'group' in groupData:
                tablelist = groupData.get('group', None)
                logger.debug("get table data: %s"%(tablelist))
                return tablelist
        return None


    def jaguarCmpDict(self, dut, getConfig, userConfig):
        '''比较字典中的值
        '''
        self.__initlib(dut)
        if (len(userConfig) > len(getConfig)):
            diffkey = userConfig.keys() - getConfig.keys()
            logger.error("user config  %s is not in the device"%(diffkey))
            return
        if (len(getConfig) > len(getConfig)):
            diffkey = getConfig.keys() - userConfig.keys()
            logger.error("device key %s is not in the user config"%(diffkey))
            return

        for k in userConfig:
            if operator.ne(getConfig[k], userConfig[k]):
                logger.error("table key %s is diff"%(k))
                self.jaguarCheckTableFieldValue(dut, userConfig[k], getConfig[k])
        return

    def jaguarCmpList(self, dut, userConfig, getConfig):
        '''比较列表中的值
        '''
        self.__initlib(dut)
        if operator.ne(userConfig, getConfig):
            logger.error("device %s user is"%(getConfig, userConfig))

        return

    def jaguarCmpTuple(self, dut, userConfig, getConfig):
        '''比较元组
        '''
        self.__initlib(dut)
        if operator.ne(userConfig, getConfig):
            logger.error("device %s user is"%(getConfig, userConfig))
        return

    def jaguarCheckTableFieldValue(self, dut, userConfig, getConfig):
        if (type(userConfig) != type(getConfig)):
            logger.error("device type is %s, user type is %s"%(type(getConfig), type(userConfig)))
        if (type(userConfig) == int or type(getConfig) == str):
            logger.error("device value is %s"%(getConfig))
            logger.error("user value is %s"%(userConfig))
        if (type(getConfig) == dict):
            self.jaguarCmpDict(dut, getConfig, userConfig)
        if (type(getConfig) == list):
            self.jaguarCmpList(dut, getConfig, userConfig)
        if (type(getConfig) == tuple):
            self.jaguarCmpTuple(dut, getConfig, userConfig)
        return

    def jaguarCheckOneTable(self, dut, tableName, userConfig, getConfig):
        '''
        userConfig----用户配置数据
        getConfig-----获取的设备上的数据，可能
        检查当前已下发的配置是否成功     
        '''
        if getConfig == None:
            return False
        self.__initlib(dut)

        checklen = False
#        checkDiffKey = True

        if getConfig != None:
            for table in getConfig:
                check = True
                if checklen:
                    if len(table) != len(userConfig):
                        check = False
                        continue

                if tableName == 'meter_table' or tableName == 'meter_profile'  or tableName == 'output_meter' or tableName == 'mirror_policy' or tableName == 'dest_mirror':
                    if 'tbl_name' in table:
                        table.pop('tbl_name', None)

                if tableName == 'classify' or tableName == 'profile' or tableName == 'wc_table':
                    if 'key' in table:
                        table.pop('key', None)
                        userConfig.pop('key', None)
                    if 'mask' in table:
                        table.pop('mask', None)
                        userConfig.pop('mask', None)

                if tableName == 'mc_group_rx':
                    if 'table' in table:
                        table['table'].pop('MC_GROUP_RX_NEXT_LEAF_INDEX', None)
                        userConfig['table'].pop('MC_GROUP_RX_NEXT_LEAF_INDEX', None)
                        
                if tableName == 'mc_group_tx':
                    if 'table' in table:
                        table['table'].pop('MC_GROUP_TX_NEXT_LEAF_INDEX', None)
                        userConfig['table'].pop('MC_GROUP_TX_NEXT_LEAF_INDEX', None)

                if tableName == 'mc_leaf_rx' or tableName == 'mc_leaf_tx':
                    if 'table' in table:
                        table['table'].pop('MC_LEAF_NEXT_INDEX', None)
                        userConfig['table'].pop('MC_LEAF_NEXT_INDEX', None)

                if tableName == 'meter_table':
                    if 'table' in table:
                        table['table'].pop('METER_TABLE_PKT_CNT', None)
                        table['table'].pop('METER_TABLE_LAST_TS', None)
                        table['table'].pop('METER_TABLE_BKT_E', None)
                        table['table'].pop('METER_TABLE_BKT_C', None)
                        table['table'].pop('METER_TABLE_BYTE_CNT', None)
                        userConfig['table'].pop('METER_TABLE_PKT_CNT', None)
                        userConfig['table'].pop('METER_TABLE_LAST_TS', None)
                        userConfig['table'].pop('METER_TABLE_BKT_E', None)
                        userConfig['table'].pop('METER_TABLE_BKT_C', None)
                        userConfig['table'].pop('METER_TABLE_BYTE_CNT', None)                                   
                        
#                if checkDiffKey:
                diffkey = table.keys() ^ userConfig.keys()
                if len(diffkey) != 0:
                    logger.error("table key field diff %s"%(diffkey))
                    check = False
                    continue

                for k in userConfig.keys():
                    if operator.ne(table[k], userConfig[k]):
                        check = False
                        logger.error("compare table name %s table key value %s fail!"%(tableName, k))
                        self.jaguarCheckTableFieldValue(dut, userConfig[k], table[k])
                        break
                if check:
                    return True

        #logger.error("check error!!! %s %s"%(table, userConfig))
        return False

    def jaguarCheckConfig(self,dut,exact=False):
        '''检查配置 未完成
        '''
        self.__initlib(dut)

        existConfig = self.zxins[dut]['tables']
        for k in existConfig:
            checkSucsess= False
            '''
            非精确查找时，按照表名get当前设备上的所有数据
            '''
            if not exact:
                retjson = self.getTable(dut, k, None)
                jsonData = self.transJsonToDict(dut, retjson)
                gettablelist = self.jaguarGetTableList(dut, jsonData)
                if gettablelist == None:
                    return False

            if 'group' in existConfig[k]:
                for userTable in existConfig[k]['group']:
                    if exact:
                        #key = dict()
                        #key.setdefault('key', userTable['key'])
                        checkresult = self.jaguarExactCheckConfig(dut,k, userTable, None, userTable)
                    else:
                        checkresult = self.jaguarCheckOneTable(dut, k, userTable, gettablelist)
                    if not checkresult:
                        break
            else:
                if exact:
                    checkresult = self.jaguarExactCheckConfig(dut,k, existConfig[k], None, existConfig[k])
                else:
                    checkresult = self.jaguarCheckOneTable(dut, k, existConfig[k], gettablelist)

            if checkresult:
                logger.info("check %s table success!!!"%(k))
            else:
                logger.error("check %s table fail!!!"%(k))
                return False

        return checkresult

    def jaguarExactCheckConfig(self,dut,tableName,data,params,userconfig):
        '''检查配置 未完成
        '''
        self.__initlib(dut)
        retjson = self.getTable(dut, tableName, None, data, params)
        jsonData = self.transJsonToDict(dut, retjson)
        gettablelist = self.jaguarGetTableList(dut, jsonData)
        if gettablelist == None:
            logger.error("get table %s None!!!"%(tableName))
            return False
        checkresult = self.jaguarCheckOneTable(dut, tableName, userconfig, gettablelist)

        return checkresult

    def jaguarRunConfig(self, dut, config):
        '''运行jaguar配置字典

        关键字处在全局配置字典的最顶层:

        | 接口配置    | 'port' : { }   | 参考 Add Port Config 关键字帮助 |
        | 路由配置    | 'flow' : { } | 参考 Add Flow 关键字帮助 |
        '''
        self.__initlib(dut)
        logger.debug("Config jaguar !!!!!")

        for k in config.keys():
            '''
            当前只支持classify表，后续判断可以删除
            '''
            self.zxins[dut]['tables'].setdefault(k, dict())
#           if k == 'classify' or k == 'em_table' or k == 'meter_table':
            self.zxins[dut]['tables'][k] = copy.deepcopy(config[k])
            successNum = 1
            if 'group' in self.zxins[dut]['tables'][k]:
                successNum = len(self.zxins[dut]['tables'][k]['group'])
            retSucNum = self.postTable(dut, k, None, config[k])         
            if retSucNum != successNum:
                logger.debug("post %s table fail!, retSucNum=%s successNum = %s"%(config[k], retSucNum, successNum))
                logger.warn("post %s table fail!"%k)
                #raise AssertionError("post %s table fail!"%config[k])
                #return False
            else:
                logger.debug("post %s table success!"%config[k])
                logger.debug("post %s table success!"%k)
            self.__urlSleep()
        return True

    def jaguarClearConfig(self,dut,config=None):
        '''删除jaguar已经配置的基本配置
        '''
        self.__initlib(dut)
        itable = self.zxins[dut]['tables']
        if config == None:
            config = copy.deepcopy(itable)

        for k,v in config.items():
            if k == 'register':
                if 'group' in v:
                    for j in v['group']:
                        if j['key']['REG_ID'] == PAE_CSR_GP0_GLOBAL_CTRL_REG:
                            j['table']['REG_VALUE'] = 0x28b38
                        else:
                            j['table']['REG_VALUE'] = 0
                        retSucNum = self.postTable(dut, k,None, j)
                else:
                    if v['key']['REG_ID'] == PAE_CSR_GP0_GLOBAL_CTRL_REG:
                        v['table']['REG_VALUE'] = 0x28b38
                    else:
                        v['table']['REG_VALUE'] = 0
                    retSucNum = self.postTable(dut, k,None, v)          
            else:
                retSucNum = self.deleteTable(dut, k, v)
            if retSucNum < 1:
                logger.error("delete %s table fail!, retSucNum=%s"%(k, retSucNum))
            self.__urlSleep()
            
        self.zxins[dut]['tables'] = dict()
        return True
    
    def jaguarClearConfigAll(self,dut):
        '''删除jaguar已经配置的基本配置
        '''
        '''
        先在这里定义，后面看支不支持从设备获取
        '''
        '''
        configlist = ['source_mode1', 'source_mode2', 'input_port_rx', 'input_port_tx', 'classify', 'profile',
                      'key_template', 'key_mask', 'mc_group_rx', 'mc_group_tx', 'mc_leaf_rx', 'mc_leaf_tx', 'mc_leaf_action_rx',
                      'mc_leaf_action_tx', 'em_table', 'register', 'meter_table', 'meter_profile', 'output_meter', 'dest_mirror', 
                      'mirror_policy']
        '''
        configlist = ['source_mode1', 'source_mode2', 'input_port_rx', 'input_port_tx', 'classify', 'profile',
                'key_template', 'key_mask', 'mc_group_rx', 'mc_group_tx', 'mc_leaf_rx', 'mc_leaf_tx', 'mirror_policy']
              
        for table in configlist:
            self.deleteTable(dut, table, None)
            self.__urlSleep()

        return True

    def jaguarClearDut(self, dut, config = None):
        '''获取设备配置，然后再删除
        '''
        self.__initlib(dut)
        if not config:
            #不清除配置， 否则清空了其他人的配置
            return True
        #根据配置清

        return True


    def jaguarCmpPktField(self, dut, chkpkt, recvpkt):
        '''比较字典中的值
        '''
        self.__initlib(dut)

        if chkpkt == None:
            logger.error("chkpkt is None")
            return False

        if recvpkt == None:
            logger.error("recvpkt is None")
            return False            
  
        if (len(chkpkt) > len(recvpkt)):
            diffkey = chkpkt.keys() - recvpkt.keys()
            logger.error("chkpkt  %s is not in the recvpkt"%(diffkey))
            return False

        for k in chkpkt:
            if k == 'options':
                continue
            if type(chkpkt[k]) == str:
                chkpkt[k] = chkpkt[k].lower()
            if type(recvpkt[k]) == str:
                recvpkt[k] = recvpkt[k].lower()               
            if operator.ne(chkpkt[k], recvpkt[k]):
                logger.error("pkt field %s is diff, chkpkt is %s, recvpkt is %s"%(k, chkpkt[k], recvpkt[k]))               
                return False
        return True

    def jaguarGetPacketFieldsByLayerName(self,dut,layername,recvpkt):
        recvpkttmp = recvpkt
        while recvpkttmp.name != 'NoPayload':
            if layername == recvpkttmp.name:
                return recvpkttmp.fields
            recvpkttmp = recvpkttmp.payload
        return None

    def jaguarCheckPacket(self,dut,pkt,flow):
        '''检查报文和流是否匹配
        '''
        self.__initlib(dut)

        if pkt == 'None':
            logger.error("recvpkt is None")
        recvpktinfo = pkt
        if not isinstance(pkt,Ether):
            recvpktinfo = Ether(pkt)
        chkpktInfo = flow['chkpkt']
        
        #logger.info('[jaguarCheckPacket]' + pktinfo)
        recvhead = recvpktinfo
        chkhead = chkpktInfo

        #检查字段是否配置，并检查报文结果
        check_error = lambda x,y : \
            True if x != y else False

        #取出报文的name
        layername = chkhead.name

        while layername != 'NoPayload':
            #trex会将报文做签名处理，这里不校验payload
            if layername == 'Raw':
                return True
            
            #检查该报文头的正确性
            recvfields = self.jaguarGetPacketFieldsByLayerName(dut, layername, recvhead)
            if self.jaguarCmpPktField(dut, chkhead.fields, recvfields) == False:
                logger.error("layer %s check error!!!"%(layername))
                return False
            chkhead =  chkhead.payload
            layername = chkhead.name
            recvhead = recvhead.payload
        return True
       
    def jaguarCheckFlowByConfig(self,dut,tx,rx,flowconfig):
        self.__initlib(dut)
      
        n_packet = 0
        if 'n_packet_last' in flowconfig:
            n_packet = n_packet - flowconfig['n_packet_last']
        flowconfig['n_packet_last'] = n_packet
        logger.info("[jaguar]Check flow n_packet:%d tx:%d rx:%d"%(n_packet,tx,rx))
   
        if flowconfig.get('action', 'none') == 'drop':
            if int(tx) > 0 and int(rx) == 0:
                logger.debug("[jaguar] flow table success")
                return True
            else:
                raise AssertionError("[jaguar] flow table failed")
        else:
            #jaguar仿真场景没有杂包，严格校验
            #BuiltIn().should_be_true((int(rx) + 2  > n_packet/2) and (rx > 2), \
            #        "[ovs]flow table failed %d != %d"%(int(rx),int(n_packet)))
            BuiltIn().should_be_true((int(rx) + 2  > int(tx)), \
                    "[jaguar]flow check failed %d != %d"%(int(rx),int(tx)))
    

    def jaguarReload(self, dut,buf=False):
        '''重载所有的配置
        '''
        pass

    def jaguarBackup(self, dut):
        '''恢复当前配置
        '''
        if dut not in self.zxinsbk:
            self.zxinsbk[dut] = []
        if dut not in self.zxins:
            self.zxinsbk[dut].append({})
            return True
        self.zxinsbk[dut].append(copy.deepcopy(self.zxins[dut]))
        return True

    def jaguarResume(self,dut):
        '''恢复当前配置 -- 未实现
        '''
        if dut not in self.zxinsbk:
            return False
        if dut not in self.zxins:
            return False
        va = copy.deepcopy(self.zxins[dut])
        bk = self.zxinsbk[dut].pop()

        if va == bk:
            return True

        logger.info("jaguar Resume]start")
        for i in va.keys():
            if i in bk and va[i] == bk[i]:
                del va[i]
                del bk[i]
                continue
            if i not in bk:
                raise AssertionError("Can not find %s"%i)

            #删除相同的参数
            for j in va[i].keys():
                if j in bk[i] and va[i][j] == bk[i][j]:
                    del bk[i][j]
                    del va[i][j]
        #清除多余的参数
        self.jaguarClearConfig(dut,va)
        #配置被删除的参数
        self.jaguarRunConfig(dut,bk)
        logger.info("[jaguar Resume]end")

    def getRealPort(self,dut,port):
        return self.getPortId(dut,port)

if __name__ == '__main__':
    jaguarlib = Jaguar()
    info = jaguarlib.flowFraseRuleToDict(rule)
    pprint(info)
    dict = jaguarlib.flowTransToRule(info)
    pprint(dict)