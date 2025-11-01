### Пример отправки письма через sendmail
```
import subprocess

# Параметры письма
subject = "Test report"
sender = "db_host@zt.ru"  # Можно любой email
recipient = "r.nazarov@zt.ru"
body = "test content"

# Формируем письмо в формате, понятном для sendmail
message = f"""From: {sender}
To: {recipient}
Subject: {subject}

{body}
"""

# Отправка через sendmail
try:
    process = subprocess.Popen(["/usr/sbin/sendmail", "-t"], stdin=subprocess.PIPE)
    process.communicate(message.encode("utf-8"))
    print("Письмо отправлено!")
except Exception as e:
    print(f"Ошибка: {e}")
```
### Пример отправки письма через mail
```
import subprocess

subprocess.run(
    ["mail", "-s", "Head", "r.nazarov@zt.ru"],
    input="Test content",
    text=True,
    check=True
)
```
echo "Test" | mail -s "Test" r.nazarov@zt.ru


Как выполнить запросы?
1. Автоматически все из директории в одном подключении: имя переменной = имя файла с запросом : резальтат
2. На каждый запрос сделать свой метод get_ 

Решение: Запросы для основных метрик в одной директории и прописываются методами, а дополнительные автоматически будут браться из другой директории с запросами.
Продумать автоматическую генерацию методов, исходя из запросов в директории.

Директория `sh_queries` для скриптов оболочки, в виде `metrica_name.sh`
