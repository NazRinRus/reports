import os, glob
from connect import db_connect
from db_conf import SQL_DIR

# функция отсечения от имени файла пути и расширения
def get_scriptname(filename: str):
    # Отделяем имя файла от пути (os.path.basename) 
    basename = os.path.basename(filename)
    # Разделяем имя и расширение (os.path.splitext)
    scriptname, _ = os.path.splitext(basename)
    return scriptname

# функция получения списка sql-скриптов (метрики)
def get_sqlscripts(sql_dir: str):
    try:
        sql_scripts = glob.glob(sql_dir + "/*.sql")
    except Exception as error:
        print("Ошибка при составлении списка sql-скриптов", error)
    return sql_scripts

# функция получения и формирование результата запросов
def get_sql_metrics(sql_scripts: list):
    result = {}
    for script in sql_scripts:
        # считываю файл с запросом в переменную content
        try:
            with open(script, 'r', encoding='utf-8') as file:
                content = file.read()
        except Exception as error:
            print(f"Ошибка при чтении файла {script}", error)
        
        metric_key = get_scriptname(script)
        metric_value = db_connect(content)

        # Вызов функции получения данных
        result[metric_key] = metric_value
    return result

print(get_sql_metrics(get_sqlscripts(SQL_DIR)))
