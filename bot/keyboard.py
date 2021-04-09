menu = {
    'Разделы': ['Спортивная', 'Повседневная', 'Хардкор'],
    'Товары': [
        {'category': 0, 'описание': 'Для бега', 'фото': 'ссылка', 'наличие': 5, 'стоимость': 2500},
        {'category': 0, 'описание': 'Для бега', 'фото': 'ссылка', 'наличие': 3, 'стоимость': 2500, },
        {'category': 0, 'описание': 'Для бега', 'фото': 'ссылка', 'наличие': 12, 'стоимость': 2500, },
        {'category': 0, 'описание': 'Для бега', 'фото': 'ссылка', 'наличие': 3, 'стоимость': 2500, },
        {'category': 1, 'описание': 'Для прогулок', 'фото': 'ссылка', 'наличие': 1, 'стоимость': 1200, },
        {'category': 1, 'описание': 'Для прогулок', 'фото': 'ссылка', 'наличие': 5, 'стоимость': 1200, },
        {'category': 1, 'описание': 'Для прогулок', 'фото': 'ссылка', 'наличие': 5, 'стоимость': 1200, },
        {'category': 1, 'описание': 'Для прогулок', 'фото': 'ссылка', 'наличие': 2, 'стоимость': 1200, },
        {'category': 1, 'описание': 'Для прогулок', 'фото': 'ссылка', 'наличие': 6, 'стоимость': 1200, },
        {'category': 2, 'описание': 'Для всего', 'фото': 'ссылка', 'наличие': 8, 'стоимость': 3500, },
        {'category': 2, 'описание': 'Для всего', 'фото': 'ссылка', 'наличие': 6, 'стоимость': 3500, },
        {'category': 2, 'описание': 'Для всего', 'фото': 'ссылка', 'наличие': 3, 'стоимость': 3500, },
    ],
    'Корзина': [],

}

steps = {
    0: {'message': 'Привет. Выбери из разделов ниже:', 'buttons': ['Разделы', 'Корзина']},
    1: {'message': 'У нас есть разная обувь, какая интересует?',
        'buttons': ['Назад', 'Спортивная', 'Повседневная', 'Хардкор']},
    3: {'message': 'Первые 5 товаров по списку:', 'buttons': ['Назад', 'Далее', 'Корзина', ]},
    4: {'message': 'Следующие 5 товаров по списку:', 'buttons': ['Назад', 'Далее', 'Корзина', ]},
}
