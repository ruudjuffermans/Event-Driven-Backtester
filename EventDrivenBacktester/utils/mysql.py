from .config import get_config
import mysql.connector


def mysql(config={}):
    config = get_config("mysql", config)
    connection = mysql.connector.connect(**config)

    def inner(query):
        c = connection.cursor(dictionary=True)
        data = []
        c.execute(query)
        connection.commit()
        for row in c:
            print(row)
            data.append(row)
        connection.commit()
        c.close()
        return data

    return inner
