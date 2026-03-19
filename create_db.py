import sqlite3

# создаём базу
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# создаём таблицу
cursor.execute("""
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guid TEXT UNIQUE,
    pin_code TEXT,
    file_path TEXT,
    attempts INTEGER DEFAULT 0
)
""")

# добавляем пример файла
cursor.execute("""
INSERT OR IGNORE INTO files (guid, pin_code, file_path) 
VALUES ('abcd-1234', '1234', 'files/example.pdf')
""")

conn.commit()
conn.close()

print("База database.db создана и готова!")