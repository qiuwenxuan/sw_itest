import logging

import pytest
import allure


from tests.pytestCase.Common.utils import netdev_util, dev_util, session_util

NET_DEV_TYPE = "net"
MODERN_QUEUE_TYPE = 'Modern'
LEGACY_QUEUE_TYPE = 'Legacy'
PACKED_QUEUE_TYPE = 'Packed'


@allure.suite('Cloud_Base_TestCase')
class TestModernNetDev:
    DEV_TYPE: str = NET_DEV_TYPE
    DEV_QUEUE_TYPE: str = MODERN_QUEUE_TYPE

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @allure.feature('COSSW-41701')
    @allure.title("net modern设备控制面协商driverOK")
    def test_netpf_modern_driver_ok(self, login):
        # 0.pre 登录前后端成功,确认host端加载驱动成功
        it_session = login
        n2_session, host_session = session_util.pretest(it_session, NET_DEV_TYPE)

        # 1. 进入后端诊断模块msg_cmd，输入查询命令device list,并对命令结果解析
        dev_list = dev_util.get_dev_list(n2_session)

        # 2.查看split (modern)队列类型的NET PF设备状态是否OK。
        ret = dev_util.check_modern_pf_status(dev_list, NET_DEV_TYPE)
        assert ret
        logging.info("test_netpf_modern_driver_ok pass")

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @allure.feature('COSSW-41761')
    @allure.title("net modern多设备多队列慢速路径流通(host-host)")
    def test_netpf_modern_multidev_host_host_lsp(self, login):
        it_session = login
        netdev_util.netpfdev_host_host_lsp(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41760')
    @allure.title("net modern多设备多队列慢速路径流通(host-uplink)")
    def test_netpf_modern_multidev_host_uplink_lsp(self, login):
        it_session = login
        netdev_util.netpfdev_host_uplink_lsp(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41762')
    @allure.title("net modern多设备多队列慢速路径流通(uplink-host)")
    def test_netpf_modern_multidev_uplink_host_lsp(self, login):
        it_session = login
        netdev_util.netpf_multidev_uplink_host_lsp(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41763')
    @allure.title("net modern多设备多队列快慢速路径叠加流通(uplink-host & uplink-host offload)")
    def test_netpf_modern_multidev_uplink_host_offload(self, login):
        it_session = login
        netdev_util.netpf_multidev_uplink_host_offload(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41764')
    @allure.title("net modern多设备多队列ctrlqueue反复修改active qp(uplink-host)")
    def test_netpf_modern_multidev_ctrlqueue_modify_qp_uplink_host(self, login):
        it_session = login
        netdev_util.netpf_multidev_ctrlqueue_modify_qp_uplink_host(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41765')
    @allure.title("net modern多设备多队列virtio net为PF设备，host反复加载卸载virtio_net驱动，慢速路径流通(host-uplink)")
    def test_netpf_modern_multidev_reload_driver_host_uplink(self, login):
        it_session = login
        netdev_util.netpf_multidev_reload_driver_host_uplink(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41766')
    @allure.title("net modern多设备多队列host reset，加载virtio_net驱动，慢速路径流通(uplink-host & uplink-host offload)")
    def test_netpf_modern_multidev_host_reset_uplink_host_and_offload(self, login):
        it_session = login
        netdev_util.netpf_multidev_host_reset_uplink_host_and_offload(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41767')
    @allure.title("net modern多设备多队列virtio net为PF设备，virtio_net设备热插拔,慢速路径流通(uplink-host & uplink-host offload)")
    def test_netpf_modern_multidev_hotplug_uplink_host_and_offload(self, login):
        it_session = login
        netdev_util.netpf_multidev_hotplug_uplink_host_and_offload(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-0000')
    @allure.title("net modern多设备多队列支持ovs断链后自动重连")
    def test_netpf_modern_multidev_ovs_reconnect(self, login):
        it_session = login
        netdev_util.netpf_multidev_ovs_reconnect(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41768')
    @allure.title("net modern多设备多队列支持hyper-commander断链后自动重连")
    def test_netpf_modern_multidev_hyper_commander_reconnect(self, login):
        it_session = login
        netdev_util.netpf_multidev_hyper_commander_reconnect(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)


@allure.suite('Cloud_Base_TestCase')
class TestLegacyNetDev:
    DEV_TYPE: str = NET_DEV_TYPE
    DEV_QUEUE_TYPE: str = LEGACY_QUEUE_TYPE

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @allure.feature('COSSW-41747')
    @allure.title("net Legacy设备控制面协商driverOK")
    def test_netpf_legacy_driver_ok(self, login):
        # 0.pre 登录前后端成功,确认host端加载驱动成功
        it_session = login
        n2_session, host_session = session_util.pretest(it_session, NET_DEV_TYPE)

        # 1. 进入后端诊断模块msg_cmd，输入查询命令device list,并对
        dev_list = dev_util.get_dev_list(n2_session)

        # 2.查看split (legacy)队列类型的NET PF设备状态是否OK。
        ret = dev_util.check_legacy_pf_status(dev_list, NET_DEV_TYPE)
        assert ret
        logging.info("test_netpf_legacy_driver_ok pass")

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @allure.feature('COSSW-41733')
    @allure.title("net legacy多设备多队列慢速路径流通(host-host)")
    def test_netpf_legacy_multidev_host_host_lsp(self, login):
        it_session = login
        netdev_util.netpfdev_host_host_lsp(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-8321')
    @allure.title("net legacy多设备多队列慢速路径流通(host-uplink)")
    def test_netpf_legacy_multidev_host_uplink_lsp(self, login):
        it_session = login
        netdev_util.netpfdev_host_uplink_lsp(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41748')
    @allure.title("net legacy多设备多队列慢速路径流通(uplink-host)")
    def test_netpf_legacy_multidev_uplink_host_lsp(self, login):
        it_session = login
        netdev_util.netpf_multidev_uplink_host_lsp(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41749')
    @allure.title("net legacy多设备多队列快慢速路径叠加流通(uplink-host & uplink-host offload)")
    def test_netpf_legacy_multidev_uplink_host_offload(self, login):
        it_session = login
        netdev_util.netpf_multidev_uplink_host_offload(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41750')
    @allure.title("net legacy多设备多队列ctrlqueue反复修改active qp(uplink-host)")
    def test_netpf_legacy_multidev_ctrlqueue_modify_qp_uplink_host(self, login):
        it_session = login
        netdev_util.netpf_multidev_ctrlqueue_modify_qp_uplink_host(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41751')
    @allure.title("net legacy多设备多队列virtio net为PF设备，host反复加载卸载virtio_net驱动，慢速路径流通(host-uplink)")
    def test_netpf_legacy_multidev_reload_driver_host_uplink(self, login):
        it_session = login
        netdev_util.netpf_multidev_reload_driver_host_uplink(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41752')
    @allure.title("net legacy多设备多队列host reset，加载virtio_net驱动，慢速路径流通(uplink-host & uplink-host offload)")
    def test_netpf_legacy_multidev_host_reset_uplink_host_and_offload(self, login):
        it_session = login
        netdev_util.netpf_multidev_host_reset_uplink_host_and_offload(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41753')
    @allure.title(
        "net legacy多设备多队列virtio net为PF设备，virtio_net设备热插拔,慢速路径流通(uplink-host & uplink-host offload)")
    def test_netpf_legacy_multidev_hotplug_uplink_host_and_offload(self, login):
        it_session = login
        netdev_util.netpf_multidev_hotplug_uplink_host_and_offload(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-8321')
    @allure.title("net legacy多设备多队列支持ovs断链后自动重连")
    def test_netpf_legacy_multidev_ovs_reconnect(self, login):
        it_session = login
        netdev_util.netpf_multidev_ovs_reconnect(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41754')
    @allure.title("net legacy多设备多队列支持hyper-commander断链后自动重连")
    def test_netpf_legacy_multidev_hyper_commander_reconnect(self, login):
        it_session = login
        netdev_util.netpf_multidev_hyper_commander_reconnect(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)


@allure.suite('Cloud_Base_TestCase')
class TestPackedNetDev:
    DEV_TYPE: str = NET_DEV_TYPE
    DEV_QUEUE_TYPE: str = PACKED_QUEUE_TYPE

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @pytest.mark.parametrize("login", ["Packed"], indirect=True)
    @allure.feature('COSSW-41776')
    @allure.title("net packed设备控制面协商driverOK")
    def test_netpf_packed_driver_ok(self, login):
        # 0.pre 登录前后端成功,确认host端加载驱动成功
        it_session = login
        n2_session, host_session = session_util.pretest(it_session, NET_DEV_TYPE)

        # 1. 进入后端诊断模块msg_cmd，输入查询命令device list,并对命令结果解析
        dev_list = dev_util.get_dev_list(n2_session)

        # 2.查看split (legacy)队列类型的NET PF设备状态是否OK。
        ret = dev_util.check_packed_pf_status(dev_list, NET_DEV_TYPE)
        assert ret
        logging.info("test_netpf_packed_driver_ok pass")

    @pytest.mark.SW_ITEST
    @pytest.mark.timeout(600)
    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @allure.feature('COSSW-41777')
    @allure.title("net legacy多设备多队列慢速路径流通(host-host)")
    def test_netpf_packed_multidev_host_host_lsp(self, login):
        it_session = login
        netdev_util.netpfdev_host_host_lsp(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41778')
    @allure.title("net packed多设备多队列ctrlqueue反复修改active qp(uplink-host)")
    def test_netpf_packed_multidev_ctrlqueue_modify_qp_uplink_host(self, login):
        it_session = login
        netdev_util.netpf_multidev_ctrlqueue_modify_qp_uplink_host(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41779')
    @allure.title("net packed多设备多队列慢速路径流通(uplink-host)")
    def test_netpf_packed_multidev_uplink_host_lsp(self, login):
        it_session = login
        netdev_util.netpf_multidev_uplink_host_lsp(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41780')
    @allure.title("net packed多设备多队列快慢速路径叠加流通(uplink-host & uplink-host offload)")
    def test_netpf_packed_multidev_uplink_host_offload(self, login):
        it_session = login
        netdev_util.netpf_multidev_uplink_host_offload(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41781')
    @allure.title("net packed多设备多队列ctrlqueue反复修改active qp(uplink-host)")
    def test_netpf_packed_multidev_ctrlqueue_modify_qp_uplink_host(self, login):
        it_session = login
        netdev_util.netpf_multidev_ctrlqueue_modify_qp_uplink_host(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41782')
    @allure.title("net packed多设备多队列virtio net为PF设备，host反复加载卸载virtio_net驱动，慢速路径流通(host-uplink)")
    def test_netpf_packed_multidev_reload_driver_host_uplink(self, login):
        it_session = login
        netdev_util.netpf_multidev_reload_driver_host_uplink(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41783')
    @allure.title("net packed多设备多队列host reset，加载virtio_net驱动，慢速路径流通(uplink-host & uplink-host offload)")
    def test_netpf_packed_multidev_host_reset_uplink_host_and_offload(self, login):
        it_session = login
        netdev_util.netpf_multidev_host_reset_uplink_host_and_offload(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41784')
    @allure.title("net packed多设备多队列virtio net为PF设备，virtio_net设备热插拔,慢速路径流通(uplink-host & uplink-host offload)")
    def test_netpf_packed_multidev_hotplug_uplink_host_and_offload(self, login):
        it_session = login
        netdev_util.netpf_multidev_hotplug_uplink_host_and_offload(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41785')
    @allure.title("net packed多设备多队列支持ovs断链后自动重连")
    def test_netpf_packed_multidev_ovs_reconnect(self, login):
        it_session = login
        netdev_util.netpf_multidev_ovs_reconnect(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)

    @pytest.mark.parametrize("login", [DEV_QUEUE_TYPE], indirect=True)
    @pytest.mark.timeout(600)
    @allure.feature('COSSW-41786')
    @allure.title("net packed多设备多队列支持hyper-commander断链后自动重连")
    def test_netpf_packed_multidev_hyper_commander_reconnect(self, login):
        it_session = login
        netdev_util.netpf_multidev_hyper_commander_reconnect(it_session, self.DEV_TYPE, self.DEV_QUEUE_TYPE)