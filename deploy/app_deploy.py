import logging
import traceback

import docker
from flask import Blueprint, request, jsonify

deploy = Blueprint('deploy', __name__)

client = docker.DockerClient(base_url='unix://var/run/docker.sock')


@deploy.route('/stop')
def stop_app():
    try:
        container_id = request.args.get('container_id')
        logging.info(f'接受的容器id为：{container_id}')
        container = client.containers.get(container_id)
        container.stop()
        logging.info(f'容器 {container.name} 已关闭')
        return jsonify(message='关闭成功', container_id=container.short_id, container_name=container.name), 200
    except:
        logging.error(f'关闭错误，错误原因：{traceback.format_exc()}')
        return jsonify(message='关闭失败', error_info=traceback.format_exc()), 500


@deploy.route('/restart')
def restart_app():
    try:
        container_id = request.args.get('container_id')
        logging.info(f'接受的容器id为：{container_id}')
        container = client.containers.get(container_id)
        container.restart()
        logging.info(f'容器 {container.name} 已重启')
        return jsonify(message='启动成功', container_id=container.short_id, container_name=container.name), 200
    except:
        logging.error(f'关闭错误，错误原因：{traceback.format_exc()}')
        return jsonify(message='启动失败', error_info=traceback.format_exc()), 500


@deploy.route('/image')
def remove_image():
    try:
        image_name = request.args.get('image_name')
        client.images.remove(image=image_name)
        logging.info(f'镜像 {image_name} 已删除')
        return jsonify(message='删除镜像成功', image_name=image_name), 200
    except:
        logging.error(f'删除镜像错误，错误原因：{traceback.format_exc()}')
        return jsonify(message='删除镜像失败', error_info=traceback.format_exc()), 500


@deploy.route('/container')
def remove_contain():
    try:
        container_id = request.args.get('container_id')
        container = client.containers.get(container_id)
        container.remove(force=True)
        logging.info(f'删除容器 {container.name} 成功')
        return jsonify(message='删除镜像成功', container_name=container.name), 200
    except:
        logging.error(f'删除容器错误，错误原因：{traceback.format_exc()}')
        return jsonify(message='删除容器失败', error_info=traceback.format_exc()), 500
