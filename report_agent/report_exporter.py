import os, time, json
from prometheus_client import start_http_server, Gauge
from db_conf import REPORT_DIR

DB_SIZE = Gauge('database_size', 'Database size in MB', labelnames=['hostname', 'database'])

class Metrics:
    """
    Класс для работы с метриками (импорт данных из файла, обработка, экспорт)
    """
    report_json = {}

    @classmethod
    def import_values_from_json_file(cls, file_path: str):
        """ Метод импорта данных из файла рапорта """
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    @classmethod
    def dir_validate(cls, path_dir: str):
        """ Метод проверки существования директории """
        if not os.path.exists(path_dir):
            raise FileNotFoundError(f"Directory {path_dir} does not exist")
        if not os.path.isdir(path_dir):
            raise NotADirectoryError(f"{path_dir} is not a directory") 
        return True
    
    @classmethod
    def file_validate(cls, file_path: str):
        """ Метод проверки существования файла """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found")
        return True
    
    def __new__(cls, *args, **kwargs):
        cls.file_validate(args[0])
        return super().__new__(cls)

    def __init__(self, report_file: str = os.readlink(os.path.join(REPORT_DIR, 'latest'))):
        self.report_file = report_file
        self.report_json = self.import_values_from_json_file(report_file)

    def get_report_json(self):
        return self.report_json

    def get_metric_names(self):
        return [key for key in self.report_json.keys()]

if __name__ == "__main__":

    start_http_server(8000)
    while True:
        P = Metrics(os.readlink(os.path.join(REPORT_DIR, 'latest')))
        print(P.get_metric_names())
        report_json = P.get_report_json()
        for database in report_json['databases']:
            
            DB_SIZE.labels(report_json["hostname"], database[0]).set(database[1])
            print(database[0] + ' : ' + str(database[1]))
        
        time.sleep(60)
