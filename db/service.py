from db.database import (
    CasinoUsers,
    CasinoGifts,
    CasinoCredits,
    engine,
    Base,
)

from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker

from datetime import datetime

import traceback

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
            logger.error(str(e) + "\n" + traceback.format_exc())
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

    def remove_user(self, id: int) -> bool:
        with self._session_scope() as session:
            session.query(CasinoUsers).where(CasinoUsers.id == id).delete()
            session.commit()
            return True
        return False

    def get_user(self, id: int) -> Optional[CasinoUsers]:
        with self._session_scope() as session:
            return session.query(CasinoUsers).filter_by(id=id).first()

    def users_list(self) -> Optional[list[CasinoUsers]]:
        with self._session_scope() as session:
            return session.query(CasinoUsers).all()

    def get(self, id: int, arg: str):
        with self._session_scope() as session:
            return getattr(session.query(CasinoUsers).filter_by(id=id).first(), arg)

    def update(self, id: int, **kwargs) -> bool:
        with self._session_scope() as session:
            user = session.query(CasinoUsers).filter_by(id=id).first()
            for arg in kwargs:
                setattr(user, arg, kwargs[arg])
            session.commit()
            return True
        return False

    def add(self, id: int, **kwargs) -> bool:
        with self._session_scope() as session:
            user = session.query(CasinoUsers).filter_by(id=id).first()
            for arg in kwargs:
                setattr(user, arg, getattr(user, arg) + kwargs[arg])
            session.commit()
            return True
        return False

    def topn(self, n: int, attr: str) -> Optional[list[CasinoUsers]]:
        with self._session_scope() as session:
            return (
                session.query(CasinoUsers)
                .order_by(getattr(CasinoUsers, attr))
                .all()[-n:][::-1]
            )

    def get_visit_list(self) -> Optional[list[CasinoUsers]]:
        with self._session_scope() as session:
            return (
                session.query(CasinoUsers)
                .where(CasinoUsers.visit_date >= datetime.now().timestamp() - 300)
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
            logger.error(str(e) + "\n" + traceback.format_exc())
        finally:
            session.close()

    def get_gift(self, gift_id: int) -> Optional[CasinoGifts]:
        with self._session_scope() as session:
            return session.query(CasinoGifts).filter_by(gift_id=gift_id).first()

    def get_all_gifts(self) -> list[CasinoGifts]:
        with self._session_scope() as session:
            return session.query(CasinoGifts).all()
        return []

    def get_typed_gifts(self, gift_type: str) -> list[CasinoGifts]:
        with self._session_scope() as session:
            return (
                session.query(CasinoGifts)
                .where(CasinoGifts.gift_type == gift_type)
                .all()
            )
        return []

    def get_user_gifts(self, user_id: int, show_gift=True) -> list[CasinoGifts]:
        with self._session_scope() as session:
            return (
                session.query(CasinoGifts)
                .filter_by(user_id=user_id, show_gift=show_gift)
                .all()
            )
        return []

    def add_gift(
        self,
        user_id: int,
        gift_type: str,
        gift_name: str,
        descr: str = "",
        show_gift: bool = True,
    ) -> bool:
        with self._session_scope() as session:
            session.add(
                CasinoGifts(
                    user_id=user_id,
                    gift_type=gift_type,
                    gift_name=gift_name,
                    descr=descr,
                    show_gift=show_gift,
                )
            )
            session.commit()
            return True
        return False

    def count_type(self, gift_type: str) -> Optional[int]:
        with self._session_scope() as session:
            return (
                session.query(CasinoGifts)
                .where(CasinoGifts.gift_type == gift_type)
                .count()
            )
        return None

    def remove_gift(self, gift_id: int) -> bool:
        with self._session_scope() as session:
            session.query(CasinoGifts).where(CasinoGifts.gift_id == gift_id).delete()
            session.commit()
            return True
        return False

    def has_gift(self, user_id: int, gift_type: str, show_gift: bool = True) -> bool:
        gifts = self.get_user_gifts(user_id, show_gift=show_gift)
        for g in gifts:
            if g.gift_type == gift_type:
                return True
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
            logger.error(str(e) + "\n" + traceback.format_exc())
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
            cred = (
                session.query(CasinoCredits)
                .where(CasinoCredits.credit_id == credit_id)
                .first()
            )
            cred.sum = sum
            session.commit()
            return True
        return False

    def update_next_date(self, credit_id: int, next_date: int) -> bool:
        with self._session_scope() as session:
            cred = (
                session.query(CasinoCredits)
                .where(CasinoCredits.credit_id == credit_id)
                .first()
            )
            cred.next_date = next_date
            session.commit()
            return True
        return False

    def update_last_date(self, credit_id: int, last_date: int) -> bool:
        with self._session_scope() as session:
            cred = (
                session.query(CasinoCredits)
                .where(CasinoCredits.credit_id == credit_id)
                .first()
            )
            cred.last_date = last_date
            session.commit()
            return True
        return False

    def add_credit(
        self,
        user_id: int,
        sum: int,
        perc: int,
        next_date: int,
        last_date: int,
        cred_period: int = 86400,
    ) -> bool:
        with self._session_scope() as session:
            session.add(
                CasinoCredits(
                    user_id=user_id,
                    sum=sum,
                    perc=perc,
                    next_date=next_date,
                    last_date=last_date,
                    cred_period=cred_period,
                )
            )
            session.commit()
            return True
        return False

    def remove_credit(self, credit_id: int) -> bool:
        with self._session_scope() as session:
            session.query(CasinoCredits).where(
                CasinoCredits.credit_id == credit_id
            ).delete()
            session.commit()
            return True
        return False
