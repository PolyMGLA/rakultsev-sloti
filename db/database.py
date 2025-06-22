import sqlalchemy as sosal
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

engine = sosal.create_engine("sqlite:///db.db")

class CasinoUsers(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    prefix = Column("prefix", String, default="")
    balance = Column("balance", Integer, default=100)
    slots_num = Column("slots_num", Integer, default=0)
    blackjack_num = Column("blackjack_num", Integer, default=0)
    dodep_num = Column("dodep_num", Integer, default=0)
    dodep_date = Column("dodep_date", Integer, default=0)
    visit_date = Column("visit_date", Integer, default=0)
    lost_money = Column("lost_money", Integer, default=0)
    gifts = relationship(
        "CasinoGifts",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="joined",
    )
    credits = relationship(
        "CasinoCredits",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="joined",
    )


class CasinoGifts(Base):
    __tablename__ = "gifts"
    gift_id = Column("gift_id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("users.id"))
    gift_type = Column("gift_type", String, nullable=False)
    gift_name = Column("gift_name", String, nullable=False)
    show_gift = Column("show_gift", Boolean, nullable=False)
    descr = Column("descr", String, default="")
    user = relationship("CasinoUsers", back_populates="gifts", lazy="joined")


class CasinoCredits(Base):
    __tablename__ = "credits"
    credit_id = Column("credit_id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("users.id"))
    sum = Column("sum", Integer, nullable=False)
    perc = Column("perc", Integer, nullable=False)
    cred_period = Column("cred_period", Integer, default=86400)
    next_date = Column("next_date", Integer, nullable=False)
    last_date = Column("last_date", Integer, nullable=False)
    user = relationship("CasinoUsers", back_populates="credits", lazy="joined")
