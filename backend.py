from flask import Flask, request, send_file, jsonify

import sqlite3
import os

app = Flask(__name__, static_folder="", template_folder="")

DB_PATH = "database.db"

def get_file_record(guid):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT pin_code, file_path, attempts FROM files WHERE guid=?", (guid,))
    row = cursor.fetchone()
    conn.close()
    return row

def increment_attempts(guid):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE files SET attempts = attempts + 1 WHERE guid=?", (guid,))
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/file", methods=["POST"])
def file_page():
    guid = request.args.get("guid")
    pin = request.form.get("pin")
    captcha = request.form.get("captcha")

    if not guid:
        return jsonify({"error": "GUID не указан"}), 400

    record = get_file_record(guid)
    if not record:
        return jsonify({"error": "Файл не найден"}), 404

    correct_pin, file_path, attempts = record
    require_captcha = attempts >= 4

    # проверка CAPTCHA
    if require_captcha and captcha != "9315":
        return jsonify({"error": "Требуется CAPTCHA"}), 400

    if pin == correct_pin:
        # проверяем, существует ли файл
        if not os.path.isfile(file_path):
            return jsonify({"error": "Файл PDF не найден на сервере"}), 500
        return send_file(file_path)
    else:
        increment_attempts(guid)
        return jsonify({"error": "Неверный PIN", "attempts": attempts + 1}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render задаёт порт через переменную PORT
    app.run(host="0.0.0.0", port=port, debug=True)