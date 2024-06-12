FROM rockylinux:9
# 系统环境
ENV LANG C.UTF-8
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN sed -e 's|^mirrorlist=|#mirrorlist=|g' \
    -e 's|^#baseurl=http://dl.rockylinux.org/$contentdir|baseurl=https://mirrors.aliyun.com/rockylinux|g' \
    -i.bak /etc/yum.repos.d/rocky-*.repo && dnf install epel-release -y
RUN yum install python3 python3-pip -y
RUN groupadd --gid 5000 py \
  && useradd --home-dir /home/py --create-home --uid 5000 \
    --gid 5000 --shell /bin/sh --skel /dev/null py \
  && yum install passwd -y && echo 'maxkbent' | passwd --stdin root
# 基础环境
WORKDIR /usr/app
#   安装接口服务所需包
ADD requirements.txt /usr/app/
RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple --upgrade pip \
    && pip3 install -r /usr/app/requirements.txt -i https://mirrors.aliyun.com/pypi/simple

#   安装接口服务
COPY ./applib /usr/app/applib
COPY ./views /usr/app/views
ADD app.py /usr/app/
ADD config/database.json /usr/app/config/
ADD config/maxkb.json /usr/app/config/
ADD config/vwork.json /usr/app/config/

USER py

ENTRYPOINT ["python3","app.py"]
