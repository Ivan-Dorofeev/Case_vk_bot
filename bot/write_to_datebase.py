import peewee
from make_fly_ticket.make_fly_ticket import make_ticket

db = peewee.SqliteDatabase('registration.db')


class BassTable(peewee.Model):
    class Meta:
        database = db


class Registration(BassTable):
    """Создадим базу данных"""
    id = peewee.TextField()
    data = peewee.TextField()
    people = peewee.IntegerField()
    telephon = peewee.IntegerField()
    comment = peewee.TextField()
    in_city = peewee.TextField()
    out_city = peewee.TextField()


db.create_tables([Registration])


def wr_to_db(user, context):
    Registration.get_or_create(
        id=user,
        data=str(context['dispatcher_res_list'][int(context['number_choose_ways']) - 1])[2::],
        people=int(context['people_count']),
        telephon=int(context['phone_number']),
        comment=str(context['comment']),
        in_city=str(context['city_to']),
        out_city=str(context['city_from']),
    )

    return True
