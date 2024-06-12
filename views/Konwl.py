'''

'''
import uuid
import json
import time
import datetime
import logging
import requests
from concurrent.futures import ThreadPoolExecutor
from flask import request, g
from flask.views import MethodView
from applib import apibase, redisc, sqldb


class OpenChat(MethodView, apibase.ViewBase): 
    ''' 开启一个会话，获取基础对话信息。 '''
    def __init__(self) -> None: 
        super().__init__()
        self.redisc = redisc.Base()
        self.redis_client = self.redisc.Create_Client()
        # 初始化maxkb接口信息
        try: 
            self.maxkb_conf = json.load(open('config/maxkb.json'))
            self.appinfo = requests.get(
                self.maxkb_conf.get('api') + '/application/profile', 
                headers={ 
                    'AUTHORIZATION': self.maxkb_conf['apps']['dealerit']['apikey'] 
                }
                ).json().get('data')
            self.appid = self.appinfo.get('id')
        except Exception as e: 
            logging.error('初始化 maxkb 相关数据失败，' + str(e))
            pass
    
    def get(self): 
        _url =  '{0}/application/{1}/chat/open'.format(
            self.maxkb_conf.get('api'), self.appid)
        _headers = { 
            'AUTHORIZATION': self.maxkb_conf['apps']['dealerit']['apikey'] }
        try: 
            chatid = requests.get(_url, headers=_headers).json().get('data')
            logging.info('用户获取了新的maxkb会话：%s  %s', str(g.tokenobj.user), chatid)
            # 创建会话缓存
            chatdata = str(uuid.uuid4()).replace('-','')
            self.redis_client.set(
                'maxkbent:knowl:cache:chatdata:' + chatdata, '',ex=2147483647)
            #
            self.RETURN.message = '获取成功'
            self.RETURN.status = apibase.Status.SUCCESS
            self.RETURN.results = {'chatid': chatid}
        except Exception as e: 
            logging.error('获取 maxkb chatid 失败，' + str(e))
            self.RETURN.message = '获取 AI 会话ID失败'
            self.RETURN.status = apibase.Status.FAILED
        return self.RETURN.Dict()



class SessionData(MethodView, apibase.ViewBase): 
    ''' 知识库问答数据接口 '''
    def __init__(self) -> None: 
        super().__init__()
        self.redisc = redisc.Base()
        self.redis_client = self.redisc.Create_Client()
        # 初始化maxkb接口信息
        try: 
            self.maxkb_conf = json.load(open('config/maxkb.json'))
            self.appinfo = requests.get(
                self.maxkb_conf.get('api') + '/application/profile', 
                headers={ 
                    'AUTHORIZATION': self.maxkb_conf['apps']['dealerit']['apikey'] 
                }
                ).json().get('data')
            self.appid = self.appinfo.get('id')
        except Exception as e: 
            logging.error('初始化 maxkb 相关数据失败，' + str(e))
            pass
    
    def get(self): 
        time.sleep(1)
        count = 1
        chatdata = []
        data = self.redis_client.get(
            'maxkbent:knowl:cache:chatdata:' + str(request.args.get('chatid'))
        ).decode('utf-8')
        for i in str(data).split('<<##$$##>>'):
            if i[:1] == 'q': 
                chatdata.append({'index': count,'type': '1', 'data': i[1:]})
                count += 1
                continue
            if i[:1] == 'a': 
                chatdata.append({'index': count,'type': '0', 'data': i[1:]})
                count += 1
                continue
            
        self.RETURN.message = '请求完成'
        self.RETURN.status = apibase.Status.SUCCESS
        self.RETURN.results = {
            'count': count, 
            'data': chatdata[-3:]
        }
        return self.RETURN.Dict()

    def post(self): 
        redata = {'mkdata': ''}
        req_json = request.get_json()
        # 向 AI 发送消息
        logging.info(
            '发送新的对话消息，chatid:%s  msg:%s  user:%s', 
            str(req_json['chatid']), req_json['chat'], g.tokenobj.user)
        self.redis_client.append(
            'maxkbent:knowl:cache:chatdata:' + str(req_json['chatid']), 
            '<<##$$##>>q' + str(req_json['chat'])
        )
        with requests.post(
            '{0}/application/chat_message/{1}'.format(
                self.maxkb_conf.get('api'),str(req_json['chatid'])),
            headers={ 
                'AUTHORIZATION': self.maxkb_conf['apps']['dealerit']['apikey'] 
            }, 
            json={ 
                'message': req_json['chat'], 
                're_chat': False,   # 是否重新生成
                'stream': True
            }, 
            stream=True
        ) as r: 
            self.redis_client.append(
                'maxkbent:knowl:cache:chatdata:' + str(req_json['chatid']), 
                '<<##$$##>>a'
            )
            for l in r.iter_lines(): 
                decoded_line = l.decode('utf-8')
                if len(decoded_line) <= 0: continue
                stream_json = json.loads(decoded_line[5:])
                self.redis_client.append(
                    'maxkbent:knowl:cache:chatdata:' + str(req_json['chatid']), 
                    str(stream_json.get('content'))
                )
                redata['mkdata'] += stream_json['content']

        self.RETURN.status = apibase.Status.SUCCESS
        self.RETURN.message = '请求完成'
        self.RETURN.results = redata
        return self.RETURN.Dict()
