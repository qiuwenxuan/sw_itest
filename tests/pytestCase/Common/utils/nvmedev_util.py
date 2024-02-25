import logging
import random
import time

from tests.pytestCase.Common.Object.DiskXMLGenerator import DiskXMLGenerator
from tests.pytestCase.Common.Object.ItestObject import EnvironmentType
from tests.pytestCase.Common.utils.blkdev_util import disable_rc_timeout_CRB, disable_rc_timeout, get_host_blk_dev
from tests.pytestCase.Common.utils.dev_util import create_disk_to_detach_dev, load_driver, detach_dev_by_dev_name, \
    login_host
from tests.pytestCase.Common.utils.exception import ENVError, GetVirtioBlkError, Error
from tests.pytestCase.Common.utils import dev_util, session_util, storage_util
from tests.pytestCase.Common.utils.storage_util import cycle_operate_vhost_CRB, cycle_operate_vhost_PX2


def check_all_devs_is_ok(dev_list):
    for device in dev_list:
        if device['status'] != 'CC_EN':
            return False
    return True


def check_nvmepf_status(dev_list):
    matched_devices = []

    for device in dev_list:
        if (
                device['pci_dev_type'] == 'PF'
                and device['dev_type'] == 'NVME_BLK'
                and device['status'] == 'CC_EN'
        ):
            matched_devices.append(device)
    logging.info(f"\n-----------------------------matched_devices:\n {matched_devices}")
    assert matched_devices, '未匹配到设备'
    ret = check_all_devs_is_ok(matched_devices)
    return ret


def get_nvme_dev_dicts_in_n2(n2_session, dev_list=None):
    if dev_list == None:
        dev_list = dev_util.get_dev_list(n2_session)

    nvme_dev_list_n2 = []
    for device in dev_list:
        if (
                device['pci_dev_type'] == 'PF'
                and device['dev_type'] == 'NVME_BLK'
                and device['status'] == 'CC_EN'
        ):
            nvme_dev_list_n2.append({device['dev_name']: device['bdf']})

    logging.info(f"\n-----------------------------n2上匹配到的nvme设备列表为:\n {nvme_dev_list_n2}")
    #  [{'vdg': 'b7:00.0'}, {'vdh': 'b8:00.0'}]
    assert nvme_dev_list_n2, "n2上未匹配到nvme设备！"
    return nvme_dev_list_n2


def get_nvme_dev_dicts_in_host(it_session, dev_list=None):
    n2_session = it_session.get_n2_session()
    host_session = it_session.get_host_session()

    if dev_list == None:
        dev_list = dev_util.get_dev_list(n2_session)

    nvme_dev_list_host = []
    devices_bdf = []
    for device in dev_list:
        if (
                device['pci_dev_type'] == 'PF'
                and device['dev_type'] == 'NVME_BLK'
                and device['status'] == 'CC_EN'
        ):
            devices_bdf.append(device['bdf'])
    logging.info(f"\n-----------------------------devices_bdf:\n {devices_bdf}")
    assert devices_bdf, '未匹配到设备'
    for bdf in devices_bdf:
        cmd = "ls -lh /sys/block/nvme* |grep -E '%s' |awk '{print $NF}'|awk -F '/' '{print $NF}'" % bdf
        nvme_dev = host_session.execute_command(f"{cmd}").strip()
        nvme_dev_list_host.append({nvme_dev: bdf})

    assert nvme_dev_list_host, 'host上未匹配到nvme设备'
    logging.info(f"\n-----------------------------host上匹配到的nvme设备列表为:\n {nvme_dev_list_host}")
    # [{'nvme0n1': 'b7:00.0'}, {'nvme1n1': 'b8:00.0'}]

    return nvme_dev_list_host


def get_host_nvme_dev(it_session):
    n2_session = it_session.get_n2_session()
    host_session = it_session.get_host_session()
    dev_list = dev_util.get_dev_list(n2_session)

    devices_bdf = []
    for device in dev_list:
        if (
                device['pci_dev_type'] == 'PF'
                and device['dev_type'] == 'NVME_BLK'
                and device['status'] == 'CC_EN'
        ):
            devices_bdf.append(device['bdf'])
    logging.info(f"\n-----------------------------devices_bdf:\n {devices_bdf}")
    # ['b7:00.0', 'b8:00.0']
    assert devices_bdf, '未匹配到设备'
    bdf = "|".join(devices_bdf)
    cmd = "ls -lh /sys/block/nvme* |grep -E '%s' |awk '{print $NF}'|awk -F '/' '{print $NF}'" % bdf
    result = host_session.execute_command(f"{cmd}")
    assert result, '未匹配到设备'
    nvme_list = result.strip().split('\n')

    # ['nvme0n1', 'nvme1n1']
    logging.info(f"\n-----------------------------nvme_list:\n {nvme_list}")

    return nvme_list


def nvmepf_multidev_io(it_session, dev_type, check_final_result=True):
    # 0.pre 登录前后端成功,确认host端加载驱动成功
    n2_session, host_session = session_util.pretest(it_session, dev_type)

    # 1.对全部设备发流
    nvme_run_fio_by_dev_name(it_session)


def nvme_run_fio_by_dev_name(it_session, nvme_dev_list=None, check_final_result=True):
    # nvme设备fio发流
    host_session = it_session.get_host_session()
    # 1.scp fio配置模版文件到host侧
    storage_util.scp_fio_cfg_to_host(it_session)

    # 2.对传入的nvme设备发流，如果不传nvme设备，表示对所有满足条件的nvme设备发流
    if nvme_dev_list == None:
        nvme_dev_list = get_host_nvme_dev(it_session)
    # 3.根据nvme盘的列表完善fio配置文件
    storage_util.complete_fio_cfg(host_session, nvme_dev_list)
    # 4.跑fio测试之前先杀死fio进程，避免已有的fio进程影响测试
    storage_util.kill_fio_process(host_session)

    # 5.跑fio测试
    storage_util.run_fio(host_session, bsrange='512B-1024k')

    # 6.获取fio的实时输出结果，确认fio已正常运行
    """
    存储设备若出现IO hang，则kill fio进程会出现kill不掉的情况，所以fio测试采用runtime=3600，
    测试过程中根据需要kill fio进程来检测是否出现IO hang的情况。
    """
    time.sleep(10)
    result = storage_util.tail_fio_result(host_session)
    assert result == True, "fio发流失败"

    if check_final_result:
        # 7.跑fio 30s
        time.sleep(30)

        # 8.提前终止fio进程
        storage_util.kill_fio_process(host_session)

        # 9.查询fio结果
        storage_util.get_final_result_of_fio(host_session)


def nvmepf_multidev_reload_driver(it_session, dev_type):
    # fio流通测试
    nvmepf_multidev_io(it_session, dev_type)
    host_session = it_session.get_host_session()

    for i in range(1, 4):
        logging.info(f"\n-----------------------------第{i}次循环-----------------------------")
        if it_session.env_type == EnvironmentType.SIM.name:
            # corsica sim环境不支持nvme的驱动卸载加载
            pass
        elif it_session.env_type == EnvironmentType.EMU.name or \
                it_session.env_type == EnvironmentType.HYBRID.name or \
                it_session.env_type == EnvironmentType.CRB.name:
            # 1.卸载nvme驱动
            dev_util.unload_driver(host_session, dev_type)

            # 2.加载nvme驱动
            dev_util.load_driver(host_session, dev_type)
        else:
            raise ENVError("environment error")
    nvmepf_multidev_io(it_session, dev_type)


def nvmepf_multidev_host_reset(it_session, dev_type):
    if it_session.env_type == EnvironmentType.SIM.name:
        # corsica sim环境不支持host reset,fio发流
        nvmepf_multidev_io(it_session, dev_type)

    elif it_session.env_type == EnvironmentType.EMU.name:
        # 1.全部设备持续发fio流
        nvmepf_multidev_io(it_session, dev_type)

        # 2.执行Power reset操作
        reboot_success = dev_util.reset_by_bmc(it_session)

        # 3.判断重启是否成功
        if reboot_success:
            host_session = login_host(it_session)  # 重新登录，同时更新局部变量的值
            it_session.set_host_session(host_session)  # 更新it_session中的host_session
        else:
            raise Error("host重启失败！")

        # 4.加载virtio_blk驱动.需要先关闭RC超时时间
        disable_rc_timeout(host_session)

        # 5.加载virtio_blk驱动
        load_driver(host_session, dev_type)

        # 6.fio再发流
        nvmepf_multidev_io(it_session, dev_type)

    elif it_session.env_type == EnvironmentType.CRB.name:

        # 1.全部设备持续发fio流
        nvmepf_multidev_io(it_session, dev_type)

        # 2.执行Power reset操作
        reboot_success = dev_util.reset_by_bmc(it_session)

        # 3.判断重启是否成功
        if reboot_success:
            host_session = login_host(it_session)  # 重新登录，同时更新局部变量的值
            it_session.set_host_session(host_session)  # 更新it_session中的host_session
        else:
            raise Error("host重启失败！")

        # 4.加载virtio_blk驱动
        load_driver(host_session, dev_type)

        # 5.fio再次发流
        nvmepf_multidev_io(it_session, dev_type)

    else:
        raise ENVError("environment error")
    # host reset后进行fio流通测试


def nvmepf_multidev_hotplug(it_session, dev_type):
    n2_session = it_session.get_n2_session()

    if it_session.env_type == EnvironmentType.SIM.name:
        # corsica sim环境不支持nvme设备的热拔插
        nvmepf_multidev_io(it_session, dev_type)

    elif it_session.env_type == EnvironmentType.EMU.name:
        # 1.随机选择host上的一个满足nvme的设备单独发流
        host_fio_dev_dict, dev_list = nvmepf_singledev_io(it_session, dev_type)
        # [{'nvme0n1': 'b7:00.0'}, {'nvme1n1': 'b8:00.0'}]

        # 2.获取host发流对应n2的设备名
        nvme_dev_bdf = list(host_fio_dev_dict.values())[0]
        nvme_dev_name = list(host_fio_dev_dict.keys())[0]
        logging.info(f"-----------------------------选择热拔插设备{nvme_dev_name}:{nvme_dev_bdf}")

        n2_fio_dev = match_n2_nvme_dev_by_host_dev(n2_session, nvme_dev_bdf, dev_list)

        # 3.热拔nvme设备
        n2_xml_file_abs = create_disk_to_detach_dev(it_session, n2_fio_dev)

        # 4.热插nvme设备
        dev_util.attach_dev(n2_session, n2_xml_file_abs)

        # 5.对刚才的热拔插的设备再次发流，验证是否发流成功
        nvme_run_fio_by_dev_name(it_session, nvme_dev_name)
    elif it_session.env_type == EnvironmentType.CRB.name:

        # 1.随机选择host上的一个满足nvme的设备单独发流
        host_fio_dev_dict, dev_list = nvmepf_singledev_io(it_session, dev_type)
        # [{'nvme0n1': 'b7:00.0'}, {'nvme1n1': 'b8:00.0'}]

        # 2.获取host发流对应n2的设备名和bdf号
        nvme_dev_bdf = list(host_fio_dev_dict.values())[0]
        nvme_dev_name = list(host_fio_dev_dict.keys())[0]
        logging.info(f"-----------------------------选择的热拔插设备------{nvme_dev_name}:{nvme_dev_bdf}")

        # 3.将选中的host设备匹配到N2的设备名称，返回N2设备名用于热插拔
        n2_fio_dev = match_n2_nvme_dev_by_host_dev(n2_session, nvme_dev_bdf, dev_list)

        # 3.热拔nvme设备
        n2_xml_file_abs = detach_dev_by_dev_name(n2_session, n2_fio_dev)

        # 4.热插nvme设备
        dev_util.attach_dev_in_CRB(n2_session, n2_xml_file_abs, 3)

        # 5.对刚才的热拔插的设备再次发流，验证是否发流成功
        nvme_run_fio_by_dev_name(it_session, nvme_dev_name)
    else:
        raise ENVError("environment error")
    # 热拔插后，进行fio流通测试


def match_n2_nvme_dev_by_host_dev(n2_session, host_dev, dev_list):
    # 根据host设备名匹配n2设备
    n2_match_dev = ""
    n2_dev_lists = get_nvme_dev_dicts_in_n2(n2_session, dev_list)

    # 遍历n2上的设备和bdf,如果n2设备的bdf与host的pcie匹配 [{'vdg': 'b7:00.0'}, {'vdh': 'b8:00.0'}]
    for n2_dev_list in n2_dev_lists:
        for n2_dev, bdf in n2_dev_list.items():
            if bdf == host_dev:
                n2_match_dev = n2_dev
    logging.info(f"\n-----------------------------n2上热插拔的设备名为:\n {n2_match_dev}")
    return n2_match_dev


def nvmepf_singledev_io(it_session, dev_type, check_final_result=True):
    # 0.pre 登录前后端成功,确认host端加载驱动成功
    n2_session, host_session = session_util.pretest(it_session, dev_type)

    # 1.获取host内所有满足条件的nvme发流设备列表
    dev_list = dev_util.get_dev_list(n2_session)
    nvme_dev_list = get_nvme_dev_dicts_in_host(it_session, dev_list)

    # 2.随机在blk_dev_list里随机选择一个满足条件的设备，获取设备的dev_name
    host_fio_dev_dict = random.choice(nvme_dev_list)
    logging.info(f"\n-----------------------------选择发流的单个设备:bdf {host_fio_dev_dict}")

    # 3.传入选中的单个设备发流
    host_fio_dev = list(host_fio_dev_dict.keys())
    nvme_run_fio_by_dev_name(it_session, host_fio_dev, check_final_result)

    # 4.返回选中的设备
    return host_fio_dev_dict, dev_list


def nvmepf_multidev_io_forcekill_vhost(it_session, dev_type):
    # 0.获取会话
    n2_session = it_session.get_n2_session()
    host_session = it_session.get_host_session()

    if it_session.env_type == EnvironmentType.SIM.name:
        # corsica sim环境不支持vhost进程重启
        # nvme设备发流
        nvmepf_multidev_io(it_session, dev_type)

    elif it_session.env_type == EnvironmentType.EMU.name:
        # 1. nvme所有设备跑起来持续的fio流
        nvmepf_multidev_io(it_session, dev_type, False)

        # 2.循环操作vhost
        cycle_operate_vhost_PX2(it_session, 1)

        # 5.杀掉fio发流
        storage_util.kill_fio_process(host_session)

    elif it_session.env_type == EnvironmentType.CRB.name:
        # 1. nvme所有设备跑起来持续的fio流
        nvmepf_multidev_io(it_session, dev_type, False)

        # 2.循环操作vhost
        cycle_operate_vhost_CRB(it_session, 3)

        # 5.杀掉fio发流
        storage_util.kill_fio_process(host_session)
    else:
        raise ENVError("environment error")
