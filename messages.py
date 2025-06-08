from games import slots, blackjack

HELP = """
- Казино Ракульцев -

/start - регистрация
/menu - основное меню
/slots - крутить слоты
/dodep - додеп

Контакты: @ya_blinchik, @Luckich000
"""

ADMIN_HELP = """
- список команд для админов - 
/novost <новость> - прислать новость для всех участников
/balance <айди> - посмортеть баланс участника
/set_balance <id> <chislo> - выдать баланс по id 

доступно только:
@ya_blinchik, @Luckich000
"""

RULES = "".join([slots.RULES, blackjack.RULES])