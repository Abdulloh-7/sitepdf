import sqlite3
import uuid
import random

# настройки
BASE_URL = "https://repository-gov-uz-o83y.onrender.com"

# генерируем GUID
guid = str(uuid.uuid4())

# генерируем PIN (4 цифры)
pin = str(random.randint(1000, 9999))

# путь к файлу (ВАЖНО: файл должен уже лежать в папке files)
file_name = input("Введите имя PDF файла (например: test.pdf): ")
file_path = f"files/{file_name}"

# запись в базу
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO files (guid, pin_code, file_path)
VALUES (?, ?, ?)
""", (guid, pin, file_path))

conn.commit()
conn.close()

# вывод результата
print("\n✅ Файл добавлен!")
print("GUID:", guid)
print("PIN:", pin)
print("Ссылка для QR:")
print(f"{BASE_URL}/?guid={guid}")