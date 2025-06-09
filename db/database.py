import sqlalchemy as sosal
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

from datetime import datetime

Base = declarative_base()

engine = sosal.create_engine('sqlite:///db.db')

class CasinoUsers(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    balance = Column("balance", Integer, default=100)
    slots_num = Column("slots_num", Integer, default=0)
    dodep_num = Column("dodep_num", Integer, default=0)
    dodeps = relationship("CasinoDodepDates", back_populates="user", uselist=False, cascade="all, delete-orphan", lazy='joined')
    visitors = relationship("CasinoVisitors", back_populates="user", uselist=False, cascade="all, delete-orphan", lazy='joined')


class CasinoDodepDates(Base):
    __tablename__ = "dates"
    id = Column("id", Integer, ForeignKey('users.id'), primary_key=True)
    date = Column("date", Integer, default=0)
    user = relationship("CasinoUsers", back_populates="dodeps", lazy='joined')

class CasinoVisitors(Base):
    __tablename__ = "visitors"
    id = Column("id", Integer, ForeignKey('users.id'), primary_key=True)
    date = Column("date", Integer, default=0)
    user = relationship("CasinoUsers", back_populates="visitors", lazy='joined')