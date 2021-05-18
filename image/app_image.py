import logging
import os
import traceback

import docker
from flask import Blueprint, request, jsonify

image = Blueprint("image", __name__)

client = docker.DockerClient(base_url='unix://var/run/docker.sock')


@image.route('/load', methods=['POST'])
def install_app():
    """
    20210511 当前：根据传入的镜像，load到相应的服务器上
    存在可能：根据传入的jar包，生成相应的镜像
    """
    try:
        # 接受压缩文件
        image_name = request.args.get('image_name')
        # image_file = request.files['image_file']
        # 解压压缩文件
        # test = zipfile.ZipFile(test_file, 'r')
        # 文件的存储目录
        test_path = '/var/k2data/images/'
        # 判断目录是否存在
        # is_exists = os.path.exists(test_path)
        # 不存在就创建
        # if not is_exists:
        #     os.makedirs(test_path)
        # 遍历解压后的文件，并存入相应目录下
        # for f in test.namelist():
        #     test.extract(f, test_path)
        # image_name = secure_filename(image_file.filename)
        # image_file.save(test_path + '/' + image_name)
        # 根据解压的dockerfile生成镜像
        # 加载镜像到服务器
        path = os.path.dirname(test_path)
        real_path = os.path.join(path, image_name)
        with open(real_path, mode='rb') as i:
            image_list = client.images.load(i.read())
            i.close()
            # 根据镜像，启动容器
            i = image_list[0]
            logging.info(f'当前镜像的short_id:{i.short_id},tags:{i.tags[0]}')
            container = client.containers.run(image=i.tags[0], ports={8090: 8090}, name=i.tags[0].split(':')[0],
                                              detach=True)
            logging.info(f'启动镜像：{i.tags[0]} 成功, 容器id为{container.short_id}')
            return jsonify(status='SUCCESS', message='启动成功', image_name=image.tags[0],
                           container_id=container.short_id), 200
    except:
        logging.error(f'启动镜像报错，错误为:{traceback.format_exc()}')
        return jsonify(status='FAILED', message='启动失败', error_info=traceback.format_exc()), 500


@image.route('/remove', methods=['DELETE'])
def remove_image():
    try:
        image_name = request.args.get('image_name')
        client.images.remove(image=image_name)
        logging.info(f'镜像 {image_name} 已删除')
        return jsonify(status='SUCCESS', message='删除镜像成功', image_name=image_name), 200
    except:
        logging.error(f'删除镜像错误，错误原因：{traceback.format_exc()}')
        return jsonify(status='FAILED', message='删除镜像失败', error_info=traceback.format_exc()), 500
