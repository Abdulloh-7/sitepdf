from flask import Flask, request, send_file, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/file", methods=["POST"])
def get_file():
    guid = request.args.get("guid")
    pin = request.form.get("pin")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT pin_code, file_path, attempts FROM files WHERE guid=?", (guid,))
    row = cursor.fetchone()

    if not row:
        return jsonify({"error": "Файл не найден"}), 404

    correct_pin, file_path, attempts = row

    if pin != correct_pin:
        attempts += 1
        cursor.execute("UPDATE files SET attempts=? WHERE guid=?", (attempts, guid))
        conn.commit()
        conn.close()
        return jsonify({"error": "Неверный PIN", "attempts": attempts}), 400

    conn.close()
    try:
        return send_file(file_path)
    except FileNotFoundError:
        return jsonify({"error": "Файл на сервере не найден"}), 404

if __name__ == "__main__":
    app.run(debug=True)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render задаёт порт через переменную PORT
    app.run(host="0.0.0.0", port=port, debug=True)