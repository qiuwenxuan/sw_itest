pip install oslo.log
pip install oslo.log[fixtures]
pip install fixtures



    def test_netdriverOk2(self, login):
        # 登录前端成功
        logging.info("test_netdriverOk2")

    def test_ssh(self, login, unlogin):
        ssh_N2client,ssh_hostServer = login
        logging.info(f"ssh_N2client:{ssh_N2client},ssh_hostServer:{ssh_hostServer}")
        result = ssh_hostServer.execute_command("lsmod | grep -q virtio_net || modprobe virtio_net")
        logging.info(f"result:{result}")
        assert result == ""
