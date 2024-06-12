import logging
import datetime
from typing import List, Type
from sqlalchemy import create_engine, text, desc
from sqlalchemy import update, delete
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker

from . import sqlorm
from . import config 


logging.info('Init Mysql Engine QueuePool.')
DB_CONFIG = config.Database()
ENGINE = create_engine(DB_CONFIG.mysql, poolclass=QueuePool, pool_size=3)


class __BASE: 
    ''' 
    mysql 的基础封装类
    '''
    def __init__(self) -> None:
        global DB_CONFIG, ENGINE
        is_try = False
        try: 
            self.sessionmaker = sessionmaker(bind=ENGINE)
            self.session = self.sessionmaker()
            self.session.execute(text('select version()'))
        except Exception as e: 
            is_try = True
            logging.error('从数据库会话池获取会话失败，' + str(e))
        #
        if is_try: 
            logging.warning('重新初始化数据库连接池')
            ENGINE = create_engine(DB_CONFIG.mysql, poolclass=QueuePool, pool_size=3)
            self.sessionmaker = sessionmaker(bind=ENGINE)
            self.session = self.sessionmaker()


    def __del__(self): 
        try: 
            self.session.close()
        except Exception as e: 
            logging.info('对象退出时，关闭数据库连接失败，' + str(e))
            pass

    def _QueryResultToDict(self, row, strftime = None): 
        ''' 查询结果转换为字典 '''
        rows = []
        if row == [None]: return rows
        for i in row:
            _i = i.__dict__
            del _i['_sa_instance_state']
            if strftime: 
                for ii in _i:
                    if type(_i[ii]) == datetime.date: 
                        _i[ii] = _i[ii].strftime(strftime)
                    if type(_i[ii]) == datetime.datetime:
                        _i[ii] = _i[ii].strftime(strftime)
            rows.append(_i)
        return rows


class SystemConfig(__BASE): 
    ''' 应用系统配置 '''
    def __init__(self) -> None:
        super().__init__()
    
    def Set(self, key, value): 
        ''' 设置指定的配置项 '''
        Table = sqlorm.SystemConfig
        tj = set()
        tj.add(Table.sc_keys == key)
        v = { 'sc_value': value}
        row = self.session.execute(update(Table).where(*tj).values(v))
        rowcount = row.rowcount
        self.session.commit()
        return rowcount
    
    def Get(self, key): 
        ''' 获取指定配置项，如果为空，则返回 None ，否则返回表对象。 '''
        Table = sqlorm.SystemConfig
        tj = set()
        tj.add(Table.sc_keys == key)
        return self.session.query(Table).filter(*tj).first()
