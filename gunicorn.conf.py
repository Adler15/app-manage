from gevent import monkey

monkey.patch_all()

import multiprocessing

bind = "0.0.0.0:8091"

# 启动的进程数
workers = multiprocessing.cpu_count()
worker_class = 'gevent'

# Logging
accesslog = '-'
loglevel = 'info'
# loglevel = 'debug'
logfile = './log/app.log'
# 设置gunicorn访问日志格式，错误日志无法设置
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
