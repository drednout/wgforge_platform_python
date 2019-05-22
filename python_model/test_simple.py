from simple.db import db_connection, db_pool_connection
from simple.player import Player
from simple.money import (
    Money,
    GOLD_CURRENCY_CODE,
    SILVER_CURRENCY_CODE
)


def prepare_db():
    print("INFO: prepare db")
    with db_connection.cursor() as cursor:
        print("INFO: truncate player")
        cursor.execute("TRUNCATE player")
        cursor.execute("TRUNCATE money")


def do_smoke_test():
    player1 = Player(nickname="Vasya", email="vasya@tut.by", password="123", db_connection=db_connection)
    player1.insert()
    print("new player was created: {}".format(player1.as_dict()))

    player2 = Player(db_connection=db_connection)
    player2.load_by_nickname(nickname="Vasya")

    player_money = Money(player_id=player1.id, db_connection=db_connection)
    player_money.init()
    player_money.give_money(GOLD_CURRENCY_CODE, 100)
    player_money.give_money(SILVER_CURRENCY_CODE, 1000)
    player_money.take_money(GOLD_CURRENCY_CODE, 10)
    player_money.take_money(SILVER_CURRENCY_CODE, 100)


def do_pool_test():
    with db_pool_connection() as db_connection:
        player1 = Player(nickname="VasyaPool", email="vasya_pool@tut.by", password="123",
                         db_connection=db_connection)
        player1.insert()
        print("new player was created: {}".format(player1.as_dict()))

        player2 = Player(db_connection=db_connection)
        player2.load_by_nickname(nickname="Vasya")


if __name__ == "__main__":
    prepare_db()
    do_smoke_test()
    do_pool_test()



