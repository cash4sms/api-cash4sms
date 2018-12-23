#!/usr/bin/python3

import psycopg2

class DB_Cash4SMS(object):
    def __init__(self):
        super(DB_Cash4SMS, self).__init__()

        self._db_config = {
            'host': 'ec2-54-247-74-131.eu-west-1.compute.amazonaws.com',
            'dbname': 'd2osvejtnnputo',
            'user': 'qkgwiflzyukfkm',
            'password': '0ce46de185a0682071e19dc5cba315b40affaf089fee59bfdaf16802bf4c34fb'
        }
        
        self._db_connect = psycopg2.connect(**self._db_config)
        self._db_cursor = self._db_connect.cursor()

    def execute(self, sql: str):
        """ return [ ( item_1, item_2, ... ) ] """
        self._db_cursor.execute(sql)
        return self._db_cursor.fetchall()

    def __del__(self):
        self._db_connect.close()
        self._db_cursor.close()


if __name__ == '__main__':

    # sql = """
    #     SELECT first_name, last_name, birth, country
    #     FROM cash4sms_users
    # """

    # array = []
    # db = DB_Cash4SMS().execute(sql)
    # for i in range(len(db)):
    #     item = {
    #         "first_name": db[i][0],
    #         "last_name": db[i][1],
    #         "birth": db[i][2],
    #         "country": db[i][3]
    #     }    
    #     array.append(item)

    # print(array)

    pass