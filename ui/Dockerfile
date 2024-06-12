#   Docker 容器构建配置文件，用于生成 Docker镜像
#
#   1.  cd 到 itsm_web 目录 ( --registry https://registry.npm.taobao.org )
#   2.  打包前端，npm run build
#   3.  docker build ./ -t 195.168.0.226:80/itsm/maxkbentweb:1.0.1
#   4.  docker push 195.168.0.226:80/itsm/maxkbentweb:1.0.1
# 

FROM rockylinux:9
ENV LANG C.UTF-8
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN dnf install nginx npm -y
ADD nginx.conf /etc/nginx/nginx.conf
COPY dist /var/html
CMD ["nginx", "-g", "daemon off;"]