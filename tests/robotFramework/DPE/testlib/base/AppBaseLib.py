#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, re , time , random, struct
import binascii
__path = os.path.realpath(os.path.join(__file__,'..')) 
if __path not in sys.path:sys.path.append(__path)

from IPy import IP
from robot.api import logger
import IPy

def appSubNet(ip,mask):
    #根据IP和掩码获取子网
    #1.1.1.1 255.255.255.0 -> 1.1.1.0 255.255.255.0
    #1.1.1.1 24 -> 1.1.1.0 255.255.255.0
    ip =IP(ip).make_net(mask)
    return str(ip.net()),str(ip.netmask())

def appIpEx(ip,mask):
    #1.1.1.1 255.255.255.0 -> 1.1.1.1/24
    if ip == None or mask == None:
        return None
    masklen = IP(1).make_net(mask).prefixlen()
    return ip+'/'+str(masklen)

def appIpPrefix(ip,mask):
    ip = IP(ip).make_net(mask)
    return str(ip)

def appIpPrefixLen(mask):
    masklen = IP(1).make_net(mask).prefixlen()
    return masklen

def appIpExGetIp(ip):
    #1.1.1.1/24 -> 1.1.1.1
    ipret = None
    ret = re.search(r"(.+)\/(.+)", ip)
    if ret :
        ipret = ret.group(1)
    return ipret

def appIpExGetNet(ip):
    #1.1.1.1/24 -> 1.1.1.0/24
    #IP(net).strNetmask() 1.1.1.0/24 -> 255.255.255.0
    return str(IP(ip,make_net=True))

def appIsIpv6(ip):
    return ':' in ip

def appWildcardMask(istr):
    #获取反掩码
    #1.1.1.0/0.0.0.255 -> 1.1.1.1,0.0.0.0
    #1.1.1.0/8         -> 1.1.1.1,0.0.0.255
    #1.1.1.1/0         -> 1.1.1.1,0.0.0.0
    #1.1.1.0/32        => 1.1.1.0,255.255.255.255
    
    ret = re.search(r"(\d+\.\d+\.\d+\.\d+)\/(\d+\.\d+\.\d+\.\d+)",istr)
    if ret:
        return ret.group(1),ret.group(2)
    ret = re.search(r"(\d+\.\d+\.\d+\.\d+)\/(\d+)",istr)
    if ret:
        mask = int(ret.group(2))
        if mask <0 or mask > 32: raise AssertionError('Error MASK %d'%mask)
        mask = (1<<mask) - 1
        mask = '.'.join([str((mask>>(i*8))&0xff) for i in range(3,-1,-1)])
        return ret.group(1),mask
    return None,None


def get_ip_list(begin_ip, count, netmask):
    ip_list = [] #用来存放生成的IP地址
    j = 0
    begin_ip = IPy.IP(begin_ip)
    ip_list.append(str(begin_ip)) #将第一个地址放入ip_列表中
    if begin_ip.version() == 4:
        for i in range(count):
            ip = IPy.IP(begin_ip)
            new_ip = IPy.IP(ip.ip + 2 ** (32 - netmask))
            begin_ip =  str(new_ip)
            ip_list.append(str(begin_ip))
    else:
        for i in range(count):
            ipv6 = IPy.IP(begin_ip)
            new_ipv6 = IPy.IP(ipv6.ip + 2 ** (128 - netmask-4))
            begin_ip =  str(new_ipv6)
            ip_list.append(str(begin_ip))
    return ip_list


def isMac(string):
    preg = re.compile('^([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}$')
    ret = preg.match(string)
    if ret is None:
        return False
    else:
        return True

def macToInt(mac):
    '''MAC转INT'''
    mac = mac.replace(":", "")
    return int(mac, 16)

def calcMacNum(mac_start, mac_end):
    mac_start = mac_start.upper()
    mac_end = mac_end.upper()
    ret = macToInt(mac_end) - macToInt(mac_start) + 1 
    if ret < 0: 
       ret = 0 
    return ret

def intToMac(intMac):
    # mac地址每段都是2位 不足位数补0 例如：f:23:54 => 0f:23:54
    j = 0
    if int(len(hex(intMac)) / 2) < 6:
        j = 6 - int(len(hex(intMac)) / 2)
    tmpStr = ''
    while j > 0:
        tmpStr += '00'
        j = j - 1

    if len(hex(intMac)) % 2 != 0:
        hexStr = '0{0:X}'.format(intMac)
    else:
        hexStr = '{0:X}'.format(intMac)

    hexStr = tmpStr + hexStr

    i = 0
    ret = ""

    while i <= len(hexStr) - 2:
        if ret == "":
            ret = hexStr[i:(i + 2)]
        else:
            ret = "".join([ret, ":", hexStr[i:(i + 2)]])
        i = i + 2
    return ret

def getMatchMac(mac):
    '''
    00:0B:C4:A8:22:B0 -> 00:0B:C4:A8:22:B0
    00:0B:C4:A8:22:B0/ff:ff:ff:ff:ff:ff->00:0B:C4:A8:22:B0
    00:0B:C4:A8:22:B0/ff:ff:ff:ff:ff:00->00:0B:C4:A8:22:01
    '''
    matchMac = mac
    ret = re.search(r"(.+)\/(.+)", mac)
    if ret:
        macNet = ret.group(1)
        macPrefix = ret.group(2)
        matchMacInt = macToInt(macNet) & macToInt(macPrefix)
        if macToInt(macPrefix) != 0xffffffffffff:
            matchMac = intToMac(matchMacInt + 1)
        else:
            matchMac = intToMac(matchMacInt)
    return matchMac

def getMatchIpAddr(ip):
    '''
    1.1.1.1 -> 1.1.1.1
    1.1.1.1/24->1.1.1.0
    1.1.1.1/25->1.1.1.128
    '''
    matchIp = ip
    ret = re.search(r"(.+)\/(.+)", ip)
    if ret:
        matchIpNet = appIpExGetNet(ip)
        matchIp = appIpExGetIp(matchIpNet)
    return matchIp   

def getMatchIpv6Addr(ip):
    '''
    1::1/64->1::1
    1::1->1::1
    '''
    matchIp = ip
    ret = re.search(r"(.+)\/(.+)", ip)
    if ret == None:
        return matchIp 
    if appIsIpv6(ret.group(2)):
        mask = IP(ret.group(2)).strNetmask()
        mask.replace("/", "")
        mask =int(mask) 
    else:
        mask = int(ret.group(2))
 
    ipv6_list  = get_ip_list(begin_ip = ret.group(1), count=10, netmask=int(ret.group(2)))
    return ipv6_list[1]
     

def getNextMac(macAddr, n):
    '''
    获取下N个MAC
    '''
    return intToMac(macToInt(macAddr) + n)

def appFindInit(buf,splite,type='nouse'):
    '''列表查找初始化
    
    '''
    info = dict()
    info["list"] = buf
    info["max"] = len(buf)
    info["cur"] = 0
    info["splite"] = splite
    info["type"] = type
    return info    
    
def appFindNext(info):
    '''列表查找获取结果
    '''
    result = []
    if "splite" not in info:
        return []
    blank = None
    find = 0
    while(info['cur'] < info['max']):
        cur = info['list'][info['cur']]
        info['cur'] += 1
        if find:
            result.append(cur)
            ret = re.search(r"^(\s*)\$\s*$",cur)
            if ret:
                if(len(ret.group(1)) == len(blank)):
                    break
        if re.search(info['splite'],cur):
            result.append(cur)
            find = 1
            ret = re.search(r"^(\s*)",cur)
            if ret:
                blank = ret.group(1) 
    return result

def appTransformToDict(*args,**argds):
    '''输入转换为字典形式
    | -dut=dut1 | -intf=fei-0/1/1/1 | -vrid=1 | -accept=enable |
    | -dut | dut1 | -intf | fei-0/1/1/1 | -vrid | 1 | -accept | enable |

    |  返回  config = {
    |           'dut'    : 'dut1',
    |           'intf'   : 'fei-0/1/1/1',
    |           'vrid'   : '1',
    |           'accept' : 'enable',
    |           }
    |
    '''
    ret = dict()
    key = None
    #logger.info(str(args)) 
    for i in args:
        if len(i) >= 0 and i.startswith('-'):
            i = i.lstrip('-').lower()
            if '=' in i:
                tmp = re.search(r'(\S+)=(\S*)',i)
                if tmp:
                    key = tmp.group(1).lower()
                    val = tmp.group(2)
                    ret[key] = val if len(val) > 0 else None
            else:
                ret[i] = None
        else:
            if key != None:
                ret[key] = i
    for k,v in argds.items():
        ret[k.lstrip('-').lower()] = v
    
    if 'no' in ret : ret['no'] = 'no'
    
    logger.info(str(ret))
    return ret

def parseTime(timestr):
    try:
        return int(timestr)
    except:
        hour = 0
        minute = 0
        second = 0
        match = re.search(r'(\d+)h',timestr)
        if match:
            hour = int(match.group(1))
        match = re.search(r'(\d+)m',timestr)
        if match:
            minute = int(match.group(1))
        match = re.search(r'(\d+)s',timestr)
        if match:
            second = int(match.group(1))
        return (hour*60+minute)*60+second

def randIp():
    choices = range(1,224)
    choices.remove(127)
    return "%s.%s.%s.%s" % (random.choice(choices),random.randint(0,255),random.randint(0,255),random.randint(0,255))

def randIpWithPrefix():
    choicesMac = range(1,255)
    choicesPrefix = range(8,32)
    return "%s.%s.%s.%s/%s" % (random.choice(choicesIp),random.randint(0,255),random.randint(0,255),random.randint(0,255),random.choice(choicesPrefix))

def randMacWithPrefix():
    '''
    排除全0的情况
    '''
    return "%s:%s:%s:%s:%s:%s/%s:%s:%s:%s:%s:%s" % (random.randint(1,255),random.randint(0,255),random.randint(0,255),random.randint(0,255),random.choice(choicesPrefix))
    
def intToIP(num):
    if not isinstance(num,int):
        num = int(num)
    return '.'.join([str(num/(256**i)%256) for i in range(3,-1,-1)])

def natIpPrefix(ip,mask):
    ip =IP(ip).make_net(mask)
    return str(ip)


def ipToInt(ip):
    if not isinstance(ip,str):
        ip = str(ip)
    return sum([256**j*int(i) for j,i in enumerate(ip.split('.')[::-1])])

def hexToIP(num):
    ip1 = int(num[-len(num):-6], 16)
    ip2 = int(num[-6:-4], 16)
    ip3 = int(num[-4:-2], 16)
    ip4 = int(num[-2:], 16)
    return "%s.%s.%s.%s" % (ip1,ip2,ip3,ip4)

def ipToHex(ip):
    return '0x'+''.join([str(hex(int(i))).strip('0x').zfill(2) for i in ip.split('.')])

def ipToBin(ip):
    return ''.join([bin(int(i))[2:].zfill(8) for i in ip.split('.')])

def binToIP(num):
    return '%s.%s.%s.%s' % (int(num[:8],2),int(num[9:16],2),int(num[17:24],2),int(num[25:],2))

def compareIp(sip,eip):
    if ipToInt(sip)>ipToInt(eip):
        return 1
    elif ipToInt(sip)<ipToInt(eip):
        return -1
    else:
        return 0

def calcIpcnt(sip,eip):
    return ipToInt(eip)-ipToInt(sip)+1

def calcEndIp(sip,num):
    #if (int(num) < 0):
    #    endip = str(IP(IP(sip).int()+int(num)))
    #else:
    endip = str(IP(IP(sip).int()+int(num)))
    match = re.search("\/(\d+)",sip)
    if match:
        endip = endip+'/'+match.group(1) #ipv6
    return endip    
    #return intToIP(ipToInt(sip)+num-1)

def calcBaseIp(ip,masklen):
    return binToIP(ipToBin(ip)[:masklen]+'0'*(32-masklen))

def ipToSet(ipstr):
    if '-' in ipstr:
        sip,eip = ipstr.split('-')
        return set(range(ipToInt(sip),ipToInt(eip)+1))
    elif '/' in ipstr:
        sip = IP(ipstr)[0]
        eip = IP(ipstr)[-1]
        return set(range(ipToInt(sip),ipToInt(eip)+1))
    else:
        return set(ipstr)  

def trimNumWithComma(buf):
    while 1:
        match = re.search(r"\d,\d", buf)
        if match:
            match = match.group()
            buf = buf.replace(match, match.replace(",", ""))
        else:
            break
    return buf
        
class IPPool(object):    
    def __init__(self,sip,eip):
        self.freepool = [ipToInt(sip),ipToInt(eip)]
        self.usedpool = []
        self.freecnt = calcIpcnt(sip,eip)
        self.usedcnt = 0
        
    def allocIP(self,ipcnt):
        sip = None
        eip = None
        if not isinstance(ipcnt,int):
            ipcnt = int(ipcnt)
        if ipcnt <= self.freecnt:
            sip = self.freepool[0]
            eip = self.freepool[0]+ipcnt-1
            self.freepool[0] = self.freepool[0]+ipcnt
            self.freecnt -= ipcnt
            for ip in range(sip,eip+1):
                if ip not in self.usedpool:
                    self.usedpool.append(ip)
                    self.usedcnt += 1
            return intToIP(sip),intToIP(eip)        
        else:
            logger.debug("ipcnt=%s,freecnt=%s" % (ipcnt,self.freecnt))
            raise AssertionError("[pool]IP pool has used up!")
        return sip,eip

    def allocIPRange(self,sip,eip):
        sip = ipToInt(sip)
        eip = ipToInt(eip)
        for ip in range(sip,eip+1):
            if ip not in self.usedpool:
                self.usedpool.append(ip)
                self.usedcnt += 1

    def allocIPRangeWithMask(self,baseip,mask):
        for ip in IP('%s/%s' % (baseip,mask)):
            ip = ipToInt(ip)
            if ip not in self.usedpool:
                self.usedpool.append(ip)
                self.usedcnt += 1
                
    def returnIPRange(self,sip,eip):
        sip = ipToInt(sip)
        eip = ipToInt(eip)
        for ip in range(sip,eip+1):
            if ip in self.usedpool:
                self.usedpool.remove(ip)
                self.usedcnt -= 1

    def returnIPRangeWithMask(self,baseip,mask):
        for ip in IP('%s/%s' % (baseip,mask)):
            ip = ipToInt(ip)
            if ip in self.usedpool:
                self.usedpool.remove(ip)
                self.usedcnt -= 1
                
    def checkIPInUse(self,sip,eip=None):
        sip = ipToInt(sip)
        if eip:
            eip = ipToInt(eip)
        else:
            eip = sip
        for ip in range(sip,eip+1):    
            if ip in self.usedpool:
                return True
        return False

class cgnrandom(object):
    ''' 随机产生字符串和数值
    
        已经产生的关键字， 将返回之前随机的值
    '''
    def __init__(self,min=None,max=None):
        self.__mykey = dict()
        self.__str = 'XX'
        self.__ipset = set()
        self.minint  = 1
        self.maxint  = 63   #最大实例数是63
        self.minstr  = 1
        self.maxstr  = 16
        if min != None:
            self.minint  = min
            self.minstr  = min
        if max != None:
            self.maxint  = max
            self.maxstr  = max
        num   = '1234567890'
        low = 'abcdefghijklmnopqrstuvwxyz'
        upp = low.upper()
        #other = '*()[]&$@'
        self.__str = num + low + upp #暂不加特殊字符+ other
        pass
    
    def __getstr(self, name,reset):  
        key = name
        mat = random.randint(self.minstr,self.maxstr)
        ret = re.search(r"\*(\d+)(\*.+)",name)
        if ret:
            key = ret.group(2)
            mat = random.randint(1,int(ret.group(1)))
        if not reset and key in self.__mykey:
            return self.__mykey[key]
        self.__mykey[key] = ''.join(random.sample(self.__str,mat))
        logger.info("[random] string [%s] = %s"%(key,self.__mykey[key]))
        return self.__mykey[key]
    
    def __getnum(self, name,reset):
        key = name
        minint = self.minint
        mat    = self.maxint
        ret = re.search(r"\$(\d+)(\$.+)",name)
        if ret:
            key = ret.group(2)
            mat = int(ret.group(1))
        if not reset and key in self.__mykey:
            return self.__mykey[key]
        num = None
        for i in range(1,10) :
            num = random.randint(minint,mat)
            
            if num in self.__mykey.values():
                continue
            break
        if num == None:
            raise AssertionError("Can not find a number!")
        logger.info("[random] string [%s] = %d"%(key,num))
        self.__mykey[key] = num
        return self.__mykey[key]

    def __getip(self, name,reset):
        key = name
        ret = re.search(r"\@(ipv\d)\.(\d+)(\@.+)",name)
        num = self.minint
        randsip = None
        baseip = None
        if ret:
            iptype = ret.group(1)
            num = int(ret.group(2))
            key = ret.group(3)
        if not reset and key in self.__mykey:
            return self.__mykey[key]
        for i in range(1,10) :
            if 'range' in key:
                randsip = randIp()
                randeip = calcEndIp(randsip,num)
                value = "%s-%s" % (randsip,randeip) 
            elif 'prefix' in key:
                if num in range(20,33):
                    masklen = num
                else:
                    masklen = random.randint(20,33)
                baseip = calcBaseIp(randIp(),masklen)
                value = "%s/%s" % (baseip,masklen)

            if ipToSet(value) & self.__ipset:
                break
        
        if not randsip and not baseip:
            raise AssertionError("Can not find a ip!")
        logger.info("[random] string [%s] = %s" % (key,value))
        self.__mykey[key] = value
        self.__ipset = self.__ipset | ipToSet(value)
        return self.__mykey[key]
        
    def __getvalue(self, name,reset=False):
        if isinstance(name,int):
            return name
        if not name:
            return name
        #字符串
        if (str(name))[0] == '*':
            return self.__getstr(name,reset)
        if (str(name))[0] == '$':
            return self.__getnum(name,reset)
        if (str(name))[0] == '@':
            return self.__getip(name,reset)
        return name
    
    def __getitem__(self, name):
        return self.__getvalue(name)
    
    def reset(self, value):
        '''重新获取一个新值
        '''
        return self.__getvalue(value,reset=True)
    
    def get(self, value):
        '''根据值，来获取原始的key
        '''
        for k,v in self.__mykey.items():
            if value == v:
                return k
        return value
        
#***********************************************
#得到报文信息
#入参: $block     报文内容
#      $time      报文时间
#      $timestart 首包时间
#返回: %info      报文解析信息
#***********************************************
def getPacketInfo(block,time=0,timestart=0):
    info = dict()
    info["TIME"] = time
    info["STARTTIME"] = timestart
    stand = 0
    type = None
    if (len(block) < 14) :
        return info
    
    try:
        info["MACDEST"] = block[0:6]
        info["MACSRC"]  = block[6:12]
        (info["MACTYPE"],) = struct.unpack(">H",block[12:14])
        info["2"] = stand
        type = info["MACTYPE"]
        #DPrint(sprintf"MAC : %#.4x, %d",$type,$stand);
        stand = 14
        if(type == 0x8100): #VLAN
            (tcid,type) = struct.unpack("nn",block[stand:stand+4])
            # Break down VLAN tag TCI into: PCP, CFI, VID
            info["VLAN.PCP"] = tcid & 0xE000 >> 13
            info["VLAN.CFI"] = tcid & 0x1000 >> 12
            info["VLAN.VID"] = tcid & 0x0FFF
            info["VLANTYPE"] = type
            info["VLAN"] = stand
            #DPrint(sprintf"VLAN : %#.4x, %d",$type,$stand);
            stand += 4
    except Exception:
        pass
    
    info["TYPE3"] = type
    info["3"]     = stand
    if(type == 0x0800):
        info["TYPE3EXT"] = "IPV4"
        info.update(getIPInfo(block,stand))
    elif(type == 0x86DD):
        info["TYPE3EXT"] = "IPV6"
        info.update(getIPInfo(block,stand))
    elif(type == 0x0806):
        info["TYPE3EXT"] = "ARP"
    else:
        return info
    return info

#***********************************************
#得到报文信息
#入参: $block           报文内容
#      $startstand      IP开始位置
#      $head            IP报文类型
#返回: %info      报文解析信息
#***********************************************
def getIPInfo(block,stand=0,head=''):
    info = dict()
    type = 0
    #避免解析异常 , 需要使用try
    tmp, = struct.unpack("B",block[stand:stand+1])
    info["IP.VERSION"] = (tmp & 0xF0)>>4
    type = info["IP.VERSION"]
    if len(head) > 0:
        head += "."
    else:
        head = ""
    info[head+"3"] = stand
    #DPrint(sprintf"TYPE3 : %#.4x, %d",type,stand);
    if(type == 4):
        info[head+"TYPE3EXT"] = "IPV4"
        tmp, = struct.unpack("B",block[stand:stand+1])
        info[head+"IP.VERSION"] = (tmp & 0xF0)>>4
        info[head+"IP.HEADLEN"] = (tmp & 0x0F)*4
        info[head+"IP.LEN"],      = struct.unpack(">H",block[stand+2:stand+4])
        info[head+"IP.ID"],       = struct.unpack(">H",block[stand+4:stand+6])
        info[head+"IP.TTL"],      = struct.unpack("B",block[stand+8:stand+9])
        info[head+"IP.TYPE"],     = struct.unpack("B",block[stand+9:stand+10])
        info[head+"IP.CHECKSUM"], = struct.unpack(">H",block[stand+10:stand+12])
        info[head+"IP.SRCBIN"]    = block[stand+12:stand+16]
        info[head+"IP.DESTBIN"]   = block[stand+16:stand+20]
        info[head+"IP.SRC"]      = str(IP("0x" + binascii.b2a_hex(info[head+"IP.SRCBIN"])))
        info[head+"IP.DEST"]     = str(IP("0x" + binascii.b2a_hex(info[head+"IP.DESTBIN"])))
        
        type =info[head+"IP.TYPE"]
        stand += info[head+"IP.HEADLEN"]
    elif(type == 6):
        info[head+"TYPE3EXT"] = "IPV6"
        tmp, = struct.unpack("B",block[stand:stand+1])
        info[head+"IPV6.VERSION"] = (tmp & 0xF0)>>4
        info[head+"IPV6.VERSION"] = info[head+"IP.VERSION"]
        info[head+"IPV6.HEADLEN"] = 40
        info[head+"IPV6.TRAF"],     = struct.unpack("B",block[stand+1:stand+2])
        info[head+"IPV6.FLOW"],     = struct.unpack(">H",block[stand+2:stand+4])
        info[head+"IPV6.LEN"],      = struct.unpack(">H",block[stand+4:stand+6])
        info[head+"IPV6.TYPE"],     = struct.unpack("B",block[stand+6:stand+7])
        info[head+"IPV6.TTL"],      = struct.unpack("B",block[stand+7:stand+8])
        info[head+"IPV6.SRCBIN"]   = block[stand+8:stand+24]
        info[head+"IPV6.DESTBIN"]  = block[stand+24:stand+40]
        #info[head+"IPV6.SRC"]      = formatIp(info[head+"IPV6.SRCBIN"]);
        #info[head+"IPV6.DEST"]     = formatIp(info[head+"IPV6.DESTBIN"]);

        type =info[head+"IPV6.TYPE"]
        stand += info[head+"IPV6.HEADLEN"]
    else:
        return info

    info[head+"TYPE4"] = type
    info[head+"4"] = stand
    #DPrint(sprintf"TYPE4 : %#.4x, %d",type,stand);
    if(type == 0x04):        #IP类型
        info[head+"TYPE4EXT"] = "IP"
        info.update(getIPInfo(block,stand,"IP"))
    elif(type == 0x06):        #tcp
        info[head+"TYPE4EXT"] = "TCP"
        info[head+"TCP.SRC"],  = struct.unpack(">H",block[stand:stand+2])
        info[head+"TCP.DEST"], = struct.unpack(">H",block[stand+2:stand+4])
        info[head+"TCP.REQ"],  = struct.unpack(">I",block[stand+4:stand+8])
        info[head+"TCP.ACK"],  = struct.unpack(">I",block[stand+8:stand+12])
        info[head+"TCP.HEADLEN"],  = struct.unpack("B",block[stand+12:stand+13])
        info[head+"TCP.HEADLEN"]  = ((info[head+"TCP.HEADLEN"] & 0xF0)>>4)*4
        info[head+"TCP.FLAG"],  = struct.unpack("B",block[stand+13:stand+14])
        info[head+"TCP.WINDOW"],  = struct.unpack(">H",block[stand+14:stand+16])
        info[head+"TCP.CHECKSUM"],  = struct.unpack(">H",block[stand+16:stand+18])
        info[head+"TCP.DATA"]       = block[info[head+"TCP.HEADLEN"]:]
        
        stand +=  18
    elif(type == 0x11):    #udp
        info[head+"TYPE4EXT"]     = "UDP"
        info[head+"UDP.SRC"],      = struct.unpack(">H",block[stand:stand+2])
        info[head+"UDP.DEST"],     = struct.unpack(">H",block[stand+2:stand+4])
        info[head+"UDP.LEN"],      = struct.unpack(">H",block[stand+4:stand+6])
        info[head+"UDP.CHECKSUM"], = struct.unpack(">H",block[stand+6:stand+8])
        info[head+"UDP.DATA"]      = block[stand+8:]
                                              
        stand +=  8
    elif(type == 0x01):    #ICMP
        info[head+"TYPE4EXT"]     = "ICMP"
        info[head+"ICMP.TYPE"],     = struct.unpack("B",block[stand:stand+1])
        info[head+"ICMP.CODE"],     = struct.unpack("B",block[stand+1:stand+2])
        info[head+"ICMP.CHECKSUM"], = struct.unpack(">H",block[stand+2:stand+4])
        #type = info[head+"ICMP.TYPE"];
        if(info[head+"ICMP.TYPE"] == 0 or   #ECHO REPLY \
           info[head+"ICMP.TYPE"] == 8):   #ECHO REQUEST  
            info[head+"ICMP.ID"], = struct.unpack(">H",block[stand+4:stand+6])
            info[head+"ICMP.SEQ"], = struct.unpack(">H",block[stand+6:stand+8])
            info[head+"ICMP.SEQLE"], = struct.unpack(">H",block[stand+8:stand+10])
        elif(info[head+"ICMP.TYPE"] == 3): # Destination Unreachable Message
            stand += 8
            info.update(getIPInfo(block,stand,head+"ICMP"))
    elif(type == 0x3a):    #ICMPv6
        info[head+"TYPE4EXT"]     = "ICMPV6"
        info[head+"ICMPV6.TYPE"],      = struct.unpack("B",block[stand:stand+1])
        info[head+"ICMPV6.CODE"],     = struct.unpack("B",block[stand+1:stand+2])
        info[head+"ICMPV6.CHECKSUM"], = struct.unpack(">H",block[stand+2:stand+4])
        #type = info[head+"ICMPV6.TYPE"];
        if(info[head+"ICMPV6.TYPE"] == 128 or #IPv6 ECHO REQUEST \
           info[head+"ICMPV6.TYPE"] == 129 ): #IPv6 ECHO REPLY  
            info[head+"ICMPV6.ID"], = struct.unpack(">H",block[stand+4:stand+6])
            info[head+"ICMPV6.SEQ"], = struct.unpack(">H",block[stand+4:stand+6])
        elif(info[head+"ICMPV6.TYPE"] == 1): #IPv6 Destination Unreachable Message
            stand += 8
            info.update(getIPInfo(block,stand,head+"ICMPV6"))
    else:
        return info
    
    if(type == 0x11):
        if (5351 == info[head+"UDP.SRC"] or 5351 == info[head+"UDP.DEST"]) :
            info[head+"TYPE5"] = 5351
            info[head+"5"] = stand
            info[head+"TYPE5EXT"]     = "PCP"
            info[head+"PCP.VERSION"],  = struct.unpack("B",block[stand:stand+1])
            info[head+"PCP.ROPCODE"],  = struct.unpack("B",block[stand+1:stand+2])
            info[head+"PCP.R"]        = info[head+"PCP.ROPCODE"]&0x80
            info[head+"PCP.OPCODE"]   = (info[head+"PCP.ROPCODE"]&0x7F)
            
            #V1 V2 头相同版本
            #R: Indicates Request (0) or Response (1).
            
            if (not info[head+"PCP.R"]) :
                #请求 / 应答长度相同
                info[head+"PCP.Reserved"], = struct.unpack(">H",block[stand+2:stand+4])
                info[head+"PCP.LIFETIME"], = struct.unpack(">I",block[stand+4:stand+8])
                info[head+"PCP.CLIENTIP"]  = block[stand+8:stand+24]
            else :
                info[head+"PCP.Reserved"], = struct.unpack("B",block[stand+2:stand+3])
                info[head+"PCP.RESULT"],   = struct.unpack("B",block[stand+3:stand+4])
                info[head+"PCP.LIFETIME"],  = struct.unpack(">I",block[stand+4:stand+8])
                info[head+"PCP.EPOCHTIME"], = struct.unpack(">I",block[stand+8:stand+12])
                # 96bit Reserved

            stand += 24
            
            if ((1 == info[head+"PCP.OPCODE"])) :
                #map request Response v1 v2格式相同
                if (info[head+"PCP.VERSION"] == 2): #v2 比v1 多NONCE
                    info[head+"PCP.MAP.NONCE"] = block[stand:stand+12]
                    stand += 12
                info[head+"PCP.MAP.PROTOCOL"], = struct.unpack("B",block[stand:stand+1])
                # 24bit Reserved
                info[head+"PCP.MAP.INPORT"], = struct.unpack(">H",block[stand+4:stand+6])
                info[head+"PCP.MAP.EXTPORT"],  = struct.unpack(">H",block[stand+6:stand+8])
                info[head+"PCP.MAP.EXTIP"]  = block[stand+8:stand+24]
                stand += 24

            while (len(block) > stand+ 4 ) :
                code, = struct.unpack("B",block[stand:stand+1])
                # 8bit Reserved
                length,  = struct.unpack(">H",block[stand+2:stand+4])
                if (1 == code) :
                    #THIRD_PARTY
                    info[head+"PCP.THIRD_PARTY"] = code
                    info[head+"PCP.THIRD_PARTY.LEN"] = length
                    info[head+"PCP.THIRD_PARTY.INIP"] = block[stand+4:stand+20]
                elif (2 == code) :
                    #PREFER_FAILURE
                    info[head+"PCP.PREFER_FAILURE"] = code
                    info[head+"PCP.PREFER_FAILURE.LEN"] = length
                elif (3 == code) :
                    info[head+"PCP.FILTER"] = code
                    info[head+"PCP.FILTER.LEN"] = length
                else :
                    print("Unknow option code : code , len len")
                stand = stand + 4 + length
    return info

app = cgnrandom()

if __name__ == '__main__':
    print (calcEndIp('1.1.1.1',10))
    print (calcEndIp('6000::1',10))
    print (app['*32*str1'])
    print (app['*str1'])
    print (app['$int1'])
    print (app['$1999$int1'])
    print (app['@ipv4.10@range1'])
    print (app['@ipv4.24@prefix1'])
    print (app[10])
    print (cgnrandom(1,2000)["$int1"])
    print (cgnrandom(1,2000)["$int12"])
    print (cgnrandom(1,63)["*str1"])
    packet = '000100000001001F5310521C08004500005800480000FF117B481F0101011F01010214E714E80044000002810000000000B4000417510000000000000000000000000000000000000000000000011100000003E803E800000000000000000000FFFF5A000001'
    packet = packet.decode('hex')
    info = getPacketInfo(packet)
    keys = info.keys()
    keys.sort()
    for i in keys:
        #if i == '':
        #    binascii.a2b_hex(info[i])
        print ("%s :%s "%(i,str(info[i])))
    
    print(IP('127.0.0.1').make_net('255.0.0.0'))
    print(IP('1.1.1.1').make_net('255.255.255.255'))
    print(IP('175.0.0.1').make_net('255.255.255.0'))
    print(IP('176.0.0.1').make_net('255.255.255.0'))
    print(IP(IP('175.0.0.1').make_net('255.255.255.0')).net())
    
    net = IP('175.0.0.1').make_net('255.255.255.0')  #ip 175.0.0.1 255.255.255.0 返回175.0.0.0/24
    networknum = IP(net).net()   #175.0.0.0
    print ('net:',net,type(net))
    print ('network:',networknum,type(networknum))
    print((IP(net).prefixlen(),type(IP(net).prefixlen())))
    wildcardbit = 32 - IP(net).prefixlen()
    print(str(networknum)+'/'+str(wildcardbit))
    print ('wildcardbit',wildcardbit)
    
