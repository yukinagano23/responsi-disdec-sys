from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host="localhost",
        port="5433",
        user="yugabyte",
        password="yugabyte",
        dbname="yugabyte"
    )

@app.route("/mahasiswa", methods=["GET"])
def get_mahasiswa():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nama, nim, jurusan FROM mahasiswa;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "nama": row[1],
            "nim": row[2],
            "jurusan": row[3]
        })
    return jsonify(result)

@app.route("/matakuliah", methods=["GET"])
def get_matakuliah():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, kode_mk, nama_mk, sks FROM matakuliah;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "kode_mk": row[1],
            "nama_mk": row[2],
            "sks": row[3]
        })
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
