'''
鉴权视图库
'''
#import uuid
import time
#import datetime
import logging
import requests
#import redis
from flask import request, redirect, make_response, g
from flask import session as flasksession
from flask.views import MethodView
from applib import apibase, config, cipher, sqldb


class Vwork(MethodView, apibase.ViewBase): 

    def __init__(self) -> None: 
        super().__init__()

    def get(self): 
        vworkconfig = config.Vwork()
        if request.args.get('code') is None: 
            session = flasksession.get('session')
            url = "https://open.weixin.qq.com/connect/oauth2/authorize?" + \
                "appid=" + vworkconfig.appid + \
                '&session=' + session + \
                "&redirect_uri=" + vworkconfig.apiurl + '/auth/vwork' \
                "&response_type=code" + \
                "&scope=snsapi_base" + \
                "&state=STATE" + \
                "&connect_redirect=1#wechat_redirect"
            url.replace('\t', "")
            return redirect(url, 307)
        if request.args.get('code') is not None: 
            #
            session = flasksession.get('session')
            logging.info('企业微信用户 code 重定向，session: ' + session)
            # 请求企业微信 token
            gettokenurl = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?' + \
                'corpid=' + vworkconfig.appid + \
                '&corpsecret=' + vworkconfig.secret
            tokendata = requests.get(gettokenurl).json()
            if tokendata.get('errcode') != 0:
                logging.warn(
                    "微信 /cgi-bin/gettoken 接口返回非 0 状态。" + str(
                        tokendata.get('errmsg')
                    ))
                return "企业微信登录失败。", 500
            # 获取员工编号
            getuserurl = 'https://qyapi.weixin.qq.com' + \
                '/cgi-bin/auth/getuserinfo?' + \
                'access_token=' + tokendata['access_token'] + \
                '&code=' + str(request.args.get('code'))
            userinfo = requests.get(getuserurl).json()
            if userinfo.get('errcode') != 0: 
                logging.warn("用户信息获取失败，微信服务器返回:" + \
                    str(userinfo) + '    session:' + session)
                return '获取企业微信用户身份失败，' + session +'，请重新打开。' + \
                    '一直无法打开，请联系系统管理员。', 500
            # 使用员工编号生成 token 令牌
            res = make_response(
                redirect(
                    vworkconfig.appurl + '?&vwork_login=1?&session=' + session, 307))
            res.set_cookie('maxkb_ent_token', cipher.Token().Encrypt(
                cipher.TokenData(
                    userinfo.get('userid'), session, int(time.time()) + 36000)
            ))
            logging.info('企业微信用户登录，%s', str(userinfo))
            return res

        return self.RETURN.Dict()
    pass

'''
NOTE: 
    maxkb-ent 是从作者所在公司的应用系统中剥离出来的。
    作者所在公司没有使用 LDAP ，因此，暂时不在这里实现 LDAP的对接。
'''
class Login(MethodView, apibase.ViewBase): 
    def __init__(self) -> None: 
        super().__init__()
        
    def post(self): 
        # 解密密码字符
        pwd = self.DecryptClientPWD(request.json.get('pwd'))
        if pwd is None: 
            self.RETURN.message = 'pwd 密码无效，无法验证密文，请检查加密参数。'
            self.RETURN.status = apibase.Status.UNAUTH
            return self.RETURN.Dict()
        # 验证登录信息
        if (pwd == 'maxkbent' and request.json.get('name') == 'maxkbent'): 
            self.RETURN.message = '登录成功。'
            self.RETURN.status = apibase.Status.SUCCESS

            retoken = cipher.Token().Encrypt(cipher.TokenData(
                request.json.get('name'), 
                flasksession.get('session'),
                int(time.time()) + 30000
            ))
            redata = {
                'expire': int(time.time()) + 30000, 
                'token': retoken ,
                'session': flasksession.get('session')
            }
            self.RETURN.results = redata
            return self.RETURN.Dict()
        else: 
            logging.info('用户登录失败，%s  %s', 
                request.json.get('name'), request.json.get('pwd'))
            self.RETURN.message = '登录失败，请检查用户名或密码是否正确。'
            self.RETURN.status = apibase.Status.UNAUTH
            return self.RETURN.Dict()
    
    def DecryptClientPWD(self,pwd:str): 
        ''' 解密客户端的密码，解密失败时，返回 None '''
        key = b'QWERTYUIOPa00000'
        iv =  b'0000000000000000'
        try: 
            aes = cipher.AEScryptor(
                key, 
                cipher.AES.MODE_CBC, 
                iv,paddingMode="ZeroPadding", 
                characterSet='utf-8')
            return aes.decryptFromBase64(pwd).toString()
        except Exception as e: 
            logging.warn('解密客户端密码失败，%s  %s', pwd, str(e))
            return None

    def DecryptDataBasePWD(self, pwd:str): 
        ''' 解密数据库的密码，失败时，返回 None '''
        try: 
            aes = cipher.AEScryptor(
                cipher.KEY, 
                cipher.AES.MODE_CBC, 
                cipher.IV, 
                paddingMode='ZeroPadding')
            return aes.decryptFromBase64(pwd).toString()
        except Exception as e: 
            logging.warn('解密数据库用户密码失败，%s  %s', pwd, str(e))

    pass