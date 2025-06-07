                                                                    #импорт всякой залупы
import os
import dotenv
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from games import slots, blackjack
from db.database import CasinoUsers, CasinoDates
from datetime import datetime

dotenv.load_dotenv()
                                                                        #лист админов
ADMINS = list(map(int, os.environ["ADMINS"].split(",")))
                                                                    #текст правил
RULES = "".join([slots.RULES, blackjack.RULES])
                                                                    #текст помощи
HELP = """
- Казино Ракульцев -

/start - регистрация
/profile - ваш профиль
/help - помощь
/rules - правила игр
/slots - крутить слоты
/dodep - додеп
/top - топ казино

Контакты: @ya_blinchik, @Luckich000
"""

ADMIN_HELP = """
- список команд для админов - 
/spisok - посмотреть список участников
/secret - посмотреть секретную комбинацию
/gen - сгенерировать новую секретку
/novost - прислать новость для всех участников

доступно только:
@ya_blinchik, @Luckich000
"""
                                                                    #дб-шки
db = CasinoUsers()
dt = CasinoDates()
db.init()
                                                                    #рег бота
BOT_TOKEN = os.environ["BOT_TOKEN"]
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

                                                                #функция для отправки новостей
async def send_news(text):
    users = db.users_list()
    if not users is None:
        for u in users:
            await bot.send_message(u.id, "- НОВОСТЬ ОТ АДМИНА -\n" + text)

                                                                #функция для регистрации
@dp.message(Command("start"))
async def gay_start(msg: types.Message):
    if db.register(
        msg.from_user.id,
        ("@" + msg.from_user.username) if not msg.from_user.username is None else msg.from_user.full_name
        ) and dt.add_user(msg.from_user.id):
        await msg.answer("Регистрация успешна!\n/help - список команд")
    else:
        await msg.answer("Регистрация не удалась, поплачь(\n/help - список команд")

                                                            #функция для вызыва текста помощи
@dp.message(Command("help"))
async def gay_help(msg: types.Message):
    await msg.answer(HELP)

                                                        #функция для вызова информации профиля
@dp.message(Command("profile"))
async def gay_profile(msg: types.Message):
    user = db.get_user(msg.from_user.id)
    if user is None or user == False:
        await msg.answer("Вы не зарегистрированы!\n/start")
    await msg.answer(
        f"Пользователь: {user.name}"
         + f"\nБаланс: {user.balance}" + (" (вы в долгах)" if user.balance < 0 else "")
         + f"\nКруток слотов: {user.slots_num}"
         + f"\nДодепов: {user.dodep_num}"
        )

#@dp.message(Command("tbgtfiqtbih"))
#async def gay_tbgtfiqtbih(msg: types.Message):
#    if msg.from_user.id in ADMINS:
#        user = db.get_user(msg.from_user.id)
#        db.update_bal(msg.from_user.id, 0)

                                                    #функция для вызова текста правил
@dp.message(Command("rules"))
async def gay_ref(msg: types.Message):
    await msg.answer(RULES)

                                                    #функция для круток
@dp.message(Command("slots"))
async def gay_spin(msg: types.Message):
    msgs = slots.spin(db, dt, msg.from_user.id)
    for m in msgs:
        await msg.answer(m)
    if msgs[0] == slots.SECRET:
        await send_news(f"{db.get_user(msg.from_user.id).name} - выбил секретную комбинацию!!\n" + "прошлое комбо:" + slots.SECRET+ "\n- КОМБИНАЦИЯ ИЗМЕНЕНА- ")
        slots.secret_regen()
    if msgs[0] == "🌈🌈🌈":
        await send_news(f"{db.get_user(msg.from_user.id).name} - absolute sigma!!")
    if msgs[0] == "💀💀💀":
        await send_news(f"{db.get_user(msg.from_user.id).name} проиграл семью в казино")

                                                        #функция для получания додепа
@dp.message(Command("dodep"))
async def gay_dodep(msg: types.Message):
    user = db.get_user(msg.from_user.id)
    if user.balance<=1:
        if dt.get_date(msg.from_user.id) is None:
            dt.add_user(msg.from_user.id)

        tdt = int(datetime.now().timestamp())
        last_dodep = dt.get_date(msg.from_user.id).date
        if tdt - last_dodep < 600:
            await msg.answer(f"подождите {(600 - tdt + last_dodep) // 60} минут {(600 - tdt + last_dodep) % 60} секунд")
        else:
            if db.update_bal(msg.from_user.id, 100) and db.add_dodep(msg.from_user.id) and dt.set_date(msg.from_user.id, tdt):
                await msg.answer("додеп прошел")
            else:
                await msg.answer("додеп не прошел")
    else:
        await msg.answer("вы слишком богатые")

                                                        #функция для вызова топа
@dp.message(Command("top"))
async def gay_top(msg: types.Message):
    top = db.top5_money()
    res = ""

    res += "Топ по счету:\n"
    if top == False:
        res += "ашипка\n\n"
    else:
        res += "\n".join([f"{i + 1}. {top[i].name} - {top[i].balance}" for i in range(len(top))]) + "\n\n"

    top = db.top5_slots()
    res += "Топ по круткам:\n"
    if top == False:
        res += "ашипка\n\n"
    else:
        res += "\n".join([f"{i + 1}. {top[i].name} - {top[i].slots_num}" for i in range(len(top))]) + "\n\n"
    
    top = db.top5_dodeps()
    res += "Топ по додепам:\n"
    if top == False:
        res += "ашипка\n\n"
    else:
        res += "\n".join([f"{i + 1}. {top[i].name} - {top[i].dodep_num}" for i in range(len(top))]) + "\n\n"

    await msg.answer(res)

                                                                #функция для просмотра секретной комбинации(админ онли)
@dp.message(Command("secret"))
async def gay_secret(msg: types.Message):
    if msg.from_user.id in ADMINS:
        await msg.answer("Секрет: " + slots.SECRET)
    else:
        await msg.answer("ты недостоин")

                                                            #функция для изменения секретной комбинации(админ онли)
@dp.message(Command("gen"))
async def gay_secret(msg: types.Message):
    if msg.from_user.id in ADMINS:
        slots.secret_regen()
        await msg.answer("Новый секрет: " + slots.SECRET)
    else:
        await msg.answer("ты недостоин")

                                                            #функция для создания новостей(админ онли)
@dp.message(Command("novost"))
async def gay_novost(msg: Message,command: CommandObject):
    if msg.from_user.id in ADMINS:
        if command.args is None:
            await msg.answer("ашипка: напишите новость\n /novost <новость>")
            return
        await send_news(command.args)
    else:
        await msg.answer("ты недостоин")

                                                                    #функция для просмотра участников(админ онли)
@dp.message(Command("spisok"))
async def gay_spisok(msg: types.Message, command: CommandObject):
    schet = 0
    if msg.from_user.id in ADMINS:
        if command.args is None:
            await msg.answer("ашипка: выберите что хотите посмотреть\n /spisok kol-vo - для количества игроков\n /spisok people - для вывода всех учащихся")
            return
        if command.args == "kol-vo":
            users = db.users_list()
            if not users is None:
                for u in users:
                    schet+=1
                await msg.answer(f"количество участников: {schet}")
        if command.args == "people":
            users = db.users_list()
            if not users is None:
                for u in users:
                    await msg.answer(f"{u.name}")

@dp.message(Command("admin_help"))
async  def gay_admin_help(msg:types.Message):
    if msg.from_user.id in ADMINS:
        await  msg.answer(ADMIN_HELP)
    else:
        await  msg.answer("ты недостоин")



async def main():
    print("starting bot..")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())