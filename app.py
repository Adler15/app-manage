import logging
import socket

from flask import Flask

from container.app_container import container as container_blueprint
from image.app_image import image as image_blueprint
from nacos_proxy.nacos_proxy import NacosProxy

# logging.basicConfig函数对日志的输出格式及方式做相关配置
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

# 注册各个板块的蓝图
app = Flask(__name__)
app.register_blueprint(container_blueprint, url_prefix='/container')
app.register_blueprint(image_blueprint, url_prefix='/image')

# 读取配置文件中的 nacos地址
app.config.from_pyfile('env.ini', silent=True)
nacos_address = app.config['NACOS_ADDRESS']
service_ip = app.config['SERVICE_IP']
service_port = app.config['SERVICE_PORT']

# nacos的服务注册
global_nacos_proxy = NacosProxy()
# hostname = socket.gethostname()
# local_address = socket.gethostbyname(hostname)
global_nacos_proxy.register_nacos('docker-api-service', nacos_address, service_ip, service_port, 'DEFAULT')


# 获取nacos配置信息
# data_id = "app-manage-service.yaml"
# group = "DEFAULT_GROUP"
# global_nacos_proxy.fetch_remote_config(data_id, group)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8091)
