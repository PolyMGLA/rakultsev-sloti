from games import slots, blackjack

HELP = """
- Казино Ракульцев -

/start - регистрация
/menu - основное меню
/slots - крутить слоты
/blackjack - играть в блэкджек
/dodep - додеп
/shop - магазин

Контакты: @ya_blinchik, @Luckich000
"""

ADMIN_HELP = """
- список команд для админов - 
/post <новость> - прислать новость для всех участников
/secret - вывести секрет
/secret_gen - сгенерить новый секрет
/balance <айди> - посмортеть баланс участника
/set_balance <id> <chislo> - выдать баланс по id
/user <id> - профиль пользователя по id
/user_list - список пользователей
/user_num - колво пользователей
/test - панель тестирования
/gift <gift_id> - получить подарок по id
/gifts_list - вывести все подарки
/remove_gift <gift_id> - удалить подарок по id
/credit <credit_id> - получить кредит по id
/credit_list - список всех кредитов
/find_users <username> - список всех пользователей, имя которых начинается на username
/get_minus - список пользователей с отрицательным балансом
/exec <command> - выполнить команду Python
/send_db - отправить текущую версию бд

/exit - !!!ОСТОРОЖНО!!! реально вырубает бота

доступно только:
@ya_blinchik, @Luckich000
"""

RULES = "".join([slots.RULES, blackjack.RULES])

DONATE = """
Донаты в приложение принимаются в виде подарков в Telegram на аккаунты @ya_blinchik, @Luckich000
"""
