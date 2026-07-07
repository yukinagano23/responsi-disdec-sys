# Pengerjaan Soal 2: REST API Python untuk YugabyteDB
## Bagian A: Persiapan Environment Python
### 1. Install Python dan pip (jika belum ada)
<img width="1040" height="664" alt="gambar" src="https://github.com/user-attachments/assets/e5319685-b4da-4c80-8508-dc14a020bdab" />

**Penjelasan**: Paket ini memastikan Python 3 beserta pip (package manager) dan venv (untuk membuat virtual environment) tersedia di WSL Debian.

### 2. Buat folder project
<img width="1031" height="213" alt="gambar" src="https://github.com/user-attachments/assets/a6b10fd0-0f5c-46f0-875e-d47c6e7d0856" />

**Penjelasan**: Folder ini akan menjadi tempat seluruh source code REST API, terpisah dari folder lain agar rapi saat nanti di-push ke GitHub.

### 3. Buat virtual environment
<img width="1033" height="164" alt="gambar" src="https://github.com/user-attachments/assets/2f760b37-ac99-441f-850e-7fb047dc53bd" />

**Penjelasan**: Virtual environment mengisolasi dependency Python khusus project ini, sehingga tidak bercampur dengan package Python lain di sistem. Setelah diaktifkan, prompt terminal biasanya menampilkan (venv) di depan.

### 4. Install library yang dibutuhkan
<img width="1037" height="534" alt="gambar" src="https://github.com/user-attachments/assets/3fc173ea-8645-40db-8a8a-378f35994f3a" />

**Penjelasan**:
* Flask dipakai sebagai framework untuk membangun REST API.
* psycopg2-binary adalah driver PostgreSQL untuk Python, dan bisa dipakai untuk konek ke YugabyteDB karena YSQL kompatibel dengan protokol PostgreSQL.

---

## Bagian B: Menentukan Cara Koneksi ke YugabyteDB
### 5. Cek port yang ter-mapping ke host
<img width="1037" height="153" alt="gambar" src="https://github.com/user-attachments/assets/51064413-b788-4c51-9249-fb3e1f4c9a49" />

**Penjelasan**: Dari hasil sebelumnya, port 5433 (YSQL) sudah ter-mapping ke 0.0.0.0:5433->5433/tcp. Ini berarti dari sisi WSL Debian (di luar container), YugabyteDB bisa diakses lewat localhost:5433, berbeda dengan koneksi dari dalam container yang harus memakai hostname container. Ini karena Docker port mapping menghubungkan port host ke port container, sehingga proses Python yang berjalan di WSL (bukan di dalam container) cukup memakai localhost.

### 6. Uji koneksi cepat dari host (opsional, sebagai verifikasi)
<img width="1034" height="103" alt="gambar" src="https://github.com/user-attachments/assets/a177ab74-32ec-41b2-a26f-cb8cd1778a46" />
Jika psql belum terinstal di WSL host, langkah ini bisa dilewati karena Python nanti yang akan menangani koneksi langsung.

**Penjelasan**: Langkah ini memverifikasi bahwa port 5433 memang bisa diakses dari luar container sebelum ditulis di kode Python, supaya jika ada error nanti, penyebabnya bisa dipersempit (kode Python vs koneksi jaringan).

## Bagian C: Membuat REST API dengan Flask
### 7. Buat file app.py
<img width="1037" height="103" alt="gambar" src="https://github.com/user-attachments/assets/ae4c5f1c-ac0d-4764-a83b-65e909ddb3f6" />
Isi file:

```bash
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
```

<img width="1032" height="696" alt="gambar" src="https://github.com/user-attachments/assets/896abe37-a971-40ef-ab9e-54ff2dde68ad" />

**Penjelasan tiap bagian kode**:

* get_connection() — fungsi terpisah untuk membuka koneksi ke YugabyteDB, dipanggil ulang di tiap endpoint supaya tiap request punya koneksi baru (praktik umum di aplikasi kecil, meski di skala besar biasanya dipakai connection pooling).
* @app.route("/mahasiswa") — endpoint yang saat diakses akan menjalankan query SELECT ke tabel mahasiswa, lalu mengubah hasilnya (berupa tuple) menjadi list of dictionary supaya bisa otomatis dikonversi Flask menjadi format JSON lewat jsonify().
* @app.route("/matakuliah") — endpoint serupa, tapi mengarah ke tabel matakuliah.
* host="0.0.0.0" pada app.run() — membuat server Flask bisa diakses dari luar localhost juga (berguna jika ingin diakses dari browser Windows, bukan cuma dari dalam WSL).

---

## Bagian D: Menjalankan dan Menguji REST API
### 8. Jalankan aplikasi Flask
<img width="1031" height="254" alt="gambar" src="https://github.com/user-attachments/assets/c94fd892-80c5-4a26-810b-bd1db577fa49" />

**Penjelasan**: Perintah ini menjalankan server Flask secara langsung (development server), yang otomatis listen di port 5000 sesuai konfigurasi pada kode.

### 9. Uji endpoint lewat curl (dari terminal WSL lain)
<img width="957" height="573" alt="gambar" src="https://github.com/user-attachments/assets/761f834a-2774-4d23-a313-0a16b54dc465" />
<img width="960" height="599" alt="gambar" src="https://github.com/user-attachments/assets/18785f5c-3a9f-47fb-9f00-a97800c48f63" />

**Penjelasan**: Kedua perintah ini mengirim HTTP GET request ke masing-masing endpoint, dan hasilnya berupa response JSON berisi data dari tabel mahasiswa dan matakuliah yang sebelumnya sudah diisi di Soal 1.

### 10. Uji lewat browser (dari Windows)
Buka browser dan akses:
```bash
http://localhost:5000/mahasiswa
http://localhost:5000/matakuliah
```
<img width="1079" height="629" alt="gambar" src="https://github.com/user-attachments/assets/cd08c7a0-dfc7-4e0b-9363-e6066d1f982b" />
<img width="1077" height="639" alt="gambar" src="https://github.com/user-attachments/assets/a3cb139b-b20f-4e73-b48e-f68fbedfb60e" />

**Penjelasan**: Karena WSL2 secara default melakukan port forwarding otomatis ke localhost Windows, alamat ini bisa langsung dibuka dari browser di sisi Windows tanpa konfigurasi tambahan, dan akan menampilkan data JSON secara langsung di halaman browser.















