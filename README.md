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
������ common                              #�Զ�������ƽ̨���ú�������������ptest_ssh�Ĵ���
��    ������ __init__.py
��    ������ com_util.py                    # �ַ������б��ֵ������ת���������ӿ�
��    ������ key_press.py
��    ������ priv_config.py                 # ���ܡ��������Ļ�ת�ӿ�
��    ������ product_test.py                # ptest ���ӡ���¼�ӿڷ�װ��
��    ������ ptest_shell.py                 # ptest shell�����࣬�̳���product_test
��    ������ regrep.py                      # ����ƥ��ӿ�
��    ������ sftp_util.py                   # ����sftp �����ϴ��ļ�����
��    ������ ssh_run.py                     # ���� paramiko ��װ��ssh��¼����ִ�нӿ���
��    ������ ssh_shell.py                   # ��¼�ӿڷ�װ
��    ������ thread_stop.py                 # ���߳���صĹ���
������ log
������ README                              # �Զ�����ܵ�˵���ĵ�
������ report                              # ���Ա����ļ����Ŀ¼
������ result                              # ���Խ���ļ����Ŀ¼
������ tests                               # �����������Ŀ¼��
    ������ __init__.py
    ������ pytestCase                       # pytest ���Ͳ����������Ŀ¼��
        ������ common                       #���ɲ����Զ������ú���
        ��    ������ Exception.py            #�쳣�������
        ��    ������ __init__.py
        ��    ������ Object                  # ���ɲ��Գ�����
        ��    ��    ������ ConfPage.py        # �����ļ���
        ��    ��    ������ Dev.py             # �豸��
        ��    ��    ������ __init__.py
        ��    ��    ������ ItestSession.py    # ���ɲ���Session
        ��    ��    ������ OVSPort.py         # OVSPort
        ��    ������ utils                   # ��������������
        ��        ������ blkdev_util.py
        ��        ������ dev_util.py
        ��        ������ easy_bm_parser.py
        ��        ������ __init__.py
        ��        ������ netdev_util.py
        ��        ������ nvmedev_util.py
        ��        ������ ovs_result_parser.py
        ��        ������ session_util.py
        ��        ������ SSHClass.py
        ��        ������ storage_util.py
        ������ config                        # �����ļ�
        ��    ������ fio_test.cfg
        ��    ������ README.md
        ��    ������ SIM-NetBlk-Legacy.conf
        ��    ������ SIM-NetBlk-Modern.conf
        ��    ������ SIM-NetBlk-Packed.conf
        ��    ������ SIM-Nvme.conf
        ������ conftest.py
        ������ __init__.py
        ������ log                           # ������־���Ŀ¼
        ��    ������ test.log
        ������ pytest.ini
        ������ test_blkdev.py                # blkdev���������ļ�
        ������ test_netdev.py                # netdev���������ļ�
        ������ test_nvmedev.py               # nvmedev���������ļ�
        ������ tmp


