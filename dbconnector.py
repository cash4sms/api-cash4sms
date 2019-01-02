#!/usr/bin/python3

import psycopg2
import psycopg2.extras

class DB(object):
    def __init__(self):
        super(DB, self).__init__()

        self._db_config = {
            'host': 'ec2-54-247-74-131.eu-west-1.compute.amazonaws.com',
            'dbname': 'd2osvejtnnputo',
            'user': 'qkgwiflzyukfkm',
            'password': '0ce46de185a0682071e19dc5cba315b40affaf089fee59bfdaf16802bf4c34fb'
        }
        
        self._db_connect = psycopg2.connect(**self._db_config)
        self._db_cursor = self._db_connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    def execute_sql(self, sql:str):
        """
        :return: [ { item_1, item_2, ... } ]
        """
        self._db_cursor.execute(sql)
        return self._db_cursor.fetchall()

    def execute_dic(self, table:str, keys:list, client_id:str = None):
        """
        :return: [ { keys[0] : value, ... } ]\n
        :return: { keys[0] : value, ... } if client_id exist
        """
        select = ', '.join(keys)
        sql = f'SELECT {select} FROM {table}'

        if client_id is not None:
            sql = sql + f' WHERE client_id LIKE \'{client_id}\''

        array = list()
        self._db_cursor.execute(sql)
        array = self._db_cursor.fetchall()

        return array if client_id is None else ( array[0] if len(array)>0 else None )

    def save(self, table:str, keys:list, data:list, client_id:str):
        
        select = ', '.join(keys)
        update = ', '.join( map( lambda it: '\'' + it + '\'', data ) )
        sql = f'UPDATE {table} SET ({select}) = ({update}) WHERE client_id LIKE \'{client_id}\''
        
        self._db_cursor.execute(sql)
        self._db_connect.commit()

    def __del__(self):
        self._db_connect.close()
        self._db_cursor.close()


if __name__ == '__main__':



    pass