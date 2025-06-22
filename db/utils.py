from db import db, dg, dc

from datetime import datetime

def init_user(msg) -> bool:
    """
    Инициализация пользователя в таблицах базы
    """
    return db.register(
        msg.from_user.id,
        (
            ("@" + msg.from_user.username)
            if not msg.from_user.username is None
            else msg.from_user.full_name
        ),
    )


def update_visit(msg) -> bool:
    """
    Обновление даты последнего посещения казино
    """
    return db.update(msg.from_user.id, visit_date=int(datetime.now().timestamp()))


def profile(id: int, show_id: bool = False) -> str:
    user = db.get_user(id)
    gifts = dg.get_user_gifts(id)
    if user is None or user == False:
        return "Вы не зарегистрированы!\n/start"
    return (
        f"- Профиль -"
        + f"\nПользователь: {user.prefix}{user.name}" + (f" ({user.id})" if show_id else "")
        + f"\nБаланс: {user.balance}"
        + (" (вы в долгах)" if user.balance < 0 else "")
        + f"\nКруток слотов: {user.slots_num}"
        + f"\nДодепов: {user.dodep_num}"
        + f"\n\n- Подарков: {len(gifts)} -\n"
        + "\n".join(f'{el.gift_name} #{el.gift_id} - "{el.descr}"' for el in gifts)
        + f"\n\nСсылка для друзей (+100🪙): https://t.me/rakultsev_sloti_bot?start={user.id}"
    )


def credit(cred_id: int, show_user: bool = False) -> str:
    cred = dc.get_credit(cred_id)
    if cred is None:
        return ""
    return f"Кредит №{cred.credit_id} на {cred.sum}🪙 под {cred.perc}% в день." \
         + f"Погасить до {datetime.fromtimestamp(cred.last_date).strftime('%d/%m/%Y, %H:%M:%S')}" \
         + (f"\nВзят на {cred.user.name} ({cred.user_id})" if show_user else "")
