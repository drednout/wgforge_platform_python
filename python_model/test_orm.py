from orm.db import db_connection, db_session
from orm.model import Player, Money


def prepare_db():
    print("INFO: prepare db")
    with db_connection.begin():
        print("INFO: truncate player")
        db_connection.execute("TRUNCATE player")
        db_connection.execute("TRUNCATE money")


def do_smoke_test():
    player1 = Player(nickname="Vasya", email="vasya@tut.by", password="123")
    db_session.add(player1)

    print("new player was created: {}".format(player1.as_dict()))

    our_player = db_session.query(Player).filter_by(nickname='Vasya').first()
    print("info from db about our player was created: {}".format(our_player.as_dict()))

    player1_money_gold = Money(player_id=player1.id, currency_code='gold', amount=100)
    player1_money_silver = Money(player_id=player1.id, currency_code='silver', amount=1000)
    db_session.add(player1_money_gold)
    db_session.add(player1_money_silver)

    player_money = db_session.query(Money).filter_by(player_id=player1.id).all()
    print("info from db about player1 money: {}".format([m.as_dict() for m in player_money]))

    db_session.commit()


if __name__ == "__main__":
    prepare_db()
    do_smoke_test()



