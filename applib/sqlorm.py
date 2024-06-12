'''
mysql 数据库对象映射

'''
from sqlalchemy import Column,  String, TIMESTAMP, Boolean, Integer
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SystemConfig(Base): 
    __tablename__ = 'system_config'
    __table_args__ = {'comment': '系统配置'}
    id = Column(INTEGER(11), primary_key=True)
    sc_keys = Column(String(1024), comment='配置项名称')
    sc_value = Column(String(1024), comment='配置项值')
    sc_txt = Column(String(1024), comment='配置项说明')





    

