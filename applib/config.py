'''
配置文件对象映射

'''


import os 
import json
import logging


class Database: 
    ''' 
    这是一个数据库配置类，用于存储 mysql、elasticsearch、redis 的连接信息。

    实例化时，会尝试读区 config/database.json 文件，如果有，则加载到对象属性中。
    
    Attributes: 
        MYSQL:  mysql连接信息
        ES:     elasticsearch 连接信息
        REDIS:  redis 连接信息
    '''
    def __init__(self) -> None:
        self.mysql:str = ''
        self.es:str = ''
        self.redis:str = ''
        self.__Load()

    def __Load(self):
        try: 
            j = json.load(open('config/database.json'))
            self.mysql = str(j.get('mysql'))
            self.es = str(j.get('elasticsearch'))
            self.redis = str(j.get('redis'))
        except Exception as e: 
            logging.error("加载 数据库配置文件 database.json 失败。" + str(e))
            
class Vwork: 
    ''' 企业微信接口配置 '''
    def __init__(self) -> None:
        self.appid:str = None
        self.appurl:str = None
        self.secret:str = None
        self.apiurl:str = None
        #
        self.__Load()

    def __Load(self): 
        try: 
            j = json.load(open('config/vwork.json'))
            self.appid = str(j.get('appid'))
            self.appurl = str(j.get('appurl'))
            self.secret = str(j.get('secret'))
            self.apiurl = str(j.get('apiurl'))
        except Exception as e: 
            logging.error("加载 数据库配置文件 vwork.json 失败。" + str(e))
