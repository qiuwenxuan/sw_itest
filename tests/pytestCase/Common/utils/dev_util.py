import logging
import os
import random
import time

from common import ssh_run
from tests.pytestCase.Common.Object.DiskXMLGenerator import DiskXMLGenerator
from tests.pytestCase.Common.utils.exception import TYPEError, Error, ENVError
from tests.pytestCase.Common.utils.util import scp_file_to_n2
from tests.pytestCase.Common.utils.netdev_util import ping_test_0_loss_rate

CRB_blk_dev_disk_path = [
    {'vda': 'blk0.xml'}, {'vdb': 'blk1.xml'}, {'vdc': 'blk2.xml'}, {'vdd': 'blk3.xml'}, {'vde': 'blk4.xml'},
    {'vdf': 'blk5.xml'}, {'vdg': 'blk6.xml'}, {'vdh': 'blk7.xml'}
]


def get_dev_type_name(dev_type):
    if dev_type == "net":
        dev_type_name = 'VIRTIO_NET'
    elif dev_type == "blk":
        dev_type_name = 'VIRTIO_BLK'
    else:
        raise TYPEError("type is error")
    return dev_type_name


def load_driver(host_session, dev_type):
    if dev_type == "net":
        cmd = f"lsmod | grep -q virtio_net || modprobe virtio_net"
    elif dev_type == "blk":
        cmd = f"lsmod | grep -q virtio_blk || modprobe virtio_blk"
    elif dev_type == "nvme":
        cmd = f"lsmod | grep -q nvme || modprobe nvme"
    else:
        raise Exception("type is error")
    result = host_session.execute_command(cmd)
    assert result == "", "驱动加载失败！"
    logging.info(f"\n-----------------------------驱动加载成功！")
    time.sleep(10)


def unload_driver(host_session, dev_type):
    if dev_type == "net":

        cmd = f"modprobe -r virtio_net; [ \"$(lsmod | grep virtio_net )\" ] " \
              f"&& echo 'Failed to unload module' || echo 'unloaded successfully'"
    elif dev_type == "blk":

        cmd = f"modprobe -r virtio_blk; [ \"$(lsmod | grep virtio_blk )\" ] " \
              f"&& echo 'Failed to unload module' || echo 'unloaded successfully'"
    elif dev_type == "nvme":

        cmd = f"modprobe -r nvme ; [ \"$(lsmod | grep nvme )\" ] && " \
              f"echo 'Failed to unload module' || echo 'unloaded successfully'"
    else:
        raise Exception("type is error")
    logging.info(f"\n-----------------------------驱动卸载的命令是： {cmd}")

    timeout = 30
    start_time = time.time()
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time > timeout:
            logging.error("超时：驱动卸载未成功")
            break

        output = host_session.execute_command(cmd).strip()
        logging.info(f"\n-----------------------------驱动卸载的结果是： {output}")
        if 'unloaded successfully' in output:
            logging.info("驱动卸载已成功")
            break

        # 间隔2秒再次卸载驱动
        time.sleep(2)
    time.sleep(5)


def parse_devs_str(devs_str):
    lines = devs_str.strip().split('\n')
    headers = lines[0].split()  # Extract headers from the first line
    device_list = []

    for line in lines[1:]:  # Skip the first two lines (header and dev list: line)
        values = line.split()
        device = {}  # Create a dictionary to store device information
        for idx, header in enumerate(headers):
            device[header] = values[idx]  # Assign each value to the corresponding header key
        device_list.append(device)

    return device_list


def run_msg_cmd(shell, param=None):
    command = param
    logging.info(f"run_msg_cmd:command:{command}")
    shell.su_login('jaguar')
    shell.set_default_end_list(['>> '])
    shell.run_by_auth_yes('ssh root@127.0.0.1 -p 6000', 'jmnd')
    shell.run('msg_cmd')
    ret = shell.run(command, mod='ret_only')
    logging.info(f"---------etPFPage.run_msg_cmd:ret:{ret}")
    shell.run('quit')
    shell.set_default_end_list(['# '])
    shell.run('quit')
    return ret


def get_dev_list(n2_session):
    # 1.进入后端诊断模块msg_cmd，输入查询命令device list
    ret = n2_session.shell_run(run_msg_cmd, param='device list')
    assert "device list" in ret and "dev list" in ret
    # 2 截取执行'device list'的结果，得到的devsString
    lines = ret.strip().split('\n')
    # 2.1 去掉前四行和最后一行
    trimmed_lines = lines[4:-1]
    devsString = '\n'.join(trimmed_lines)
    logging.info(f"\n-----------------------------devsString:\n {devsString}")

    # 3.把devs 字符串转化为 dev_list
    dev_list = parse_devs_str(devsString)
    logging.info(f"\n-----------------------------dev_list:\n {dev_list}")
    return dev_list


def check_all_devs_is_ok(dev_list):
    for device in dev_list:
        if device['status'] != 'DRIVER_OK':
            return False
    return True


def get_random_dev(devs):
    # 随机选择一个字典并获取其 dev_name 值
    if devs:
        random_dev = random.choice(devs)
        dev_name = random_dev.get('dev_name')
        if not dev_name:
            logging.error("dev_name isn\'t finded.")
        return random_dev
    else:
        logging.error("devs is None")
        raise Error("devs is None")


def reset_by_bmc(it_session):
    # 1.获取host bmc会话
    n2_session = it_session.get_n2_session()
    bmc_server = it_session.get_configure().get_bmc_server()
    host_server = it_session.get_configure().get_host_server()
    # host_server = it_session.get_configure()

    logging.info(f"----bmc_server:{bmc_server.hostname},{bmc_server.username},{bmc_server.password},{bmc_server.port}")

    # 2.执行冷重启
    cmd = f"ipmitool -I lanplus -H {bmc_server.hostname} -U {bmc_server.username} -P {bmc_server.password} power reset"
    result = n2_session.execute_command(cmd)
    logging.info(f"-----------------------------执行冷重启命令:{cmd}")
    logging.info(f"-----------------------------冷重启执行结果:{result}")

    time.sleep(15)

    # 3.查看冷重启之后host状态
    cmd = f"ipmitool -I lanplus -H {bmc_server.hostname} -U {bmc_server.username} -P {bmc_server.password} power status"
    result = n2_session.execute_command(cmd)
    logging.info(f"-----------------------------查看冷重启状态命令:{cmd}")
    logging.info(f"-----------------------------冷重启状态:{result}")

    # 4.在windows调试机上启动冷重启后，检查host重启成功
    host_name = host_server.hostname
    result = check_host_reset(n2_session, host_name)
    if result:
        return True
        # it_session.set_host_session(login_host(it_session))  # 重新登录，并更新it_session中的host_session
    else:
        return False
        # raise Error("host重启失败！")


def check_host_reset(n2_session, host_name):
    # 检查host侧是否重启成功
    timeout = 15 * 60
    start_time = time.time()
    cmd = f"ping {host_name} -c 1"
    logging.info(f'---------------------正在等待host重启-------------------------')
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time > timeout:
            logging.error(f"host：{host_name}重启超时!")
            return False

        if ping_test_0_loss_rate(n2_session, host_name):
            logging.info(f"host：{host_name}重启成功!")
            time.sleep(10)
            return True
        time.sleep(20)


def create_disk_to_detach_dev(it_session, dev_name):
    n2_session = it_session.get_n2_session()

    # 生成disk.xml文件病拷贝到N2
    disk_xml_file = DiskXMLGenerator.create_disk_xml(dev_name)
    scp_file_to_n2(it_session, disk_xml_file)

    # 删除本地的xml文件
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    xml_file_abs = f'{parent_dir}/../../tmp/{disk_xml_file}'
    os.remove(xml_file_abs)

    # 执行热拔命令
    n2_xml_file_abs = f'/root/{disk_xml_file}'
    detach_dev(n2_session, n2_xml_file_abs)
    return n2_xml_file_abs


def detach_dev(n2_session, xml_path):
    # TODO，qmp detach-device easy_bm nvme7.xml
    cmd = f"qmp detach-device easy_bm {xml_path}"
    n2_session.execute_command(cmd)


def detach_dev_in_CRB(n2_session, xml_path):
    # TODO，qmp detach-device bm_itest blkx.xml
    cmd = f"qmp detach-device bm_itest {xml_path}"
    logging.info(f"\n-----------------------------热拔操作命令:{cmd}")
    output = n2_session.execute_command(cmd)
    logging.info(f"\n-----------------------------热拔操作输出结果:{output}")


def attach_dev(n2_session, xml_path):
    # TODO，qmp attach-device easy_bm nvme7.xml
    cmd = f"qmp attach-device bm_itest {xml_path}"
    logging.info(f"\n-----------------------------热插操作命令:{cmd}")
    output = n2_session.execute_command(cmd)
    logging.info(f"\n-----------------------------热插操作输出结果:{output}")


def attach_dev_in_CRB(n2_session, xml_path, num=1):
    # CRB环境目前热插命令需要执行至少两次才能成功，因此添加一个循环操作重复执行命令
    # TODO，qmp attach-device bm_itest blkx.xml
    cmd = f"qmp attach-device bm_itest {xml_path}"
    for i in range(num):
        logging.info(f"\n-----------------------------热插操作命令:{cmd}")
        output = n2_session.execute_command(cmd)
        logging.info(f"\n-----------------------------热插操作输出结果:{output}")


def detach_dev_by_dev_name(n2_session, dev_name):
    # 适用于CRB环境热插拔
    # 1.循环遍历CRB_blk_dev_disk_path列表找到设备对应的disk文件名
    disk_path = ""
    for blk_dev_dict in CRB_blk_dev_disk_path:
        for dev, path in blk_dev_dict.items():
            if dev == dev_name:
                disk_path = path
                break
    assert disk_path, "设备没有对应的disk.xml文件，检查设备是否正确！"
    # 2.拼接成绝对路径
    file_dir = '/usr/share/jmnd/libvirt_xml/bm_itest_blk'
    absolute_path = rf"{file_dir}/{disk_path}"
    logging.info(f"\n-----------------------------热插拔文件路径为:{absolute_path}")

    detach_dev_in_CRB(n2_session, absolute_path)
    time.sleep(30)
    return absolute_path


def get_legacy_dev_by_dev_name(dev_list, dev_type):
    matched_devices = []
    dev_type_name = get_dev_type_name(dev_type)

    for device in dev_list:
        if (
                device['pci_dev_type'] == 'PF'
                and device['dev_type'] == dev_type_name
                and int(device['guest_features'], 16) & (1 << 34) == 0
                and int(device['guest_features'], 16) & (1 << 32) == 0
        ):
            matched_devices.append(device)
    if len(matched_devices) == 0:
        raise Error(f"get legacy dev error.dev_type={dev_type},dev_list={dev_list}")
    return matched_devices


def get_modern_dev_by_dev_name(dev_list, dev_type):
    matched_devices = []
    dev_type_name = get_dev_type_name(dev_type)

    for device in dev_list:
        if (
                device['pci_dev_type'] == 'PF'
                and device['dev_type'] == dev_type_name
                and (int(device['guest_features'], 16) >> 32) & 1 == 1
                and (int(device['guest_features'], 16) >> 34) & 1 == 0
        ):
            matched_devices.append(device)
    if len(matched_devices) == 0:
        raise Error(f"get modern dev error.dev_type={dev_type},dev_list={dev_list}")
    return matched_devices


def get_packed_dev_by_dev_name(dev_list, dev_type):
    matched_devices = []
    dev_type_name = get_dev_type_name(dev_type)

    for device in dev_list:
        if (
                device['pci_dev_type'] == 'PF'
                and device['dev_type'] == dev_type_name
                and int(device['guest_features'], 16) & (1 << 34) != 0
        ):
            matched_devices.append(device)
    if len(matched_devices) == 0:
        error_info = f"get packed dev error.dev_type={dev_type},dev_list={dev_list}"
        logging.error(error_info)
        raise Error(error_info)
    return matched_devices


def check_modern_pf_status(dev_list, dev_type):
    matched_devices = get_modern_dev_by_dev_name(dev_list, dev_type)
    ret = check_all_devs_is_ok(matched_devices)
    return ret


def check_packed_pf_status(dev_list, dev_type):
    matched_devices = get_packed_dev_by_dev_name(dev_list, dev_type)
    ret = check_all_devs_is_ok(matched_devices)
    return ret


def check_legacy_pf_status(dev_list, dev_type):
    matched_devices = get_legacy_dev_by_dev_name(dev_list, dev_type)
    ret = check_all_devs_is_ok(matched_devices)
    return ret


# 检查N2端dev_queue_type对应的设备是否driver ok,默认检查N2所有的设备
def check_dev_pf_status(dev_list, dev_type, dev_queue_type='all'):
    if dev_queue_type == 'legacy':
        matched_devices = get_legacy_dev_by_dev_name(dev_list, dev_type)
    elif dev_queue_type == 'modern':
        matched_devices = get_modern_dev_by_dev_name(dev_list, dev_type)
    elif dev_queue_type == 'packed':
        matched_devices = get_packed_dev_by_dev_name(dev_list, dev_type)
    elif dev_queue_type == 'all':
        matched_devices = dev_list
    else:
        raise ENVError("environment error")
    ret = check_all_devs_is_ok(matched_devices)
    return ret


def login_host(it_session):
    host_server = it_session.get_configure().get_host_server()

    logging.info('-----------------正在登录host-----------------')
    host_session = ssh_run.SSHSessions(host_server.hostname, host_server.username, host_server.password)
    result = host_session.connect()
    logging.info(f'------------连接host的结果：{result}-------------')
    assert result == 0, '登录host失败'
    return host_session
