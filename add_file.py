import sqlite3
import uuid
import os

# ссылка твоего сайта
BASE_URL = "https://repository-gov-uz-o83y.onrender.com"

# ввод имени файла
file_name = input("Введите имя PDF файла (например: test.pdf): ").strip()
file_path = f"files/{file_name}"

# проверка: существует ли файл
if not os.path.isfile(file_path):
    print("❌ Файл не найден в папке files/")
    exit()

# ввод PIN
pin = input("Введите PIN (4 цифры): ").strip()

# проверка PIN
if not pin.isdigit() or len(pin) != 4:
    print("❌ PIN должен быть ровно 4 цифры")
    exit()

# генерация GUID
guid = str(uuid.uuid4())

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
print("\n✅ Файл успешно добавлен!")
print("📄 Файл:", file_name)
print("🔑 PIN:", pin)
print("🆔 GUID:", guid)
print("\n🔗 Ссылка для QR:")
print(f"{BASE_URL}/?guid={guid}")