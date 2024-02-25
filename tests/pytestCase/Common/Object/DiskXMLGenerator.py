import logging
import os
from os.path import abspath


class DiskXMLGenerator:
    # 定义设备名称与vhost的映射
    dev_path_dicts = {
        'vdb': 'vhost.2', 'vdc': 'vhost.3', 'vdd': 'vhost.4',
        'vde': 'vhost.5', 'vdf': 'vhost.6', 'vdg': 'vhost.7',
        'vdh': 'vhost.8', 'vdj': 'vhost.9'
    }
    xml_template = """<disk type='vhostuser' device='disk' model='virtio-transitional'>
      <driver name='qemu' type='raw' queues='4'/>
      <source type='unix' path='/var/tmp/{vhost_value}'>
        <reconnect enabled='yes' timeout='10'/>
      </source>
      <target dev='{blk_dev}' bus='virtio'/>
    </disk>\n"""

    # 创建disk.xml文件类方法
    @classmethod
    def create_disk_xml(cls, dev_lists, file_path='../../tmp'):
        xml_content = ''
        dev_list = []
        # 确保blk_devs是一个列表
        if not isinstance(dev_lists, list):
            dev_list = [dev_lists]
        file_name = 'disk.xml'

        parent_dir = os.path.dirname(os.path.abspath(__file__))
        full_file_path = f"{parent_dir}/{file_path}/{file_name}"
        logging.info(f"\n----------------------------本地disk.xml文件路径full_file_path: {full_file_path}")
        for dev in dev_list:
            # 获取对应的vhost值
            vhost_value = cls.dev_path_dicts.get(dev, '')

            # 使用模板生成特定的XML字符串
            xml_content += cls.xml_template.format(vhost_value=vhost_value, blk_dev=dev)

        # 写入到文件
        with open(full_file_path, 'w') as file:
            file.write(xml_content)
        logging.info(f"\n----------------------------disk.xml:\n {xml_content}")
        return file_name


if __name__ == '__main__':
    # 使用示例
    blk_dev_list = ['vda', 'vdb', 'vdc', 'vde', 'vdf', 'vdg', 'vdh', 'vdj']
    DiskXMLGenerator.create_disk_xml(blk_dev_list)
