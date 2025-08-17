import psycopg2
import db_conf


def db_connect(content: str):
    try:
        # Устанавливаем соединение
        connection = psycopg2.connect(
            host=db_conf.HOST,
            database=db_conf.DATABASE,
            user=db_conf.USER,
            password=db_conf.PASSWORD
        )

        # Создаем курсор для выполнения операций с базой данных
        cursor = connection.cursor()

        # Пример выполнения запроса
        cursor.execute(content)
        sql_result = cursor.fetchall()


    except Exception as error:
        print("Ошибка при подключении к PostgreSQL", error)

    finally:
        # Закрываем курсор и соединение
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("Соединение с PostgreSQL закрыто")
   
    return sql_result 
