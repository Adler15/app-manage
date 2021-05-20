FROM python:3.8.6

ENV TZ Asia/Shanghai

ADD ./  /app

WORKDIR /app

#RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
#RUN pip3 config set install.trusted-host pypi.tuna.tsinghua.edu.cn
RUN pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip3 install -r requirements.txt

CMD ["gunicorn","app:app","-c","gunicorn.conf.py"]
#CMD [ "python", "./app.py" ]

#ENTRYPOINT ["gunicorn", "--config", "gunicorn.conf.py", "app:app"]

# docker run -d -p 8091:8091 --name docker-api-service
# -v /tmp/gunicorn_socket:/tmp/gunicorn_socket
# -v /var/run/docker.sock:/var/run/docker.sock
# -v /home/k2data/bcf-deploy-dist-v1.0.0/bcf/app-images:/k2data/images docker-api-service:0.1
