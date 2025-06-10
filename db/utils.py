from db import db, dt, dv, dg


def init_user(msg) -> bool:
    """
    Инициализация пользователя в таблицах базы
    """
    x = not db.register(
        msg.from_user.id,
        (
            ("@" + msg.from_user.username)
            if not msg.from_user.username is None
            else msg.from_user.full_name
        ),
    )
    y = not dt.add_user(msg.from_user.id)
    z = not dv.add_user(msg.from_user.id)
    return not (x or y or z)


def update_visit(msg):
    """
    Обновление даты последнего посещения казино
    """
    return dv.set_date(msg.from_user.id)


def profile(id: int):
    user = db.get_user(id)
    gifts = dg.get_user_gifts(id)
    if user is None or user == False:
        return "Вы не зарегистрированы!\n/start"
    return f"- Профиль -" \
            + f"\nПользователь: {user.name}" \
            + f"\nБаланс: {user.balance}" \
            + (" (вы в долгах)" if user.balance < 0 else "") \
            + f"\nКруток слотов: {user.slots_num}" \
            + f"\nДодепов: {user.dodep_num}" \
            + f"\n\n- Подарков: {len(gifts)} -\n" \
            + "\n".join(
                f"{el.gift_type} #{el.gift_id} - \"{el.descr}\"" for el in gifts
            )
