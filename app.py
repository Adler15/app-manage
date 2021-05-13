import logging
import socket

from flask import Flask

from deploy.app_deploy import deploy as deploy_blueprint
from install.app_install import install as install_blueprint
from nacos_proxy.nacos_proxy import NacosProxy

# logging.basicConfig函数对日志的输出格式及方式做相关配置
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

# 注册各个板块的蓝图
app = Flask(__name__)
app.register_blueprint(deploy_blueprint, url_prefix='/deploy')
app.register_blueprint(install_blueprint, url_prefix='/install')

# nacos的服务注册
global_nacos_proxy = NacosProxy()
hostname = socket.gethostname()
local_address = socket.gethostbyname(hostname)
global_nacos_proxy.register_nacos('app-manage-service', '192.168.130.117', local_address, 5000, 'DEFAULT')


# 获取nacos配置信息
# data_id = "app-manage-service.yaml"
# group = "DEFAULT_GROUP"
# global_nacos_proxy.fetch_remote_config(data_id, group)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8091)
