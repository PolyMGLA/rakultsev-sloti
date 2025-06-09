from db.database import CasinoUsers, CasinoDodepDates, CasinoVisitors, engine, Base

from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker

from datetime import datetime

from typing import Optional

class UserService:
    def __init__(self):
        self.session = sessionmaker(bind=engine, expire_on_commit=False)
        Base.metadata.create_all(engine)

    @contextmanager
    def _session_scope(self):
        """Контекстный менеджер для работы с сессией"""
        session = self.session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            print(str(e))
        finally:
            session.close()

    def register(self, id: int, name: str) -> bool:
        with self._session_scope() as session:
            session.add(CasinoUsers(id=id, name=name))
            session.commit()
            return True
        return False

    def get_user(self, id: int) -> Optional[CasinoUsers]:
        with self._session_scope() as session:
            return session.query(CasinoUsers).filter_by(id=id).first()
            
    def users_list(self) -> Optional[list[CasinoUsers]]:
        with self._session_scope() as session:
            return session.query(CasinoUsers).all()
    
    def get_bal(self, id: int) -> bool | int:
        with self._session_scope() as session:
            return session.query(CasinoUsers).filter_by(id=id).first().balance
        return False
            
    def update_bal(self, id: int, newbal: int) -> bool:
        with self._session_scope() as session:
            user = session.query(CasinoUsers).filter_by(id=id).first()
            user.balance = newbal
            session.commit()
            return True
        return False
            
    def add_slot(self, id: int) -> bool:
        with self._session_scope() as session:
            user = session.query(CasinoUsers).filter_by(id=id).first()
            user.slots_num += 1
            session.commit()
            return True
        return False
            
    def add_dodep(self, id: int) -> bool:
        with self._session_scope() as session:
            user = session.query(CasinoUsers).filter_by(id=id).first()
            user.dodep_num += 1
            session.commit()
            return True
        return False
            
    def top5_money(self) -> Optional[list[CasinoUsers]]:
        with self._session_scope() as session:
            return session.query(CasinoUsers).order_by(CasinoUsers.balance).all()[-5:][::-1]
            
    def top5_slots(self) -> Optional[list[CasinoUsers]]:
        with self._session_scope() as session:
            return session.query(CasinoUsers).order_by(CasinoUsers.slots_num).all()[-5:][::-1]
    
    def top5_dodeps(self) -> Optional[list[CasinoUsers]]:
        with self._session_scope() as session:
            return session.query(CasinoUsers).order_by(CasinoUsers.dodep_num).all()[-5:][::-1]


class DodepService:
    def __init__(self):
        self.session = sessionmaker(bind=engine, expire_on_commit=False)
        Base.metadata.create_all(engine)

    @contextmanager
    def _session_scope(self):
        """Контекстный менеджер для работы с сессией"""
        session = self.session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            print(str(e))
        finally:
            session.close()

    def add_user(self, id) -> bool:
        with self._session_scope() as session:
            session.add(CasinoDodepDates(id=id))
            session.commit()
            return True
        return False

    def get_date(self, id) -> Optional[list[CasinoDodepDates]]:
        with self._session_scope() as session:
            return session.query(CasinoDodepDates).filter_by(id=id).first()

    def set_date(self, id, date) -> bool:
        with self._session_scope() as session:
            user = session.query(CasinoDodepDates).filter_by(id=id).first()
            user.date = date
            session.commit()
            return True
        return False
            

class VisitorsService:
    def __init__(self):
        self.session = sessionmaker(bind=engine, expire_on_commit=False)
        Base.metadata.create_all(engine)
    
    @contextmanager
    def _session_scope(self):
        """Контекстный менеджер для работы с сессией"""
        session = self.session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            print(str(e))
        finally:
            session.close()

    def add_user(self, id) -> bool:
        with self._session_scope() as session:
            session.add(CasinoVisitors(id=id))
            session.commit()
            return True
        return False
        
    def get_date(self, id) -> Optional[list[CasinoVisitors]]:
        with self._session_scope() as session:
            return session.query(CasinoVisitors).filter_by(id=id).first()

    def set_date(self, id) -> bool:
        with self._session_scope() as session:
            user = session.query(CasinoVisitors).filter_by(id=id).first()
            if user is None:
                self.add_user(id)
                session.commit()
                user = session.query(CasinoVisitors).filter_by(id=id).first()
            user.date = int(datetime.now().timestamp())
            session.commit()
            return True
        return False
    
    def get_list(self) -> Optional[list[CasinoVisitors]]:
        with self._session_scope() as session:
            return session.query(CasinoVisitors).where(CasinoVisitors.date >= datetime.now().timestamp() - 60).all()