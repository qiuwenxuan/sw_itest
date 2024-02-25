import logging

import pytest
import allure
import time

from tests.pytestCase.Common.utils import nvmedev_util, dev_util, session_util
from tests.pytestCase.Common.utils import storage_util

NVME_DEV_TYPE = "nvme"


@allure.suite('Cloud_Base_TestCase')
class TestNVMeDev:

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @pytest.mark.parametrize("login", ["Nvme"], indirect=True)
    @allure.feature('COSSW-41801')
    @allure.title("nvme-PF设备控制面协商OK")
    def test_nvmepf_cc_enable(self, login):
        # 0.pre 登录前后端成功,确认host端加载驱动成功
        it_session = login
        n2_session, host_session = session_util.pretest(it_session, NVME_DEV_TYPE)

        # 1. 进入后端诊断模块msg_cmd，输入查询命令device list
        dev_list = dev_util.get_dev_list(n2_session)

        # 2.查看NVMe PF设备状态是否已使能
        ret = nvmedev_util.check_nvmepf_status(dev_list)
        assert ret
        logging.info("test_nvmepf_cc_enable pass")

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @pytest.mark.parametrize("login", ["Nvme"], indirect=True)
    @allure.feature('COSSW-41802')
    @allure.title("nvme-PF多设备多队列FIO随机包流通(512B-1MB)")
    def test_nvmepf_multidev_io(self, login):
        it_session = login
        nvmedev_util.nvmepf_multidev_io(it_session, NVME_DEV_TYPE)

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @pytest.mark.parametrize("login", ["Nvme"], indirect=True)
    @allure.feature('COSSW-41803')
    @allure.title("nvme-PF多设备多队列host反复加载卸载nvme驱动")
    def test_nvmepf_multidev_reload_driver(self, login):
        it_session = login
        nvmedev_util.nvmepf_multidev_reload_driver(it_session, NVME_DEV_TYPE)

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @pytest.mark.parametrize("login", ["Nvme"], indirect=True)
    @allure.feature('COSSW-41804')
    @allure.title("nvme-PF多设备多队列host reset测试")
    def test_nvmepf_multidev_host_reset(self, login):
        it_session = login
        nvmedev_util.nvmepf_multidev_host_reset(it_session, NVME_DEV_TYPE)

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @pytest.mark.parametrize("login", ["Nvme"], indirect=True)
    @allure.feature('COSSW-41805')
    @allure.title("nvme-PF多设备多队列热插拔测试")
    def test_nvmepf_multidev_hotplug(self, login):
        it_session = login
        nvmedev_util.nvmepf_multidev_hotplug(it_session, NVME_DEV_TYPE)


    @pytest.mark.timeout(600)
    @pytest.mark.parametrize("login", ["Nvme"], indirect=True)
    @allure.feature('COSSW-41806')
    @allure.title("nvme-PF多设备多队列，带流kill-9杀掉vhost进程再拉起测试")
    def test_nvmepf_multidev_io_forcekill_vhost(self, login):
        it_session = login
        nvmedev_util.nvmepf_multidev_io_forcekill_vhost(it_session, NVME_DEV_TYPE)
