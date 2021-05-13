from threading import Timer

import nacos


class NacosProxy(object):
    def __init__(self):
        self.config = "not init"
        self.client = None
        self.service_name = None
        self.server_addresses = None
        self.ip = None
        self.port = None
        self.cluster_name = None

    # 注册到nacos
    def register_nacos(self, service_name, server_addresses, ip, port, cluster_name):
        self.service_name = service_name
        self.server_addresses = server_addresses
        self.ip = ip
        self.port = port
        self.cluster_name = cluster_name
        self.client = nacos.NacosClient(self.server_addresses, namespace='public')
        self.client.add_naming_instance(self.service_name, self.ip, self.port, self.cluster_name)
        self.send_heartbeat()

    # 30s发送一次心跳
    def send_heartbeat(self):
        self.client.send_heartbeat(self.service_name, self.ip, self.port, self.cluster_name)
        # print('TimeNow:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        # print("beat")
        t = Timer(30, self.send_heartbeat)
        t.start()

    def fetch_remote_config(self, data_id, group):
        self.config = self.client.get_config(data_id, group)
        print(self.config)

    def get_config(self):
        return self.config
