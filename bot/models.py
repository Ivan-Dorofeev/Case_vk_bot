import os

from pony.orm import Database, Required, Json, select, db_session, desc

from Settings import DB_CONFIG

db = Database()
db.bind(**DB_CONFIG)


class UserStates(db.Entity):
    """Состояние корзины пользователя"""
    user_id = Required(str, unique=True)
    basket = Required(Json)


class Products(db.Entity):
    """Товары в базе данных"""
    name = Required(str)
    description = Required(str)
    category = Required(str)
    picture = Required(str)
    price = Required(int)
    counts = Required(int)


db.generate_mapping(create_tables=True)


@db_session
def write_to_db():
    count = 0
    for i in range(0, 3):
        count += 1
        name_count = 'Название ' + str(count)
        Products(name=name_count, description='Крутая обувь для повседневной деятельности', category='Повседневная',
                 picture=f'/stocks/pictures/product_category/daily/{count}.jpg',
                 price=2500, counts=10)


@db_session
def change_counts(name_product):
    products = Products.get(name=name_product)
    if products == 1:
        print('Это был последний', products.id, products.name)
        products.counts = 0
    else:
        products.counts -= 1


@db_session
def get_products_no_null():
    res = list(Products.select(lambda p: p.counts > 0))
    print(res)
    return res


@db_session
def get_products_by_type(shoes_type):
    products_by_type = list(Products.select(lambda p: p.category == shoes_type).order_by(Products.name))
    res = [p.name for p in products_by_type]
    print(res)
    return res


@db_session
def get_products_picture(product_number):
    product = Products.select(lambda p: p.name == product_number)
    product_picture = product.picture
    return product_picture


if __name__ == "__main__":
    write_to_db()
    # get_products_by_type(shoes_type='Повседневная')
    # get_products()
    # change_counts('Название 10')
