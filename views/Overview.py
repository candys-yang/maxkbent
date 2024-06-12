'''
概览视图库
'''
from flask import g
from flask.views import MethodView
from applib import apibase


class Userinfo(MethodView, apibase.ViewBase): 
    def __init__(self) -> None: 
        super().__init__()
    
    def get(self): 
        self.RETURN.message = '请求成功'
        self.RETURN.status = apibase.Status.SUCCESS
        self.RETURN.results = {
            'username': '演示用户', 
            'staff_id': g.tokenobj.user, 
            'staff_jobs': '演示职位'
        }
        return self.RETURN.Dict()



