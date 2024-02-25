import os
import imp
import inspect,re

dpe_register= []
num=0
start=0
def c_enum_2_dict():
    file= open('/home/wanglin/code/automatedscripts-net/jaguar-top11-old/jnet_register.h',"r",encoding='utf-8') 
    f= open('/home/wanglin/code/automatedscripts-net/jaguar-top11-old/register.py',"w",encoding='utf-8')
    print('# ****** B400  register ******', file=f)
    for line in file.readlines():
         global start, num
         if "enum" in line:
            start=1
            tmp=re.findall(r'enum(.*?)', line)
            if len(tmp): 
              enum_name = tmp[0].replace(" ", "")
              if len(enum_name):
                output=enum_name+" = "+"{"
                print(output, file=f)
                continue
         elif '{' in line:
           continue
         elif "}" in line:
            start=0
            num=0
            print('\n', file=f)
         elif start:
            tmp1=re.findall(r'\t(.*?)\n', line)
            if len(tmp1):
                regname = tmp1[0].replace(",", "")
                if "_MAX\n" in regname:
                  endOfReg=""
                output=""+regname+" =  "+str(num)
                print(output, file=f)
                num +=1

    file.close()
    f.close()
            
c_enum_2_dict()

# print (dpe_register)


 
 
#p1 = re.compile(r'[(](.*?)[)]', re.S)  #最小匹配
#p2 = re.compile(r'[(](.*)[)]', re.S)   #贪婪匹配
#print(re.findall(p1, string))
#print(re.findall(p2, string))
    

