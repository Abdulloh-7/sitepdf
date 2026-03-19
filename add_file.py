import sqlite3
import uuid

file_name = input("Имя PDF (в папке files): ").strip()
pin = input("PIN для файла (4 цифры): ").strip()

if not pin.isdigit() or len(pin) != 4:
    print("PIN должен быть 4 цифры")
    exit()

guid = str(uuid.uuid4())
file_path = f"files/{file_name}"

conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute("INSERT INTO files (guid, pin_code, file_path) VALUES (?, ?, ?)", (guid, pin, file_path))
conn.commit()
conn.close()

print("Файл добавлен!")
print("GUID:", guid)
print("PIN:", pin)
print("Ссылка:", f"https://repository-gov-uz-o83y.onrender.com/?guid={guid}")