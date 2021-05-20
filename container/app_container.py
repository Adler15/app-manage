import logging
import traceback

import docker
from flask import Blueprint, request, jsonify

container = Blueprint('container', __name__)

client = docker.DockerClient(base_url='unix://var/run/docker.sock')


@container.route('/run')
def run_container():
    try:
        image_name = request.args.get('image_name')
        logging.info(f'接受的镜像名为：{image_name}')
        c = client.containers.run(image=image_name, ports={8090: 8090}, name=image_name.split(':')[0],
                                  detach=True)
        logging.info(f'容器 {c.name} 已启动')
        return jsonify(status='SUCCESS', message='启动成功', container_id=c.short_id,
                       container_name=c.name), 200
    except:
        logging.error(f'启动错误，错误原因：{traceback.format_exc()}')
        return jsonify(status='FAILED', message='启动失败', error_info=traceback.format_exc()), 500


@container.route('/stop')
def stop_container():
    try:
        container_id = request.args.get('container_id')
        logging.info(f'接受的容器id为：{container_id}')
        c = client.containers.get(container_id)
        c.stop()
        logging.info(f'容器 {c.name} 已关闭')
        return jsonify(status='SUCCESS', message='关闭成功', container_id=c.short_id,
                       container_name=c.name), 200
    except:
        logging.error(f'关闭错误，错误原因：{traceback.format_exc()}')
        return jsonify(status='FAILED', message='关闭失败', error_info=traceback.format_exc()), 500


@container.route('/restart')
def restart_container():
    try:
        container_id = request.args.get('container_id')
        logging.info(f'接受的容器id为：{container_id}')
        c = client.containers.get(container_id)
        c.restart()
        logging.info(f'容器 {c.name} 已重启')
        return jsonify(status='SUCCESS', message='启动成功', container_id=c.short_id,
                       container_name=c.name), 200
    except:
        logging.error(f'关闭错误，错误原因：{traceback.format_exc()}')
        return jsonify(status='FAILED', message='启动失败', error_info=traceback.format_exc()), 500


@container.route('/remove', methods=['DELETE'])
def remove_contain():
    try:
        container_id = request.args.get('container_id')
        c = client.containers.get(container_id)
        c.remove(force=True)
        logging.info(f'删除容器 {c.name} 成功')
        return jsonify(status='SUCCESS', message='删除镜像成功', container_name=c.name), 200
    except:
        logging.error(f'删除容器错误，错误原因：{traceback.format_exc()}')
        return jsonify(status='FAILED', message='删除容器失败', error_info=traceback.format_exc()), 500


@container.route('/status')
def get_container_status():
    try:
        container_id = request.args.get('container_id')
        c = client.containers.get(container_id)
        status = c.status
        status_code = None
        if status == 'running':
            status_code = 1
        elif status == 'exited':
            status_code = 0
        logging.info(f'容器状态为： {status} ')
        return jsonify(status='SUCCESS', message='获取容器状态成功', container_status=status, status_code=status_code), 200
    except:
        logging.error(f'查询容器状态错误，错误原因：{traceback.format_exc()}')
        return jsonify(status='FAILED', message='查询容器状态失败', error_info=traceback.format_exc()), 500
