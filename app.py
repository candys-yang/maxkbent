
import sys
import time
import uuid
import logging
from flask import Flask, g, request, session
import views
from applib import apibase, cipher, logs


NOUSE_TOKEN_VIEW = []  # 不要求鉴定token的视图


def BeforeRequest(): 
    # 设置会话ID
    if request.headers.get('session') is not None: 
        session['session'] = request.headers.get('session')
    if session.get('session') is None: 
        session['session'] = str(uuid.uuid4()).replace('-','')
        logging.info('新的用户会话：%s', session.get('session'))
    # Token 验证
    if str(request.url_rule) not in NOUSE_TOKEN_VIEW: 
        req_token = request.headers.get('token')
        if req_token is None: 
            logging.info('一个请求没有携带token，%s', get_flask_request_headers())
            return apibase.API(apibase.Status.UNAUTH, msg='缺少必要的鉴权信息').Dict()
        # 解密token，设置会话变量
        if req_token is not None: 
            tokendata = None
            try:
                # 设置token对象全局变量 
                tokendata = cipher.Token().Decrypt(req_token)
                g.tokenobj = tokendata
            except Exception as e: 
                logging.info('解密请求token失败，%s    %s', str(e), get_flask_request_headers())
                return apibase.API(apibase.Status.UNAUTH, msg='token无效').Dict()
        # 过期token
        if g.tokenobj.expire <= int(time.time()): 
            return apibase.API(apibase.Status.UNAUTH, msg='token过期').Dict() 

    pass

def get_flask_request_headers():
    # 获取请求头并转换为列表形式
    headers_list = [f"{key}: {value}" for key, value in request.headers.items()]
    # 将列表合并为一行，使用空格分隔
    headers_str = ' '.join(headers_list)
    return headers_str

def ErrorRequest_4xx(error): 
    pass

def ErrorRequest_5xx(error): 
    print(error)
    logging.error('')
    return 'Error'


if __name__ == '__main__': 
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config['SESSION_COOKIE_NAME'] = 'maxkbnet-session'
    app.secret_key = 'abc123'
    app.before_request(BeforeRequest)
    app.errorhandler(404)(ErrorRequest_4xx)
    app.errorhandler(500)(ErrorRequest_5xx)
    if '--debug' in sys.argv:  
        app.debug = True
        logging.info("服务启动为 Debug 方式。")
    for i in views.VIEWS: 
        app.add_url_rule(i[0], view_func=i[1].as_view(i[0]))
        if i[2] is False: 
            NOUSE_TOKEN_VIEW.append(i[0])
        logging.info('Load View: %s  ', str(i[0]) )
    app.run(host='0.0.0.0', port=5000)


