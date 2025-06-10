import sqlalchemy as sosal
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

engine = sosal.create_engine("sqlite:///db.db")


class CasinoUsers(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    balance = Column("balance", Integer, default=100)
    slots_num = Column("slots_num", Integer, default=0)
    dodep_num = Column("dodep_num", Integer, default=0)
    dodeps = relationship(
        "CasinoDodepDates",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined",
    )
    visitors = relationship(
        "CasinoVisitors",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined",
    )
    gifts = relationship(
        "CasinoGifts",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined",
    )


class CasinoDodepDates(Base):
    __tablename__ = "dates"
    id = Column("id", Integer, ForeignKey("users.id"), primary_key=True)
    date = Column("date", Integer, default=0)
    user = relationship("CasinoUsers", back_populates="dodeps", lazy="joined")


class CasinoVisitors(Base):
    __tablename__ = "visitors"
    id = Column("id", Integer, ForeignKey("users.id"), primary_key=True)
    date = Column("date", Integer, default=0)
    user = relationship("CasinoUsers", back_populates="visitors", lazy="joined")


class CasinoGifts(Base):
    __tablename__ = "gifts"
    gift_id = Column("gift_id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("users.id"))
    gift_type = Column("gift_type", String, nullable=False)
    gift_name = Column("gift_name", String, nullable=False)
    descr = Column("descr", String, default="")
    user = relationship("CasinoUsers", back_populates="gifts", lazy="joined")