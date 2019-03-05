# coding=utf-8

import enum

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, Integer, String, CHAR, SmallInteger, ForeignKey, Date,
    Boolean
)
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = None
Session = None


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    staff_id = Column(Integer)
    password = Column(CHAR(64))  # only store sha256 hashed password


class Course(Base):
    __tablename__ = "courses"
    course_id = Column(Integer, primary_key=True)
    course_name = Column(String(96))
    start = Column(Date())
    end = Column(Date())


class Class(Base):
    __tablename__ = 'classes'
    class_id = Column(Integer, primary_key=True)
    class_name = Column(String(96))
    weekday = Column(SmallInteger)  # 周几
    start = Column(SmallInteger)  # 第几节课开始
    end = Column(SmallInteger)  # 第几节课结束
    teacher_id = Column(Integer, ForeignKey(User.user_id))
    course_id = Column(Integer, ForeignKey(Course.course_id))


class RelationUserClass(Base):  # 用户(学生)与班级的关系表
    __tablename__ = 'relation_user_class'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.user_id))
    class_id = Column(Integer, ForeignKey(Class.class_id))


class CheckinCodes(Base):
    __tablename__ = "check-in-codes"
    code_id = Column(Integer, primary_key=True)
    code = Column(SmallInteger)
    class_id = Column(Integer, ForeignKey(Class.class_id))
    started = Column(Boolean)
    expire_at = Column(Integer)


class CheckedInLogs(Base):
    __tablename__ = "checked-in-logs"
    log_id = Column(Integer, primary_key=True)
    code_id = Column(Integer, ForeignKey(CheckinCodes.code_id))
    user_id = Column(Integer, ForeignKey(User.user_id))


def startup(conf):
    global engine, Session
    if engine and Session:
        return

    engine = create_engine(
        '{dialect}+{driver}://{user}:{password}@{host}/{dbname}'.format(
            **conf.db), echo=conf.app.debug)
    Session = sessionmaker(bind=engine)


def init_db(conf):
    startup(conf)
    Base.metadata.bind = engine
    Base.metadata.create_all()
