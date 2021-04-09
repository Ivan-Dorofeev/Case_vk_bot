from pony.orm import Database, Required, Json, select

from Settings import DB_CONFIG

db = Database()
db.bind(**DB_CONFIG)


class UserStates(db.Entity):
    """Состояние корзины пользователя"""
    user_id = Required(str, unique=True)
    basket = Required(Json)


class Products(db.Entity):
    name = Required(str)
    category = Required(str)
    counts = Required(int)


db.generate_mapping(create_tables=True)

a = {
    1: ['Название 1', 'Спортивная', 10],
    2: ['Название 2', 'Спортивная', 10],
    3: ['Название 3', 'Спортивная', 10],
    4: ['Название 4', 'Спортивная', 10],
    5: ['Название 5', 'Спортивная', 10],
    6: ['Название 6', 'Спортивная', 10],
    7: ['Название 7', 'Спортивная', 10],
    8: ['Название 8', 'Спортивная', 10],
    9: ['Название 9', 'Спортивная', 10],
    10: ['Название 10', 'Спортивная', 10],
    11: ['Название 11', 'Спортивная', 10],
    12: ['Название 12', 'Спортивная', 10],
    13: ['Название 13', 'Спортивная', 10],
    14: ['Название 14', 'Спортивная', 10],
    15: ['Название 15', 'Спортивная', 10],

}

for name, items in a.items():
    Products(name=items[0], category=items[1], counts=items[2])

print(db.select().where(name='Название 1'))
