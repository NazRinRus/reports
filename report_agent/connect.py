import psycopg2

HOST = "localhost"
DATABASE = "demo"
USER = "postgres"
PASSWORD = "postgres"

# считываю файл с запросом в переменную content
try:
    with open('query.sql', 'r', encoding='utf-8') as file:
        content = file.read()

except Exception as error:
    print("Ошибка при чтении файла query.sql", error)

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
    print(sql_result)

except Exception as error:
    print("Ошибка при подключении к PostgreSQL", error)

finally:
    # Закрываем курсор и соединение
    if cursor:
        cursor.close()
    if connection:
        connection.close()
        print("Соединение с PostgreSQL закрыто")
