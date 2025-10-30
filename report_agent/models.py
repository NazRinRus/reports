import os, glob, datetime, json, socket # yaml
import db_conf
from sqlalchemy import create_engine, text
from pathlib import Path

# Дополнительные функции для работы с файловой системой

def dir_validate(dir_path: str):
    """ Функция проверки существования директории """
    if not os.path.exists(path_dir):
        raise FileNotFoundError(f"Directory {path_dir} does not exist")
    if not os.path.isdir(path_dir):
        raise NotADirectoryError(f"{path_dir} is not a directory") 
    return True
    
def file_validate(file_path: str):
    """ Функция проверки существования файла """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")
    return True

def get_content_file(file_path: str):
    """ Функция извлечения содержимого файла """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as error:
        print(f"Ошибка при чтении файла {file_path}", error)
    return content

def get_scriptname(filename: str):
    """ Функция отсечения пути и расширения от имени SQL-файла """
    # Отделяем имя файла от пути (os.path.basename) 
    basename = os.path.basename(filename)
    # Разделяем имя и расширение (os.path.splitext)
    scriptname, _ = os.path.splitext(basename)
    return scriptname

def get_sqlscripts(sql_dir: str):
    """ Функция получения списка sql-скриптов (метрики) """
    try:
        sql_scripts = glob.glob(sql_dir + "/*.sql")
    except Exception as error:
        print("Ошибка при составлении списка sql-скриптов", error)
    return sql_scripts

def report_generation(result_report: dict):
    """ Функция формирования файла-отчета в формате .json"""
    current_date = datetime.datetime.now().strftime("%d_%m_%Y")
    hostname = socket.gethostname()
    filename = f"{db_conf.REPORT_DIR}/report_{hostname}_{current_date}.json"
#    report_yaml = yaml.dump(result_report, allow_unicode=True)
    report_json = json.dumps(result_report, indent=4, ensure_ascii=False)
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(report_json)
        update_latest_symlink(os.path.abspath(filename), 'latest')
    except:
        print(f"Ошибка при записи файла {filename}", error)
    return filename

def update_latest_symlink(target_file: str, symlink_name: str = 'latest'):
    """
    Функция обновляет симлинк 'latest' на указанный файл
    Args:
        target_file: путь к целевому файлу
        symlink_name: имя симлинка (по умолчанию 'latest')
    """
    target_path = Path(target_file)
    symlink_path = target_path.parent / symlink_name
    try:
        # Проверяем целевой файл
        if not target_path.exists():
            raise FileNotFoundError(f"Целевой файл не существует: {target_file}")       
        # Удаляем старый симлинк если существует
        if symlink_path.exists() or symlink_path.is_symlink():
            symlink_path.unlink()
        # Создаем новый симлинк
        symlink_path.symlink_to(target_path)
        print(f"✓ Симлинк обновлен: {symlink_path} -> {target_path.name}")
    except Exception as e:
        print(f"✗ Ошибка обновления симлинка: {e}")

# Классы описывающие калстера
class PostgreSQLCluster:
    """
    Класс, описывающий общие свойства и методы баз данных PostgreSQL
    """
    def __init__(self, connect_string: str = 'postgresql://postgres:@localhost:5432/postgres'):
        self.connect_string = connect_string

    def connect_db(self, sql_queries: str):
        """
        Метод подключения к БД и выполнения запроса.
        """
        engine = create_engine(self.connect_string, echo=True)
        with engine.connect() as conn:
	        result = conn.execute(text(sql_queries))
        return [tuple(row) for row in result.all()]


class PostgresDatabase(PostgreSQLCluster):
    """
    Класс, описывающий атрибуты и методы кластера целиком. Методы типа get_metrics_ генерируются автоматически из файлов-SQL-скриптов в директории SQL_DIR/for_the_cluster/
    """
    def __init__(self, connect_string: str = 'postgresql://postgres:@localhost:5432/postgres'):
        super().__init__(connect_string)
        self._generate_metric_methods()
    
    def _generate_metric_methods(self):
        """Автоматически генерирует методы get_metric_* для всех SQL файлов в директории"""
        sql_dir = os.path.join(db_conf.SQL_DIR, 'for_the_cluster')
        
        for sql_file in os.listdir(sql_dir):
            if sql_file.endswith('.sql'):
                method_name = f"get_metric_{get_scriptname(sql_file)}"
                sql_path = os.path.join(sql_dir, sql_file)
                
                # Создаем метод для этого SQL файла
                def create_metric_method(sql_path=sql_path):
                    def metric_method(self):
                        result = {}
                        if file_validate(sql_path):
                            sql_query = get_content_file(sql_path)    
                            metric_key = get_scriptname(sql_path)
                            metric_value = self.connect_db(sql_query)
                            result[metric_key] = metric_value
                        else:
                            result[get_scriptname(sql_path)] = None
                        return result
                    return metric_method
                
                # Добавляем метод в класс
                setattr(PostgresDatabase, method_name, create_metric_method())

    def get_all_metrics(self) -> dict:
        """
        Метод объединения результатов всех методов, начинающихся с get_metric_ в один словарь
        """
        all_metrics = {}
        
        # Ищем все методы, начинающиеся с get_metric_
        for method_name in dir(self):
            if method_name.startswith('get_metric_'):
                method = getattr(self, method_name)
                if callable(method):
                    try:
                        # Вызываем метод и получаем результат
                        result = method()
                        # Объединяем словари
                        all_metrics.update(result)
                    except Exception as e:
                        # Логируем ошибку, но продолжаем сбор других метрик
                        metric_name = method_name.replace('get_metric_', '')
                        all_metrics[metric_name] = f"Error: {e}"
        
        return all_metrics
