import logging
import pytest
import allure

from tests.pytestCase.Common.utils import blkdev_util, dev_util, session_util
from tests.pytestCase.conftest import unlogin

BLK_DEV_TYPE = 'blk'
LEGACY_QUEUE_TYPE = 'Legacy'


@allure.suite('Cloud_Base_TestCase')
class TestLegacyBlkDev:
    DEV_TYPE: str = BLK_DEV_TYPE
    DEV_QUEUE_TYPE: str = LEGACY_QUEUE_TYPE

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41755')
    @allure.title("blk-legacy-设备控制面协商driverOK")
    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    def test_blkpf_legacy_driver_ok(self, login, unlogin):
        # 0.pre 登录前后端成功,确认host端加载驱动成功
        it_session = login
        n2_session, host_session = session_util.pretest(it_session, self.DEV_TYPE)

        # 1. 进入后端诊断模块msg_cmd，输入查询命令device list,并对
        dev_list = dev_util.get_dev_list(n2_session)

        # 2.查看split (modern)队列类型的BLK PF设备状态是否OK。
        ret = dev_util.check_modern_pf_status(dev_list, self.DEV_TYPE)
        assert ret
        logging.info("test_blkpf_modern_driver_ok pass")
        unlogin

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41756')
    @allure.title("blk-legacy-多设备多队列FIO随机包流通（512B-1MB）")
    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    def test_blkpf_legacy_multidev_io(self, login, unlogin):
        it_session = login
        blkdev_util.blkpf_multidev_io(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)
        unlogin

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41757')
    @allure.title("blk-legacy-host反复加载卸载virtio-blk驱动，FIO流通")
    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    def test_blkpf_legacy_multidev_reload_driver(self, login, unlogin):
        it_session = login
        blkdev_util.blkpf_multidev_reload_driver(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)
        unlogin

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41758')
    @allure.title("blk-legacy-host reset，加载virtio-blk驱动，FIO流通")
    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    def test_blkpf_legacy_multidev_host_reset(self, login, unlogin):
        it_session = login
        blkdev_util.blkpf_multidev_host_reset(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)
        unlogin

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41759')
    @allure.title("blk-legacy-virtio_blk设备热插拔，FIO流通")
    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    def test_blkpf_legacy_multidev_hotplug(self, login):
        it_session = login
        blkdev_util.blkpf_multidev_hotplug(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)
        unlogin

    @allure.feature('COSSW-41760')
    @pytest.mark.timeout(600)
    @allure.title("blk-legacy_virtio-blk，FIO带流kill-9杀掉vhost进程再拉起，FIO恢复")
    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    def test_blkpf_legacy_multidev_io_forcekill_vhost(self, login, unlogin):
        it_session = login
        blkdev_util.blkpf_multidev_io_forcekill_vhost(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)
        unlogin


MODERN_QUEUE_TYPE = 'Modern'


@allure.suite('Cloud_Base_TestCase')
class TestModernBlkDev:
    DEV_TYPE: str = BLK_DEV_TYPE
    DEV_QUEUE_TYPE: str = MODERN_QUEUE_TYPE

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @allure.feature('COSSW-41769')
    @allure.title("blk-modern-设备控制面协商driverOK")
    def test_blkpf_modern_driver_ok(self, login, unlogin):
        # 0.pre 登录前后端成功,确认host端加载驱动成功
        it_session = login
        n2_session, host_session = session_util.pretest(it_session, self.DEV_TYPE)

        # 1. 进入后端诊断模块msg_cmd，输入查询命令device list,并对
        dev_list = dev_util.get_dev_list(n2_session)

        # 2.查看split (modern)队列类型的BLK PF设备状态是否OK。
        ret = dev_util.check_modern_pf_status(dev_list, self.DEV_TYPE)
        assert ret
        logging.info("test_blkpf_modern_driver_ok pass")
        unlogin

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41770')
    @allure.title("blk-modern-多设备多队列FIO随机包流通（512B-1MB）")
    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    def test_blkpf_modern_multidev_io(self, login, unlogin):
        it_session = login
        blkdev_util.blkpf_multidev_io(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)
        unlogin

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41771')
    @allure.title("blk-modern-host反复加载卸载virtio-blk驱动，FIO流通")
    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    def test_blkpf_modern_multidev_reload_driver(self, login, unlogin):
        it_session = login
        blkdev_util.blkpf_multidev_reload_driver(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)
        unlogin

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41772')
    @allure.title("blk-modern-host reset，加载virtio-blk驱动，FIO流通")
    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    def test_blkpf_modern_multidev_host_reset(self, login, unlogin):
        it_session = login
        blkdev_util.blkpf_multidev_host_reset(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)
        unlogin

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41773')
    @allure.title("blk-modern-virtio_blk设备热插拔，FIO流通")
    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    def test_blkpf_modern_multidev_hotplug(self, login, unlogin):
        it_session = login
        blkdev_util.blkpf_multidev_hotplug(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)
        unlogin

    @allure.feature('COSSW-41774')
    @pytest.mark.timeout(600)
    @allure.title("blk-modern-virtio_blk，FIO带流kill-9杀掉vhost进程再拉起，FIO恢复")
    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    def test_blkpf_modern_multidev_io_forcekill_vhost(self, login, unlogin):
        it_session = login
        blkdev_util.blkpf_multidev_io_forcekill_vhost(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)
        unlogin


PACKED_QUEUE_TYPE = 'Packed'


@allure.suite('Cloud_Base_TestCase')
class TestPackedBlkDev:
    DEV_TYPE: str = BLK_DEV_TYPE
    DEV_QUEUE_TYPE: str = PACKED_QUEUE_TYPE

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41776')
    @allure.title("blk-packed-设备控制面协商driverOK")
    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    def test_blkpf_packed_driver_ok(self, login, unlogin):
        # 0.pre 登录前后端成功,确认host端
        # 加载驱动成功
        it_session = login
        n2_session, host_session = session_util.pretest(it_session, self.DEV_TYPE)

        # 1. 进入后端诊断模块msg_cmd，输入查询命令device list,并对
        dev_list = dev_util.get_dev_list(n2_session)

        # 2.查看packed队列类型的BLK PF设备状态是否OK。
        ret = dev_util.check_packed_pf_status(dev_list, self.DEV_TYPE)
        assert ret

        logging.info("test_blkpf_packed_driver_ok pass")
        unlogin

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41786')
    @allure.title("blk-packed-多设备多队列FIO随机包流通（512B-1MB）")
    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    def test_blkpf_packed_multidev_io(self, login, unlogin):
        it_session = login
        blkdev_util.blkpf_multidev_io(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)
        unlogin

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41787')
    @allure.title("blk-packed-host反复加载卸载virtio-blk驱动，FIO流通")
    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    def test_blkpf_packed_multidev_reload_driver(self, login, unlogin):
        it_session = login
        blkdev_util.blkpf_multidev_reload_driver(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)
        unlogin

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41772')
    @allure.title("blk-packed-host reset，加载virtio-blk驱动，FIO流通")
    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    def test_blkpf_packed_multidev_host_reset(self, login, unlogin):
        it_session = login
        blkdev_util.blkpf_multidev_host_reset(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)
        unlogin

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41759')
    @allure.title("blk-packed-virtio_blk设备热插拔，FIO流通")
    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    def test_blkpf_packed_multidev_hotplug(self, login):
        it_session = login
        blkdev_util.blkpf_multidev_hotplug(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)
        unlogin

    @allure.feature('COSSW-41760')
    @pytest.mark.timeout(600)
    @allure.title("blk-packed-virtio_blk，FIO带流kill-9杀掉vhost进程再拉起，FIO恢复")
    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    def test_blkpf_packed_multidev_io_forcekill_vhost(self, login, unlogin):
        it_session = login
        blkdev_util.blkpf_multidev_io_forcekill_vhost(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)
        unlogin
