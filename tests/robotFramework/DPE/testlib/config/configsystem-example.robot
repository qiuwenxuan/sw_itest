*** Settings ***
Documentation     测试testpmd，需要启动在screen -R testpmdzho中，dut type为testpmd
...               | 设备名称包括 cha1/cha2/dut1/dut2/dut3
...               | dut1ip
...               | dut1port
...               | dut1type   linux / testpmd
...               | dut1user
...               | dut1password
...               | dut1port101 连接 cha1port1
...               | dut1port201 连接 cha2port1

*** Variables ***
${dut1ip}         10.20.25.154
${dut1port}       2250
${dut1type}       linux
${dut2ip}         10.42.119.55
${dut2port}       2002
${dut1user}       root
${dut1password}    qwe123
${cha1ip}         10.20.69.12
${cha1port}       4500
${cha1type}       cha
${cha1port1}      101/0
${cha1port2}      101/1
${dut1port101}    0000:00:15.0
${dut1port102}    0000:00:17.0
