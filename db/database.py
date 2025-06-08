import sqlalchemy as sosal
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

engine = sosal.create_engine('sqlite:///db.db')

class CasinoUsers(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    balance = Column("balance", Integer, default=100)
    slots_num = Column("slots_num", Integer, default=0)
    dodep_num = Column("dodep_num", Integer, default=0)
    session_maker = sessionmaker(bind=engine)

    def init(self):
        Base.metadata.create_all(engine)

    def register(self, id: int, name: str) -> bool:
        with self.session_maker() as session:
            session.add(CasinoUsers(id=id, name=name))

            try:
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                print(str(e))
                return False

    def get_user(self, id: int):
        with self.session_maker() as session:
            try:
                user = session.query(CasinoUsers).filter_by(id=id).first()
                return user
            except Exception as e:
                print(str(e))
                return None
            
    def users_list(self):
        with self.session_maker() as session:
            try:
                user = session.query(CasinoUsers).all()
                return user
            except Exception as e:
                print(str(e))
                return None
    
    def get_bal(self, id: int) -> bool | int:
        with self.session_maker() as session:
            try:
                user = session.query(CasinoUsers).filter_by(id=id).first()
                return user.balance
            except Exception as e:
                print(str(e))
                return False
            
    def update_bal(self, id: int, newbal: int) -> bool:
        with self.session_maker() as session:
            try:
                user = session.query(CasinoUsers).filter_by(id=id).first()
                user.balance = newbal
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                print(str(e))
                return False
            
    def add_slot(self, id: int) -> bool:
        with self.session_maker() as session:
            try:
                user = session.query(CasinoUsers).filter_by(id=id).first()
                user.slots_num += 1
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                print(str(e))
                return False
            
    def add_dodep(self, id: int) -> bool:
        with self.session_maker() as session:
            try:
                user = session.query(CasinoUsers).filter_by(id=id).first()
                user.dodep_num += 1
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                print(str(e))
                return False
            
    def top5_money(self) -> list:
        with self.session_maker() as session:
            try:
                user = session.query(CasinoUsers).order_by(CasinoUsers.balance).all()[-5:][::-1]
                return user
            except Exception as e:
                print(str(e))
                return False
            
    def top5_slots(self) -> list:
        with self.session_maker() as session:
            try:
                user = session.query(CasinoUsers).order_by(CasinoUsers.slots_num).all()[-5:][::-1]
                return user
            except Exception as e:
                print(str(e))
                return False
    
    def top5_dodeps(self) -> list:
        with self.session_maker() as session:
            try:
                user = session.query(CasinoUsers).order_by(CasinoUsers.dodep_num).all()[-5:][::-1]
                return user
            except Exception as e:
                print(str(e))
                return False
            
class CasinoDates(Base):
    __tablename__ = "dates"
    id = Column("id", Integer, primary_key=True)
    date = Column("date", Integer, default=0)
    session_maker = sessionmaker(bind=engine)

    def init(self):
        Base.metadata.create_all(engine)

    def add_user(self, id) -> bool:
        with self.session_maker() as session:
            session.add(CasinoDates(id=id))

            try:
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                print(str(e))
                return False

    def get_date(self, id):
        with self.session_maker() as session:
            try:
                user = session.query(CasinoDates).filter_by(id=id).first()
                return user
            except Exception as e:
                print(str(e))
                return None

    def set_date(self, id, date) -> bool:
        with self.session_maker() as session:
            try:
                user = session.query(CasinoDates).filter_by(id=id).first()
                user.date = date
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                print(str(e))
                return False
            

db = CasinoUsers()
dt = CasinoDates()
db.init()
dt.init()