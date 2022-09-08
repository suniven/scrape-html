from sqlalchemy import Column, String, create_engine, Integer, SmallInteger, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import mysql

Base = declarative_base()


# 定义对象
class WebpageInfo(Base):
    # 表名
    __tablename__ = 'webpage_info'

    id = Column(mysql.BIGINT, primary_key=True)
    url = Column(String(1500))
    url_hash = Column(String(32))
    landing_page = Column(String(5000))
    intermediate_urls = Column(Text)
    html = Column(Text)
    text = Column(Text)
    vpn = Column(String(50))


class WebpageInfoAbs(Base):
    # 表名
    __tablename__ = 'webpage_info_abs'

    id = Column(mysql.BIGINT, primary_key=True)
    url = Column(String(1500))
    url_hash = Column(String(32))
    landing_page = Column(String(5000))
    intermediate_urls = Column(Text)
    vpn = Column(String(50))
