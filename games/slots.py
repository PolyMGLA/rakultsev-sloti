from games import utils
from datetime import datetime

RULES = """
- Правила игры в Слоты -

Случайно выбираются три фигуры. В зависимости от полученной комбинации вы получаете выигрыш/бонусы.
Цена: 2р

🍌🍌🍌 - Шимпанзини бананнини (получаете 1р)
🍓🍓🍓 - Клубничка хмм (получаете 10р)
🍒🍒🍒 - В лес по ягоды (получаете 15р)
🍍🍍🍍 - идешь в ананас (теряешь 30р)
🍑🍑🍑 - не щовел (получаете 40р)
🌈🌈🌈 - Absolute cinema
💀💀💀 - Вы проиграли хату
? ? ? ? ? ?  - Также есть доп.бонусы)

Играть: /slots
"""

fruits =  ["🍓", "🍌", "🍒", "🍍", "🍑", "🌈", "💀"]
weights = [10,   15,   9,    8,    10,   1,    1   ]
secrw =   [3,    2,    1,    3,    2,    5,    5  ]

fruits_weighted = []
for i in range(7):
    fruits_weighted += [fruits[i]] * weights[i]

secret_weighted = []
for i in range(7):
    secret_weighted += [fruits[i]] * secrw[i]

def _spin(arr: list[str]) -> str:
    return "".join(utils.choice(arr) for i in range(3))


def secret_regen():
    global SECRET
    SECRET = _spin(secret_weighted)
secret_regen()

def spin(db, dt, id: int) -> str:
    global SECRET

    s = _spin(fruits_weighted)
    bal = db.get_bal(id)
    if db.get_user(id) == False:
        return ["Вы еще не зарегистрированы!\n/start"]
    if bal < 2:
        return ["Недостаточно денег.\nБез додепа не разобраться\n /dodep"]
    newbal = bal - 2
    comb = ""

    if s == SECRET:
        newbal += utils.randint(a= -1000,b = 1000)
        comb += "secret; "

    match s:
        case "🍌🍌🍌":
            newbal += 1
            comb = "Шимпанзини бананнини"
        case "🍓🍓🍓":
            newbal += 10
            comb = "Клубничка хмм"
        case "🍒🍒🍒":
            newbal += 15
            comb = "🍒Мама! Я спелая вишня🍒"
        case "🍍🍍🍍":
            newbal -= 30
            comb = "идешь в ананас"
        case "🍑🍑🍑":
            newbal += 40
            comb = "не щовел"
        case "🌈🌈🌈":
            newbal += 999
            comb = "Absolute cinema"
        case "💀💀💀":
            newbal -= 5000
            comb = "Вы проиграли хату"
        case "🍌🍑🍌":
            newbal += utils.randint(-50, 50)
            comb = "Пайпер Перри..?"
        case _:
            if s.count("🍑") == 2 and s.count("🍍") == 1:
                newbal += 25
                comb = "суй ананас.."
            if s.count("🌈") == 1:
                newbal += 10
                comb += "1 радуга; "
            if s.count("🌈") == 2:
                newbal += 100
                comb += "2 радуги; "
            if s.count("💀") == 1:
                newbal -= 10
                comb += "1 череп; "
            if s.count("💀") == 2:
                newbal -= 100
                comb += "2 черепа; "
    if not comb: comb = "ничего"
    if db.update_bal(id, newbal) and db.add_slot(id):
        # if newbal < 0:
        #     dt.set_date(id, dt.get_date(id).date - 10 * newbal)
        return [s, f"Выпало: {comb}\nТекущий баланс: {newbal}"]

    return ["Ошибка при крутке"]