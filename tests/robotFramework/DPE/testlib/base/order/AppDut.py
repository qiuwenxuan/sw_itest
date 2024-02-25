#!/usr/bin/python
# -*- coding: utf-8 -*-

import telnetlib , sys, re , copy
import time
import robot.errors
from robot.api import logger
from robot.libraries.Telnet import Telnet
from robot.libraries.BuiltIn import BuiltIn
from SSHLibrary import SSHLibrary
import requests

class Dutconnect(object):
    timeout = 120
    expect  = r"\S*$"
    lastdata = None      #最后一次输出结果
    cpulist = None
    lastshowrun = None
    docker = None
    
    def __init__(self,ip=None,port=22,username='',password=''):
        self.mngip = None
        self.who = None
        if ip != None:
            self.connect(ip,port,username,password)
    
    def __getResultList(self, ret=None):
        if ret == None:
            ret = self.lastdata
        buf = re.split(r"[\r\n]+",ret) #或使用ret.splitlines
        if len(buf) < 1:
            raise AssertionError("Get result error!")
        buf.pop()    #去除提示符
        return buf
        
    def connect(self,ip,port=22,username=None,password=None):
        self.ip = ip
        self.port = port
        self.docker = None
        if ip == None :
            return False
        self.conn = SSHLibrary(timeout=self.timeout)
        self.conn.open_connection(self.ip,port=self.port)
        self.conn.login(username,password)
        if self.docker != None:
            #self.conn.write("docker exec -it %s bash"%docker)
            #self.conn.set_client_configuration(prompt="#")
            #self.conn.read_until_regexp(r"root@\w*:/#")
            pass
        else:
            self.who = self.conn.execute_command("whoami")
            logger.info("%s : %s"%(self.ip,self.who))
        #self.conn.DEFAULT_LOGLEVEL='WARN'
        return True

    def isRoot(self):
        return "root" == self.who

    def process(self, order):
        order = str(order)
        order = re.sub(r'\s*$',"",order)
        if self.docker != None:
            #self.conn.write(order)
            #ret = self.conn.read_until_regexp(r"root@\w*:/#")
            #self.conn.write("echo $?")
            #lastret = self.conn.read_until_regexp(r"root@\w*:/#")
            #当执行错误，就报错
            #如果需要捕获错误，可以通过try catch 获取 Exception 类型错误
            #retid = re.search(r"^(\d+)",lastret)
            #if retid:
            #    if int(retid.group(1)) != 0:
            #        raise AssertionError("[ERROR ID]",retid.group(1))
            ret,rc = self.conn.execute_command("docker exec -t %s %s"%(self.docker,order),return_rc=True)
            if rc != 0:
                raise AssertionError("[ERROR ID]",rc)
        else:
            if self.isRoot():
                ret,ret_err,rc = self.conn.execute_command(order,return_rc=True,return_stderr=True)
            else:
                ret,ret_err,rc = self.conn.execute_command(order,sudo=True,return_rc=True,return_stderr=True)
            if rc != 0:
                raise AssertionError("[ERROR ID]",str(rc), order,ret_err)
        self.lastdata = ret
        return ret
    
    def pmdConnect(self):
        self.conn.write("screen -O -d -r testpmd\n")
        self.conn.set_client_configuration(prompt='testpmd>',width=200,height=1000)
        for i in range(0,10): #等待运行完成，输出信息结束
            something = self.conn.read(delay=2)
            if something == None or len(something) <= 0:
                break
        self.conn.write('\r\n')
        for i in range(0,2):
            something = self.conn.read(delay=1)
            if 'testpmd>' in something:
                break
        something = self.conn.read()
        if len(something) >0 : logger.info('[pmdProcess] something error ]'+something)
        self.conn.write(' ')
        something = self.conn.read_until_prompt()
        if something == None or len(something) <= 0 or 'testpmd>' not in something: 
            raise AssertionError('[pmdProcess] testpmd process error!')

    def pmdProcess(self,order):
        order = str(order)
        order = re.sub(r'\s*$',"",order)
        something = self.conn.read()
        something = self.conn.read()
        if len(something) >0 : logger.info('[pmdProcess] pre ]'+something)
        self.conn.write(order)
        time.sleep(1)
        logger.info('[pmdProcess]'+order)
        ret = self.conn.read_until_prompt(strip_prompt=True)
        ret = re.sub(r"\033\[..","",ret)
        ret = re.sub(r"202\d-\d+-\d+ \d+\:.*[\r\n]+","",ret)  #删除打印的日志
        logger.debug('[pmdProcess]'+ret)
        self.lastdata = ret
        return ret

    def close(self):
        if self.conn == None :
            return True
        self.conn.close()
        self.conn = None
        return True
    
    def getip(self):
        return self.ip
    
    def getPrompt(self):
        if self.lastdata == None:
            self.process('')
        retmp = re.search(r'([\S]+#)\s*$|(Router[\S]+)#\s*$',self.lastdata)
        if retmp:
            return retmp.group(1)
        raise AssertionError("DUT:Can't find dut Prompt!")
        

class AppDut(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    dutins = {}
    #终端对应的设备类型
    devtype = {
        "linux"   : "terminal",
        "sonic"   : "net",
        "zxros"   : "net",
        "sonic"   : "net",
        "testpmd" : "ovs",
        "ovs"     : "ovs"
    }
    def __init__(self):
        pass
    
    def __checkdut(self, dut):
        if dut not in self.dutins:
            raise AssertionError('Dut(%s) is not connect!'%(dut))
    
    def dutConnect(self,dut,ip,port,username='zte',password='zte',type='linux',docker=None):
        port = int(port)
        logger.debug("1 Connect to %s %d %s"%(ip,port,username))
        username = str(username)
        password = str(password)
        if dut not in self.dutins:
            self.dutins[dut] = {}
            self.dutins[dut]['ip'] = ip
            self.dutins[dut]['port'] = port
            self.dutins[dut]['username'] = username
            self.dutins[dut]['password'] = password
            self.dutins[dut]['type'] = type
            self.dutins[dut]['oam'] = Dutconnect(ip,port,username,password)
    
    def dutConnectConfig(self, dut,config=None):
        '''连接设备
        '''
        if dut in self.dutins and 'oam' in self.dutins:
            return

        if config != None:
            self.dutins[dut] = copy.deepcopy(config)

        self.dutins[dut]['oam'] = Dutconnect(self.dutins[dut]['ip'],self.dutins[dut]['port'], \
                                                self.dutins[dut]['username'], \
                                                self.dutins[dut]['password'])

    def dutSetConfig(self,dut,config):
        self.dutins.setdefault(dut,config)

    def dutGetConfig(self,dut):
        self.__checkdut(dut)
        return self.dutins[dut]

    def dutGet(self,dut):
        self.__checkdut(dut)
        return self.dutins[dut]['oam']

    def dutGetType(self,dut):
        self.__checkdut(dut)
        return self.dutins[dut]['type']

    def dutGetDevType(self,dut):
        self.__checkdut(dut)
        return self.devtype.get(self.dutins[dut]['type'],"UNKNOW")

    def process(self,dut,order):
        self.__checkdut(dut)
        buf = self.dutins[dut]['oam'].process(order)
        return buf

    def pmdConnect(self,dut):
        self.__checkdut(dut)
        self.dutins[dut]['oam'].pmdConnect()

    def pmdProcess(self,dut,order):
        self.__checkdut(dut)
        return self.dutins[dut]['oam'].pmdProcess(order)

    def getPrompt(self, dut):
        self.dutins[dut]['oam'].getPrompt(dut)

    def reboot(self,dut,shell):
        ''' ushell 进入admin模式
        '''
        self.__checkdut(dut)
        self.dutins[dut][shell].reboot()
        
    def getErrorId(self, err):
        if isinstance(err,robot.errors.ExecutionFailed):
            pass
        #通过Exception抓取err
        if "[ERROR ID]" not in str(err.full_message):
            return None
        msg = eval(err.full_message)
        if isinstance(msg,tuple):
            if msg[0] == '[ERROR ID]':
                return msg[1:]
        return None

    def configMode(self,dut):
        return
        
    def rootConfigMode(self,dut):
        return
        
    def getConnet(self,dut):
        self.__checkdut(dut)
        return self.dutins[dut]['oam'].conn

    def setDebugShowrunOn(self):
        pass

    def setDebugShowrunOff(self):
        pass

    def isTestPMD(self,dut):
        self.__checkdut(dut)
        return self.dutins[dut]['type']=='testpmd'
        
