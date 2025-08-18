import requests
from db_conf import SERVER_HOST

# функция экспорта файлов-рапортов по протоколу http(s)
def upload_report_http(file_path: str):
    url = f"http://{SERVER_HOST}:8001/upload/"

    with open(file_path, "rb") as f:
        files = {"file": (file_path, f)}
        response = requests.post(url, files=files)

    return response.json()

if __name__ == "__main__":
    upload_report_http('./report_dir/report_notebook_18_08_2025.json')