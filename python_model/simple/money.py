import copy

GOLD_CURRENCY_CODE = "gold"
SILVER_CURRENCY_CODE = "silver"

AVAILABLE_CODES = set([GOLD_CURRENCY_CODE, SILVER_CURRENCY_CODE])


class Money(object):
    """Model class for money entity.
    """

    GET_BY_PLAYER_ID = """
        SELECT 
            id, player_id, currency_code, amount, created, updated
        FROM 
            money
        WHERE id=%(id)s
    """
    INSERT = """
        INSERT INTO money
            (player_id, currency_code, amount) 
        VALUES 
            (%(player_id)s, %(currency_code)s, %(amount)s)
        RETURNING
            id, created, updated
    """

    GIVE_MONEY = """
        UPDATE 
            money
        SET 
            amount =  amount + %(amount)s, updated=now()
        WHERE 
            player_id=%(player_id)s AND currency_code=%(currency_code)s
    """
    TAKE_MONEY = """
        UPDATE 
            money
        SET 
            amount = amount - %(amount)s, updated=now()
        WHERE 
            player_id=%(player_id)s AND currency_code=%(currency_code)s
    """

    def __init__(self, player_id=None, money_dict=None, db_connection=None):
        self.player_id = player_id
        self.money_dict = {}
        self.default_money_dict = {
            GOLD_CURRENCY_CODE: 0,
            SILVER_CURRENCY_CODE: 0
        }
        if money_dict is None:
            self.money_dict = copy.copy(self.default_money_dict)
        else:
            self.money_dict = copy.copy(money_dict)

        self.db_connection = db_connection


    def load_by_player_id(self, player_id):
        with self.db_connection.cursor() as cursor:
            cursor.execute(self.GET_BY_PLAYER_ID, {"player_id": player_id})
            row = cursor.fetchone()
            self.player_id = row[1]
            currency_code = row[2]
            amount = row[3]
            self.money_dict[currency_code] = amount



    def init(self):
        with self.db_connection.cursor() as cursor:
            for code, amount in self.default_money_dict.items():
                cursor.execute(self.INSERT, {"player_id": self.player_id,
                                             "currency_code": code,
                                             "amount": amount})
            self.db_connection.commit()


    def give_money(self, code, amount):
        # TODO: add validation of code
        with self.db_connection.cursor() as cursor:
            cursor.execute(self.GIVE_MONEY, {"player_id": self.player_id,
                                             "currency_code": code,
                                             "amount": amount})
            self.money_dict[code] += amount
            self.db_connection.commit()
        # TODO: add logging of money event

    def take_money(self, code, amount):
        # TODO: add validation of code
        with self.db_connection.cursor() as cursor:
            cursor.execute(self.TAKE_MONEY, {"player_id": self.player_id,
                                             "currency_code": code,
                                             "amount": amount})
            self.money_dict[code] -= amount
            self.db_connection.commit()
        # TODO: add logging of money event


    def as_dict(self):
        return self.money_dict