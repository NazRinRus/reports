import requests, shutil, os, subprocess
from db_conf import SERVER_HOST, NFS_DIR, SERVER_EMAIL

# функция экспорта файлов-рапортов по протоколу http(s)
def upload_report_http(file_path: str):
    url = f"http://{SERVER_HOST}:8001/upload/"
    if not os.path.exists(file_path):
        print(f"Ошибка: файл {file_path} не существует!")
        exit(1)

    with open(file_path, "rb") as f:
        files = {"file": (file_path, f)}
        response = requests.post(url, files=files)

    return response.json()

# функция экспорта файлов-рапортов в NFS-директорию
def upload_report_nfs(file_path: str):
    # Проверяем, существует ли исходный файл
    if not os.path.exists(file_path):
        print(f"Ошибка: файл {file_path} не существует!")
        exit(1)
    # Проверяем, существует ли целевая директория, и создаем её, если нет
    if not os.path.exists(NFS_DIR):
        os.makedirs(NFS_DIR, exist_ok=True)
    # Формируем полный путь к целевому файлу (можно сохранить исходное имя файла)
    destination_path = os.path.join(NFS_DIR, os.path.basename(file_path))
    # Копируем файл
    try:
        shutil.copy2(file_path, destination_path)  # copy2 сохраняет метаданные (время модификации и т. д.)
        print(f"Файл успешно скопирован в {destination_path}")
    except Exception as e:
        print(f"Ошибка при копировании файла: {e}")

    return destination_path

# функция экспорта содержимого рапортов по EMail
def upload_report_email(file_path: str):
    # Проверяем, существует ли исходный файл
    if not os.path.exists(file_path):
        print(f"Ошибка: файл {file_path} не существует!")
        exit(1)
    try:
        with open(file_path, 'r') as file:
            report_content = file.read()
    except:
        print(f"Ошибка при чтения файла {file_path}", error)
    subprocess.run(
        ["mail", "-s", "report", SERVER_EMAIL],
        input=report_content,
        text=True,
        check=True
    )
    return report_content

if __name__ == "__main__":
    upload_report_http(os.readlink('./report_dir/latest'))
