#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
日期 :  2015-8-21

作者 ： APP RF小组
'''

import os, sys, traceback, re, time
from copy import copy
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

class AppDevice(object):
    '''App关联模块组织
    
    顶层类， 不能被其他模块引用
    '''
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    dutlib = None
    isClear = True                        #为0不清配置，为1清配置
    isReload = False

    def __init__(self):
        self.sonic = None
        self.zxros = None
        self.cisco = None
        self.linux = None

    def appArpShow(self, dut): self.appRun(sys._getframe().f_code.co_name,dut)

    def __initlib(self):
        if self.dutlib == None:
            self.dutlib = BuiltIn().get_library_instance('AppDut')
        if self.linux == None:
            self.linux = self.__loadlib('Linux')
            self.ovs = self.__loadlib('Ovs')
            self.sonic = self.__loadlib('Sonic')
            self.cisco = self.__loadlib('Cisco')
            self.zxros = self.__loadlib('Zxros')
            self.tester = self.__loadlib('Tester')
            self.isClear = self.appIsClear()
            self.isReload = self.appIsReload()
            
    def __loadlib(self, name):
        try:
            lib = BuiltIn().get_library_instance(name)
            logger.info("Load lib %s OK!"%name)
            return lib
        except Exception:
            #logger.info("Load lib %s Error!"%name)
            pass
        return None
    
    def __getModlist(self, config=None):
        if config == None:
            return self.modlist
        self.modlist = None
        if isinstance(config,list):
            self.modlist = copy(config)
        return self.modlist

    def __libRun(self,lib,name,*args):
        '''检查命令执行错误ID
        '''
        pre = ""
        if(lib == self.sonic): pre = "sonic"
        elif(lib == self.zxros): pre = "zxros"
        elif(lib == self.cisco): pre = "cisco"
        elif(lib == self.linux): pre = "linux"

        if hasattr(lib,pre+name):
            return getattr(self.sonic,pre+name.capitalize())(*args)
        elif hasattr(self.linux,name):
            return getattr(self.linux,name)(*args)

        AssertionError("Can't find %s in %s."%(name,pre.upper()))
        return None

    def __getDevLibs(self):
        libs = list()
        if self.sonic : libs.append(self.sonic)
        if self.zxros : libs.append(self.zxros)
        if self.cisco : libs.append(self.cisco)
        if self.linux : libs.append(self.linux)
        return libs

    def __getDevLib(self,dut):
        t = self.dutlib.dutGetType(dut)
        if(t == "sonic"): return self.sonic
        if(t == 'zxros'): return self.zxros
        if(t == 'cisco'): return self.cisco
        if(t == 'linux'): return self.linux
        AssertionError("Can't find lib for %s."%dut)
        return None

    def AppGetMacByIp(self, ip):
        '''通过IP获取到mac和设备名
        ret = ('dut1','001f.5310.521c')
        '''
        self.__initlib()
        for lib in self.__getDevLibs() :
            dut,mac = self.__libRun(lib,"getMacByIp",ip)
            if dut:
                return (dut,mac)
        return(None,None)

    def appIsClear(self):
        '''获取是否设定了${clear}标记
        '''
        value = BuiltIn().get_variable_value('${clear}','true').lower()
        if value == 'false' or value == 'no':
            return False
        return True
    
    def appIsReload(self):
        '''获取是否设定了${reload}标记
        '''
        value = BuiltIn().get_variable_value('${reload}','false').lower()
        if value != 'false' and value != 'no':
            return True
        return False
    
    def appRunConfig(self,dut,config):
        '''运行配置文件
        
        详细内容可以参考 ：config-example.py
        
        '''
        logger.info("===========app runconfig==================")
        self.__initlib()
        self.dutlib.configMode(dut)
        if self.isReload:
            self.appReloadConfig(dut)
            return True
        if(self.dutlib.dutGetType(dut) == "linux"):
            if self.linux: self.linux.linuxRunConfig(dut,config)
        return True    

    def appReloadConfig(self, dut,buf=False):
        '''获取设备的配置
        
            buf    是否从dut缓冲中重载
        '''
        self.__initlib()
        if(self.dutlib.dutGetType(dut) == "linux"):
            self.linux.linuxReload(dut,buf)
        
    def appClearConfig(self,dut,config=None):
        '''清空设备的配置
        
        在reload模式下，不清除
        '''
        self.__initlib()
        self.dutlib.configMode(dut)
        #如果设定的reload， 在最后不要清除配置
        if (not self.isClear) or self.isReload:
            raise AssertionError("Set not clear configure")
        if(self.dutlib.dutGetType(dut) == "linux"):
            if self.linux : self.linux.linuxClearConfig(dut,config)
            
        return True

    def appClearDut(self, dut, config = None):
        '''获取设备配置，然后再删除
        '''
        self.__initlib()
        if not config:
            #不清除配置， 否则清空了其他人的配置
            return True
        #根据配置清
        if(self.dutlib.dutGetType() == "linux"):
            if self.linux : self.linux.linuxClearDut(dut,config)
        return True

    def appReload(self, dut,buf=False):
        '''重载所有的配置
        '''
        self.__initlib()
        if(self.dutlib.dutGetType(dut) == "linux"):
            if self.linux : 
                return self.linux.linuxReload(dut,buf)
        return False

    def appBackup(self, dut):
        '''恢复当前配置
        '''
        self.__initlib()
        if(self.dutlib.dutGetType(dut) == "linux"):
            if self.linux : 
                return self.linux.linuxBackup(dut)
        return False
    
    def appResume(self,dut):
        '''恢复当前配置 -- 未实现
        '''
        self.__initlib()
        if(self.dutlib.dutGetType(dut) == "olinuxs"):
            if self.linux : 
                return self.linux.linuxResume(dut)
        return False

    def appClearAll(self,dut,config=None):
        '''
        获取设备的nat配置，并全部删除
        '''
        self.__initlib()
        #一般会在使用前全清， 所以这个不应当清
        #if not self.isClear:  
        #    raise AssertionError("set Can't clear configure")
        
        #在Reload的时候， 不清数据
        if self.isReload:
            return True
        if(self.dutlib.dutGetType() == "linux"):
            if self.linux : self.linux.linuxClearDut(dut,config)
    
    def appRun(self,name,dut,*args):
        '''检查命令执行错误ID
        '''
        self.__initlib()
        lib = self.__getDevLib(dut)
        ret = self.__libRun(lib,name,dut,*args)
        return ret

    def appRunKeyword(self,name,dut,*args):
        '''执行keyword
        '''
        self.__initlib()
        if(self.dutlib.dutGetType() == "linux"):
            ret = BuiltIn().run_keyword("linux."+name, dut, *args)
        return ret

    def appRunKeywordError(self,id,name,*args):
        '''检查命令执行错误ID
        '''
        self.__initlib()
        opid = []
        try:
            self.dutlib.setDebugShowrunOff()
            BuiltIn().run_keyword(name, *args)
        except Exception as err:
            opid = self.dutlib.getErrorId(err)
            if not opid:
                raise AssertionError("Expected error did not occur.")
        finally:
            self.dutlib.setDebugShowrunOn()
        if str(id) not in opid:
            raise AssertionError("Expected error '%d' but got '%s'."
                                 % (int(id), str(opid)))
        logger.debug("FIND ERROR ID %d [OK]"%(int(id)))
        return True
    
    def appWaitUntilRunKeywordSuccess(self,maxtime,step,name,*args):
        u'''== 功能 ==
        等待执行关键字是否成功
        maxtime 为最长等待时间 单位 s
        step    为检查失败,下一次查询等待时间
        name    检查关键字或者函数(该关键字检查结果失败可以断言 若用返回值表示失败，需要返回False)
        '''
        self.__initlib()
        cur = 0
        maxtime = int(maxtime)
        step = int(step)
        while(cur<maxtime):
            try:
                ret = BuiltIn().run_keyword(name, *args)
                cur +=step
                if(ret==False):
                    if(cur>=maxtime):
                        raise AssertionError("After waiting(%d s), run Keyword still don't succeed"%cur)
                else:
                    return
            except Exception as err:
                cur +=step
                if(cur>=maxtime):
                    raise AssertionError("After waiting(%d s), run Keyword still don't succeed"%cur)
            time.sleep(step)
        return
