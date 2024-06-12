'''
用于统一返回接口数据给前端
'''

import enum
from flask import request, session
from flask.views import MethodView


class Status(enum.Enum):
    ''' 
    状态返回码 
    
    >>> ENUM: 
        SUCCESS = 200 
        BAD = -400 
        UNAUTH = -401
        NOACCESS = -403
        NOFOUND = -404
        ERROR = -500
        TIMEOUT = -504
    '''
    SUCCESS = 200
    BAD = -400
    UNAUTH = -401
    NOACCESS = -403
    NOFOUND = -404
    FAILED = -413
    ERROR = -500
    TIMEOUT = -504


class API:

    def __init__(
            self, 
            status:Status=Status.BAD, 
            msg='请求失败', result={}, reqid=None) -> None:
        self.status = status
        self.message = msg
        self.results = result
        self.reqid = reqid
        pass

    def Dict(self): 
        ''' 返回 Dict 类型的数据 '''
        _re_results = None
        if type(self.results) == dict: 
            _re_results = self.results
        elif type(self.results) == list: 
            _re_results = self.results
        else:
            try: 
                _re_results = self.results.__dict__
            except:
                _re_results = str(self.results)
        return {
            "status": self.status.value,
            "message": self.message,
            "results": _re_results,
            "reqid": self.reqid
        }
    
    def Str(self) -> str:
        ''' 返回 Str 类型的数据 '''
        _re_results = None
        if type(self.results) == dict: 
            _re_results = self.results
        else:
            _re_results = self.results.__dict__

        return str({
            "status": self.status.value,
            "message": self.message,
            "results": _re_results,
            "reqid": self.reqid
        })


class ViewBase(): 
    ''' 视图基础类 '''
    def __init__(self) -> None: 
        self.reqid = request.headers.get('Reqid')
        if self.reqid is None: 
            self.reqid = session['session']
        self.RETURN = API(Status.BAD, '服务器内部错误', {}, self.reqid)




