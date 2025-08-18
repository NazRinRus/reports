import requests
from db_conf import SERVER_HOST, REPORT_DIR

# функция экспорта файлов-рапортов по протоколу http(s)
def upload_report_http(file_name: str):
    url = f"http://{SERVER_HOST}:8001/upload/"
    file_path = f"{REPORT_DIR}/{file_name}"

    with open(file_path, "rb") as f:
        files = {"file": (file_path, f)}
        response = requests.post(url, files=files)

    return response.json()

if __name__ == "__main__":
    upload_report_http('report_notebook_18_08_2025.json')