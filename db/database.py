import sqlalchemy as sosal
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

engine = sosal.create_engine('sqlite:///db.db')

class CasinoBase(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    balance = Column("balance", Integer, default=100)
    maxbal = Column("maxbal", Integer, default=100)
    session_maker = sessionmaker(bind=engine)

    def init(self):
        Base.metadata.create_all(engine)

    def register(self, id: int, name: str) -> bool:
        with self.session_maker() as session:
            session.add(CasinoBase(id=id, name=name))

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
                user = session.query(CasinoBase).filter_by(id=id).first()
                return user
            except Exception as e:
                print(str(e))
                return None
    
    def get_bal(self, id: int) -> bool | int:
        with self.session_maker() as session:
            try:
                user = session.query(CasinoBase).filter_by(id=id).first()
                return user.balance
            except Exception as e:
                print(str(e))
                return False
            
    def update_bal(self, id: int, newbal: int) -> bool:
        with self.session_maker() as session:
            try:
                user = session.query(CasinoBase).filter_by(id=id).first()
                user.balance = newbal
                user.maxbal = max(user.maxbal, newbal)
                session.commit()
                return True
            except Exception as e:
                print(str(e))
                return False