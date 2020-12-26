#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from sqlalchemy import create_engine, Column, String, Integer, BigInteger, Date, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

SQLALCHEMY_DATABASE_URL = 'sqlite:///./coronavirus.db'
# SQLALCHEMY_DATABASE_URL = "postgresql://username:password@host:port/database_name"  # MySQL或PostgreSQL的连接方法

engine = create_engine(
    # echo=True表示引擎将用repr()函数记录所有语句及其参数列表到日志
    # 由于SQLAlchemy是多线程，指定check_same_thread=False来让建立的对象任意线程都可使用
    SQLALCHEMY_DATABASE_URL, encoding='utf-8', echo=True, connect_args={'check_same_thread': False}
)

# 在SQLAlchemy中，CRUD都是通过会话(session)进行的，所以我们必须要先创建会话
# flush()是指发送数据库语句到数据库，但数据库不一定执行写入磁盘；commit()是指提交事务，将变更保存到数据库文件
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=True)

# 创建基本映射类
Base = declarative_base(bind=engine, name='Base')


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    province = Column(String(100), unique=True, nullable=False, comment='省/直辖市')
    country = Column(String(100), nullable=False, comment='国家')
    country_code = Column(String(100), nullable=False, comment='国家代码')
    country_population = Column(BigInteger, nullable=False, comment='国家人口')
    data = relationship('Data', backref='city')  # 'Data'是关联的类名；backref来指定反向访问的属性名称

    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    __mapper_args__ = {"order_by": country_code}  # 默认是正序，倒序加上.desc()方法

    def __repr__(self):
        return f'{self.country}_{self.province}'


class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('city.id'), ondelete='CASCADE', comment='所属省/直辖市')  # ForeignKey里的字符串格式不是类名.属性名，而是表名.字段名
    date = Column(Date, nullable=False, comment='数据日期')
    confirmed = Column(BigInteger, default=0, nullable=False, comment='确诊数量')
    deaths = Column(BigInteger, default=0, nullable=False, comment='死亡数量')
    recovered = Column(BigInteger, default=0, nullable=False, comment='痊愈数量')
    city = relationship('City', backref='data')  # 'City'是关联的类名；backref来指定反向访问的属性名称

    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    __mapper_args__ = {"order_by": confirmed}

    def __repr__(self):
        return f'{repr(self.date)}：确诊{self.confirmed}例'


""" 附上三个SQLAlchemy教程

SQLAlchemy的基本操作大全 
    http://www.taodudu.cc/news/show-175725.html

Python3+SQLAlchemy+Sqlite3实现ORM教程 
    https://www.cnblogs.com/jiangxiaobo/p/12350561.html

SQLAlchemy基础知识 Autoflush和Autocommit
    https://zhuanlan.zhihu.com/p/48994990
"""