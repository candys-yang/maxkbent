
from . import Auth
from . import Overview
from . import Konwl

# 应用视图注册 (视图, 视图类, 要求鉴权)
VIEWS = [
    ('/auth/vwork', Auth.Vwork , False), 
    ('/auth/login', Auth.Login, False), 
    ('/overview/userinfo', Overview.Userinfo, True), 
    ('/knowl/openchat', Konwl.OpenChat, True),
    ('/knowl/sessiondata', Konwl.SessionData, True)
]