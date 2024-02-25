"""
__author__= 'vinny.yang'
"""
import logging
import os
import pytest
import sys

from tests.pytestCase.Common.Object.ItestSession import SimSession, ItSessionFactory

sys.path.append(os.getcwd())


def pytest_addoption(parser):
    group = parser.getgroup('JaguarMrico Itest')
    group.addoption("--env-type",
                    default="SIM",
                    dest="env-type",
                    help="set test run env-type,eg.SIM,EMU,CRB,HYBRID")
    group.addoption("--env-sub-type",
                    default="all",
                    dest="env-sub-type",
                    help="set test run env-sub-type,eg.all,LEGACY,MODERN,PACKED,NVME")


# # 定义一个参数化的fixture，参数化的值是scope
# @pytest.fixture(params=["SIM", "EMU", "HYBRID"])
# def env_type(request):
#     if request.param == "SIM":
#         env_type = "SIM"


@pytest.fixture(scope="session", autouse=True)
def environment(request):
    env_type = request.config.getoption("--env-type")
    env_sub_type = request.config.getoption("--env-sub-type")
    logging.info(f"env_type: {env_type}, env_sub_type: {env_sub_type}")
    return {"env_type": env_type, "env_sub_type": env_sub_type}


def login_scope(environment):
    env_type = environment["env_type"]
    logging.info(f"env_type: {env_type}")
    if env_type == "SIM":
        scope = "class"
    elif env_type == "EMU":
        scope = "session"
    elif env_type == "HYBRID":
        scope = "session"
    elif env_type == "CRB":
        scope = "session"
    return scope


def get_itsession(env_type, env_sub_type):
    if env_type == "SIM":
        it_session = SimSession(type)
    elif env_type == "EMU":
        scope = "session"
    elif env_type == "CRB":
        scope = "session"
    elif env_type == "HYBRID":
        scope = "session"


# # 在测试函数中获取命令行选项的值
# @pytest.fixture(scope="session", autouse=True)
# def environment(request):
#     env_type = request.config.getoption("--env-type")
#     env_sub_type = request.config.getoption("--env-sub-type")
#     return {"env_type": env_type, "env_sub_type": env_sub_type}

@pytest.fixture(scope="class")
def login(request, environment):
    # 1. 获取配置信息,并完成登录
    env_type = environment["env_type"]
    p_dev_type = request.param
    dev_type = p_dev_type.upper()
    logging.info(f"env_type: {env_type}, dev_type: {dev_type}")
    it_session = ItSessionFactory.create_itSession(env_type, dev_type)

    # it_session = SimSession(type)
    #
    # 2. 获取N2_SSHSession
    N2_SSHSession = it_session.get_n2_session()
    assert N2_SSHSession.connect() == 0
    # 3. 获取host_SSHSession
    host_SSHSession = it_session.get_host_session()
    assert host_SSHSession.connect() == 0

    logging.info("完成登录")
    yield it_session


@pytest.fixture(scope="class")
def unlogin(login):
    yield
    it_session = login
    it_session.close()
    N2_SSHSession = it_session.get_n2_session()
    host_SSHSession = it_session.get_host_session()

    assert N2_SSHSession is None
    assert host_SSHSession is None
    logging.info("完成登出")
