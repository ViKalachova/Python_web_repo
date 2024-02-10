import sqlite3


def execute_query(sql_query) -> list:
    with open(sql_query, 'r') as f:
        sql = f.read()
        with sqlite3.connect('grades.db') as con:
            cur = con.cursor()
            cur.execute(sql)
            return cur.fetchall()


if __name__ == '__main__':
    print(execute_query('query_1.sql'))
    print(execute_query('query_2.sql'))
    print(execute_query('query_3.sql'))
    print(execute_query('query_4.sql'))
    print(execute_query('query_5.sql'))
    print(execute_query('query_6.sql'))
    print(execute_query('query_7.sql'))
    print(execute_query('query_8.sql'))
    print(execute_query('query_9.sql'))
    print(execute_query('query_10.sql'))
    print(execute_query('query_11.sql'))
    print(execute_query('query_12.sql'))
