# MaxKB 对接企业微信

MaxKB-Ent 是将 MaxKB 与企业微信对接的应用程序。

这是演示程序，仅实现企业微信单点登录与对接MaxKB对话功能。有功能需求，请提交issue。


## 开始使用

> 中国内地Docker仓库已被阻断，请提前使用离线方式安装 rockylinux:9 容器镜像。


### Nginx网关

如果内网已经有对外的 nginx 网关，可参考这个反向代理配置

```config
http {
    # 设置客户端连接超时时间
    client_body_timeout 5m;
    client_header_timeout 5m;
    # 设置代理连接超时时间
    proxy_connect_timeout 5m;
    proxy_send_timeout 5m;
    proxy_read_timeout 5m;
}

server {
    listen      80;
    location /maxkbent/ {
        proxy_pass http://应用服务器IP端口/;
        proxy_set_header Host      $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $http_connection;
        proxy_set_header Proxyser gateway_proxy_node_root;
    }
    location /maxkbent_api/ {
        proxy_pass http://前端服务器IP端口/;
        proxy_set_header Host      $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header REMOTE-HOST $remote_addr;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $http_connection;
    }
}
```

### 修改接口配置文件

接口配置文件位于 config/*.json

database.json   
这个文件可以留空值，当前项目没有使用数据库
```json
{
    "mysql": "mysql+pymysql://数据库账号:数据库密码@数据库IP/maxkbent?&autocommit=true", 
    "elasticsearch": "http://elastic:ES密码@ES节点IP:9200", 
    "redis": "redis://redis服务器IP"
}
```

maxkb.json
```json
{
    "api": "http://maxkb服务器的IP和端口/api", 
    "apps": {
        "dealerit": {
            "apikey": "maxkb的应用 api key"
        }
    }
}
```

vwork.json  
appurl 是前端的访问地址，apiurl是前端的接口地址。
```json
{
    "appid": "企业微信应用ID", 
    "appurl": "http://domain/maxkbent", 
    "secret": "企业微信应用密钥", 
    "apiurl": "http://domain/maxkbent_api"
}
```

### 修改前端页面服务配置文件

前端使用 nginx 来处理跨域问题，配置文件为： ui/nginx.conf

```config
# 修改 nginx.conf 文件的第74行，填写maxkbnet接口服务器的IP和地址。
# 如下面示例：
proxy_pass http://192.168.10.56:5000/;      #接口服务器IP
```

### 打包容器

```shell
# 打包接口
docker build ./ -t maxkbentapi:0.1

# 打包前端
cd ui
npm install     # 首次运行
npm run build 
docker build ./ -t maxkbnetweb:0.1

```

### 启动应用

```shell
docker run --rm  -p 自定义你的接口端口:5000 maxkbentapi:0.1 
docker run --rm  -p 自定义你的前端端口:80   maxkbentweb:0.1
```

### 企业微信应用配置

设置应用主页：http://域名/maxkbent_api/auth/vwork?&ver=1


## 技术栈

-   前端：[Vue.js](https://cn.vuejs.org/) \ [elementui](https://element.eleme.cn)
-   后端：[Python / Flask](https://flask.palletsprojects.com)

## 许可 

Copyright (c) 1994-2024 删库不跑路的杨主任

This project is licensed under the MIT License - see the [LICENSE](https://opensource.org/licenses/MIT) for details.

