from db import db, dt, dv

def init_user(msg) -> bool:
    """
    Инициализация пользователя в таблицах базы
    """
    x = not db.register(
        msg.from_user.id,
        ("@" + msg.from_user.username) if not msg.from_user.username is None else msg.from_user.full_name
    )
    y = not dt.add_user(msg.from_user.id)
    z = not dv.add_user(msg.from_user.id)
    return not (x or y or z)

def update_visit(msg):
    """
    Обновление даты последнего посещения казино
    """
    return dv.set_date(msg.from_user.id)