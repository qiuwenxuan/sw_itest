[env]
SIM EMU(PX2) Hybrid

[depend]
apt install python3.8
pip3 install pytest
pip3 install paramiko
pip3 install allure-pytest

[run]
pytest -vs  --alluredir=./result --clean-alluredir
allure generate -c -o ./allure-report ./result
allure open ./allure-report


[source code]
.
├── common                              #自动化测试平台公用函数，基本复用ptest_ssh的代码
│    ├── __init__.py
│    ├── com_util.py                    # 字符串、列表、字典等数据转换处理公共接口
│    ├── key_press.py
│    ├── priv_config.py                 # 加密、明文密文互转接口
│    ├── product_test.py                # ptest 连接、登录接口封装类
│    ├── ptest_shell.py                 # ptest shell管理类，继承于product_test
│    ├── regrep.py                      # 正则匹配接口
│    ├── sftp_util.py                   # 新增sftp 下载上传文件代码
│    ├── ssh_run.py                     # 基于 paramiko 封装的ssh登录命令执行接口类
│    ├── ssh_shell.py                   # 登录接口封装
│    └── thread_stop.py                 # 多线程相关的功能
├── log
├── README                              # 自动化框架的说明文档
├── report                              # 测试报告文件存放目录
├── result                              # 测试结果文件存放目录
└── tests                               # 测试用例存放目录。
    ├── __init__.py
    └── pytestCase                       # pytest 类型测试用例存放目录。
        ├── common                       #集成测试自动化公用函数
        │    ├── Exception.py            #异常处理相关
        │    ├── __init__.py
        │    ├── Object                  # 集成测试抽象类
        │    │    ├── ConfPage.py        # 配置文件类
        │    │    ├── Dev.py             # 设备类
        │    │    ├── __init__.py
        │    │    ├── ItestSession.py    # 集成测试Session
        │    │    └── OVSPort.py         # OVSPort
        │    └── utils                   # 测试用例工具类
        │        ├── blkdev_util.py
        │        ├── dev_util.py
        │        ├── easy_bm_parser.py
        │        ├── __init__.py
        │        ├── netdev_util.py
        │        ├── nvmedev_util.py
        │        ├── ovs_result_parser.py
        │        ├── session_util.py
        │        ├── SSHClass.py
        │        └── storage_util.py
        ├── config                        # 配置文件
        │    ├── fio_test.cfg
        │    ├── README.md
        │    ├── SIM-NetBlk-Legacy.conf
        │    ├── SIM-NetBlk-Modern.conf
        │    ├── SIM-NetBlk-Packed.conf
        │    └── SIM-Nvme.conf
        ├── conftest.py
        ├── __init__.py
        ├── log                           # 测试日志存放目录
        │    └── test.log
        ├── pytest.ini
        ├── test_blkdev.py                # blkdev测试用例文件
        ├── test_netdev.py                # netdev测试用例文件
        ├── test_nvmedev.py               # nvmedev测试用例文件
        └── tmp


