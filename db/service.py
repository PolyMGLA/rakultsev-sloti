from db.database import (
    CasinoUsers,
    CasinoDodepDates,
    CasinoVisitors,
    CasinoGifts,
    CasinoCredits,
    engine,
    Base,
)

from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker

from datetime import datetime

import logging

logger = logging.getLogger(__name__)

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
            logger.error(str(e))
        finally:
            session.close()

    def register(self, id: int, name: str) -> bool:
        with self._session_scope() as session:
            if not self.get_user(id) is None:
                return False
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
            return (
                session.query(CasinoUsers)
                .order_by(CasinoUsers.balance)
                .all()[-5:][::-1]
            )

    def top5_slots(self) -> Optional[list[CasinoUsers]]:
        with self._session_scope() as session:
            return (
                session.query(CasinoUsers)
                .order_by(CasinoUsers.slots_num)
                .all()[-5:][::-1]
            )

    def top5_dodeps(self) -> Optional[list[CasinoUsers]]:
        with self._session_scope() as session:
            return (
                session.query(CasinoUsers)
                .order_by(CasinoUsers.dodep_num)
                .all()[-5:][::-1]
            )


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
            logger.error(str(e))
        finally:
            session.close()

    def add_user(self, id) -> bool:
        with self._session_scope() as session:
            if not self.get_date(id) is None:
                return False
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
            logger.error(str(e))
        finally:
            session.close()

    def add_user(self, id) -> bool:
        with self._session_scope() as session:
            if not self.get_date(id) is None:
                return False
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
            return (
                session.query(CasinoVisitors)
                .where(CasinoVisitors.date >= datetime.now().timestamp() - 300)
                .all()
            )


class GiftsService:
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
            logger.error(str(e))
        finally:
            session.close()

    def get_gift(self, gift_id: int) -> Optional[CasinoGifts]:
        with self._session_scope() as session:
            return session.query(CasinoGifts).filter_by(gift_id=gift_id).first()

    def get_all_gifts(self) -> list[CasinoGifts]:
        with self._session_scope() as session:
            return session.query(CasinoGifts).all()
        return []
    
    def get_user_gifts(self, user_id: int) -> list[CasinoGifts]:
        with self._session_scope() as session:
            return session.query(CasinoGifts).filter_by(user_id=user_id).all()
        return []

    def add_gift(
        self, user_id: int, gift_type: str, gift_name: str, descr: str = ""
    ) -> bool:
        with self._session_scope() as session:
            session.add(
                CasinoGifts(
                    user_id=user_id,
                    gift_type=gift_type,
                    gift_name=gift_name,
                    descr=descr,
                )
            )
            session.commit()
            return True
        return False


    def count_type(self, gift_type: str) -> Optional[int]:
        with self._session_scope() as session:
            return session.query(CasinoGifts).where(CasinoGifts.gift_type == gift_type).count()
        return None


    def remove_gift(self, gift_id: int) -> bool:
        with self._session_scope() as session:
            session.query(CasinoGifts).where(CasinoGifts.gift_id == gift_id).delete()
            session.commit()
            return True
        return False


    def has_gift(self, user_id: int, gift_type: str) -> bool:
        gifts = self.get_user_gifts(user_id)
        for g in gifts:
            if g.gift_type == gift_type: return True
        return False


class CreditsService:
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
            logger.error(str(e))
        finally:
            session.close()

    def get_credit(self, credit_id: int) -> Optional[CasinoCredits]:
        with self._session_scope() as session:
            return session.query(CasinoCredits).filter_by(credit_id=credit_id).first()

    def get_all_credits(self) -> list[CasinoCredits]:
        with self._session_scope() as session:
            return session.query(CasinoCredits).all()
        return []
    
    def get_user_credits(self, user_id: int) -> list[CasinoCredits]:
        with self._session_scope() as session:
            return session.query(CasinoCredits).filter_by(user_id=user_id).all()
        return []
    
    def update_sum(self, credit_id: int, sum: int) -> bool:
        with self._session_scope() as session:
            cred = session.query(CasinoCredits).where(CasinoCredits.credit_id == credit_id).first()
            cred.sum = sum
            session.commit()
            return True
        return False
    
    def update_next_date(self, credit_id: int, next_date: int) -> bool:
        with self._session_scope() as session:
            cred = session.query(CasinoCredits).where(CasinoCredits.credit_id == credit_id).first()
            cred.next_date = next_date
            session.commit()
            return True
        return False

    def add_credit(
        self, user_id: int, sum: int, perc: int, next_date: int, last_date: int
    ) -> bool:
        with self._session_scope() as session:
            session.add(
                CasinoCredits(
                    user_id=user_id,
                    sum=sum,
                    perc=perc,
                    next_date=next_date,
                    last_date=last_date,
                )
            )
            session.commit()
            return True
        return False


    def remove_credit(self, credit_id: int) -> bool:
        with self._session_scope() as session:
            session.query(CasinoCredits).where(CasinoCredits.credit_id == credit_id).delete()
            session.commit()
            return True
        return False

