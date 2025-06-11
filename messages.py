from games import slots, blackjack

HELP = """
- Казино Ракульцев -

/start - регистрация
/menu - основное меню
/slots - крутить слоты
/dodep - додеп
/shop - магазин

Контакты: @ya_blinchik, @Luckich000
"""

ADMIN_HELP = """
- список команд для админов - 
/post <новость> - прислать новость для всех участников
/balance <айди> - посмортеть баланс участника
/set_balance <id> <chislo> - выдать баланс по id
/user <id> - профиль пользователя по id
/gift <gift_id> - получить подарок по id
/remove_gift <gift_id> - удалить подарок по id

доступно только:
@ya_blinchik, @Luckich000
"""

RULES = "".join([slots.RULES, blackjack.RULES])

DONATE = """
Донаты в приложение принимаются в виде подарков в Telegram на аккаунты @ya_blinchik, @Luckich000
"""
